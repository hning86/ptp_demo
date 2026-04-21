import os
import re
from google import genai
from google.genai import types
from google.adk.agents import Agent
from google.cloud import discoveryengine
import vertexai
from vertexai.preview import rag

from .shared import transfer_action, common_instruction, search_safety_guideline, DEFAULT_MODEL

def search_osha_guidelines(query: str) -> str:
    """
    Search the OSHA website (osha.gov) for safety compliance rules, standards, and hazard guidelines.
    Use this tool to augment local safety guidelines with federal OSHA standards.
    """
    from google import genai
    from google.genai import types
    
    client = genai.Client()
    full_query = f"site:osha.gov {query}"
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_query,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        return response.text
    except Exception as e:
        return f"Error searching OSHA guidelines: {e}"

hazard_mitigator = Agent(
    name="hazard_mitigator",
    model=DEFAULT_MODEL,
    description="Analyzes potential hazards associated with the user's task using VAIS Search and OSHA standards.",
    tools=[search_safety_guideline, search_osha_guidelines],
    instruction=f"""
    {common_instruction}
    Given a data center construction task, just ask user if they want to analyze potential hazards of the task and provide the mitigation plan. Make sure you wait for user's response before proceeding.
    
    If user answers yes, your job is to analyze the potential hazards associated with the task and list mitigation measures. 
    
    You must use the `search_safety_guideline` tool to find specific hazards and controls from the Safety Requirements document. You must strictly use the Safety Requirements content returned by the tool as the main reference. 
    
    You can also augment your analysis with information from OSHA using the `search_osha_guidelines` tool. Please provide citation (including file name, section numbers, or OSHA standard codes) or reference to the specific content found when you mention a specific hazard and mitigation.
    
    Also be concise and to the point. Don't list more than 5 risks and their mitigations. If more than 5 risks are found, just list the top 5. Make sure at least one of them is from Energy Wheel PDF if applicable.

    Make sure you share the findings with the user before you transfer the control back to the parent agent.
    
    {transfer_action}
    """
)
