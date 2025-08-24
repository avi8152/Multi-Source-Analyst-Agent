import json5
import re
import duckdb
import pandas as pd
import random
from src.llms import LLMEngine

async def get_llm_instances():
    """
    Asynchronously selects a LLM client  and retrieves corresponding client instances.

    """
    client = LLMEngine()
    llm_type = random.choice(["OPENAI", "GEMINI"])            
    llm_instance = await client.get_llm_instance(llm_type=llm_type)
    return llm_instance

async def sql_node(state):
    print("SQL node invoked")
    question = state["question"]
    csv_files = state.get("csv_paths", [])
    print(f"CSV files available: {csv_files}")
    try:
        df = pd.read_csv(csv_files[0])
        con = duckdb.connect()
        con.register("data", df)
        columns = con.execute("SELECT * FROM data LIMIT 1").df().columns.tolist()

        prompt = f"""
        You are a SQL generation agent. You will receive natural language questions related to a marketing campaign database and must respond with a SQL query that can answer the question.
        Table name : data
        The database schema is as follows:
        The database contains one table with the following columns name:
        -{columns}

        Instructions:
        1. If the user query clearly relates to this schema, generate a syntactically correct SQL query for a PostgreSQL database.
        2. If the user query is not relevant to this schema or asks something unrelated (e.g., weather, sports, biology), reply only with:
        "NO DATA FOUND"
        3. Avoid assumptions—only use the columns explicitly listed above.
        4. Do not hallucinate columns or use data not in the table.

        QUESTION: {question}

        Output format :
        {{'query': 'SELECT ... FROM data WHERE ...'}}
        {{'query': 'NO DATA FOUND'}}
        Now, respond to the user question accordingly.
        """
        llm_instance = await get_llm_instances()
        query = await llm_instance.query_llm(prompt)
        query = query.strip("`'\",").strip()  # Clean unwanted characters
        print(f"Generated SQL query: {query}")
        # Extract JSON from the first '{' to the last '}'
        match = re.search(r'\{.*\}', query, re.DOTALL)

        if match:
            json_data = match.group()  # Extract JSON
            try:
                query = json5.loads(json_data) # Parse JSON with comments support
            except Exception as e:
                raise e
        else:
            raise Exception("Chart Data not found") 
        query = query.get("query", "").strip()
        if query.lower() == "no data found":
            raise Exception("No data found")
        
        result = con.execute(query).fetchdf().to_markdown()
        print(f"SQL Result: {result}")
        # prompt= f" you are question answering agent. You will have the data from the SQL query result and must respond with a concise answer to the question.\n\nQuestion: {question}\n\nSQL Result:\n{result}\n\nAnswer:"
        # result = await query_llm(prompt)
            
        return {
            "sql_answer": result
        }
    except Exception as e:
        return {
            "sql_answer": "NO DATA FOUND"
        }
