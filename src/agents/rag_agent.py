from src.utils.pdf_loader import load_and_split_pdfs,search_tool

async def rag_node(state):
    print("RAG node invoked")
    question = state["question"]
    pdf_paths = state.get("pdf_paths", [])
    try:
        index,chunked_docs = await load_and_split_pdfs(pdf_paths)
        docs = await search_tool(question, index, chunked_docs, top=3)

        if not docs:
            raise Exception("No relevant chunks found in PDF")

        return {
            "rag_answer": docs
        }
    except Exception as e:
        return {
                "rag_answer": []
            }


