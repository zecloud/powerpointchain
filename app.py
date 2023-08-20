from langchain.chat_models import AzureChatOpenAI
from langchain.agents import Tool
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.utilities import BingSearchAPIWrapper
from langchain.callbacks import StreamlitCallbackHandler
import streamlit as st
import os

openai_api_key= os.environ.get('OPENAIAPIKEY')
azure_resource_name = os.environ.get('RESOURCE_NAME')
azure_deployment_name = os.environ.get('DEPLOYMENT_NAME')
BASE_URL = "https://"+azure_resource_name+".openai.azure.com"
API_KEY = openai_api_key
DEPLOYMENT_NAME = azure_deployment_name

search = BingSearchAPIWrapper()
llm =  AzureChatOpenAI(
        openai_api_base=BASE_URL,
        openai_api_version="2023-05-15",
        deployment_name=DEPLOYMENT_NAME,
        openai_api_key=API_KEY,
        openai_api_type="azure",
        streaming=True
    )
tools = [Tool(
        name = "Search",
        func=search.run,
        description="useful for when you need to answer questions about current events and new technologies"
    )]
agent = initialize_agent(
    tools, llm, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent.run(prompt, callbacks=[st_callback])
        st.write(response)