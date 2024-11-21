import json
import os
import pandas as pd
from utils import test_data

KEY_USER_QUERY = "user_query"
KEY_REFINED_TRIP = "refined_trip"
KEY_SELECTED_TRIP = "selected_trip"

file_path = "TripPlanState.json"

test_conversation_id = "ginny-test"

# Function to save data to a JSON file
def save_data(json_file_path, conversation_id, key, value):
    # Load existing data or initialize as an empty dictionary
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        data = {}

    # If conversation_id already exists, update it; otherwise, create a new entry
    if conversation_id in data:
        data[conversation_id][key] = value
    else:
        data[conversation_id] = {key: value}

    # Save the updated data back to the JSON file
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    print(f"{key} saved successfully to {json_file_path}")

# Function to query data and convert to a DataFrame
def query_data(json_file_path):
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        # Convert the JSON data into a DataFrame
        df = pd.DataFrame.from_dict(data, orient='index')
        return df
    else:
        print(f"No data found at {json_file_path}")
        return pd.DataFrame()
    
def save_user_query(conversation_id, user_query):
    save_data(file_path, conversation_id=conversation_id, key = KEY_USER_QUERY, value = user_query)

def save_selected_trip(conversation_id, selected_trip):
    save_data(file_path, conversation_id=conversation_id, key = KEY_SELECTED_TRIP, value = selected_trip)

def save_refined_trip(conversation_id, refined_trip):
    save_data(file_path, conversation_id=conversation_id, key = KEY_REFINED_TRIP, value = refined_trip)

def save_verification_result(conversation_id, result, key):
    save_data(file_path, conversation_id=conversation_id, key = key, value = result)

def get_user_query(conversation_id):
    return query_data(file_path).loc[conversation_id, KEY_USER_QUERY]

def get_selected_trip(conversation_id):
    return query_data(file_path).loc[conversation_id, KEY_SELECTED_TRIP]

def get_refined_trip(conversation_id):
    return query_data(file_path).loc[conversation_id, KEY_REFINED_TRIP]

# save_user_query(conversation_id=test_conversation_id, user_query=test_data.USER_QUERY)
# save_selected_trip(conversation_id=test_conversation_id, selected_trip=test_data.TRIP)
# print(get_user_query(conversation_id=test_conversation_id))