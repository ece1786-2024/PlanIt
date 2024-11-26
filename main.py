from flask import Flask, request, jsonify, render_template
from utils.utils import *
from refinement_agent.refinement import refinement_agent
from verification_agent.main import get_verification_result
from selection_agent.selection_agent_v3 import find_best_plan
import re
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

app = Flask(__name__)

def extract_scores(output_text):
    satisfaction_match = re.search(r"User Satisfaction Rate: (\d+)", output_text)
    realism_match = re.search(r"Trip Realism Score: (\d+)", output_text)

    satisfaction_rate = int(satisfaction_match.group(1)) if satisfaction_match else None
    realism_score = int(realism_match.group(1)) if realism_match else None

    return satisfaction_rate, realism_score

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_query', methods=['POST'])
def process_query():
    data = request.json
    user_query = data.get('user_query')

    conversation_id = "test001"

    # step 1: get & save user query
    save_user_query(conversation_id, user_query)

    # step 2: select best-matched trip plan
    selected_trip_plan = find_best_plan(user_query)
    save_selected_trip(conversation_id, selected_trip_plan)

    # step 3: refined selected_trip_plan
    refined_trip_plan = refinement_agent(user_query, selected_trip_plan)
    save_refined_trip(conversation_id, refined_trip_plan)

    # step 4: verify selected_trip_plan
    selected_result = get_verification_result(client, user_query, selected_trip_plan)
    selected_user_satisfaction_rate, selected_trip_realism_score = extract_scores(selected_result)
    if selected_user_satisfaction_rate is None or selected_trip_realism_score is None:
        print("Error extracting scores from selected_result")
    save_verification_result(conversation_id, selected_result, "selected_verification")

    # step 5: verify refined_trip_plan
    refined_result = get_verification_result(client, user_query, refined_trip_plan)
    refined_user_satisfaction_rate, refined_trip_realism_score = extract_scores(refined_result)
    if refined_user_satisfaction_rate is None or refined_trip_realism_score is None:
        print("Error extracting scores from refined_result")
    save_verification_result(conversation_id, refined_result, "refined_verification")

    # verify baseline model
    

    # step 6: compare and output (weight 8:2)
    refined_score = (refined_user_satisfaction_rate * 0.8) + (refined_trip_realism_score * 0.2)
    selected_score = (selected_user_satisfaction_rate * 0.8) + (selected_trip_realism_score * 0.2)
    if refined_score > selected_score:
        final_result = refined_trip_plan
    else:
        final_result = selected_trip_plan
    print("refined score: ", refined_score)
    print("selected score: ", selected_score)

    return jsonify({'result': final_result})

if __name__ == '__main__':
    app.run(debug=True)
