# Google ADK: Craft PTP Agent User Journey Demo

An interactive, multi-scene visual showcase mimicking continuous Pre-Task Planning (PTP) compliance across field operations via modular AI Agent pipelines.

## Project Contents

- **`backend/`**: Python microservice mapping independent Google ADK inference workflows across 3 stages:
  - **`scene_1_agent/`**: Coordinates Morning Task summaries.
  - **`scene_2_agent/`**: Audits local stop-work procedures.
  - **`scene_3_agent/`**: Aggregates Continuous Improvements (Plus/Delta).
- **`index.html`**: Embedded interactive viewer styling responsive checklists, real-time mock connection events, and Presenter action templates.

## Running Locally

### 1. Deploy Backend Stream Endpoints
As per global rules, please invoke `uv` inside the core terminal:
```bash
cd backend
uv pip install -r requirements.txt
uv run uvicorn main:app --reload --port 8000
```

### 2. Access Core Visualization (Frontend Web Server)
Open a separate terminal from the backend, navigate to the root directory, and launch a local static file server:
```bash
python3 -m http.server 5500
```
Once running, navigate your web browser to [http://localhost:5500](http://localhost:5500) to interact with the visual presentation fully!
