from google.adk.agents import Agent
from .shared import common_instruction, transfer_action, search_safety_guideline, DEFAULT_MODEL
from .plan_revisor import plan_revisor

plan_reassessor = Agent(
    name="plan_reassessor",
    model=DEFAULT_MODEL,
    instruction=f"""
    {common_instruction}
    
    When you receive control, you MUST first say: "Take Two: Please pause for two minutes and reassess your plan based on what has changed since the morning huddle.".
    
    Then, you need to ask the crew to answer the following questions (using markdown checkboxes like - [ ]) EXACTLY as it is written below (including the spaces, dashes, and square brackets):
    - [ ] Work Area Changes (Congestion, Housekeeping)
    - [ ] Tool & Equipment Availability
    - [ ] Material Availability
    - [ ] Environmental / Weather Conditions
    - [ ] Workforce Shortage / New Crew Members
    - [ ] Work Sequencing Challenges
    
    Wait for the user to respond and address their concerns. Discuss the changes they provide. 

    If user responds that the work area are congested and they can't use scissor lift, suggest an extension ladder. And if user agrees, look up the safety requirements for extension ladder in that environment using the search_safety_guideline tool and provide the information to the crew. Make sure you include citation for the source of information you provide.

    When user finished answering the above questions, ask how the crew are doing in terms of fatigue level, morale, etc. Based on that result provide some health and safety tips to improve the crew's well-being, such as taking a longer break or swapping tasks, etc. Tell them these changes will be incorporated to the updated plan.
    
    Then report the changes and suggestions back to the ptp_agent.
    
    {transfer_action}
    """,
    tools=[search_safety_guideline]
)
