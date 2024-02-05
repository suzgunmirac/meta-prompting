from typing import Any, Dict, List, Optional, Union
from .meta_scaffolding import MetaPromptingScaffolding


# Expert prompting scaffolding
class ExpertPrompting(MetaPromptingScaffolding):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Generate the expert's identity
    def generate_expert_identity(
        self,
        prompt_or_messages: Union[str, List[Dict[str, str]]],
        stop_tokens: Optional[List[str]] = None,
        max_tokens: int = 512,
        num_return_sequences: int = 1,
        temperature: float = 0.7,
        top_p: Optional[float] = None,
        **kwargs: Any,
    ) -> str:
        """
        Create the identity and description of the expert.
        """
        meta_model_output = self.language_model.generate(
            prompt_or_messages=prompt_or_messages,
            stop_tokens=stop_tokens,
            max_tokens=max_tokens,
            num_return_sequences=num_return_sequences,
            temperature=temperature,
            top_p=top_p,
            **kwargs,
        )[0]

        return meta_model_output
