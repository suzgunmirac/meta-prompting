"""
Defines function sonnet_errors(poem, target: str) -> Dict[str, Any]
which takes a target rhyme scheme (and optionally a list of required words) and returns a dict of errors

Returns an empty dictionary if there are no errors, so bool(sonnet_errors(poem, target)) is False if there are no
errors. It's a permissive check for sonnets errors, meaning that if it is unsure then it doesn't return an error.

Specifically, 

* Check if it adheres to a given rhyming scheme
* Check if each line has 10-11 syllables, more precisely, there's some pronounciation of each line with 10-11 syllalbes

This omits a few things like rhymes and iambic pentameter.

# Rhymes

For rhymes, we use python `pronouncing` library based on:

* CMU pronouncing dictionary http://www.speech.cs.cmu.edu/cgi-bin/cmudict

# Syllable counting 

Given that there are multiple ways to pronounce many words (e.g. "caramel" can be pronounced with 2 or 3 syllables),
we adopt a "permissive" approach and consult multiple tools for syllable counting:

* pronounce - a well-known pronunciation dict based on from CMU's pronouncing dictionary 
* syllables - a Python library for syllable counting
* pyphen - a Python wrapper for the hyphenation library
"""

from typing import Set, Dict, Any
import re
import joblib
import pyphen
import syllables
import pronouncing


ALLOWED_SYLLABLES = {
    10,
    11,
}  # about 3-4% of legit lines have 11 syllables, so we allow it, > 99% have 10 or 11
NUM_REQUIRED_WORDS = 3

memory = joblib.Memory(
    ".cache", verbose=0
)  # use cache to speed up repeated rhyme/syllable calls


def sonnet_errors(poem: str, target: str, verbose=False) -> Dict[str, Any]:
    """
    Checks for sonnet errors with respect to target rhyme scheme (and optional required words)

    args:
        poem: the poem to check
        target: the rhyme scheme, e.g. "ABBA ABBA CDC DCD"
                optionally target can have a list of required words, like
                "ABBA ABBA CDC DCD, love train snail" each of these must be in the poem
        verbose: if True, print out more details
    """
    if ", " in target:
        scheme, rest = target.split(", ")
        required_words = rest.split()
    else:
        scheme = target
        required_words = []

    errors = scheme_errors(poem, scheme, verbose=verbose)
    assert isinstance(errors, dict)
    missing_words = [w for w in required_words if w.lower() not in poem.lower()]
    if any(missing_words):
        errors["missing words"] = missing_words

    syllable_errors = []
    for line in split_poem(poem):
        variations = syllable_variations(line)
        if not (variations & ALLOWED_SYLLABLES):
            syllable_errors.append((line, sorted(variations)))
    if syllable_errors:
        errors["syllable errors"] = syllable_errors

    return errors


def clean_word(text: str):
    return text.lower().strip(",.!?;: \"'[]()/")


def clean_line(line: str):
    """
    Clean a line from a poem.
    Check if line ends with (A) or (B) ... and remove it
    """
    line = re.sub(r"\s*\([A-Za-z]\)\s*$", "", line)
    return line.strip()


def split_poem(poem: str, min_line_len=3):
    ans = [clean_line(l) for l in poem.splitlines()]
    return [l for l in ans if len(l) > min_line_len]


@memory.cache
def slant_rhyming_parts(word: str):
    consonants = set("BCDFGHJKLMNPQRSTVWXYZ")
    ans = [
        "".join(
            ("R" if "R" in p else (p if p in consonants else "?"))
            for p in pronouncing.rhyming_part(ph).split()
        )
        for ph in pronouncing.phones_for_word(word)
    ]
    ans = [a for a in ans if not all(i == "?" for i in a)]
    ans = [a.replace("?", "") + ("?" if a.endswith("?") else "") for a in ans]
    return set(ans)


@memory.cache
def get_rhymes(w):
    return set(pronouncing.rhymes(w))


