import streamlit as st
import pandas as pd
from sqlalchemy.engine import create_engine
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
import secrets
import os
import re

# Create the Streamlit app
st.title("Chat with Your Database")

# Set up your credentials and configurations using github secret
# Set up your credentials and configurations using github secret
gcp_service_account = st.secrets["gcp_service_account"]

# Extract the required fields from the AttrDict
private_key_id = gcp_service_account["private_key_id"]
private_key = gcp_service_account["private_key"]
client_email = gcp_service_account["client_email"]

# Create a JSON key string
gcp_service_account_json = f'''
{{
  "type": "service_account",
  "project_id": "intricate-idiom-379506",
  "private_key_id": "{private_key_id}",
  "private_key": "{private_key}",
  "client_email": "{client_email}",
  "client_id": "114664848711218640743",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/{client_email}",
  "universe_domain": "googleapis.com"
}}
'''

# Set the environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcp_service_account_json
# Database connection
project = "intricate-idiom-379506"
dataset = "volveprod"
table = "volveprod"
sqlalchemy_url = f'bigquery://{project}/{dataset}'

db = SQLDatabase.from_uri(sqlalchemy_url)
llm = OpenAI(temperature=0, model="text-davinci-003")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    top_k=1000,
)

# Sidebar with information about the app
st.sidebar.header("About")
st.sidebar.markdown(
    """
This is a demo of utilizing the LangChain framework to chat with your database.
the database used is the Volve dataset from the Norwegian Petroleum Directorate.
Below all the wellname in the dataset
15/9-F-4' ; '15/9-F-5' ; '15/9-F-12' ; '15/9-F-14' ; '15/9-F-11' ; '15/9-F-15 D' ;
'15/9-F-1 C'
the dataset is uploaded to the google bigquery
"""
)

# Input text box for user input
st.markdown(
    """
    Put your query here, for instance:
    show 5 row oil volume of well 15/9-F-1 C? descending by date where oil volume is not zero,
    or you can ask to show the well name in the dataset distinct by well name
    """
)
user_input = st.text_input("Enter your query:")

# Button to execute the agent
if st.button("Execute"):
    if user_input:
        # Execute the agent with user input
        result = agent_executor.run(user_input)
        st.write("Agent Response:")
        st.write(result)      

    else:
        st.warning("Please enter a query.")
