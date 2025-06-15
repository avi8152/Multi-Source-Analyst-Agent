import json5
import re
import duckdb
import pandas as pd
from src.clients.openai import query_llm


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
        query = await query_llm(prompt)
        query = query.strip("'\",").strip()  # Clean unwanted characters
        print(f"Generated SQL query: {query}")
        # Extract JSON from the first '{' to the last '}'
        match = re.search(r'\{.*\}', query, re.DOTALL)

        if match:
            json_data = match.group()
            try:
                query = json5.loads(json_data)
            except Exception as e:
                raise e
        else:
            raise Exception("Chart Data not found") 
        query = query.get("query", "").strip()
        if query.lower() == "no data found":
            raise Exception("No data found")
        
        result = con.execute(query).fetchdf().to_markdown()
        print(f"SQL Result: {result}")
            
        return {
            "sql_answer": result
        }
    except Exception as e:
        return {
            "sql_answer": "NO DATA FOUND"
        }