from openai import OpenAI
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
    
    system_prompt = """"""

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

