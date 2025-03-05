import os
import openai
from dotenv import find_dotenv, load_dotenv
from langchain_community.llms import OpenAI  
# from langchain_community.chat_models import ChatOpenAI  # depricated
from langchain_openai import ChatOpenAI
# from langchain.prompts import ChatPromptTemplate  # depricated
from langchain_core.prompts import ChatPromptTemplate


load_dotenv(find_dotenv())
client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

llm_model = "gpt-4o-mini"
chat = ChatOpenAI(temperature=0.0, model=llm_model)


email_response = """
Here's our itinerary for our upcoming trip to Europe.
There will be 5 of us on this vacation trip.
We leave from Denver, Colorado airport at 8:45 pm, and arrive in Amsterdam 10 hours later
at Schipol Airport.
We'll grab a ride to our airbnb and maybe stop somewhere for breakfast before 
taking a nap.

Some sightseeing will follow for a couple of hours. 
We will then go shop for gifts 
to bring back to our children and friends.  

The next morning, at 7:45am we'll drive to to Belgium, Brussels - it should only take aroud 3 hours.
While in Brussels we want to explore the city to its fullest - no rock left unturned!

"""

email_template = """
From the following email, extract the following information:

leave_time: when are they leaving for vacation to Europe. If there's an actual
time written, use it, if not write unknown.

leave_from: where are they leaving from, the airport or city name and state if
available.

cities_to_visit: extract the cities they are going to visit. If there are more than 
one, put them in square brackets like '["cityone", "citytwo"].

Format the output as JSON with the following keys:
leave_time
leave_from
cities_to_visit

email: {email}
"""

# Using pydantic, we will create a class that allows us to specify the field that we want
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, field_validator #, validator => depricated
from typing import List

# Defining desired data structure
class VacationInfo(BaseModel):  # This will be our data class
    leave_time: str = Field(description="When they are leaving. It's usually")  # string type with the descirption of the field
    leave_from: str = Field(description="Where are they leaving from.\
                                          it's a city, airport or state, or province")
    cities_to_visit: List = Field(description="The cities, towns they will be visiting on \
                                        their trip. This needs to be in a list")
    num_people: int = Field(description="this is an integer for a number of people on this trip")

    # We can also add a validator to build a more robust application to validate certain fields and throw errors if field type is not satisfied
    @field_validator('num_people')
    def check_sum_people(cls, field):
        if field <=0:
            raise ValueError("Badly formatted number")
        return field

# Setup a parser and inject the instructions
pydantic_parser = PydanticOutputParser(pydantic_object=VacationInfo)
format_instructions = pydantic_parser.get_format_instructions()

# reviewed email template - we updated to add the {format_instructions}
email_template_revised = """
From the following email, extract the following information regarding 
this trip.

email: {email}

{format_instructions}
"""

updated_prompt = ChatPromptTemplate.from_template(template=email_template_revised)
messages = updated_prompt.format_messages(email=email_response,
                                          format_instructions=format_instructions)

format_response = chat.invoke(messages)

print(format_response)
print(type(format_response))  # We get type langchain_core.messages.ai.AIMessage
print(type(format_response.content))  # We get type string (str)

# Parsing the response to get the python dictionary (JSON)
vacation = pydantic_parser.parse(format_response)
