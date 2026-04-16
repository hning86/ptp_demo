# Google ADK: Craft PTP Agent User Journey Demo

An interactive, multi-scene visual showcase mimicking continuous Pre-Task Planning (PTP) compliance across field operations via modular AI Agent pipelines.

## Project Contents

- **`backend/`**: Python microservice mapping independent Google ADK inference workflows across 3 stages:
  - **`scene_1_agent/`**: Coordinates Morning Task summaries.
    ```mermaid
    flowchart TD
        R["root_agent (scene_1_planning_agent)"]
        S["schedule_conflict_finder"]
        H["hazard_mitigator (Energy Wheel RAG)"]
        P["ptp_generator"]
        A["plan_augmentor"]

        R -->|"1. Check location overlaps"| S
        R -->|"2. Assess task hazard state"| H
        R -->|"3. Generate core plan"| P
        R -->|"4. Request team substitutions"| A
    ```
  - **`scene_2_agent/`**: Audits local stop-work procedures.
  - **`scene_3_agent/`**: Aggregates Continuous Improvements (Plus/Delta).
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
