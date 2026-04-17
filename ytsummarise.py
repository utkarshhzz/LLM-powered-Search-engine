import validators,streamlit as st
from langchain_classic.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader
import os
from dotenv import load_dotenv
load_dotenv()

# streamlit app
st.set_page_config(page_title="Langchain: Summarize text from YT or website")
st.title("Langchain: Summarize text from YT or website")
st.subheader("Summarize URL")

# get the groq api key and   url(yt or website to be summarized)

groq_api_key=os.getenv("GROQ_API_KEY")

generic_url=st.text_input("URL",label_visibility="collapsed")
llm=ChatGroq(model="llama-3.1-8b-instant",api_key=groq_api_key)
prompt_template="""
Provide  a summary of the following content in 300 words.
content:{text}
"""
prompt=PromptTemplate(template=prompt_template,input_variables=["text"])


if st.button("Summarize the content from yt or website"):
    # validate
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide both GROQ API key and URL") 
    elif not validators.url(generic_url):
        st.error("PLease enter a valid URL.It can be a yt video url or website url")
    else:
        try:
            with st.spinner("Waiting..."):
                # loading  the website or yt data
                if "youtube.com" in generic_url or "youtu.be" in generic_url:
                    loader=YoutubeLoader.from_youtube_url(generic_url, add_video_info=False)
                else:
                    loader=UnstructuredURLLoader(urls=[generic_url],ssl_verify=False,headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})
                docs=loader.load()
                
                # Chain for summarization
                chain=load_summarize_chain(llm,chain_type="stuff",prompt=prompt)
                output_summary=chain.run(docs)
                
                st.success("Output summary:")
                st.write(output_summary)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")