def scheme_errors(poem: str, scheme: str, verbose=False):
    """Find errors with respect to a given rhyming scheme"""
    lines = split_poem(poem)
    scheme = scheme.replace(" ", "")

    if len(lines) != len(scheme):
        return {
            "line count": f"Poem has {len(lines)} != {len(scheme)} lines in pattern {scheme}"
        }

    last_words = [clean_word(l.replace("-", " ").split()[-1]) for l in lines]

    dictionary = pronouncing.cmudict.dict()  # we ignore words not in dictionary

    groups = []
    for chars in sorted(set(scheme)):
        groups.append(
            [w for w, p in zip(last_words, scheme) if p == chars and w in dictionary]
        )

    slant_sets = {w: set(slant_rhyming_parts(w)) for g in groups for w in g}

    scores = {}

    if verbose:
        print(groups)

    for g in groups:
        internal_words = set(g)
        external_words = {w for h in groups if h is not g for w in h}
        if len(internal_words) == 1:
            continue  # don't check rhymes if only word word in the group is in dictionary
        for w in g:
            rhymes = get_rhymes(w)
            scores[w] = []
            for comparisons in [internal_words, external_words]:
                m = dict(rhymes=[], slant_rhymes=[])
                scores[w].append(m)
                for v in comparisons:
                    if v == w:
                        continue
                    if v in rhymes:
                        m["rhymes"].append(v)
                    elif slant_sets[v] & slant_sets[w]:
                        m["slant_rhymes"].append(v)

    error_reasons = {}
    suspicious_reasons = {}

    for w in scores:
        internal, external = scores[w]

        if internal["rhymes"] or internal["slant_rhymes"]:
            pass  # ok if it rhymes (perfect or slant) with at least one other word in the group
        elif len(external["rhymes"]) >= 2:
            error_reasons[w] = "no internal rhymes, 2+ external perfect rhymes"
        elif external["rhymes"]:
            if len(external["slant_rhymes"]) >= 2:
                error_reasons[
                    w
                ] = "no internal rhymes, 1 external perfect rhyme, 2+ external slant rhymes"
            else:
                suspicious_reasons[
                    w
                ] = "no internal rhymes/slant rhymes, 1 external perfect rhymes"
        elif len(external["slant_rhymes"]) >= 3:
            error_reasons[
                w
            ] = "no internal rhymes/slant rhymes, 3+ external slant rhymes"
        if verbose:
            print(w, "internal:", internal, "external:", external)

    if len(error_reasons) + len(suspicious_reasons) >= 3:
        error_reasons.update(suspicious_reasons)

    return {
        w: {
            "reason": error_reasons[w],
            "internal": scores[w][0],
            "external": scores[w][1],
        }
        for w in error_reasons
    }


def syllable_variations(text, verbose=False) -> Set[int]:
    """
    Given a text, return the set of possible numbers of syllables. It's a set because some words like "caramel" can
    be pronounced with different numbers of syllables.
    """
    ans = {0}
    for word in re.split("[ -]+", text):
        word = clean_word(word)
        if not word:
            continue
        options = word_syllables(word)
        options = range(
            min(options), max(options) + 1
        )  # make it a range (so {2, 4} moves to [2, 3, 4])
        ans = {x + y for x in ans for y in options}
    return ans


@memory.cache
def word_syllables(word: str) -> Set[int]:
    assert word == clean_word(
        word
    ), "Word should be cleaned before hitting word_syllables cache"
    return SyllableCounters.count_word(word)


class SyllableCounters:
    """
    Simple class to count syllables in text.
    """

    _cmu_dict = None
    _pyphen_counter = None

    @staticmethod
    def cmu_dict():
        if not SyllableCounters._cmu_dict:
            SyllableCounters._cmu_dict = pronouncing.cmudict.dict()
        return SyllableCounters._cmu_dict

    def cmu(word):
        return {
            pronouncing.syllable_count(pro) for pro in pronouncing.phones_for_word(word)
        }

    @staticmethod
    def pyphen_counter():
        if not SyllableCounters._pyphen_counter:
            SyllableCounters._pyphen_counter = pyphen.Pyphen(lang="en")
        return SyllableCounters._pyphen_counter

    @staticmethod
    def count_word(word) -> Set[int]:
        if not word:
            return {0}

        cmu = SyllableCounters.cmu(word)

        pyph = SyllableCounters.pyphen_counter().inserted(word).count("-") + 1

        syll = syllables.estimate(word)

        ans = cmu | {pyph, syll}

        if 0 in ans and len(ans) > 1:
            ans.remove(0)

        return ans


