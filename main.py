import asyncio
import os
from langgraph.graph import StateGraph,START,END
from src.agents.sql_agent import sql_node
from src.agents.rag_agent import rag_node
from src.agents.web_search_agent import web_search_node
from src.agents.summarize_agent import summarize
from typing import TypedDict
from IPython.display import Image, display


class State(TypedDict):
    question: str
    sql_answer: str
    internet_answer: list[dict]
    rag_answer: list
    answer: str
    pdf_paths: list[str]
    csv_paths: list[str]
    source: list[str]
    internet_flag: bool
    

class get_answer_response():
    def get_answer(question: str,web_search: bool = True):
        pdf_paths = []
        csv_paths = []
        pdf_files = os.listdir("src/data/docs")
        if pdf_files:
            pdf_paths = [os.path.join("src/data/docs", pdf) for pdf in pdf_files]
        csv_files = os.listdir("src/data/sheets")
        if csv_files:
            csv_paths = [os.path.join("src/data/sheets", csv) for csv in csv_files] if csv_files else []



        graph = StateGraph(State)
        graph.add_node("sql", sql_node)
        graph.add_node("rag", rag_node)
        graph.add_node("internet", web_search_node)
        graph.add_node("summarize", summarize)

     
        graph.add_conditional_edges(
            START,
            lambda state: (
                "sql" if state.get("csv_paths") else
                "rag" if state.get("pdf_paths") else
                "internet"
            ),
            path_map={"sql": "sql", "rag": "rag", "internet": "internet"}
        )

        # SQL → RAG and/or Internet → Summarize
        graph.add_conditional_edges(
            "sql",
            lambda state: (
                "rag" if state.get("pdf_paths") else
                "internet" if state.get("internet_flag") else
                "summarize"
            ),
            path_map={"rag": "rag", "internet": "internet", "summarize": "summarize"}
        )

        # RAG → Internet or Summarize
        graph.add_conditional_edges(
        "rag",
        lambda state: "internet" if state.get("internet_flag") else "summarize",
        path_map={"internet": "internet", "summarize": "summarize"}
    )
        graph.add_conditional_edges(
            "internet",
            lambda state: "summarize",
            path_map={"summarize": "summarize"}
        )

        graph.add_edge("summarize", END)
        # Compile
        agent_executor = graph.compile()

        
 
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(agent_executor.ainvoke({
        "question": question,
        "pdf_paths": pdf_paths,
        "csv_paths":csv_paths,
        "internet_flag":web_search 
        }))
        loop.close()
        return {
        "answer": response['answer'],
        "source": response['source']
    }
