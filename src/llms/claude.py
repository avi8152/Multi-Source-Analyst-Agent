import anthropic
from.base import BaseLLM

class ClaudeLLM(BaseLLM):
    def __init__(self):
        self.llm_instance = anthropic.Anthropic()
        self.model="claude-sonnet-4-20250514"
        self.max_tokens = 1024

    def query_llm(self,prompt):
        messages=[
        {"role": "user", "content": prompt}
    ]
        response = self.llm_instance.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=messages
        )
        final_response = response['choices'][0]['message']['content']
        return final_response
    
