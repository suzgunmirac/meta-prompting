# Description: Example commands for running experiments and evaluation


### EXAMPLE COMMANDS FOR RUNNING EXPERIMENTS ###
# The following section for running experiments is commented out so that you do not accidentally run it and consume your quota.
# Please uncomment the section, modify the parameters as needed, and run the commands in your local environment.
# The following commands are examples of how to run experiments for different prompting strategies.

# Additional notes: For now, we set the `--max_num` to 1 to run the experiments on a single example for each task. 
# Similarly, we set the `--model_name` to `gpt-35-turbo` to use the GPT-3.5-turbo model (which is cheaper than GPT-4).
# You can modify these parameters as needed based on your requirements and quota.

# # META PROMPTING WITH PYTHON EXPERT INSTRUCTION
# for task in "GameOf24"
# do
# python run_experiments.py \
#     --task_name ${task} \
#     --meta_config_path prompts/meta-v0-2023-08-14-baseline.json \
#     --output_directory TEST-CHATGPT-META-PROMPTING-WITH-PYTHON \
#     --temperature 0.1 \
#     --include_expert_name_in_instruction \
#     --question_prefix_or_path prompts/meta-prompting-instruction.txt \
#     --model_name "gpt-3.5-turbo" \
#     --fresh_eyes \
#     --max_num 1
# done

# # META PROMPTING WITH NO PYTHON EXPERT INSTRUCTION
# meta-prompting-with-no-python-expert-instruction.txt
# for task in "GameOf24"
# do
# python run_experiments.py \
#     --task_name ${task} \
#     --meta_config_path prompts/meta-v0-2023-08-14-baseline.json \
#     --output_directory TEST-CHATGPT-META-PROMPTING-WITH-NO-PYTHON \
#     --temperature 0.1 \
#     --include_expert_name_in_instruction \
#     --question_prefix_or_path prompts/meta-prompting-with-no-python-expert-instruction.txt \
#     --model_name "gpt-3.5-turbo" \
#     --fresh_eyes
# done

# # MULTIPERSONA PROMPTING
# for task in "GameOf24"
# do
#     python run_experiments.py \
#         --task_name ${task} \
#         --meta_config_path prompts/meta-v0-2023-08-14-baseline.json \
#         --output_directory TEST-CHATGPT-MULTIPERSONA-PROMPTING \
#         --temperature 0.1 \
#         --include_expert_name_in_instruction \
#         --question_prefix_or_path prompts/multipersona-prompting-text.txt \
#         --question_suffix_or_path "" \
#         --model_name "gpt-3.5-turbo"
# done

# # ZERO-SHOT COT PROMPTING
# for task in "GameOf24"
# do
#     python run_experiments.py \
#         --task_name ${task} \
#         --meta_config_path prompts/meta-v0-2023-08-14-baseline.json \
#         --output_directory TEST-CHATGPT-ZERO-SHOT-COT-PROMPTING \
#         --temperature 0.1 \
#         --include_expert_name_in_instruction \
#         --question_suffix_or_path prompts/zero-shot-cot-prompting-suffix-text.txt \
#         --question_prefix_or_path "" \
#         --model_name "gpt-3.5-turbo"
# done

# # STATIC (GENERIC) EXPERT PROMPTING
# for task in "GameOf24"
# do
#     python run_experiments.py \
#         --task_name ${task} \
#         --meta_config_path prompts/meta-v0-2023-08-14-baseline.json \
#         --output_directory TEST-CHATGPT-STATIC-EXPERT-PROMPTING \
#         --temperature 0.1 \
#         --include_expert_name_in_instruction \
#         --question_prefix_or_path prompts/expert-generic-instruction.txt \
#         --question_suffix_or_path "" \
#         --model_name "gpt-3.5-turbo"
# done

# # STANDARD (ZERO-SHOT) PROMPTING
# for task in "GameOf24"
# do
#     python run_experiments.py \
#         --task_name ${task} \
#         --meta_config_path prompts/meta-v0-2023-08-14-baseline.json \
#         --output_directory TEST-CHATGPT-STANDARD-PROMPTING \
#         --temperature 0.1 \
#         --include_expert_name_in_instruction \
#         --question_suffix_or_path "" \
#         --question_prefix_or_path "" \
#         --model_name "gpt-3.5-turbo"
# done


### EXAMPLE COMMANDS FOR RUNNING EVALUATION ###
# The following are example commands for running evaluation on the outputs of the experiments.
# Please uncomment the section, modify the parameters as needed, and run the commands in your local environment.
# You can also add more tasks to the list of tasks to evaluate or modify the task evaluation methods/metrics as desired.

# # THE GAME OF 24 TASK EVALUATION
# python evaluate_outputs.py \
#     --directory "outputs/*/" \
#     --task "GameOf24"

# # CHECKMATE-IN-ONE TASK EVALUATION
# python evaluate_outputs.py \
#     --directory "outputs/*/" \
#     --task "CheckmateInOne"

# # WORD SORTING TASK EVALUATION
# python evaluate_outputs.py \
#     --directory "outputs/*/" \
#     --task "word_sorting"

# # P3 (PYTHON PROGRAMMING PUZZLES) TASK EVALUATION
# python evaluate_outputs.py \
#     --directory "outputs/*/" \
#     --task "P3_Test"
