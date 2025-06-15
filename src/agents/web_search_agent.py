from langchain_tavily import TavilySearch

async def web_search_node(state):
    
    question = state["question"]

    print("Web search node invoked")
    tool = TavilySearch(
    max_results=3,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
    )
    try:
        tool_message=tool.invoke({"query": question})
        response_list = []
        for item in tool_message.get("results", []):
            response_list.append({
                'url': item['url'],
                'content': item['content']
            })
        print(f"Web search results: {response_list}")
        return {
            "internet_answer": response_list
        }
    except Exception as e:
        print(f"Error during web search: {e}")
        return {
            "internet_answer": []
        }