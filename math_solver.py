import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_classic.agents.agent_types import AgentType
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_classic.agents import Tool,initialize_agent
from dotenv import load_dotenv
load_dotenv()
from langchain_community.callbacks import StreamlitCallbackHandler
import os


#  set up the steralit app
st.set_page_config(page_title="Text to MAth problem solver and Data Search ASsistant")
st.title("Text to MAth Problem solver USning Gemma2")

groq_api_key=os.getenv("GROQ_API_KEY")
 
if not groq_api_key:
    st.info("Please add your groq api key to continue")
    st.stop()
    
llm=ChatGroq(model="llama-3.1-8b-instant",api_key=groq_api_key)

# initialising our tools
wikipedia_wrapper=WikipediaAPIWrapper()
wikipedia_tool=Tool(
    name="Wikipedia",
    func=wikipedia_wrapper.run,
    description="A tool for searching the internet and solving your math problem"
)

# initialise the math tool using LCEL and LLM directly
math_prompt = PromptTemplate.from_template(
    "You are a strict math calculator capable of evaluating complex math expressions. Safely calculate the following mathematical expression and return ONLY the numeric result. Do not add any text, reasoning, or explanation.\n\nExpression: {expression}\nResult:"
)
math_chain = math_prompt | llm | StrOutputParser()

calculator = Tool(
    name="Calculator",
    func=lambda expr: math_chain.invoke({"expression": expr}),
    description="A tool for solving math problems. Only input mathematical expression needs to be provided." 
)

prompt="""
You are an agent tasked for solving user's mathematical qiestions.Logically arrive at the solution .
provide detailed explanation and display it pointwise.
If you need to search the internet for any information use the wikipedia tool and if you need to solve any mathematical expression use the calculator tool.
Always provide detailed explanation for your answer.
Question:{question}
"""

prompt_template=PromptTemplate(
    input_variables=["question"],
    template=prompt
)

# combine the prompt and LLM using LCEL (replaces deprecated LLMChain)
chain = prompt_template | llm | StrOutputParser()

reasoning_tool=Tool(
    name="Reasoning Tool",
    func=lambda q: chain.invoke({"question": q}),
    description="A tool for answering logic based questions. Input should be a natural language question that may require reasoning and/or mathematical calculations. The tool will provide a detailed, step-by-step explanation of the solution."
    
)

# initialsie the agents

assistant_agent=initialize_agent(
    tools=[wikipedia_tool,calculator,reasoning_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_error=True
)

if "messages"not in st.session_state:
    st.session_state["messages"]=[
        {"role": "assistant", "content":"Hi,i'm a math chatbot who can answer all your math related questions. How can I help you today?"}
        
    ]
    
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])
    
# function to generate the response
def generate_response(question):
    response=assistant_agent.invoke({"input":question})
    return response

# letss tart the interacfiton

question= st.text_area("Enter your question:","I have 5 bananas and I eat 2. How many bananas do I have left?")
if st.button("Find my Answer"):
    if question:
        with st.spinner("Generate response..."):
            st.session_state.messages.append({"role":"user","content":question})
            st.chat_message("user").write(question)
            st_cb=StreamlitCallbackHandler(st.container(), expand_new_thoughts=True)
            response=assistant_agent.run(st.session_state.messages,callbacks=[st_cb])
            
            st.session_state.messages.append({'role': 'assistant','content':response})
            st.write('### Response:')
            st.success(response)
    else:
        st.warning("Please enter a question to get the answer.")
            