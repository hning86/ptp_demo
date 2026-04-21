import json
import os
import uvicorn
import io
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from google.cloud import bigquery
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()

from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types

# Import our three custom scene agents
from .ptp_agent.agent import root_agent as craft_ptp_agent
from .ptp_agent.sub_agents.shared import get_current_weather


app = FastAPI(title="Craft PTP Interactive Demo App")

# Allow local demo clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_service = InMemorySessionService()

@app.get("/schedule")
async def get_schedule():
    project_id = "ninghai-ccai"
    dataset_id = "ptp_demo"
    table_id = "simulated_schedule"
    
    client = bigquery.Client(project=project_id)
    query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"
    
    try:
        query_job = client.query(query)
        results = query_job.result()
        
        schedule = []
        for row in results:
            schedule.append({
                "task_id": row.task_id,
                "description": row.description,
                "start_date": row.start_date,
                "end_date": row.end_date,
                "location": row.location,
                "crew_foreperson": row.crew_foreperson
            })
        return schedule
    except Exception as e:
        return {"error": str(e)}

@app.get("/weather")
async def get_weather():
    return {"weather": get_current_weather()}

@app.get("/safety-docs")
async def get_docs():
    return [
        {"title": "Energy Wheel.pdf", "category": "energy-wheel", "url": "/safety-docs/Energy%20Wheel.pdf"},
        {"title": "Construction Barriers, Barricades, and Tagging Usage CON-EHS-TSS-020.00.pdf", "category": "safety-requirements", "url": "/safety-docs/Construction%20Barriers,%20Barricades,%20and%20Tagging%20Usage%20CON-EHS-TSS-020.00.pdf"},
        {"title": "Construction Cutting Tool Use CON-EHS-TSS-008.00.pdf", "category": "safety-requirements", "url": "/safety-docs/Construction%20Cutting%20Tool%20Use%20CON-EHS-TSS-008.00.pdf"},
        {"title": "Construction Ladder Usage CON-EHS-TSS-012.00.pdf", "category": "safety-requirements", "url": "/safety-docs/Construction%20Ladder%20Usage%20CON-EHS-TSS-012.00.pdf"},
        {"title": "Contractor Safety Improvement Plan CON-EHS-TSS-019.00 (1).pdf", "category": "safety-requirements", "url": "/safety-docs/Contractor%20Safety%20Improvement%20Plan%20CON-EHS-TSS-019.00%20(1).pdf"},
        {"title": "Copy of Risk Assessment Program CON-EHS-TSS-015.00.pdf", "category": "safety-requirements", "url": "/safety-docs/Copy%20of%20Risk%20Assessment%20Program%20CON-EHS-TSS-015.00.pdf"},
        {"title": "Crane and Rigging Usage CON-EHS-TSS-010.00.pdf", "category": "safety-requirements", "url": "/safety-docs/Crane%20and%20Rigging%20Usage%20CON-EHS-TSS-010.00.pdf"},
        {"title": "Excavation and Trenching CON-EHS-TSS-005.00.pdf", "category": "safety-requirements", "url": "/safety-docs/Excavation%20and%20Trenching%20CON-EHS-TSS-005.00.pdf"},
        {"title": "Permit To Work Systems CON-EHS-TSS-018.00.pdf", "category": "safety-requirements", "url": "/safety-docs/Permit%20To%20Work%20Systems%20CON-EHS-TSS-018.00.pdf"},
        {"title": "Risk Assessment Program CON-EHS-TSS-015.00.pdf", "category": "safety-requirements", "url": "/safety-docs/Risk%20Assessment%20Program%20CON-EHS-TSS-015.00.pdf"}
    ]

@app.get("/safety-docs/{filename}")
async def get_doc(filename: str):
    bucket_name = "ninghai-bucket-0"
    
    paths = [
        f"ptp_demo/{filename}",
        f"ptp_demo/safety_requirements/{filename}"
    ]
    
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    
    for path in paths:
        blob = bucket.blob(path)
        if blob.exists():
            content = blob.download_as_bytes()
            return StreamingResponse(io.BytesIO(content), media_type="application/pdf")
            
    return {"error": "File not found"}

# Instantiate runner singletons for each scene
runner_craft_ptp_agent = Runner(
    app_name="craft_ptp_app",
    agent=craft_ptp_agent,
    session_service=session_service,
    auto_create_session=True
)



def event_generator(runner, session_id: str, message: str):
    async def _gen():
        try:
            agen = runner.run_async(
                user_id="demo_user",
                session_id=session_id,
                new_message=types.Content(parts=[types.Part(text=message)])
            )
            async for event in agen:
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            yield f"data: {json.dumps({'text': part.text})}\r\n\r\n"
                        elif part.function_call:
                            yield f"data: {json.dumps({'text': '\n\n'})}\r\n\r\n"
            yield "data: [DONE]\r\n\r\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\r\n\r\n"
    return _gen()

@app.post("/scene1/chat")
async def chat_scene_1(request: Request):
    data = await request.json()
    session_id = data.get("session_id", "default-s1")
    message = data.get("message", "")
    return StreamingResponse(event_generator(runner_craft_ptp_agent, session_id, message), media_type="text/event-stream")



@app.post("/reset")
async def reset_sessions(request: Request):
    data = await request.json()
    session_id = data.get("session_id", "default-s1")
    try:
        # InMemorySessionService maintains ._sessions map
        if hasattr(session_service, "delete_session"):
            session_service.delete_session(session_id)
        elif hasattr(session_service, "_sessions"):
            if session_id in session_service._sessions:
                del session_service._sessions[session_id]
        return {"status": "reset_complete"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

from fastapi.staticfiles import StaticFiles
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
