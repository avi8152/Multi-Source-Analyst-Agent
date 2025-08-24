import numpy as np
from PyPDF2 import PdfReader
import faiss
import random
from src.llms import LLMEngine

async def get_llm_instances():
    """
    Asynchronously selects a research agent type and retrieves corresponding client and agent instances.
    """
    client = LLMEngine()
    llm_type = random.choice(["OPENAI", "GEMINI"])            
    llm_instance = await client.get_llm_instance(llm_type=llm_type)
    return llm_instance


def chunk_text(text: str, chunk_size: int = 1000) -> list[str]:
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def read_pdf(file_path: str) -> list[str]:
    try:
        reader = PdfReader(file_path)
        text = "".join(page.extract_text() + "\n" for page in reader.pages)
        return [text]
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        raise

async def search_tool(query: str, index, chunked_docs, top: int = 3) -> list[str]:
    llm_instance = await get_llm_instances()
    embed = await llm_instance.get_embeddings([query])
    faiss.normalize_L2(embed)
    _, indices = index.search(embed, top)
    return [chunked_docs[idx] for idx in indices[0]]

async def load_and_split_pdfs(pdf_paths: list[str]) -> list[str]:
    all_chunked_docs = []
    all_embeddings = []
    for pdf_path in pdf_paths:
        docs = read_pdf(pdf_path)
        chunked_docs = [chunk for doc in docs for chunk in chunk_text(doc)]
        all_chunked_docs.extend(chunked_docs)
        llm_instance = await get_llm_instances()
        # Get embeddings for the chunked documents
        embeddings = await llm_instance.get_embeddings(chunked_docs)
        faiss.normalize_L2(embeddings)
        all_embeddings.append(embeddings)

    # Combine all embeddings into a single array
    all_embeddings = np.vstack(all_embeddings)

    # Create FAISS index
    d = all_embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(all_embeddings)
    print(f"Loaded {len(all_chunked_docs)} chunks from {len(pdf_paths)} PDFs.")
    return index, all_chunked_docs