from google.adk.agents import Agent
from .shared import transfer_action, common_instruction, DEFAULT_MODEL

import json

def get_past_incidents(task: str) -> str:
    """
    Retrieve past incidents from Iris database for a given task.
    """
    incidents = [
        {
            "id": "IRIS-2025-0302",
            "date": "2025-03-02 2:39PM",
            "task": "Electrical Work / Scissor Lift Operation",
            "incident": "Electrician was working in the DC1 east zone when his scissor lift came in contact with a nearby ladder crushing the ladder on impact. No worker was using the ladder.",
            "type": "Near Miss",
            "key_focus": "Barricades requirements, Spotters & Banksperson requirements.",
            "suggested_resource": "OSHA Toolbox Talk on working around tight spaces with scissor lifts."
        },
        {
            "id": "IRIS-2024-0623",
            "date": "2024-06-23 3:45PM",
            "task": "Overhead Cable Pulling",
            "incident": "Worker was working on overhead cable pulling when he felt a sharp pain in his left shoulder.",
            "type": "Injury / Ergonomic Hazard",
            "key_focus": "Ergonomics",
            "suggested_resource": "OSHA Worksite Ergonomics Guide (https://www.oshaeducationcenter.com/worksite-ergonomics-guide/)"
        }
    ]
    return json.dumps(incidents, indent=2)

def get_scissor_lift_video_link() -> str:
    """
    Retrieve the scissor lift safety video link.
    """
    return "https://www.youtube.com/watch?v=coYQOu2Y1pI"

learning_resources_provider = Agent(
    name="learning_resources_provider",
    model=DEFAULT_MODEL,
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
