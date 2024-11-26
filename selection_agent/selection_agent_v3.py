import pandas as pd
import faiss
import numpy as np
import ast
from openai import OpenAI

client = OpenAI()

travel_plans = pd.read_csv('travel_plans.csv')

# Clean and preprocess data
def preprocess_travel_plans(data):
    data['budgets'] = data['budgets'].apply(pd.to_numeric, errors='coerce')
    data['durations'] = data['durations'].apply(pd.to_numeric, errors='coerce')
    return data

# Preprocess the travel data
travel_plans = preprocess_travel_plans(travel_plans)

# Extract user preferences from query using GPT
def extract_user_preferences(user_input):
    prompt = (
        f"You are a travel assistant. Extract the user's preferences from the following query: '{user_input}'. "
        f"Return a Python dictionary with keys: 'country', 'destination', 'budget', 'duration', and 'points_of_interest'. "
        f"country should be which country the user wants to go, destination should be what area/city/attraction the user wants to go, budget should be how much money the user wants to spend, durations should be how long the user want to travel, points of interest should be how many tourist attraction the user want to go."
        f"Output must have the same format like this and wrapped in braces without anything else: 'country': 'Mexico', 'destination': None, 'budget': 2500, 'duration': 8, 'points_of_interest': 'natural sites'"
        f"Use None for missing information and ensure the output is in one line."
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    # Parse the response into a Python dictionary
    response_content = response.choices[0].message.content.strip()
    print(response_content)
    user_preferences = ast.literal_eval(response_content)
    return user_preferences

# Generate embeddings for text
def generate_embeddings(texts, model="text-embedding-ada-002"):
    embeddings = []
    for text in texts:
        response = client.embeddings.create(input=text, model=model)
        embeddings.append(response.data[0].embedding)
    return np.array(embeddings, dtype='float32')

# Build vector database
def build_faiss_index(embeddings):
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)  # Normalize
    index = faiss.IndexFlatIP(embeddings.shape[1])  # Inner product for cosine similarity
    index.add(embeddings)
    return index

# Generate embeddings for the travel plans
if 'details' in travel_plans.columns:
    travel_plans['search_text'] = travel_plans.apply(
        lambda row: f"{row['country']} {row['destination']} {row['durations']} days {row['budgets']} budget {row['details']}",
        axis=1
    )
    plan_embeddings = generate_embeddings(travel_plans['search_text'].tolist())
    faiss_index = build_faiss_index(plan_embeddings)

# Query the vector database and retrieve top 5 matches
def retrieve_top_matches(user_query, top_k=5):
    query_embedding = generate_embeddings([user_query])[0]
    query_embedding = query_embedding / np.linalg.norm(query_embedding)  # Normalize
    distances, indices = faiss_index.search(query_embedding.reshape(1, -1), top_k)
    return travel_plans.iloc[indices[0]].copy()

# Use GPT to pick the best match
def select(user_query, top_matches):
    context = top_matches[['country', 'destination', 'durations', 'budgets', 'details']].to_dict(orient='records')
    # print("context: ", context)
    prompt = (
        f"The user asked: '{user_query}'.\n\n"
        f"Here are the top 5 travel plans:\n"
        f"{context}\n\n"
        f"Based on the user preferences and numerical details, first consider about destination, then duration and budget, "
        f"select the best travel plan among them, if no one match return 'None of them match'"
        f"Output the best travel plan as this format (using exactly same words from the input):\n"
        f"Summary:\n"
        f"- duration: ... days\n"
        f"- destination: \n"
        f"- budget: $...\n\n"
        f"Details:\n"
        f"Day 1: ...\n"
        f"Day 2: ...\n"
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a travel assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

# Main function to find the best travel plan
def find_best_plan(user_query):
    #Extract user preferences
    user_preferences = extract_user_preferences(user_query)
    
    #Create a query string for retrieval
    query_string = f"{user_preferences.get('country', '')} {user_preferences.get('destination', '')} " \
                   f"{user_preferences.get('duration', 'days')} days {user_preferences.get('budget', 'budget')} budget"
    
    #Retrieve top matches
    top_matches = retrieve_top_matches(query_string)
    
    #Refine results and select the best plan
    best_plan = select(user_query, top_matches)
    return best_plan

# user_input = "I want a 4-day trip to China, I plan to visit Hong Kong and Macao. My budget is 1100"
# best_plan = find_best_plan(user_input)
# print(best_plan)