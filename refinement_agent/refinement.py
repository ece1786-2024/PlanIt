from openai import OpenAI
from utils.utils import *

client = OpenAI(api_key ='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')

def refinement_agent(user_query, initial_trip_plan):
    """
    Refines the initial trip plan based on the user's preferences.
    
    Parameters:
    - user_query (str): User's preferences for the trip.
    - initial_trip_plan (str): The initial trip plan selected from a real-world source.
    
    Returns:
    - str: Refined trip plan as a string.
    """
    
    system_prompt = """
    You are the Refinement Agent in a multi-agent trip planning system. Your primary goal is to adjust and enhance a trip plan provided to you to align it precisely with the user’s specific requirements. These requirements include budget, duration, density of points of interest, and destination preferences.

    Your goals and guidelines:

    1. Interpret User Requirements: Review the user's requirements, paying special attention to:
        - Budget: Ensure the trip plan fits within the specified budget, making adjustments to hotel, transport, and activity costs as necessary.
        - Duration: Adjust the trip plan to match the specified travel duration, adding or removing activities as needed.
        - Density of Points of Interest: Modify the schedule based on the desired pace—either adding more points of interest for a high-density plan or allowing more downtime for a relaxed itinerary.
        - Destination Preferences: Ensure the trip aligns with any specific destinations or regions the user wishes to visit.
    2. Adapt with Subtle Adjustments: Begin with the plan provided by the Selection Agent and make careful modifications rather than overhauling the structure entirely.
    3. Handle Conflicting Requirements Thoughtfully: If you identify any conflicting requirements (e.g., low budget with high-density activities), prioritize the user’s explicit preferences.
    4. Communicate Adjustments Clearly: Document each modification you make to the trip plan, explaining how it better satisfies the user’s needs. If constraints limit your adjustments, provide a concise explanation.
    5. Success for You Means: Delivering a trip plan that meets 100% of the user’s stated requirements. Your answer should include the trip plan analysis.
    """

    user_prompt = f"""
    User Query: {user_query}
    Initial Trip Plan: {initial_trip_plan}
    
    “Initial Trip Plan” is selected from a real-world source, may not perfectly align with user’s needs.
    “User Query” contains user’s preferences about their expired trip plan.
    
    Based on the "Initial Trip Plan" and the user’s preferences described in the "User Query", refine this plan to better suit the user’s needs. Focus on:
    - Adjusting the budget to fit the user’s spending limit
    - Modifying or adding activities to match their interests
    - Aligning the trip style with their expectations
    
    Make sure the refined plan is both practical and realistic, taking into account any real-world limitations or constraints. Make sure the refined plan is both practical and realistic, taking into account any real-world limitations or constraints. The refined plan should have the same format as the "Initial Trip Plan”, and output follow this format:

    Refined Plan:

    Modifications:

    1.

    2.

    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    refined_plan = response.choices[0].message.content
    return refined_plan

# initial_trip_plan = """
# 3-Day Budget-Friendly Iceland Adventure

# Day 1: Arrival and Reykjavík Exploration

# Morning/Afternoon: Arrive at Keflavík International Airport and transfer to budget accommodation in Reykjavík (hostel or guesthouse recommended for cost savings).
# Evening: Explore downtown Reykjavík. Key spots include Hallgrímskirkja Church and the Sun Voyager sculpture. Enjoy an affordable meal at a local café or try the popular Bæjarins Beztu Pylsur hot dog stand.

# Day 2: Golden Circle Highlights

# Morning: Join a budget-friendly bus tour of the Golden Circle. Key stops include:
# - Þingvellir National Park: Walk between tectonic plates (North American and Eurasian).
# - Geysir Geothermal Area: Watch Strokkur geyser erupt every few minutes.
# - Gullfoss Waterfall: One of Iceland's most iconic waterfalls.
# Afternoon: Return to Reykjavík and explore local museums or relax at a geothermal pool, like Laugardalslaug.
# Evening: Join a budget Northern Lights bus tour (if conditions allow).

# Day 3: South Coast Adventure

# Morning: Take a day tour of Iceland's south coast. Stops include:
# - Seljalandsfoss Waterfall: Unique waterfall where you can walk behind the cascade.
# - Skógafoss Waterfall: 60-meter tall, one of Iceland’s most majestic.
# - Reynisfjara Black Sand Beach: Known for its black sands and basalt formations.
# Afternoon: Continue exploring with an optional glacier hike at Sólheimajökull (additional cost).
# Evening: Return to Reykjavík and enjoy one last night with local dining or live music.

# Additional Tips:
# - Accommodation: Opt for budget-friendly hostels, guesthouses, or Airbnb.
# - Meals: Use Reykjavík’s affordable eateries, bakeries, or supermarkets. Prepare some meals if possible.
# - Transportation: Walk or use public transportation; most city attractions are easily accessible.
# - Tours: Book in advance for best prices, seek package deals.

# Trip Plan Analysis:
# - Budget: CA$750 (estimated based on budget accommodation, meals, and tours)
# - Destination: Reykjavík, Iceland
# - Density of Points of Interest: 6 major highlights (Golden Circle sites, Reykjavík attractions, South Coast stops)
# - Duration: 3 days
# """

# user_query = "I would like to go to Iceland for a short road trip. I really like a short duration trips that should be above 3 days. I don’t have too much budget. It should be below $500 USD. In terms of the itineraries, arrange it as much as possible. Hopefully the trip can be intense, low-cost, and a enjoyable short trip."

conversation_id = "refinement-initial-trip-plan-example"
user_query = get_user_query(conversation_id)
initial_trip_plan = get_selected_trip(conversation_id)

refined_trip_plan = refinement_agent(user_query, initial_trip_plan)
print("Refined Trip Plan:\n", refined_trip_plan)