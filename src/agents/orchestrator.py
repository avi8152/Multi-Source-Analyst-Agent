import asyncio
from .rag_agent import rag_node
from .sql_agent import sql_node 
from .web_search_agent import web_search_node

async def parallel_tasks_node(state):
    tasks = []

    if state.get("csv_paths"):
        tasks.append(sql_node(state))

    if state.get("pdf_paths"):
        tasks.append(rag_node(state))

    if state.get("internet_flag"):
        tasks.append(web_search_node(state))

    results = await asyncio.gather(*tasks)

    combined_state = {}
    for partial_state in results:
        combined_state.update(partial_state)

    # Merge original state + updates from all 3
    return {**state, **combined_state}
