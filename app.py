from langchain.chat_models import AzureChatOpenAI
from langchain.agents import Tool
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.utilities import BingSearchAPIWrapper
from langchain.callbacks import StreamlitCallbackHandler
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks import HumanApprovalCallbackHandler
from langchain.output_parsers import PydanticOutputParser
from langchain.tools import StructuredTool
from pydantic.v1 import BaseModel, Field, validator
from msal_streamlit_authentication import msal_authentication
from pptx import Presentation
from typing import List
import streamlit as st
import os
import json

openai_api_key= os.environ.get('OPENAIAPIKEY')
azure_resource_name = os.environ.get('RESOURCE_NAME',"zecloud")
azure_deployment_name = os.environ.get('DEPLOYMENT_NAME',"chatgpt")
BASE_URL = "https://"+azure_resource_name+".openai.azure.com"
API_KEY = openai_api_key
DEPLOYMENT_NAME = azure_deployment_name

with st.sidebar:
    token = msal_authentication(
        auth={
            "clientId": "bba1e505-6268-4e5b-a685-92567d288344",
            "authority": "https://login.microsoftonline.com/9d430f15-406c-4dc1-9606-6a7406d91642",
            "redirectUri": "/",
            "postLogoutRedirectUri": "/"
        },
        cache={
            "cacheLocation": "sessionStorage",
            "storeAuthStateInCookie": False
        },
        login_request={
            "scopes": ["files.readwrite.all"]
        },
        key=1)

os.environ["BING_SEARCH_URL"]=os.environ.get("BING_ENDPOINT","https://api.bing.microsoft.com//v7.0/search") 
search = BingSearchAPIWrapper()
llm =  AzureChatOpenAI(
        openai_api_base=BASE_URL,
        openai_api_version="2023-05-15",
        deployment_name=DEPLOYMENT_NAME,
        openai_api_key=API_KEY,
        openai_api_type="azure",
        streaming=True
    )

class Slide(BaseModel):
    title: str = Field(description="Title of the slide")
    content: List[str] = Field(description="Content of the slide")
    prompt: str = Field(description="Prompt of the slide")

class Slides(BaseModel):
    subject: str = Field(description="Subject of the presentation")
    slides: List[Slide] = Field(description="Slides of the presentation")
    


def save_slides(subject:str,slides: Slides):
    
    prs = Presentation("template.pptx")
    bullet_slide_layout = prs.slide_layouts[6]
    prs.slides[0].shapes[2].text = subject
    for i in range(0,len(slides)):
        
        slide = prs.slides.add_slide(bullet_slide_layout)
        shapes = slide.shapes

        title_shape = shapes.title
        
        body_shape = shapes.placeholders[10]

        title_shape.text = slides[i]["title"]
        tf = body_shape.text_frame
        for content in slides[i]["content"]:
            p = tf.add_paragraph()
            p.text = content
            p.level = 1
    prs.save('test.pptx')
    #with open("slides.json", "w") as f:
    #     f.write(json.dumps(slides))

tool_save_slide = StructuredTool.from_function(save_slides,description="Save the slides to a local file",args_schema=Slides)

parser = PydanticOutputParser(pydantic_object=Slides)

prompt = PromptTemplate(
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
    template="""You are a software developer creating an automated PowerPoint generation program.
         
         You decide the content that goes into each slide of the PowerPoint.
         Each slide typically consists of a topic, introduction, main points, conclusion, and references.
         Follow the rules below:\n
         Summarize and extract the key contents from the user's input around 5 slides.\n
         Each slide contains 'title', 'content' and 'prompt'.\n
         'content' is a bullet point that breaks down the core content into brief, step-by-step chunks.\n
         All of the slides contain images.\n
         If the slide contains a image, create a prompt to generate an image using the DALL-E API. And save it into 'prompt'.\n
         {format_instructions}\n
         {query}\n"""
         #Focus on nouns and adjectives and separate them with commas so that 'prompt' is a good visual representation of 'content'.\n
         #Set the above contents as keys named 'title', 'content', and 'prompt'.\n
         #Save the results of each slide as a JSON list.\n
         #Output the final output in JSON format.\n
         #Make sure output JSON can be parsed with Python `json.loads()`.\n
         #Must return JSON format only\n
)

llm_chain = LLMChain(llm=llm, prompt=prompt)

# initialize the LLM tool
llm_tool = Tool(
    name='Slide Generator',
    func=llm_chain.run,
    description='useful to generate slides for your next presentation'
)


#tools = load_tools(["llm-math"], llm=llm)
tools=[Tool(
        name = "Search",
        func=search.run,
        description="useful for when you need to answer questions about current events or the current state of the world"
    ),llm_tool,tool_save_slide]
agent = initialize_agent(
    tools, llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent.run(prompt, callbacks=[st_callback])
        st.write(response)