import os
import openai 
from dotenv import find_dotenv, load_dotenv
from langchain_community.llms import OpenAI  # LangChain wrapper that simplifies interaction with OpenAI API, independently of the openai module imported above
from langchain_community.chat_models import ChatOpenAI  # LangChain wrapper for the ChatOpenAI
from langchain.schema import HumanMessage  # Object to pass to the ChatOpenAI instanciated object when we want to invoke the predict_messages method

load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

llm_model = "gpt-4o-mini"


prompt = "How old is the universe"
messages = [HumanMessage(content=prompt)]

# The higher the temperature, the more creative of an answer we will get
llm = OpenAI(
#    openai_api_key=os.getenv("OPENAI_API_KEY"), 
    temperature=0.7)  # We could have written llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY")) but no need to do this since we already passed the key to the openai object and it goes through the same channel.

chat_model = ChatOpenAI(temperature=0.7)

print(llm.predict("Descibe what is the difference between langchain and langgraph in a simple manner in a brief single phrase"))
print("===============================================================")
# print(chat_model.predict("Descibe what is the difference between langchain and langgraph in a simple manner in a brief single phrase"))
print(chat_model.predict_messages(messages))