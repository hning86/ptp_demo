from google.adk.agents import Agent
from .shared import transfer_action, common_instruction

def get_past_incidents(task: str) -> str:
    """
    Retrieve past incidents from Iris database for a given task.
    """
    return """
    [Iris Incident Report #IRIS-2025-0302]
    Date: 2025-03-02 2:39PM
    Task: Electrical Work / Scissor Lift Operation
    Incident: Electrician was working in the DC1 east zone when his scissor lift came in contact with a nearby ladder crushing the ladder on impact. No worker was using the ladder.
    Type: Near Miss
    Key Focus: Barricades requirements, Spotters & Banksperson requirements.
    Suggested Resource: OSHA Toolbox Talk on working around tight spaces with scissor lifts.

    [Iris Incident Report #IRIS-2024-0623]
    Date: 2024-06-23 3:45PM
    Task: Overhead Cable Pulling
    Incident: Worker was working on overhead cable pulling when he felt a sharp pain in his left shoulder.
    Type: Injury / Ergonomic Hazard
    Suggested Resource: OSHA Worksite Ergonomics Guide (https://www.oshaeducationcenter.com/worksite-ergonomics-guide/)
    """

def get_scissor_lift_video_link() -> str:
    """
    Retrieve the scissor lift safety video link.
    """
    return "https://www.youtube.com/watch?v=coYQOu2Y1pI"

learning_resources_provider = Agent(
    name="learning_resources_provider",
    model="gemini-2.5-flash",
    instruction=f"""
    {common_instruction}
    Provide learning resources for the safety topic, which are related to the task. First, use the get_past_incidents tool to retrieve past incidents for the task. Also use get_scissor_lift_video_link to get the video link. Then display the following as a list of resources: 
    - [Toolbox doc](https://examples.com/doc_place_holder.docx)
    - Training video (Provide the link retrieved by get_scissor_lift_video_link)
    - List past incidents (from the get_past_incidents tool in simple one-line-bullet-points format. No more than one sentence per line with a link to the full report)

    Stops and ask user to take some time to review the above materials. Once the user is ready, continue with the next step by using transfer action.
        
    {transfer_action}
    """,
    tools=[get_past_incidents, get_scissor_lift_video_link]
)
