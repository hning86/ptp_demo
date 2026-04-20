from google.adk.agents import Agent
from .learning_resources_provider import learning_resources_provider

from .shared import transfer_action, common_instruction

def get_current_weather():
    """
    Get the current weather for a given location.
    """
    return "Weather advisory: Dark clouds are rolling in with scattered light rain. Temperature is 52°F and humidity is 75%. Winds are steady at 25 mph with occasional gusts up to 35 mph."

plan_revisor = Agent(
    name="plan_revisor",
    model="gemini-2.5-flash",
    instruction=f"""
    {common_instruction}
    After PTP v1 is presented to the user, you job is to revise PTP with additional considerations. Ask questions in the following areas (using markdown checkboxes like - [ ]) EXAXTLY as it is written below (including the spaces, dashes, and square brackets):
        - [ ] Changing Work Area Conditions
        - [ ] Tools/equipment Availability
        - [ ] Materials Availability
        - [ ] Changing Environmental Conditions/weather
        - [ ] Workforce (New Workers/Worker Substitution)
        - [ ] Changes in Work Sequence/Trade Flow
        - [ ] Changing Task assignment(s)
        - [ ] Means & Methods Substitution
        - [ ] Changes - Human Factors (Mental Health/Wellness)
    Ask user related questions about these areas, until user confirms that there is no more additional information to provide. Make sure you inform the user that you will take all that information into consideration to update the PTP.

    If user checks "Changing Environmental Conditions/weather", check the current weather using the get_current_weather tool. If the weather is bad, inform the crew that it will be taken into consideration. 

    If user checks "Workforce (New Workers/Worker Substitution)", use learning_resources_provider to provide learning resources for the new crew member.

    {transfer_action}
    """,
    sub_agents=[learning_resources_provider],
    tools=[get_current_weather]
)
