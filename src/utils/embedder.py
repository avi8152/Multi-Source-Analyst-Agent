import os
import numpy as np
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
embed_model =  OpenAIEmbeddings(model="text-embedding-3-small", api_key=api_key)

async def get_embeddings(text_data
) -> np.ndarray:
    embeddings_result = embed_model.embed_documents(text_data)
    embeddings_array = np.asarray(embeddings_result, dtype="float32")
    return embeddings_array