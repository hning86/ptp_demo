import os
from google import genai
from google.genai import types
from google.adk.agents import Agent

pdf_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "docs", "Energy Wheel.pdf")
pdf_bytes = None

if os.path.exists(pdf_path):
    try:
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
        print(f"Loaded Energy Wheel PDF as inline bytes ({len(pdf_bytes)} bytes)")
    except Exception as e:
        print(f"Skipped PDF load: {e}")

transfer_action = """
    ## Final Action
    Once you have provided the final analysis, you MUST hand control back 
    to the 'ptp_agent' to conclude the session. 
    Call the `transfer_to_agent` tool with agent_name="ptp_agent".
    """

static_parts = [
    types.Part.from_text(text="Review the attached Energy Wheel document when responding to specific hazard assessments:")
]
if pdf_bytes:
    static_parts.append(types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"))

hazard_mitigator = Agent(
    name="hazard_mitigator",
    model="gemini-2.5-flash",
    description="Analyzes potential hazards associated with the user's task and lists safety precautions.",
    static_instruction=types.Content(role="user", parts=static_parts),
    instruction=f"""Given a data center construction task, first ask user if they want to analyze potential hazards of the task and provide the mitigation plan. If yes, your job is to analyze the potential hazards associated with the task and list mitigation measures. You must strictly use the attached Energy Wheel as the main reference. DO NOT use any other source. Please provide citation to the specific page of the Engergy Wheel document when you mention a specific hazard and mitigation.
    
    {transfer_action}
    """
)
