from google.adk.agents import Agent

from .shared import transfer_action, common_instruction

learning_resources_provider = Agent(
    name="learning_resources_provider",
    model="gemini-2.5-flash",
    instruction=f"""
    {common_instruction}
    Provide learning resources for the safety topic, which are related to the task. Display the following as a list of resources: 
    - Toolbox doc (A Gemini-generated 1-page summary on cable pulling fall hazards based on TSS)
    - Training video (A 5-minute manufacturer video on hybrid scissor lift)
    - Past incidents (A list of 5 relevant Iris incident reports from the last 5 years)
    {transfer_action}
    """
)
