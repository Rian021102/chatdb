import streamlit as st
from sqlalchemy.engine import create_engine
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
import os

# Create the Streamlit app
st.title("Chat with Your Database")

# Set up your credentials and configurations
project = "intricate-idiom-379506"
dataset = "volveprod"
table = "volveprod"

# Retrieve the JSON key content from Streamlit secrets
service_account_info = st.secrets["gcp_service_account"]

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/tmp/gcp_credentials.json"

# Create a temporary file and write the JSON key content to it
with open("/tmp/gcp_credentials.json", "w") as credentials_file:
    credentials_file.write(service_account_info)

# Initialize SQLDatabase, OpenAI, and the agent executor
db = SQLDatabase.from_uri(f'bigquery://{project}/{dataset}')
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
    Put your query here for instance:
    show 5 row oil volume of the well bore named 15/9-F-1 C? descending by DATEPRD where BORE_OIL_VOL > 0.0
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
