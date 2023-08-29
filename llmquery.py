import streamlit as st
from google.cloud import bigquery
from sqlalchemy.engine import create_engine
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
import os
import secrets

# Set up your credentials and configurations
service_account_file = os.environ["BIG_QUERY_KEY"]  # Change to your service account key file
project = "intricate-idiom-379506"
dataset = "volveprod"
table = "volveprod"
sqlalchemy_url = f'bigquery://{project}/{dataset}?credentials_path={service_account_file}'
os.environ["OPENAI_API_KEY"] = secrets["OPEN_AI_KEY"]

# Initialize SQLDatabase, OpenAI, and the agent executor
db = SQLDatabase.from_uri(sqlalchemy_url)
llm = OpenAI(temperature=0, model="text-davinci-003")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    top_k=1000,
)

# Create the Streamlit app
st.title("Chat with Your Database")

#make a body on the left side
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
#put mark down above the input box
st.markdown(
    """
    Put your query here for instance:
    show 5 row oil volume of well 15/9-F-1 C? descending by date where oil volume is not zero,
    or you can ask show the well name in the dataset distinct by well name
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

# Add any other Streamlit components as needed
