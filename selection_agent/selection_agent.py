import pandas as pd
from openai import OpenAI
import ast
import os
from dotenv import load_dotenv

# Initialize the OpenAI client
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Load the travel plans
travel_plans = pd.read_csv('travel_plans.csv')

# Helper function to clean and convert data
def preprocess_travel_plans(travel_data):
    travel_data['budgets'] = travel_data['budgets'].apply(pd.to_numeric, errors='coerce')
    travel_data['durations'] = travel_data['durations'].apply(pd.to_numeric, errors='coerce')
    travel_data['points of interest'] = travel_data['points of interest'].apply(pd.to_numeric, errors='coerce')
    return travel_data

travel_plans = preprocess_travel_plans(travel_plans)

# Function to extract criteria and query the CSV
def find_best_plan(user_input, travel_data):
    # Create the prompt to extract criteria
    prompt = (
        f"You are a travel assistant. Extract the user's travel preferences from this input: '{user_input}'. "
        f"Return the result as a Python dictionary with keys: 'country', 'destination', 'max_budget', "
        f"'max_duration_days', and 'min_points_of_interest'. Use None for missing information. Output the dictionary in one line instead of multi-line."
    )
    
    # Use OpenAI to interpret the user input
    try:
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Parse the response content
        response_content = completion.choices[0].message.content.strip()
        print(f"Raw Response: {response_content}")  # Debugging
        
        # Extract the dictionary part from the response
        if "{" in response_content and "}" in response_content:
            start_index = response_content.index("{")
            end_index = response_content.rindex("}") + 1
            dictionary_str = response_content[start_index:end_index]
            user_criteria = ast.literal_eval(dictionary_str)
        else:
            raise ValueError("No valid dictionary found in the response.")
        
    except (SyntaxError, ValueError) as e:
        print(f"Error extracting criteria: {e}")
        return "Unable to understand user input. Please try again."

    # Apply filtering based on extracted criteria
    filtered_data = travel_data.copy()
    
    if user_criteria.get('country'):
        filtered_data = filtered_data[filtered_data['country'].str.contains(user_criteria['country'], case=False, na=False)]
    if user_criteria.get('destination'):
        filtered_data = filtered_data[filtered_data['destination'].str.contains(user_criteria['destination'], case=False, na=False)]
    if user_criteria.get('max_budget'):
        filtered_data = filtered_data[filtered_data['budgets'] <= user_criteria['max_budget']]
    if user_criteria.get('max_duration_days'):
        filtered_data = filtered_data[filtered_data['durations'] <= user_criteria['max_duration_days']]
    if user_criteria.get('min_points_of_interest'):
        filtered_data = filtered_data[filtered_data['points of interest'] >= user_criteria['min_points_of_interest']]

    # Find the best-matched travel plan (closest to user requirements)
    filtered_data = filtered_data.sort_values(
        by=['points of interest', 'budgets', 'durations'], 
        ascending=[False, True, True]
    )

    # Return the best match
    if not filtered_data.empty:
        return filtered_data.iloc[0].to_dict()
    else:
        return "No matching travel plans found."

# Example usage
user_input = "I want to visit a place in Mexico for about 5 days, around $1900 budget, with at least 6 points of interest."
best_plan = find_best_plan(user_input, travel_plans)
print("Selected Travel Plan:")
print(best_plan)