TESTS = [
    ["In savannah where tall trees kiss the sky,", 10],
    ["A giraffe named Joe with love-stricken grace,", 10],
    ["Did find a turtle named Sarah nearby,", 10],
    ["Their eyes did meet, hearts raced in sweet embrace.", 10],
    ["Though nature's laws deemed their love quite absurd,", 10],
    ["Joe's neck would bend to whisper words of flame,", 10],
    ["And Sarah's shell would tremble at each word,", 10],
    ["In love's bizarre dance, they found no one to blame.", 11],
    ["Through sun and storm, they'd wander, hoof and claw,", 10],
    ["With love that no one ever could unravel,", 11],
    ["In each other's eyes, perfection they saw,", 10],
    ["A love so fierce, no distance could they travel.", 11],
    ["So let us learn from turtle and giraffe,", 10],
    ["That love's own shape can make the coldest laugh.", 10],
    ["In yonder sky where colours blend so high,", 10],
    ["A rainbow arcs, a bridge 'twixt earth and air.", 10],
    ["Its radiant hues draw every gazing eye,", 12],
    ["A painter's dream, a sight beyond compare.", 10],
    ["Yet in the world of man, delight so small,", 10],
    ["As gumball's sphere, with colours bright and clear.", 10],
    ["Such simple joy it brings to one and all,", 10],
    ["Its sweetness matched by colours we hold dear.", 10],
    ["Both nature's arc and candy sphere delight,", 10],
    ["The vast expanse and tiny bite unite,", 10],
    ["In tales of wonder, stories to be told.", 10],
    ["So let us cherish both the grand and small,", 10],
    ["For beauty’s found in rainbow and in gumball.", 11],
    ["When night's embrace hath shrouded all in black,", 10],
    ["A flashlight's beam doth pierce the dark so deep,", 10],
    ["From paths we've chosen, and vows we mean to keep.", 11],
    ["Thou art like that beam, true, clear, and bright,", 9],
    ["Cutting through the fog of my mind's own night,", 10],
    ["Yet oft I find, by folly or by chance,", 10],
    ["Distractions lead my wandering glance.", 9],
    ["But even as stars, obscured by fleeting cloud,", 11],
    ["Return to grace the heavens, proud and loud,", 10],
    ["So shall my focus, once by ails distraught,", 10],
    ["Return to thee, as ever it hath sought.", 10],
    ["For in this world of fleeting sight and sound,", 10],
]


def fixed_tests():
    failures = []
    for line, expected in TESTS:
        variations = syllable_variations(line)
        if expected not in variations:
            print(f"Line `{line}` has {expected} syllables which isn't in {variations}")
            failures.append((line, expected, variations))

    # tests from https://www.mentalfloss.com/article/53661/car-mel-or-car-mel-3-reasons-syllabically-ambiguous-words :
    for words, expected in [
        (
            "fire tire hour liar buyer flower drawer layer loyal royal file orange poem crayon".split(),
            [1, 2],
        ),
        (
            "caramel mayonnaise family chocolate camera different separate favorite realtor".split(),
            [2, 3],
        ),
        ("mischievous".split(), [3, 4]),
    ]:
        for w in words:
            variations = syllable_variations(w)
            for i in expected:
                if i not in variations:
                    print(
                        f"{w} give syllable_variations {variations} but should include {i}"
                    )
                    failures.append((w, i, variations))
    return failures


def summarize_errors(errors, num_samples):
    print(
        f"Sonnet failure rate: {len(errors)/num_samples:.1%} out of {num_samples:,}, breakdown:"
    )
    wnl = sum("line count" in e for e in errors.values()) / num_samples
    print(f"{wnl:.1%} wrong number of lines")
    mw = sum(bool("missing words" in e) for e in errors.values()) / num_samples
    print(f"{mw:.1%} missing words")
    bl = sum(bool("syllable errors" in e) for e in errors.values()) / num_samples
    print(f"{bl:.1%} poems with at least one line with wrong number of syllables")
    rhyme_errors = (
        sum(any(" " not in k for k in e) for e in errors.values()) / num_samples
    )
    both = (
        sum(
            (bool("syllable errors" in e) and any(" " not in k for k in e))
            for e in errors.values()
        )
        / num_samples
    )
    print(
        f"{rhyme_errors:.1%} poems with rhyme errors ({both:.1%} poems with both rhyme and syllable errors)"
    )


def corpus_check_scheme(corpus_filename, scheme):
    with open(corpus_filename, "r") as f:
        poems = [p.strip() for p in f.read().split("\n\n") if p]
    errors = {}
    for p in poems:
        e = sonnet_errors(p, scheme)
        if e:
            errors[p] = e
            print("*" * 50)
            sonnet_errors(p, scheme, verbose=True)
            print("scheme", scheme)
            print(p)
            print()
            print(e)
            print("<" * 50)

    summarize_errors(errors, len(poems))


