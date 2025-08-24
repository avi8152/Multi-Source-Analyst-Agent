"""
This module defines the LLMFactory class, which is responsible for creating instances of different
LLMS based on the provided llm_type. It imports necessary modules and initializes the factory.
"""

from .claude import ClaudeLLM
from .openai import OpenAILLM
from .gemini import GeminiLLM

class LLMEngine():

    def __init__(self):
        pass
        
    async def get_llm_instance(self, llm_type):

        if llm_type == "ANTHROPIC":
            return ClaudeLLM()
        elif llm_type == "GEMINI":
            return GeminiLLM()
        else:
            return OpenAILLM()
