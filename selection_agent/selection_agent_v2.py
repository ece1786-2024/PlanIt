import openai
import pandas as pd
from openai import OpenAI
import faiss
import numpy as np
import re

client = OpenAI()
#travel_data = pd.read_csv('travel_plans_v2.csv')
travel_data = pd.read_csv('travel_plans.csv')

def extract_duration_budget(query):
    duration = int(re.search(r'(\d+)-day', query).group(1))  
    budget = int(re.search(r'budget of around (\d+)', query).group(1))  
    return duration, budget

def generate_embeddings(texts, model="text-embedding-ada-002"):
    embeddings = []
    for text in texts:
        response = client.embeddings.create(input=text, model=model)
        embeddings.append(response.data[0].embedding)
    return embeddings

def query_embedding(query, model="text-embedding-ada-002"):
    response = client.embeddings.create(input=query, model=model)
    return np.array(response.data[0].embedding, dtype='float32')

details = travel_data['details'].tolist()
embeddings = generate_embeddings(details)

dimension = len(embeddings[0])  
index = faiss.IndexFlatIP(dimension)  

embeddings = np.array(embeddings)
embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)  
index.add(embeddings.astype('float32'))

faiss.write_index(index, "travel_plans_index.faiss")
travel_data.to_csv("travel_plans_metadata.csv", index=False)
index = faiss.read_index("travel_plans_index.faiss")
metadata = pd.read_csv("travel_plans_metadata.csv")

travel_data['durations'] = travel_data['durations'].astype(float)
travel_data['budgets'] = travel_data['budgets'].astype(float)

user_query = "I want a 5-day trip to Mexico with a budget of around 1500."

query_duration, query_budget = extract_duration_budget(user_query)

query_emb = query_embedding(user_query)
query_emb = query_emb / np.linalg.norm(query_emb)  

distances, indices = index.search(query_emb.reshape(1, -1).astype('float32'), k=5)

results = travel_data.iloc[indices[0]].copy()
results['similarity_score'] = 1 / (1 + distances[0])  

results['duration_diff'] = abs(results['durations'] - query_duration)
results['budget_diff'] = abs(results['budgets'] - query_budget)

results['duration_diff_normalized'] = results['duration_diff'] / results['duration_diff'].max()
results['budget_diff_normalized'] = results['budget_diff'] / results['budget_diff'].max()

results['overall_score'] = (results['similarity_score'] / (results['duration_diff_normalized'] + 1) + results['similarity_score'] / (results['budget_diff_normalized'] + 1))

best_match = results.sort_values(by='overall_score', ascending=False).iloc[0]
best_match = best_match[['country', 'destination','durations', 'budgets', 'details']]
print(best_match)