from google.adk.agents import Agent

from .shared import transfer_action, common_instruction, DEFAULT_MODEL

ptp_generator = Agent(
    name="ptp_generator",
    model=DEFAULT_MODEL,
    instruction=f"""
    {common_instruction}
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

Here is the plan generated: [ptp_task_plan.xlsx](https://example.com/ptp_task_plan.xlsx)

    {transfer_action}
    
    """
)
