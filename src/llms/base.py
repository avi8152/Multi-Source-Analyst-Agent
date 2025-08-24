import numpy as np
from google.generativeai import embed_content
from dotenv import load_dotenv
load_dotenv()

class BaseLLM:

    def __init__(self):
        """
        Initialize the BaseLLM with authentication details and base URL.
        """
        pass

    async def query_llm(self, prompt):
        pass

    async def get_embeddings(self,text_data
    ) -> np.ndarray:
        embeddings_list = []
        result = embed_content(model="models/text-embedding-004",
        content=text_data)
        embeddings = result.get("embedding")
        if isinstance(embeddings, list):
            embeddings_list.extend(embeddings)    # Append directly if it's a list of vectors
        else:
            print("Unexpected embedding format: %s", type(embeddings))
            raise TypeError("Embedding result is not a list")
                    
        embeddings_array = np.asarray(embeddings_list, dtype="float32")
        return embeddings_array
