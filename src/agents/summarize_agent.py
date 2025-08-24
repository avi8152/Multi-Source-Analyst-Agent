from src.llms import LLMEngine
import random
async def get_llm_instances():
    """
    Asynchronously selects a LLM client  and retrieves corresponding client instances.
    """
    client = LLMEngine()
    llm_type = random.choice(["OPENAI", "GEMINI"])            
    llm_instance = await client.get_llm_instance(llm_type=llm_type)
    return llm_instance

async def summarize(state):
    sql_answer = state.get("sql_answer", "")
    rag_answer = state.get("rag_answer", [])
    internet_answer = state.get("internet_answer", [])
    question = state.get("question", "")
    try:
        source =[]
        template= f""" You are question answering agent.Summarize the findings from different sources as reteived by the question answering agent.\n\nYou will be given the data from different sources and must respond with a concise answer to the question.
        Question: {question}"""
        if sql_answer and sql_answer.lower() != "no data found":
            source.append("SQL database")
            template += f"\n Data retrived from datasource: {sql_answer}"
        if rag_answer != []:
            source.append("PDF documents")
            template += f"\n Data retrieved from PDF documents: {rag_answer}"
        if internet_answer != []:
            source.append("Internet")
            template += f"\n Data retrieved from the internet: {internet_answer}"
        print(f"Template for summarization: {template}")
        llm_instance = await get_llm_instances()
        result = await llm_instance.query_llm(template)
        return {
            "answer": result,
            "source":source
        }
    except Exception as e:
            print(f"Error during summarization: {e}")
            {
            "answer": "AGENT IS DOWN , PLEASE TRY AGAIN LATER",
            "source": "NO DATA FOUND"
        }
