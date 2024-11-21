import sys
from utils.utils import *
from refinement_agent.refinement import refinement_agent
from verification_agent.main import get_verification_result
import re
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def extract_scores(output_text):
    satisfaction_match = re.search(r"User Satisfaction Rate: (\d+)", output_text)
    realism_match = re.search(r"Trip Realism Score: (\d+)", output_text)

    satisfaction_rate = int(satisfaction_match.group(1)) if satisfaction_match else None
    realism_score = int(realism_match.group(1)) if realism_match else None

    return satisfaction_rate, realism_score

conversation_id = "test001" 

# step 1: get & save user query
user_query = input("Please enter your trip requirements: ")
save_user_query(conversation_id, user_query)

# step 2: select best-matched trip plan


# step 3: refined selected_trip_plan
selected_trip_plan = get_selected_trip(conversation_id)
refined_trip_plan = refinement_agent(user_query, selected_trip_plan)
save_refined_trip(conversation_id, refined_trip_plan)

# step 4: verify selected_trip_plan
selected_result = get_verification_result(client, user_query, selected_trip_plan)
selected_user_satisfaction_rate, selected_trip_realism_score = extract_scores(selected_result)
save_verification_result(conversation_id, selected_result, "selected_verification")

# step 5: verify refined_trip_plan
refined_result = get_verification_result(client, user_query, refined_trip_plan)
refined_user_satisfaction_rate, refined_trip_realism_score = extract_scores(refined_result)
save_verification_result(conversation_id, refined_result, "refined_verification")

# step 6: compare and output
if refined_user_satisfaction_rate > selected_user_satisfaction_rate:
    print(refined_result)
elif refined_user_satisfaction_rate < selected_user_satisfaction_rate:
    print(selected_result)
else:
    if refined_trip_realism_score > selected_trip_realism_score:
        print(refined_result)
    elif refined_trip_realism_score < selected_trip_realism_score:
        print(selected_result)
    else:
        print("Both plans are equally satisfactory and realistic.")