def test():
    assert not sonnet_errors(
        """Not like the brazen giant of Greek fame,
        With conquering limbs astride from land to land;
        Here at our sea-washed, sunset gates shall stand
        A mighty woman with a torch, whose flame
        Is the imprisoned lightning, and her name
        Mother of Exiles. From her beacon-hand
        Glows world-wide welcome; her mild eyes command
        The air-bridged harbor that twin cities frame.

        "Keep, ancient lands, your storied pomp!" cries she
        With silent lips. "Give me your tired, your poor,
        Your huddled masses yearning to breathe free,
        The wretched refuse of your teeming shore.
        Send these, the homeless, tempest-tost to me,
        I lift my lamp beside the golden door!"
                """,
        "ABBA ABBA CDCDCD",
    )

    assert not sonnet_errors(
        """How do I love thee? Let me count the ways.
        I love thee to the depth and breadth and height
        My soul can reach, when feeling out of sight
        For the ends of being and ideal grace.
        I love thee to the level of every day’s
        Most quiet need, by sun and candle-light.
        I love thee freely, as men strive for right.
        I love thee purely, as they turn from praise.
        I love thee with the passion put to use
        In my old griefs, and with my childhood’s faith.
        I love thee with a love I seemed to lose
        With my lost saints. I love thee with the breath,
        Smiles, tears, of all my life; and, if God choose,
        I shall but love thee better after death.""",
        "abba abba cdcdcd",
    )

    assert not sonnet_errors(
        """When, in disgrace with fortune and men’s eyes,
        I all alone beweep my outcast state,
        And trouble deaf heaven with my bootless cries,
        And look upon myself, and curse my fate,
        Wishing me like to one more rich in hope,
        Featur’d like him, like him with friends possess’d,
        Desiring this man’s art and that man’s scope,
        With what I most enjoy contented least;
        Yet in these thoughts myself almost despising,
        Haply I think on thee, and then my state,
        Like to the lark at break of day arising
        From sullen earth, sings hymns at heaven’s gate;
        For thy sweet love remember’d such wealth brings
        That then I scorn to change my state with kings.""",
        "ABAB CDCD EFEF GG",
    )

    assert sonnet_errors(
        """How do I love thee? Let me count the ways.
        I love thee to the depth and breadth and height
        My soul can reach, when feeling out of sight
        For the ends of being and ideal grace.
        I love thee to the level of every day’s
        Most quiet need, by sun and candle-light.
        I love thee freely, as men strive for right.
        I love thee purely, as they turn from praise.
        I love thee with the passion put to use
        In my old griefs, and with my childhood’s faith.
        I love thee with a love I seemed to lose
        With my lost saints. I love thee with the breath,
        Smiles, tears, of all my life; and, if God choose,
        I shall but love thee better after death.""",
        "ABAB CDCD EFEF GG",
    )

    aaa = sonnet_errors(
        """How do I love thee? Let me count the ways.
        I love thee to the depth and breadth and height
        My soul can reach, when feeling out of sight
        For the ends of being and ideal grace.
        I love thee to the level of every day’s
        Most quiet need, by sun and candle-light.
        I love thee freely, as men strive for right.
        I love thee purely, as they turn from praise.
        I love thee with the passion put to use
        In my old griefs, and with my childhood’s faith.
        I love thee with a love I seemed to lose
        With my lost saints. I love thee with the breath,
        Smiles, tears, of all my life; and, if God choose,
        I shall but love thee better after death.""",
        "ABBA ABBA CDC DCD",
        # abba abba cdc dcd: (correct)
        # "ABAB CDCD EFEF GG", (false)
    )

    print(aaa)

    aaa = sonnet_errors(
        """How do I love thee? Let me count the ways (A)
        I love thee to the depth and breadth and height (B)
        My soul can reach, when feeling out of sight (B)
        For the ends of being and ideal grace (A)
        I love thee to the level of every day’s (A)
        Most quiet need, by sun and candle-light (B)
        I love thee freely, as men strive for right (B)
        I love thee purely, as they turn from praise (A)
        I love thee with the passion put to use (C)
        In my old griefs, and with my childhood’s faith (D)
        I love thee with a love I seemed to lose (C)
        With my lost saints. I love thee with the breath (D)
        Smiles, tears, of all my life; and, if God choose (C)
        I shall but love thee better after death (D).""",
        "ABBA ABBA CDC DCD",
        # abba abba cdc dcd: (correct)
        # "ABAB CDCD EFEF GG", (false)
    )
