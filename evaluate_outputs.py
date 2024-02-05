import json
import re
from glob import glob
from tap import Tap


# Use multiple processes to generate the outputs
from joblib import Parallel, delayed

# Import the relevant functions from utils
from utils.execute_code import execute_code_with_timeout
from utils.sonnet_eval import sonnet_errors


def extract_answer(
    txt: str, first_split: str = '>> final answer:\n"""', second_split: str = '"""'
) -> str:
    """
    Given a string, extract the answer between the first and second split.

    Args:
        txt (str): The string to extract the answer from.
        first_split (str): The first split.
        second_split (str): The second split.

    Returns:
        str: The final answer.
    """
    try:
        first_split = txt.split(first_split)[-1]
        second_split = first_split.split(second_split)[0]
        return second_split
    except Exception as e:
        return None


def clean_output_for_arithmetic(output: str) -> str:
    """
    Clean the output for arithmetic problems.

    Args:
        output (str): The output to clean.

    Returns:
        str: The cleaned output.
    """
    if "=" in output:
        output = output.split("=")[1].strip()
    if " is" in output:
        output = output.split(" is")[1].strip()
    if " equals" in output:
        output = output.split(" equals")[1].strip()
    if " evaluates to" in output:
        output = output.split(" evaluates to")[1].strip()
    if " is equal to" in output:
        output = output.split(" is equal to")[1].strip()
    return output


def clean_output_for_GameOf24(output: str) -> str:
    """
    Clean the output for GameOf24 problems.
    """
    if "=" in output:
        output = output.split("=")[0].strip()
    if "is" in output:
        output = output.split("is")[1].strip()
    if "equals" in output:
        output = output.split("equals")[0].strip()
    if "evaluates to" in output:
        output = output.split("evaluates to")[0].strip()
    return output


def eval_for_GameOf24(input: str, output: str) -> bool:
    """
    Given an input and output, check if the output is correct and follows the rules of the game.
    """
    clean_output = clean_output_for_GameOf24(output)
    try:
        # Get the value of the expression using eval
        value = eval(clean_output)
        if not (abs(value - 24) < 1e-3):
            return False
        # Split the input and output digits by space
        input_digits = input.split(" ")
        # Replace the following symbols with space
        replacements = ["+", "-", "*", "/", "÷", "(", ")"]
        for symbol in replacements:
            clean_output = clean_output.replace(symbol, " ")
        # Replace multiple spaces with single space
        clean_output = re.sub(" +", " ", clean_output)
        clean_output = clean_output.strip()
        output_digits = clean_output.split(" ")
        # Sort the digits
        input_digits.sort()
        output_digits.sort()
        # Check if the digits are the same
        if input_digits != output_digits:
            return False
        return True
    except Exception as e:
        return False


def remove_punctuation(output: str) -> str:
    markers = [",", ";", ":", ".", '"']
    for marker in markers:
        output = output.replace(marker, "")
    return output


def convert_newline_to_space(output: str) -> str:
    output = output.replace("\n", " ")
    return output


def eval_for_exact_matching_with_no_punctuation(
    input: str, output: str, target: str
) -> bool:
    output = remove_punctuation(output)
    output = convert_newline_to_space(output)
    if target == output:
        return True
    return False


def eval_for_softmatch(input: str, output: str, target: str) -> bool:
    output = remove_punctuation(output)
    if target in output:
        return True
    return False


def eval_for_CheckmateInOne(input: str, output: str, target: str) -> bool:
    # Based on the input, determine the number of the last move
    last_move = input.split(".")[-1].strip()
    move_idx = input.split(".")[-2].split(" ")[-1].strip()
    # If the last move is an empty string, then the last move is white; otherwise, it is black
    if last_move == "":
        last_move = "White"
    else:
        last_move = "Black"
    next_move_idx = str(int(move_idx) + 1)
    if not (next_move_idx in output):
        if target in output:
            return True
    else:
        output = output.split(next_move_idx)[0].strip()
        if target in output:
            return True
    return False


