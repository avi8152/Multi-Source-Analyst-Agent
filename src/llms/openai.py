import os
from dotenv import load_dotenv
load_dotenv()
from langchain.schema import SystemMessage
from langchain_openai import ChatOpenAI
from .base import BaseLLM
class OpenAILLM(BaseLLM):
    def __init__(self):
        self.model="gpt-4o-mini"
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.llm_instance = ChatOpenAI(model=self.model, api_key=self.api_key)
        
    async def query_llm(self,prompt):
        print("entered openai")
        messages = [SystemMessage(content=prompt)]
        response = await self.llm_instance.ainvoke(messages)
        return response.content
