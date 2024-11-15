import openai
from openai import OpenAI

api_key = ""
sys_prompt = """
Given the user requirement and a trip, tell me the percentage of user requirements are satisfied by the trip. Also tell me if the trip is realistic or not based on the ticket price, hotel price, agenda, etc, and give me a reason why you think so. Structure your answer like this:

User satisfication rate: [% of requirements satisfied by the trip]
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

user_query = """
Give me a 5 day chill trip plan to Sydney, my budget is $3000 CAD.
"""

trip = """
**Destination:** Sydney, Australia

**Duration:** 5 days, 4 nights

**Points of Interest:** 13

**Budget**: CA$3263

### Day 01: Arrival in Sydney

- **Flight:** From home city to Sydney.
- **Breakfast:** Not included (recommendation for local meals).
- **Transportation:** Airport transfer (1 hour).
- **Dinner:** Not included (recommendation for local meals).
- **Hotel:** Stanford Plaza Sydney Airport or Pullman Sydney Airport.

### Day 02: Sydney Sightseeing

- **Breakfast:** Hotel breakfast (30 CNY per person).
- **Transportation:** Private transfer.
- **Activities:** Visit Sydney University, Sydney Harbour Bridge, Sydney Opera House, Royal Botanic Gardens, and Queen Victoria Building. (Total 5 POIs)
- **Dinner:** Not included (recommendation for local meals).
- **Hotel:** Same as Day 01.

### Day 03: Markets, Parks, and Beaches

- **Breakfast:** Hotel breakfast.
- **Transportation:** Private transfer.
- **Activities:** Visit Sydney Fish Market, Hyde Park, Taronga Zoo, and Bondi Beach. (Total 4 POIs)
- **Dinner:** Not included (recommendation for local meals).
- **Hotel:** Same as Day 01.

### Day 04: Blue Mountains National Park

- **Breakfast:** Hotel breakfast.
- **Transportation:** Private transfer.
- **Activities:** Explore Blue Mountains National Park, Three Sisters, and Leura Main Street. (Total 3 POIs)
- **Dinner:** Not included (recommendation for local meals).
- **Hotel:** Same as Day 01.

### Day 05: Departure

- **Breakfast:** Hotel breakfast.
- **Transportation:** Transfer to the airport for flight back to home city.
- **Lunch & Dinner:** Not included.
- **Flight:** Based on flight time.
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

# assume api_key already defined
client = OpenAI(api_key=api_key)
output_text = get_verification_result(user_query, trip)
print(f"INPUT user_query:\n {user_query}\ntrip: {trip}\n")
print(f"OUTPUT: \n{output_text}")
