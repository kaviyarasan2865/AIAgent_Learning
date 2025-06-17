from langchain_core.language_models import BaseLLM
from langchain_core.outputs import LLMResult
from typing import Optional, List, Any, Mapping
from pydantic import Field, BaseModel
import google.generativeai as genai

class GeminiLLM(BaseLLM, BaseModel):
    model_name: str = Field(default="gemini-1.5-flash")
    api_key: str = Field(...)
    
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        super().__init__(api_key=api_key, model_name=model)
        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel(model)

    def invoke(self, prompt: str, **kwargs: Any) -> str:
        """Direct invocation method for simple string inputs"""
        try:
            response = self._model.generate_content(prompt)
            if hasattr(response, 'text'):
                return response.text.strip()
            return str(response)
        except Exception as e:
            return f"Error generating response: {str(e)}"

    @property
    def _llm_type(self) -> str:
        return "gemini"
    
    def _generate(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> LLMResult:
        """Generate method required by LangChain"""
        generations = []
        for prompt in prompts:
            response = self.invoke(prompt, **kwargs)
            generations.append([{"text": response, "generation_info": {}}])
        return LLMResult(generations=generations)
