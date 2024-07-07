import os
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
import gradio as gr
from dotenv import load_dotenv
load_dotenv()

MSSQL_AGENT_PREFIX = """

You are an agent designed to interact with a SQL database.
## Instructions:
- Given an input question, create a syntactically correct {dialect} query
to run, then look at the results of the query and return the answer.
- Unless the user specifies a specific number of examples they wish to
obtain, **ALWAYS** limit your query to at most {top_k} results.
- You can order the results by a relevant column to return the most
interesting examples in the database.
- Never query for all the columns from a specific table, only ask for
the relevant columns given the question.
- You have access to tools for interacting with the database.
- You MUST double check your query before executing it.If you get an error
while executing a query,rewrite the query and try again.
- DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.)
to the database.
- DO NOT MAKE UP AN ANSWER OR USE PRIOR KNOWLEDGE, ONLY USE THE RESULTS
OF THE CALCULATIONS YOU HAVE DONE.
- Your response should be in Markdown. However, **when running  a SQL Query
in "Action Input", do not include the markdown backticks**.
Those are only for formatting the response, not for executing the command.
- ALWAYS, as part of your final answer, explain how you got to the answer
on a section that starts with: "Explanation:". Include the SQL query as
part of the explanation section.
- If the question does not seem related to the database, just return
"I don\'t know" as the answer.
- Only use the below tools. Only use the information returned by the
below tools to construct your query and final answer.
- Do not make up table names, only use the tables returned by any of the
tools below.

## Tools:

"""

MSSQL_AGENT_FORMAT_INSTRUCTIONS = """

## Use the following format:

Question: the input question you must answer.
Thought: you should always think about what to do.
Action: the action to take, should be one of [{tool_names}].
Action Input: the input to the action.
Observation: the result of the action.
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer.
Final Answer: the final answer to the original input question.

The database contains information about pricing of Firmbee app.
The most important information about available difference in packages is store in table: PricingPackages.
Remaining tables contain useful information about available modules: 
module 'Administration & handy tools' is in table AdministrationHandyTools,  
module 'Integrations' is in table Integrations,              
module 'Recruitment and HR tools' is in table  RecruitmentHRTools, 
module 'Cooperation tools' is in table CooperationTools,
module 'Finance tools' is in table  FinanceTools
and module 'Projects and remote work' is in table  ProjectsRemoteWork.      


"""

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

database_file_path = 'data/firmbee_offering.db'
db = SQLDatabase.from_uri(f'sqlite:///{database_file_path}')
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

QUESTION = """I run marketing agency. What is the best offer for me and what are the main features and cost?
"""

agent_executor_SQL = create_sql_agent(
    prefix=MSSQL_AGENT_PREFIX,
    format_instructions = MSSQL_AGENT_FORMAT_INSTRUCTIONS,
    llm=llm,
    toolkit=toolkit,
    top_k=30,
    verbose=True
)

# agent_executor_SQL.invoke(QUESTION)

iface = gr.Interface(
    fn=agent_executor_SQL,
    inputs="text",
    outputs="text",
    title="Chatbot",
    description="Ask a question and get an answer from the custom document"
)

iface.launch(share=True)

