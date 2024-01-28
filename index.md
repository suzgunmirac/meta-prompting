---
layout: project_page
permalink: /

title: "Meta-Prompting: Enhancing Language Models with Task-Agnostic Scaffolding"
authors:
    Mirac Suzgun
    Adam Tauman Kalai
affiliations:
    Stanford University
    OpenAI
paper: https://arxiv.org/abs/2401.12954
code: Coming soon
data: Coming soon
---

<div class="columns is-centered has-text-centered">
    <div class="column is-four-fifths">
        <h2>Abstract</h2>
        <div class="content has-text-justified">
            We introduce meta-prompting, an effective scaffolding technique designed to enhance the functionality of language models (LMs). This approach transforms a single LM into a multi-faceted conductor, adept at managing and integrating multiple independent LM queries. By employing high-level instructions, meta-prompting guides the LM to break down complex tasks into smaller, more manageable subtasks. These subtasks are then handled by distinct "expert" instances of the same LM, each operating under specific, tailored instructions. Central to this process is the LM itself, in its role as the conductor, which ensures seamless communication and effective integration of the outputs from these expert models. It additionally employs its inherent critical thinking and robust verification processes to refine and authenticate the end result. This collaborative prompting approach empowers a single LM to simultaneously act as a comprehensive orchestrator and a panel of diverse experts, significantly enhancing its performance across a wide array of tasks. The zero-shot, task-agnostic nature of meta-prompting greatly simplifies user interaction by obviating the need for detailed, task-specific instructions. Furthermore, our research demonstrates the seamless integration of external tools, such as a Python interpreter, into the meta-prompting framework, thereby broadening its applicability and utility. Through rigorous experimentation with GPT-4, we establish the superiority of meta-prompting over conventional scaffolding methods: When averaged across all tasks, including the Game of 24, Checkmate-in-One, and Python Programming Puzzles, meta-prompting, augmented with a Python interpreter functionality, surpasses standard prompting by 17.1%, expert (dynamic) prompting by 17.3%, and multipersona prompting by 15.2%.
        </div>
    </div>
</div>

![Meta-Prompting-Results](/static/image/meta-prompting-results.png)

**Enhancing GPT-4 with meta-prompting.** In this study, we introduce and examine the effectiveness of meta- prompting, contrasting it with a range of zero-shot prompting techniques, including standard zero-shot (Std), zero-shot chain-of-thought (0-CoT), generic and dynamic expert (Ex-St and Ex-Dy), and multipersona (MP). Our research demonstrates that meta-prompting, particularly when combined with a Python interpreter, significantly improves overall accuracy and robustness in GPT-4 across a variety of tasks.

## Citation

We encourage citing our paper if our data or findings are used in your research. Please also acknowledge the original authors and datasets referenced in our work.

```
@article{suzgun2024metaprompting,
      title={Meta-Prompting: Enhancing Language Models with Task-Agnostic Scaffolding}, 
      author={Mirac Suzgun and Adam Tauman Kalai},
      year={2024},
      eprint={2401.12954},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```