def eval_for_Sonnet(output: str, rhyme_scheme: str) -> bool:
    try:
        errors = sonnet_errors(output, rhyme_scheme)
        if not errors:
            return True
        return False
    except Exception as e:
        return False


def eval_for_multiple_choice(input: str, output: str, target: str) -> bool:
    if target in output[: len(target)]:
        return True
    # else:
    #     try:
    #         options_text = input.split("Options:")[1].strip().lower() # .split(")")[1].split("\n")[0].strip()
    #         idx =  ord(target[1]) - ord('a')
    #         options_text = options_text.split("\n")
    #         option_text = options_text[idx].split(")")[1].strip()
    #         if option_text in output:
    #             return True
    #     except Exception as e:
    #         pass
    return False


def eval_for_pyton_programming_puzzles(input: str, output: str, target: str) -> bool:
    if "```python" in output:
        output = output.split("```python")[-1].strip()
        output = output.split("```")[0].strip()

    if "def sat" in output:
        if "from typing" not in output:
            output = f"from typing import *\n{output}"
        code = f"{output}\nanswer = solution()\nprint(sat(answer))"
    else:
        code = f"from typing import *\n{input}\n{output}\nanswer = solution()\nprint(sat(answer))"

    code = code.replace("List[", "list[")
    eval_bool = execute_code_with_timeout(code, timeout=3)
    if "NameError: name 'answer' is not defined" in eval_bool:
        print(f"Eval bool: {eval_bool}")
        print(f"Code:\n{code}")
        print("*" * 100)
    if "True" in eval_bool:
        return True
    return False


def run_eval(datum, task):
    input = datum["input"]
    output = datum["output"].lower()
    # print(f"ORIGINAL: {output}")
    output = extract_answer(output).strip()
    target = datum["target"].lower()

    if "GameOf24" in task:
        return eval_for_GameOf24(input, output)
    elif any([x in task for x in ["word_sorting", "multistep_arithmetic_two"]]):
        return eval_for_exact_matching_with_no_punctuation(input, output, target)
    elif any([x in task for x in ["CheckmateInOne"]]):
        decision = eval_for_CheckmateInOne(input, output, target)
        return decision
    elif any([x in task for x in ["Sonnets-Standard"]]):
        return eval_for_Sonnet(output, "ABAB CDCD EFEF GG")
    elif any([x in task for x in ["geometric_shapes", "ruin_names"]]):
        decision = eval_for_multiple_choice(input, output, target)
        return decision
    elif any([x in task for x in ["MGSM"]]):
        return eval_for_softmatch(input, output, target)
    elif any([x in task for x in ["P3", "P3_Test"]]):
        output = datum["output"]
        output = extract_answer(
            txt=output, first_split='>> FINAL ANSWER:\n"""', second_split='"""'
        )
        decision = eval_for_pyton_programming_puzzles(input, output, target)
        return decision
    print(f"Task {task} not implemented yet.")
    assert False, f"Task {task} not implemented yet."


class Arguments(Tap):
    """
    The arguments to pass to the program.
    """
    # The directory and task to evaluate
    directory: str = "outputs/*/"
    task: str = "GameOf24*"


def main(args: Arguments):
    directory = args.directory
    task = args.task
    files = glob(f"{directory}/*{task}*.jsonl")
    files.sort()
    for file in files:
        if "data" in file:
            continue
        with open(file, "r") as f:
            data = [json.loads(line) for line in f.readlines()]

        if len(data) == 0:
            continue

        # Run the evaluation function in parallel
        results = Parallel(n_jobs=-1, verbose=0, prefer="threads")(
            delayed(run_eval)(datum=datum, task=task) for datum in data
        )

        # Return the accuracy
        correct = sum(results)
        size = len(results)
        accuracy = correct / size
        print(f"{file}: {accuracy} ({correct}/{size})")


if __name__ == "__main__":
    args = Arguments().parse_args()
    main(args)
