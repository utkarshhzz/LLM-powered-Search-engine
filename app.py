import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper,WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun,DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
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
    st.chat_message(msg["role"].write(msg['content']))
    
if prompt:=st.chat_input(placeholder="What is machine learning"):
    st.session_state.messages.append({"role":"user","content":prompt})
    st.chat_message("user").write(prompt)
    
    llm=ChatGroq(api_key=api_key,model="llama-3.1-8b-instant",streaming=True)
    tools=[search,arxiv,wikipedia]
    
    search_agent=initialize_agent(tools,llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,verbose=True )
    with st.spinner("Generating response..."):
        with st.chat_message("assistant"):
            st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
            response=search_agent.run(st.session_state.messages,callbacks=[st_cb])
            st.session_state.messages.append({"role":"assistant","content":response})
            st.write(response)
            
    