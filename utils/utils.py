import json
import os
import pandas as pd

from test_data import *

file_path = "TripPlanState.json"

def save_data(json_file_path, user_query, trip):
  if os.path.exists(json_file_path):
      with open(json_file_path, 'r', encoding='utf-8') as file:
          data = json.load(file)
  else:
      data = []
  data.append({"user_query": user_query, "trip": trip})
  with open(json_file_path, 'w', encoding='utf-8') as file:
      json.dump(data, file, indent=4)
  print(f"Data saved successfully to {json_file_path}")

def query_data(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return pd.DataFrame(data)

# save_data(file_path, user_query = USER_QUERY, trip = TRIP)
df = query_data(file_path)
print(df['user_query'].iloc[-1])