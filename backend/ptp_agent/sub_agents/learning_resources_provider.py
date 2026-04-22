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
        },
        {
            "id": "IRIS-2025-1114",
            "date": "2025-11-14 10:15AM",
            "task": "Hot Work / Welding",
            "incident": "Welder dropped a hot slag spark onto an empty cardboard box causing a small localized fire. Extinguished immediately by fire watch.",
            "type": "Fire Hazard / Near Miss",
            "key_focus": "Fire watch protocol, clearing combustibles from hot work zones.",
            "suggested_resource": "NFPA 51B Standard for Fire Prevention During Welding."
        },
        {
            "id": "IRIS-2025-0822",
            "date": "2025-08-22 1:30PM",
            "task": "Working at Heights",
            "incident": "Ironworker disconnected their safety lanyard temporarily to reach an out-of-bounds tool. Spotted by safety supervisor and corrected.",
            "type": "Safety Violation / Near Miss",
            "key_focus": "100% Tie-off enforcement, harness compliance.",
            "suggested_resource": "OSHA Fall Protection Guidelines."
        },
        {
            "id": "IRIS-2025-0505",
            "date": "2025-05-05 9:00AM",
            "task": "Material Handling",
            "incident": "Reach forklift operator misjudged distance while turning in the staging area, striking a pallet racking unit causing structural bending.",
            "type": "Property Damage",
            "key_focus": "Operator awareness, load management, strict speed limits.",
            "suggested_resource": "OSHA Powered Industrial Trucks Standard."
        },
        {
            "id": "IRIS-2024-1201",
            "date": "2024-12-01 11:00AM",
            "task": "Excavation / Trenching",
            "incident": "Minor trench wall collapse on the perimeter of a 4ft deep utility line trench. No workers were actively deployed inside the zone.",
            "type": "Near Miss",
            "key_focus": "Protective systems, trench shoring evaluation.",
            "suggested_resource": "OSHA Trenching and Excavation Safety."
        },
        {
            "id": "IRIS-2024-0915",
            "date": "2024-09-15 4:00PM",
            "task": "Personal Protective Equipment",
            "incident": "Crew members identified removing mandatory safety eyewear due to fogging in humid staging environments.",
            "type": "Safety Violation",
            "key_focus": "Anti-fog lens alternatives, consistent PPE checks.",
            "suggested_resource": "OSHA Eye and Face Protection."
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
