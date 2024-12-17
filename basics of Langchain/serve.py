from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from langserve import add_routes
from dotenv import load_dotenv
load_dotenv()


groq_api_key=os.getenv("GROQ_API_KEY")
model=ChatGroq(model="Gemma2-9b-It",groq_api_key=groq_api_key)

# creae prompt template
system_templtes="Translate the following into{language}"
prompt_Template=ChatPromptTemplate.from_messages(

    [('system',system_templtes),
     ("user","{text}")]
)

parser=StrOutputParser()

# create chain

chain=prompt_Template|model|parser

# app defination
app=FastAPI(title="langchain_server",
           version="1.0",
           description="A simple API server using Lnagchain runnable interfaces")
# adding chain route
add_routes(

    app,
    chain,
    path="/chain"
)

if __name__=='__main__':
    import uvicorn
    uvicorn.run(app,host="localhost",port=8000)

