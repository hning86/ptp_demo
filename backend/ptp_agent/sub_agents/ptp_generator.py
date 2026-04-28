from datetime import date
from google.adk.agents import Agent

from .shared import transfer_action, common_instruction, DEFAULT_MODEL

today_str = date.today().strftime('%B %d, %Y')

ptp_generator = Agent(
    name="ptp_generator",
    model=DEFAULT_MODEL,
    instruction=f"""
    {common_instruction}
    
    You will receive a parameter from the parent agent telling you which version of the plan to generate (e.g., PTP v1 or PTP v2). 
    Generate a high level summary of the requested PreTask Plan version based on the task and hazards information in the exact format as below and show it back to the user. 

<plan_template>
    ### 📋 Integrated Work Plan (IWP)

| General Information | Details |
|---|---|
| **Activity Name** | [Agent to fill] |
| **DFOW** | [Agent to fill] |
| **Date** | {today_str} |

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

Here is the plan generated: [ptp_task_plan_version_x.xlsx](https://example.com/ptp_task_plan_version_x.xlsx) 
<note>x = "v1", "v2", or "v3" etc. depending on the version of the plan to generate.</note>

</plan_template>

    {transfer_action}
    
    """
)
