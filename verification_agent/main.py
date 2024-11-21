import openai
from openai import OpenAI
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print(sys.path)

from utils.utils import *
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

sys_prompt = """
Given the user requirement and a trip, tell me the percentage of user requirements are satisfied by the trip. Also tell me if the trip is realistic or not based on the ticket price, hotel price, agenda, etc, and give me a reason why you think so. Structure your answer like this:

User Satisfaction Rate: [% of requirements satisfied by the trip]
[REASON]

Trip Realism Score: [% of how realistic this trip is]
[REASON]

Your inputs will be USER QUERY and TRIP.

USER QUERY:
[USER QUERY]

TRIP:
[TRIP]
"""

input_text = """
USER QUERY:
[USER QUERY]

TRIP:
[TRIP]
"""

def get_verification_result(user_query, trip):
  user_input = input_text.replace("[USER QUERY]", user_query)
  user_input = user_input.replace("[TRIP]", trip)
  completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": user_input}
    ],
    #temperature=0.7,
    max_tokens=500
  )
  return(completion.choices[0].message.content)

conversation_id = "ginny-test"
user_query = get_user_query(conversation_id)
trip = get_selected_trip(conversation_id)
output_text = get_verification_result(user_query, trip)
print(f"INPUT user_query:\n {user_query}\ntrip: {trip}\n")
print(f"OUTPUT: \n{output_text}")
