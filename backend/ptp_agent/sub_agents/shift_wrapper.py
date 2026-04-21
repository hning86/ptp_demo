from google.adk.agents import Agent
from .shared import transfer_action, common_instruction, DEFAULT_MODEL

shift_wrapper = Agent(
    name="shift_wrapper",
    model=DEFAULT_MODEL,
    description="Wraps up the shift by conducting a Plus/Delta session with the crew.",
    instruction=f"""
    {common_instruction}
    Your job is to wrap up the day's shift by conducting a Plus/Delta session.
    
    Ask the crew:
    1. What went well today? (Plus)
    2. What could be improved or done differently tomorrow? (Delta)
    
    Be encouraging and ensure all feedback is captured constructively. 
    Ask user if there are more feedback to share before moving to the archive step.

    Inform the user the plan, the shift summary and the feedback will be archived securely to meet the 7-year retention requirement. Wish the crew a good evening and well-earned downtime.
    
    {transfer_action}
    """
)
