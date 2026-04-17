from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper,WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun,DuckDuckGoSearchRun
from langchain_classic.agents import AgentExecutor,create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()

app=FastAPI(title="Agentic AI backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    prompt:str
    
# initialising tools and llm
api_key=os.getenv("GROQ_API_KEY")
llm=ChatGroq(api_key=api_key,model="llama-3.1-8b-instant")

arxiv_wrapper=ArxivAPIWrapper(top_k_results=1,doc_content_chars_max=200)
arxiv=ArxivQueryRun(api_wrapper=arxiv_wrapper)

wikipedia_wrapper=WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=200)
wikipedia=WikipediaQueryRun(api_wrapper=wikipedia_wrapper)

search=DuckDuckGoSearchRun(name="Search")
tools=[search,arxiv,wikipedia]

# creating agent
prompt_template=ChatPromptTemplate.from_messages([
    ("system","You are a helpful assistant.USe tools if neccesary to asnwer the user's queries. "),
    ("human","{input}"),
    ("placeholder","{agent_scratchpad}"),
])
agent=create_tool_calling_agent(llm,tools,prompt_template)
agent_executor=AgentExecutor(agent=agent,tools=tools,verbose=True,return_intermediate_steps=True)

# Creating the API endpoint
@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    # running the agent 
    response=agent_executor.invoke({"input":request.prompt})
    # extracting the tools it used so we can show on next js frontend
    steps=[]
    
    for action,observation in response.get("intermediate_steps",[]):
        steps.append({
            "tool": action.tool,
            "input": action.tool_input,
            "output": observation
        })
        
    return {
            "answer": response["output"],
            "steps": steps
        }
