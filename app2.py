import streamlit as st
from pathlib import Path
from langchain_classic.agents import create_sql_agent
from langchain_classic.sql_database import SQLDatabase
from langchain_classic.agents.agent_types import AgentType
from langchain_classic.callbacks import StreamlitCallbackHandler
from langchain_classic.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq


st.set_page_config(page_title="Langchain: Chat with SQL db",page_icon=":bird:")
st.title("Langchain: Chat with SQL db")

LOCALDB="USE_LOCALDB"
MYSQL="USE_MYSQL"

# radio options
radio_opt=[]