from google.adk.agents import Agent
from ..search_util import search_vais

def search_schedule_conflict(query: str) -> str:
    """
    Search the Primavera P6 schedule for conflicts in a given location.
    Use this tool to find schedule overlaps.
    """
    return search_vais(query, category="p6_schedules")

transfer_action = """
    ## Final Action
    Once you have provided the final analysis, you MUST hand control back 
    to the 'ptp_agent' to conclude the session. 
    Call the `transfer_to_agent` tool with agent_name="ptp_agent".
    """

schedule_conflict_finder = Agent(
    name="schedule_conflict_finder",
    model="gemini-2.5-flash",
    description="Checks the Primavera P6 schedule for conflicts in a given location using VAIS Search.",
    tools=[search_schedule_conflict],
    instruction=f"""
    DO NOT greet the user. DO NOT introduce yourself.
    Inform user that you are now going to look for any potential overlaps in the Primavera Schedule for your task. 
    You must use the `search_schedule_conflict` tool to search for overlaps.
    If the tool returns results, use them to report conflicts. Make sure you cite specific references where the conflict is found.
    If the tool returns no results or fails, to keep the demo flow working, you MUST report that you found an overlap: 'Overhead mechanical pipeline installation scheduled in Area B, Aisle 3.' (mention that you are simulating this for the demo).
    
    {transfer_action}
    """
)
