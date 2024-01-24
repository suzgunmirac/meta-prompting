# Meta Prompting

[![arXiv](https://img.shields.io/badge/arXiv-2401.12954-b31b1b.svg)](https://arxiv.org/abs/2401.12954) **Meta-Prompting: Enhancing Language Models with Task-Agnostic Scaffolding**

![Meta-Prompting](https://github.com/suzgunmirac/meta-prompting-dev/blob/main/figures/meta-prompting-results.png)

**Enhancing GPT-4 with meta-prompting.** In this study, we introduce and examine the effectiveness of meta- prompting, contrasting it with a range of zero-shot prompting techniques, including standard zero-shot (Std), zero-shot chain-of-thought (0-CoT), generic and dynamic expert (Ex-St and Ex-Dy), and multipersona (MP). Our research demonstrates that meta-prompting, particularly when combined with a Python interpreter, significantly improves overall accuracy and robustness in GPT-4 across a variety of tasks.

## Abstract
We introduce **meta-prompting**, an effective scaffolding technique designed to enhance the functionality of language models (LMs). This approach transforms a single LM into a multi-faceted conductor, adept at managing and integrating multiple independent LM queries. By employing high-level instructions, meta-prompting guides the LM to deconstruct complex tasks into smaller, more manageable subtasks. These subtasks are then handled by distinct "expert" instances of the same LM, each operating under specific, tailored instructions. Central to this process is the LM itself, in its role as the conductor, which ensures seamless communication and effective integration of the outputs from these expert models. It additionally employs its inherent critical thinking and robust verification processes to refine and authenticate the end result. This collaborative prompting approach empowers a single LM to simultaneously act as a comprehensive orchestrator and a panel of diverse experts, significantly enhancing its performance across a wide array of tasks. The zero-shot, task-agnostic nature of meta-prompting greatly simplifies user interaction by obviating the need for detailed, task-specific instructions. Furthermore, our research demonstrates the seamless integration of external tools, such as a Python interpreter, into the meta-prompting framework, thereby broadening its applicability and utility. Through rigorous experimentation with GPT-4, we establish the superiority of meta-prompting over conventional scaffolding methods: When averaged across all tasks, including the Game of 24, Checkmate-in-One, and Python Programming Puzzles, meta-prompting, augmented with a Python interpreter functionality, surpasses standard prompting by 17.1\%, expert (dynamic) prompting by 17.3\%, and multipersona prompting by 15.2\%.

## Data Files
All task-related files can be found in the `/data` directory.

* Our raw input-output data files are also available for access via Hugging Face Datasets: [https://huggingface.co/datasets/turingmachine/meta-prompting](https://huggingface.co/datasets/turingmachine/meta-prompting)

## Prompt Collection
All prompt templates from our experiments are located in the `/prompts` directory.

## Experiment Outputs
All outputs from our experiments are stored in the `/outputs` directory.

## Citation Guidelines 
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

## Datasets Referenced in Our Study
* The Game of 24 from [(Yao et al., 2023)](https://github.com/princeton-nlp/tree-of-thought-llm):
```
@misc{yao2023tree,
      title={{Tree of Thoughts}: Deliberate Problem Solving with Large Language Models}, 
      author={Shunyu Yao and Dian Yu and Jeffrey Zhao and Izhak Shafran and Thomas L. Griffiths and Yuan Cao and Karthik Narasimhan},
      year={2023},
      eprint={2305.10601},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

* Geometric Shapes, Multi-Step Arithmetic Two, and Word Sorting from [BIG-Bench Hard](https://github.com/suzgunmirac/BIG-Bench-Hard) ([Suzgun et al., 2023](https://arxiv.org/abs/2210.09261); [BIG-Bench authors, 2023](https://github.com/google/BIG-bench/tree/main)):
```
@inproceedings{suzgun2023bigbenchhard,
    title = "Challenging {BIG}-Bench Tasks and Whether Chain-of-Thought Can Solve Them",
    author = {Suzgun, Mirac  and Scales, Nathan  and Sch{\"a}rli, Nathanael  and Gehrmann, Sebastian  and Tay, Yi  and Chung, Hyung Won  and Chowdhery, Aakanksha  and Le, Quoc  and Chi, Ed  and Zhou, Denny  and Wei, Jason},
    editor = "Rogers, Anna  and Boyd-Graber, Jordan  and Okazaki, Naoaki",
    booktitle = "Findings of the Association for Computational Linguistics: ACL 2023",
    month = jul,
    year = "2023",
    address = "Toronto, Canada",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.findings-acl.824",
    doi = "10.18653/v1/2023.findings-acl.824",
    pages = "13003--13051",
}

```

* Checkmate-in-One from the original [BIG-Bench suite](https://github.com/google/BIG-bench/tree/main) [(BIG-Bench authors, 2023)](https://arxiv.org/abs/2206.04615):
```
@article{srivastava2023beyond,
  title={Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models},
  author={BIG-bench authors},
  journal={Transactions on Machine Learning Research},
  issn={2835-8856},
  year={2023},
  url={https://openreview.net/forum?id=uyTL5Bvosj},
}
```

* [Python Programming Puzzles](https://github.com/microsoft/PythonProgrammingPuzzles) (P3; [Schuster et al. (2021)](https://arxiv.org/abs/2106.05784)):
```
@inproceedings{
  schuster2021programming,
  title={Programming Puzzles},
  author={Tal Schuster and Ashwin Kalyan and Alex Polozov and Adam Tauman Kalai},
  booktitle={Thirty-Fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track},
  year={2021},
  url={https://arxiv.org/abs/2106.05784}
}
```

* [Multilingual Grade School Math](https://github.com/google-research/url-nlp) (MGSM; [Shi et al. (2023)](https://openreview.net/pdf?id=fR3wGCk-IXp)):
```
@inproceedings{
  shi2023language,
  title={Language models are multilingual chain-of-thought reasoners},
  author={Freda Shi and Mirac Suzgun and Markus Freitag and Xuezhi Wang and Suraj Srivats and Soroush Vosoughi and Hyung Won Chung and Yi Tay and Sebastian Ruder and Denny Zhou and Dipanjan Das and Jason Wei},
  booktitle={The Eleventh International Conference on Learning Representations },
  year={2023},
  url={https://openreview.net/forum?id=fR3wGCk-IXp}
}
```
