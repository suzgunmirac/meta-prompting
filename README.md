# Meta-Prompting

[![arXiv](https://img.shields.io/badge/arXiv-2401.12954-b31b1b.svg)](https://arxiv.org/abs/2401.12954) **Meta-Prompting: Enhancing Language Models with Task-Agnostic Scaffolding**

![Meta-Prompting](https://github.com/suzgunmirac/meta-prompting/blob/main/figures/meta-prompting-results.png)

**Enhancing GPT-4 with meta-prompting.** In this study, we introduce and examine the effectiveness of meta- prompting, contrasting it with a range of zero-shot prompting techniques, including standard zero-shot (Std), zero-shot chain-of-thought (0-CoT), generic and dynamic expert (Ex-St and Ex-Dy), and multipersona (MP). Our research demonstrates that meta-prompting, particularly when combined with a Python interpreter, significantly improves overall accuracy and robustness in GPT-4 across a variety of tasks.

## Table of Contents

[**Abstract**](#abstract) | [**Dataset**](#tasks-and-datasets) | [**Prompts**](#prompt-templates) | [**Outputs**](#model-outputs) | [**Implementation and Evaluation**](#running-experiments-and-evaluation) | [**Citation**](#citation-guidelines) | [**Related Work**](#related-and-concurrent-investigations) | [**Thanks**](#acknowledgements)

## Abstract

We introduce **meta-prompting**, an effective scaffolding technique designed to enhance the functionality of language models (LMs). This approach transforms a single LM into a multi-faceted conductor, adept at managing and integrating multiple independent LM queries. By employing high-level instructions, meta-prompting guides the LM to deconstruct complex tasks into smaller, more manageable subtasks. These subtasks are then handled by distinct "expert" instances of the same LM, each operating under specific, tailored instructions. Central to this process is the LM itself, in its role as the conductor, which ensures seamless communication and effective integration of the outputs from these expert models. It additionally employs its inherent critical thinking and robust verification processes to refine and authenticate the end result. This collaborative prompting approach empowers a single LM to simultaneously act as a comprehensive orchestrator and a panel of diverse experts, significantly enhancing its performance across a wide array of tasks. The zero-shot, task-agnostic nature of meta-prompting greatly simplifies user interaction by obviating the need for detailed, task-specific instructions. Furthermore, our research demonstrates the seamless integration of external tools, such as a Python interpreter, into the meta-prompting framework, thereby broadening its applicability and utility. Through rigorous experimentation with GPT-4, we establish the superiority of meta-prompting over conventional scaffolding methods: When averaged across all tasks, including the Game of 24, Checkmate-in-One, and Python Programming Puzzles, meta-prompting, augmented with a Python interpreter functionality, surpasses standard prompting by 17.1\%, expert (dynamic) prompting by 17.3\%, and multipersona prompting by 15.2\%.

## Data, Prompt, and Output Files

### Tasks and Datasets

All input-output files related to tasks are available for access within the `/data` directory.

- If you wish to access our raw input-output data files, they are also available through Hugging Face Datasets at [https://huggingface.co/datasets/turingmachine/meta-prompting](https://huggingface.co/datasets/turingmachine/meta-prompting)

### Prompt Templates

All prompt templates and system instructions used in our experiments are located in the `/prompts` directory.

### Model Outputs

All outputs generated during our experiments are stored in the `/outputs` directory.

- The majority of our experiments were conducted in August 2023.

## Meta-Prompting Implementation

If you are interested in implementing our meta-prompting framework, you can find an example implementation in `utils/meta_scaffolding.py`. This code contains the primary scaffolding structure and necessary functionalities required to run your own meta-prompting experiments. Please feel free to adapt and use this code for your experiments as you wish.

Initially, we employed the Azure OpenAI Service to run our experiments; however, you should be able to use the OpenAI API service to run your experiments as well.

### Running Experiments and Evaluation

To conduct your own experiments, please feel free to modify and use the `run_experiments.py` file. Before executing this code, however, please ensure that you have installed all the required packages (e.g., `pip install -r requirements.txt`) and have exported all relevant OpenAI API keys and credentials to your local environment (e.g., `export OPENAI_API_KEY="YOUR_API_KEY"`).

Here is an example command to run the experiments:

```python
python run_experiments.py \
    --task_name "GameOf24" \
    --meta_config_path "prompts/meta-v0-2023-08-14-baseline.json" \
    --output_directory "TEST-CHATGPT-META-PROMPTING-WITH-PYTHON" \
    --question_prefix_or_path "prompts/meta-prompting-instruction.txt" \
    --model_name "gpt-3.5-turbo" \
    --temperature 0.1 \
    --include_expert_name_in_instruction \
    --fresh_eyes \
    --max_num 1
```

**Note:** For now, we set the `max_num` to `1` and `model_name` to `gpt-35-turbo` to run this experiment on a single example for the Game of 24 task using the GPT-3.5-turbo model. You can, however, modify these parameters as needed based on your requirements and quota.

Once you have completed the experiments, you can evaluate the outputs using the `evaluate_outputs.py` script. This script facilitates the measurement of your model outputs' accuracy and their comparison against the ground truth.

Here, we provide an example command for evaluating the outputs of our own experiments. You can modify the parameters as needed based on your requirements and the tasks you have evaluated.

```python
python evaluate_outputs.py \
    --directory "outputs/*/" \
    --task "GameOf24"
```

**Example Commands:** For your convenience, we have included a set of example scripts for running experiments and evaluating outputs in the `example_commands.sh` file. You can use the commands in this file as a starting point for your own experiments and evaluations.

## Citation Guidelines

We encourage citing our paper if our data or findings are used in your research. Please also acknowledge the original authors and datasets referenced in our work.

```bibtex
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

**The Game of 24** from [(Yao et al., 2023)](https://github.com/princeton-nlp/tree-of-thought-llm):

```bibtex
@misc{yao2023tree,
      title={{Tree of Thoughts}: Deliberate Problem Solving with Large Language Models}, 
      author={Shunyu Yao and Dian Yu and Jeffrey Zhao and Izhak Shafran and Thomas L. Griffiths and Yuan Cao and Karthik Narasimhan},
      year={2023},
      eprint={2305.10601},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

**Geometric Shapes, Multi-Step Arithmetic Two, and Word Sorting** from [BIG-Bench Hard](https://github.com/suzgunmirac/BIG-Bench-Hard) ([Suzgun et al., 2023](https://arxiv.org/abs/2210.09261); [BIG-Bench authors, 2023](https://github.com/google/BIG-bench/tree/main)):

```bibtex
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

**Checkmate-in-One** from [the BIG-Bench suite](https://github.com/google/BIG-bench/tree/main) [(BIG-Bench authors, 2023)](https://arxiv.org/abs/2206.04615):

```bibtex
@article{srivastava2023beyond,
  title={Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models},
  author={BIG-bench authors},
  journal={Transactions on Machine Learning Research},
  issn={2835-8856},
  year={2023},
  url={https://openreview.net/forum?id=uyTL5Bvosj},
}
```

[**Python Programming Puzzles**](https://github.com/microsoft/PythonProgrammingPuzzles) (P3; [Schuster et al. (2021)](https://arxiv.org/abs/2106.05784)):

```bibtex
@inproceedings{
  schuster2021programming,
  title={Programming Puzzles},
  author={Tal Schuster and Ashwin Kalyan and Alex Polozov and Adam Tauman Kalai},
  booktitle={Thirty-Fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track},
  year={2021},
  url={https://arxiv.org/abs/2106.05784}
}
```

[**Multilingual Grade School Math**](https://github.com/google-research/url-nlp) (MGSM; [Shi et al. (2023)](https://openreview.net/pdf?id=fR3wGCk-IXp)):

```bibtex
@inproceedings{
  shi2023language,
  title={Language models are multilingual chain-of-thought reasoners},
  author={Freda Shi and Mirac Suzgun and Markus Freitag and Xuezhi Wang and Suraj Srivats and Soroush Vosoughi and Hyung Won Chung and Yi Tay and Sebastian Ruder and Denny Zhou and Dipanjan Das and Jason Wei},
  booktitle={The Eleventh International Conference on Learning Representations },
  year={2023},
  url={https://openreview.net/forum?id=fR3wGCk-IXp}
}
```

## Related and Concurrent Investigations

- [Agents: An Open-source Framework for Autonomous Language Agents](https://arxiv.org/abs/2309.07870) (Zhou et al., 2023)
- [AutoAgents: A Framework for Automatic Agent Generation](https://arxiv.org/abs/2309.17288) (Chen et al., 2023)
- [AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation](https://arxiv.org/abs/2308.08155) (Wu et al., 2023)
- [ExpertPrompting: Instructing Large Language Models to be Distinguished Experts](https://arxiv.org/abs/2305.14688) (Xu et al., 2023)
- [MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework](https://arxiv.org/abs/2308.00352) (Hong et al., 2023)
- [Meta Prompting for AGI Systems](https://arxiv.org/abs/2311.11482) (Zhang, 2023)
- [On Meta-Prompting](https://arxiv.org/abs/2312.06562) (de Wynter et a., 2023)
- [Prompt Engineering a Prompt Engineer](https://arxiv.org/abs/2311.05661) (Ye et al., 2023)
- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) (Yao et al., 2023)
- [Self-Taught Optimizer (STOP): Recursively Self-Improving Code Generation](https://arxiv.org/abs/2310.02304) (Zelikman et al., 2023)
- [Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761) (Shick et al., 2023)
- [Unleashing the Emergent Cognitive Synergy in Large Language Models: A Task-Solving Agent through Multi-Persona Self-Collaboration](https://arxiv.org/abs/2307.05300) (Wang et al., 2023)

## Acknowledgements

This work was completed during the summer of 2023 when both authors were affiliated with Microsoft Research New England (MSR NE). We extend our gratitude to the members and interns at MSR NE for their valuable feedback throughout various phases of this project, and we appreciate the Azure team's support in facilitating our GPT-4 experiments.
