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

def get_verification_result(client,user_query, trip):
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

def verify_selected_trip(client, conversation_id):
  user_query = get_user_query(conversation_id)
  trip = get_selected_trip(conversation_id)
  return get_verification_result(client, user_query, trip)

def verify_refined_trip(client, conversation_id):
  user_query = get_user_query(conversation_id)
  trip = get_refined_trip(conversation_id)
  return get_verification_result(client, user_query, trip)

def main():
  conversation_id = "ginny-test"
  result = verify_selected_trip(client, conversation_id)
  print(f"OUTPUT: \n{result}")

if __name__ == "__main__":
  main()
