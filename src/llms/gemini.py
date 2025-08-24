import textwrap
from.base import BaseLLM
from google.generativeai import GenerativeModel
from dotenv import load_dotenv
load_dotenv()


class GeminiLLM(BaseLLM):
    def __init__(self):
        self.model = "gemini-1.5-flash-002"

    async def query_llm(self, prompt):
        print("entered google")
        system_instruction = """
                You are an expert at providing search results to other LLMs in a clear and concise manner.
                You will be asked a question and you should respond only with factual statements based on the search results.
                """
        model = GenerativeModel(
            model_name=self.model,
            system_instruction=textwrap.dedent(system_instruction).strip()
        )
        response = await model.generate_content_async(
            contents=prompt,
        )
        parts = response.candidates[0].content.parts
        full_text = "\n\n".join(p.text for p in parts)
        return full_text
