from google.adk.agents import Agent

transfer_action = """
    ## Final Action
    Once you have provided the final analysis, you MUST hand control back 
    to the 'ptp_agent' to conclude the session. 
    Call the `transfer_to_agent` tool with agent_name="ptp_agent".
    """

ptp_generator = Agent(
    name="ptp_generator",
    model="gemini-2.5-flash",
    instruction=f"""
    Generate a high level summary of the PreTask Plan based on the task and hazards information. Make sure you include a hyperlink to the actual plan document towards the end of the summary. The link should be pointing to an Excel file stored on a Google Drive. Here is the format you should try to stick to:

    ### 📋 Integrated Work Plan (IWP)

| General Information | Details |
|---|---|
| **Activity Name** | [Agent to fill] |
| **DFOW** | [Agent to fill] |
| **Date** | [Agent to fill] |

| Step | Operational Step Description | Tools & Equipment | Hazards & Mitigations | Quality Expectations |
|---|---|---|---|---|
| 1 | [Description] | [Tools needed] | [Hazards & Controls] | [Quality standard] |
| 2 | [Description] | [Tools needed] | [Hazards & Controls] | [Quality standard] |

| Safety Requirements | Details |
|---|---|
| **High-Risk Activities** | [List top risks from the steps above] |
| **Specific PPE / Permits** | [List specific requirements beyond standard] |

---

### 🔍 Inspection & Test Plan (ITP)

| Phase | Activity / Step | Test or Inspection | Responsible Party | Verification Document |
|---|---|---|---|---|
| Pre-Con | [Activity] | [Inspection type] | [Party name] | [Doc required] |
| Con | [Activity] | [Inspection type] | [Party name] | [Doc required] |
| Post-Con| [Activity] | [Inspection type] | [Party name] | [Doc required] |


<link to the generated actual Excel file> in the format of <https://docs.google.com/spreadsheets/d/1BxiAGCzWMrV2vFuHezL0XZdp7jJwbD-oBtW6OSB_Uwo/edit?usp=sharing>

    {transfer_action}
    
    """
)
