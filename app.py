#importing the libraries:
import os
from dotenv import load_dotenv
import streamlit as st
from fastapi import FastAPI
import uvicorn
import requests
from langserve import add_routes
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama

#loading the environment variables:
load_dotenv()

#initializing fast-api app:
app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="Api Server Demo")

#creating a prompt template:
prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Please respond to the user's queries."),
        ("user","Question:{question}")
    ]
)


#creating the LLM model using ollama LLAMA2:
llm = Ollama(model="llama2")
output_parser = StrOutputParser()

#creating the chain:
chain = prompt | llm | output_parser


#creating the UI:
st.title("Langchain Chatbot")
input_text = st.text_input("Ask a question...")
if input_text:
    st.write(chain.invoke({"question":input_text}))


#creating a route:
add_routes(
    app=app,
    runnable=chain,
    path="/chatbot")


#creating a fucntion to get response from api:
def get_response(input_text):
    response = requests.post("http://localhost:8000/chatbot/invoke",
                             json={"input":{"question":input_text}})
    return response.json()['output']


#running with uvicorn:
if __name__ == "__main__":
    uvicorn.run(app=app,
                host="localhost",
                port=8000)







