import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper,WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun,DuckDuckGoSearchRun
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv
load_dotenv()


st.title("Langchain- Chat with search")
"""in this example we are using StreamLitcallback handler to display the thoughts and actions of an agent in an interactive streamit app.

    """
st.sidebar.title("Settings")
api_key=os.getenv("GROQ_API_KEY")

# arxiv and wikipedia tools
arxiv_wrapper=ArxivAPIWrapper(top_k_results=1,doc_content_chars_max=200)
arxiv=ArxivQueryRun(api_wrapper=arxiv_wrapper)

wikipedia_wrapper=WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=200)
wikipedia=WikipediaQueryRun(api_wrapper=wikipedia_wrapper)

search=DuckDuckGoSearchRun(name="Search")

if "messages" not in st.session_state:
    st.session_state["messages"]=[
        {"role":"assisstant",
         "content":"Hi,i'm a chatbot that can search the web "}
    ]
    
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])
    
if prompt:=st.chat_input(placeholder="What is machine learning"):
    st.session_state.messages.append({"role":"user","content":prompt})
    st.chat_message("user").write(prompt)
    
    llm=ChatGroq(api_key=api_key,model="llama-3.1-8b-instant",streaming=True)
    tools=[search,arxiv,wikipedia]
    
    prompt_template=ChatPromptTemplate.from_messages([
        ("system","You are a helpful assistant.Use tools if neccesary to answer the user's queries"),
        ("human","{input}"),
        ("placeholder","{agent_scratchpad}"),
    ]) 
    agent=create_tool_calling_agent(llm,tools,prompt_template)
    
    # creating the executor
    agent_executor=AgentExecutor(agent=agent,tools=tools,verbose=True)
    with st.spinner("Generating response..."):
        with st.chat_message("assistant"):
            st_container=st.empty()
            st_cb=StreamlitCallbackHandler(st_container,expand_new_thoughts=False)
            
            response=agent_executor.invoke(
                {"input":prompt},
                callbacks=[st_cb]
            )
            
            result_text=response["output"]
            st.session_state.messages.append({"role":"assistant","content":result_text})
            st.write(result_text)
    