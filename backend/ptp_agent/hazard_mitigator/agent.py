import os
import re
from google import genai
from google.genai import types
from google.adk.agents import Agent
from google.cloud import discoveryengine

transfer_action = """
    ## Final Action
    Once you have provided the final analysis, you MUST hand control back 
    to the 'ptp_agent' to conclude the session. 
    Call the `transfer_to_agent` tool with agent_name="ptp_agent".
    """

def search_safety_guideline(query: str) -> str:
    """
    Search the Safety Requirements document for safety guidelines and hazard mitigations.
    Use this tool to find specific hazards and controls from the Safety Requirements document.
    """
    print(f"\n\n---DEBUG: Searching Safety Requirements for: {query}")
    client = discoveryengine.SearchServiceClient()
    project_id = os.environ.get('GOOGLE_CLOUD_PROJECT', 'ninghai-ccai')
    location = os.environ.get('VAIS_LOCATION', 'global')
    datastore_id = os.environ.get('VAIS_DATASTORE_ID', 'ptp-docs-store')
    serving_config = f"projects/{project_id}/locations/{location}/collections/default_collection/dataStores/{datastore_id}/servingConfigs/default_search"
    
    request = discoveryengine.SearchRequest(
        serving_config=serving_config,
        query=query,
        page_size=3,
        content_search_spec=discoveryengine.SearchRequest.ContentSearchSpec(
            extractive_content_spec=discoveryengine.SearchRequest.ContentSearchSpec.ExtractiveContentSpec(
                max_extractive_segment_count=1
            )
        )
    )
    
    try:
        response = client.search(request=request)
        results = []
        for result in response.results:
            derived = result.document.derived_struct_data
            if derived:
                for seg in derived.get("extractive_segments", []):
                    raw_seg = seg.get("content", "")
                    # Clean up tags and ellipses
                    clean_seg = re.sub(r'</?b>', '', raw_seg)
                    clean_seg = clean_seg.replace('...', '').strip()
                    if clean_seg:
                        results.append(clean_seg)
            
        if not results:
            return "No specific guidelines found in Safety Requirements for this query."
            
        # Remove duplicates
        unique_results = list(set(results))
        return "\n\n".join(unique_results)
    except Exception as e:
        return f"Error searching Safety Requirements: {e}"

hazard_mitigator = Agent(
    name="hazard_mitigator",
    model="gemini-2.5-flash",
    description="Analyzes potential hazards associated with the user's task and lists safety precautions using VAIS Search.",
    tools=[search_safety_guideline],
    instruction=f"""
    Given a data center construction task, just ask user if they want to analyze potential hazards of the task and provide the mitigation plan. (There is no need to introduct yourself.) If user answers yes, your job is to analyze the potential hazards associated with the task and list mitigation measures. 
    
    You must use the `search_safety_guideline` tool to find specific hazards and controls from the Safety Requirements document. You must strictly use the Safety Requirements content returned by the tool as the main reference. DO NOT use any other source. Please provide citation or reference to the specific content found when you mention a specific hazard and mitigation.
    
    {transfer_action}
    """
)
