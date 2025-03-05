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

cities_to_visit: extract the cities they are going to visit. 
If there are more than one, put them in square brackets like '["cityone", "citytwo"].

Format the output as JSON with the following keys:
leave_time
leave_from
cities_to_visit

email: {email}
"""

# desired_format = {
#     "leave_time": "8:45 pm",
#     "leave_from": "Denver, Colorado",
#     "cities_to_visit": ["Amsterdam", "Brussels"]
# }

prompt_template = ChatPromptTemplate.from_template(email_template)

# print(prompt_template)

messages = prompt_template.format_messages(email=email_response)

# response = chat.invoke(messages)
# print(response.content)  # Reminder : The output here is a string, not a JSON. This is another reason to use LangChain's Parser instead


## The problem with what we did above is that the model is moody ==> sometimes it works and sometimes not. LangChain has a solution for this. 
# We can use LangChain's Parser instead and it guarantees (99% of the time) that we will get the desired format ##

# ----------------- LangChain Parsers ----------------- #
from langchain.output_parsers import ResponseSchema  # allows us to create the instructions of what fields we want to extract along with their formats
from langchain.output_parsers import StructuredOutputParser  # actual output parsers

leave_time_schema = ResponseSchema(name="leave_time",
                                   description="When they are leaving. \
                                        It's usually numerical time of the day. \
                                        If not available write N/A")  # It's important to use a good description because this is what the langchain agent will use when creating the response schema.

leave_from_schema = ResponseSchema(name="leave_from",
                                   description="Where are they leaving from.\
                                        it's a city, airport or state, or province")

cities_to_visit_schema = ResponseSchema(name="cities_to_visit",
                                        description="The cities, towns they will be visiting on \
                                            their trip. This needs to be in a list")

# Storing the response schema for each field in a list which will later be fed to the langchain instructions output parser
response_schema = [
    leave_time_schema,
    leave_from_schema,
    cities_to_visit_schema
]

# Setup the output parser
output_parser = StructuredOutputParser.from_response_schemas(response_schema)
format_instructions = output_parser.get_format_instructions()

print(format_instructions)

# reviewed email template - we updated to add the {format_instructions}
email_template_revised = """
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
{format_instructions}
"""

updated_prompt = ChatPromptTemplate.from_template(template=email_template_revised)
messages = prompt_template.format_messages(email=email_response,
                                           format_instructions=format_instructions)

response = chat.invoke(messages)

print(type(response.content))  # Still a string but we are not done yet. We can now use the langchain parser to parse the response

output_dict = output_parser.parse(response.content)  # parse into dict (JSON)
print(output_dict)
print(type(output_dict))
print(f"Cities: {output_dict['cities_to_visit'][0]}")  # Extracting the first city in cities_to_visit key


