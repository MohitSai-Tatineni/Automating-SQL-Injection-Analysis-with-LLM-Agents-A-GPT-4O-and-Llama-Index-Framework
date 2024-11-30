# from scripts.get_all_tables import table_names
# from scripts.get_columns_for_tables import columns_tables
# from scripts.get_user_tom import data_of_user
import json
import requests
import os
import sys


from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI

from scripts.get_all_tables import discover_and_return_table_names
from scripts.get_columns_for_tables import discover_columns
from scripts.get_user_tom import fetch_user_data

# Define tools
table_names_tool = FunctionTool.from_defaults(fn=discover_and_return_table_names)
columns_tables_tool = FunctionTool.from_defaults(fn=discover_columns)
data_of_user_tool = FunctionTool.from_defaults(fn=fetch_user_data)

# Define LLM
llm = OpenAI(model="gpt-4o", temperature=0, timeout=3600)

# Define Agent
agent = ReActAgent.from_tools(
    [table_names_tool, columns_tables_tool, data_of_user_tool],
    llm=llm,
    verbose=True,
    max_retries=3
)

# Example Agent Prompt
prompt = """
Identify all the table names in the database. Determine which table contains user-related information, extract the details of all users, and retrieve the password associated with the user named 'Tom'.
"""

# Run Agent
response = agent.chat(prompt)

print(response)