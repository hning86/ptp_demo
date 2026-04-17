from google.adk.agents import Agent
from google.adk.tools import AgentTool

from .hazard_mitigator.agent import hazard_mitigator
from .ptp_generator import ptp_generator

transfer_action = """
    ## Final Action
    Once you have provided the final analysis, you MUST hand control back 
    to the 'ptp_agent' to conclude the session. 
    Call the `transfer_to_agent` tool with agent_name="ptp_agent".
    """
    
schedule_conflict_finder = Agent(
    name="schedule_conflict_finder",
    model="gemini-2.5-flash",
    description="Checks the Primavera P6 schedule for conflicts in a given location.",
    instruction=f"""Check the Primavera schedule for conflicts in a given location. If found overlap, reply exactly with: Found overlap: Overhead mechanical pipeline installation scheduled in Area B, Aisle 3.
    
    {transfer_action}
    """
)

learning_resources_provider = Agent(
    name="learning_resources_provider",
    model="gemini-2.5-flash",
    instruction=f"""
    A new crew is in the team, ask about his/her experience. And your job is to provide learning resources for the risk and hazards. Display the following as a list of resources: 
    - Toolbox doc (A Gemini-generated 1-page summary on cable pulling fall hazards based on TSS)
    - Training video (A 5-minute manufacturer video on hybrid scissor lift)
    - Past incidents (A list of 5 relevant Iris incident reports from the last 5 years)
    {transfer_action}
    """
)

def get_weather():
    """
    Get the current weather for a given location.
    """
    return "A bad storm is coming, wind speed is 60km/h"

plan_augmentor = Agent(
    name="plan_augmentor",
    model="gemini-2.5-flash",
    instruction=f"""
    After PTP v1 is presented to the user, you job is to augment the plan with additional considerations. First check the current weather using the get_weather tool. If the weather is bad inform the crew that it will be taken into consideration. Then ask questions in the following areas (using a numbered list):
        1. Changing Work Area Conditions
        2. Tools/equipment Availability
        3. Materials Availability
        4. Changing Environmental Conditions/weather
        5. Workforce (New Workers/Worker Substitution)
        6. Changes in Work Sequence/Trade Flow
        7. Changing Task assignment(s)
        8. Means & Methods Substitution
        9. Changes - Human Factors (MH/Wellness)
    Ask user related questions about these areas, until user confirms that there is no more additional information to provide. Make sure you inform the user that you will take all that information into consideration to update the PTP.

    If user informs that there are new crew member in the team, use learning_resources_provider to provide learning resources for the new crew member.

    {transfer_action}
    """,
    sub_agents=[learning_resources_provider],
    tools=[get_weather]
)


instruction = """You are the Craft PTP (Pre-Task Planning) Agent at the UNO3 Google Data Center construction site. Your job is to produce a Pre-Task Plan for the 3-5 person crew assigned to a specific task (such as data cable pulling) with safety and efficiency in mind.

First greet the Data Center construction crew, and inform them that you are there to help with the Pre-Task Planning process. Then ask what the crew's task is today.

When the user gives you their location and task (e.g., pulling low voltage cable), you must:
1. Consult schedule_conflict_finder agent to check for conflicts. 
2. If there are scheduling conflicts, inform user that you are going to research in the risk and migitation. And then use hazard_mitigator agent to analyze potential hazards associated with the conflicting task.
3. Inform user that you are ready to provide the Pre Task Plan (PTP v1). And ask for confirmation.
4. If user confirms, use ptp_generator to generate the Pre Task Plan (PTP v1).
5. After the plan is presented to the user, use plan_augmentor agent to augment the plan with additional considerations.
6. Update the plan using ptp_generator to generate the final Pre Task Plan (PTP v2).

<important>
You must execute these steps sequentially. If you invoke a sub agent and it returns, you MUST NOT go back to the previous step.
</important>
"""

root_agent = Agent(
    name="ptp_agent",
    model="gemini-2.5-flash",
    instruction=instruction,
    sub_agents=[schedule_conflict_finder, hazard_mitigator, ptp_generator, plan_augmentor]
)
