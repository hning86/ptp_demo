import os
import re
from google import genai
from google.genai import types
from google.adk.agents import Agent
from google.cloud import discoveryengine
import vertexai
from vertexai.preview import rag

from .shared import transfer_action, common_instruction, search_safety_guideline, DEFAULT_MODEL

hazard_mitigator = Agent(
    name="hazard_mitigator",
    model=DEFAULT_MODEL,
    description="Analyzes potential hazards associated with the user's task and lists safety precautions using VAIS Search.",
    tools=[search_safety_guideline],
    instruction=f"""
    {common_instruction}
    Given a data center construction task, just ask user if they want to analyze potential hazards of the task and provide the mitigation plan. If user answers yes, your job is to analyze the potential hazards associated with the task and list mitigation measures. 
    
    You must use the `search_safety_guideline` tool to find specific hazards and controls from the Safety Requirements document. You must strictly use the Safety Requirements content returned by the tool as the main reference. DO NOT use any other source. Please provide citation or reference to the specific content found when you mention a specific hazard and mitigation.
    
    Also be concise and to the point. Don't list more than 3 risks and their mitigations. 
    
    {transfer_action}
    """
)
