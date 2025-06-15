import os
from dotenv import load_dotenv
load_dotenv()
from langchain.schema import SystemMessage
from langchain_openai import ChatOpenAI
api_key = os.getenv("OPENAI_API_KEY")


llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)

async def query_llm(prompt):
    messages = [SystemMessage(content=prompt)]
    response = await llm.ainvoke(messages)
    return response.content