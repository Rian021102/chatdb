from google.cloud import bigquery
from sqlalchemy import *
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import *
import os
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor

service_account_file = "/Users/rianrachmanto/pypro/bigquery/intricate-idiom-379506-21563d575ba3.json" # Change to where your service account key file is located
project = "intricate-idiom-379506"
dataset = "volveprod"
table = "volveprod"
sqlalchemy_url = f'bigquery://{project}/{dataset}?credentials_path={service_account_file}'


os.environ["OPENAI_API_KEY"] = "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"

db = SQLDatabase.from_uri(sqlalchemy_url)
llm = OpenAI(temperature=0, model="text-davinci-003")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent_executor = create_sql_agent(
llm=llm,
toolkit=toolkit,
verbose=True,
top_k=1000,
)


agent_executor.run("show 5 row oil volume of the well bore named 15/9-F-1 C? descending by DATEPRD where BORE_OIL_VOL > 0.0 ")

