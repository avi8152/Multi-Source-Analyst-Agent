import asyncio
import os
from langgraph.graph import StateGraph,START,END
from src.agents.orchestrator import parallel_tasks_node
from src.agents.summarize_agent import summarize
from typing import TypedDict


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
        # pdf_paths = []


        graph = StateGraph(State)


        # graph.add_node("router", router_node)
        graph.add_node("parallel_tasks", parallel_tasks_node)
        graph.add_node("summarize", summarize)
        graph.add_edge(START, "parallel_tasks")
        graph.add_edge("parallel_tasks", "summarize")
        graph.add_edge("summarize", END)
        # Compile
        agent_executor = graph.compile()

 
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(agent_executor.ainvoke({
        "question": question,
        "pdf_paths": pdf_paths,
        "csv_paths":csv_paths,
        "internet_flag":web_search  # Assuming pdf_paths is defined somewhere in your code
        }))
        loop.close()
        return {
        "answer": response['answer'],
        "source": response['source']
    }

if __name__ == "__main__":
    question = "How many campaigns were conducted in Spanish?"
    response = get_answer_response.get_answer(question)
    print(response)
