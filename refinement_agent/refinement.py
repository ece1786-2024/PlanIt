from openai import OpenAI
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.utils import *
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

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
    
    Make sure the refined plan is both practical and realistic, taking into account any real-world limitations or constraints. Make sure the refined plan is both practical and realistic, taking into account any real-world limitations or constraints. The refined plan should have the same format as the "Initial Trip Plan”, and only output the plan without any extra words.

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

# conversation_id = "test001"
# user_query = get_user_query(conversation_id)
# initial_trip_plan = get_selected_trip(conversation_id)

# refined_trip_plan = refinement_agent(user_query, initial_trip_plan)
# # print("Refined Trip Plan:\n", refined_trip_plan)
# save_refined_trip(conversation_id, refined_trip_plan)