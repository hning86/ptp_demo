# Google ADK: Craft PTP Agent User Journey Demo

An interactive, multi-scene visual showcase mimicking continuous Pre-Task Planning (PTP) compliance across field operations via modular AI Agent pipelines.

## Overview & User Journey

The Craft PTP Agent demo leverages the Google Agent Development Kit (ADK) to simulate an end-to-end digital safety compliance assistant for modern construction environments (modeled around data center deployments). 

The experience follows a structured daily workflow:
1. **Morning Task Initiation**: Crews declare geographic staging targets. The core orchestrator leverages BigQuery to sweep cross-trade schedule conflicts immediately.
2. **Dynamic Mitigation Search**: Context-aware algorithms query structured Vertex AI RAG repositories against safety requirements to highlight hazards.
3. **Iterative Optimization**: Generates baseline spreadsheets (`PTP v1`) subsequently hardened into `PTP v2` utilizing team substitution rules. 
4. **Adaptive Reassessment ("Take Two")**: Intercepts active site blockers (like equipment layout changes) gracefully.
5. **Shift Closeout (Plus/Delta)**: Validates performance KPIs, safety milestones, and physical fatigue management.

## Project Contents

- **`backend/`**: Python microservice mapping Google ADK inference workflows via a centralized agent topology:
  - **`ptp_agent`**: Coordinates the full shift lifecycle using modular sub-agents.
    ```mermaid
    flowchart TD
        R["root_agent (ptp_agent)"]
        S["schedule_conflict_finder"]
        H["hazard_mitigator"]
        P["ptp_generator"]
        PR["plan_revisor"]
        LRP["learning_resources_provider"]
        PA["plan_reassessor"]
        W["shift_wrapper"]

        BQ[("BigQuery: simulated_schedule")]
        RAG[("Vertex AI RAG: Safety Requirements")]
        IRIS[("Mock IRIS Logs & YouTube")]
        WX[("Weather Advisory")]

        R -->|"1. Check conflicts"| S
        S -->|"search_schedule_conflict"| BQ
        
        R -->|"2. Analyze hazards"| H
        H -->|"search_safety_guideline"| RAG
        
        R -->|"3. Generate PTP v1"| P
        
        R -->|"4. Revise plan"| PR
        PR -->|"get_current_weather"| WX
        PR -->|"Consult"| LRP
        LRP -->|"get_past_incidents / video"| IRIS
        
        R -->|"5. Generate PTP v2"| P
        
        R -->|"6. Pause & reassess"| PA
        PA -->|"search_safety_guideline"| RAG
        
        R -->|"7. Generate PTP v3"| P
        
        R -->|"8. Wrap up shift"| W
    ```

### Sub-Agents, Tools & Data Sources

| Sub-Agent | Tools Implemented | Backing Data Source / API |
| :--- | :--- | :--- |
| **`schedule_conflict_finder`** | `search_schedule_conflict` | Google BigQuery (`simulated_schedule`) |
| **`hazard_mitigator`** | `search_safety_guideline` | Vertex AI RAG (Safety Requirement PDFs) |
| **`ptp_generator`** | *Implicit Generation* | Context Ingestion |
| **`plan_revisor`** | `get_current_weather` | Environment Overrides |
| **`learning_resources_provider`**| `get_past_incidents`<br>`get_scissor_lift_video_link` | Mock IRIS logs & YouTube references |
| **`plan_reassessor`** | `search_safety_guideline` | Vertex AI RAG (Safety Requirement PDFs) |
| **`shift_wrapper`** | *Implicit Collection* | Form Payload state |

- **`index.html`**: Embedded interactive viewer styling responsive checklists, real-time mock connection events, and Presenter action templates.

## Running Locally

### 1. Launch Integrated Application Server
Run our integrated service on your core terminal via `uv`. This embeds the full web GUI stack directly out of the `/frontend` module mapped securely inline:
```bash
uv pip install -r backend/requirements.txt
uv run uvicorn backend.main:app --reload --port 8000
```

### 2. Access Simulation Center
Simply click and interact online at: [http://localhost:8000](http://localhost:8000) with full multi-scene capabilities loaded out-of-the-box automatically! No other separate manual client nodes required to run!

---

## Remote Cloud Access (Local Proxying)

Once successfully deployed to Google Cloud Run using `./deploy.sh`, you can securely bridge the hosted service back to your workstation via `gcloud proxy` without requiring manual authorization redirects:

```bash
gcloud run services proxy craft-ptp-demo --region us-central1 --port 8000
```
After opening the secure tunnel, navigate standardly to **[http://localhost:8000](http://localhost:8000)**. Your client presentation will route directly against the scalable remote backend APIs securely!
