transfer_action = """
    ## Final Action
    Once you have provided the final analysis, you MUST hand control back 
    to the 'ptp_agent' to conclude the session. 
    Call the `transfer_to_agent` tool with agent_name="ptp_agent".
    """

common_instruction = """
    ## Common Rules
    - DO NOT greet the user.
    - DO NOT introduce yourself.
    - DO NOT repeat what was just said by the user or previous agents.
    """
