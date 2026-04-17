from google.adk.agents import Agent
from google.cloud import bigquery
import json

def search_schedule_conflict(query: str) -> str:
    """
    Search the Primavera P6 schedule for conflicts in a given location.
    Use this tool to find schedule overlaps.
    """
    project_id = "ninghai-ccai"
    dataset_id = "ptp_demo"
    table_id = "simulated_schedule"
    
    client = bigquery.Client(project=project_id)
    
    query_str = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"
    
    try:
        query_job = client.query(query_str)
        results = query_job.result()
        
        rows = []
        for row in results:
            rows.append(dict(row))
            
        return json.dumps(rows, indent=2)
    except Exception as e:
        print(f"Error querying BigQuery: {e}")
        return f"Error querying BigQuery: {e}"

transfer_action = """
    ## Final Action
    Once you have provided the final analysis, you MUST hand control back 
    to the 'ptp_agent' to conclude the session. 
    Call the `transfer_to_agent` tool with agent_name="ptp_agent".
    """

from datetime import date

today = date.today().strftime("%Y-%m-%d")

schedule_conflict_finder = Agent(
    name="schedule_conflict_finder",
    model="gemini-2.5-pro",
    description="Checks the Primavera P6 schedule for conflicts in a given location using VAIS Search.",
    tools=[search_schedule_conflict],
    instruction=f"""
    DO NOT greet the user. DO NOT introduce yourself.
    Today is {today}.
    Inform user that you are now going to look for any potential overlaps in the Primavera Schedule for your task. 
    
    1. Identify the location where the crew is working. 
    2. Use the `search_schedule_conflict` tool to search for work that's going on in the same area around the same time.
    
    If the tool returns results, use them to report conflicts. Make sure you cite specific references where the conflict is found.
    
    {transfer_action}
    """
)
