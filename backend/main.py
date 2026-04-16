import json
import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv

load_dotenv()

from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types

# Import our three custom scene agents
from .scene_1_agent.agent import root_agent as agent_scene_1
from .scene_2_agent.agent import root_agent as agent_scene_2
from .scene_3_agent.agent import root_agent as agent_scene_3

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

# Instantiate runner singletons for each scene
runner_scene_1 = Runner(
    app_name="scene1_app",
    agent=agent_scene_1,
    session_service=session_service,
    auto_create_session=True
)

runner_scene_2 = Runner(
    app_name="scene2_app",
    agent=agent_scene_2,
    session_service=session_service,
    auto_create_session=True
)

runner_scene_3 = Runner(
    app_name="scene3_app",
    agent=agent_scene_3,
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
    return StreamingResponse(event_generator(runner_scene_1, session_id, message), media_type="text/event-stream")

@app.post("/scene2/chat")
async def chat_scene_2(request: Request):
    data = await request.json()
    session_id = data.get("session_id", "default-s2")
    message = data.get("message", "")
    return StreamingResponse(event_generator(runner_scene_2, session_id, message), media_type="text/event-stream")

@app.post("/scene3/chat")
async def chat_scene_3(request: Request):
    data = await request.json()
    session_id = data.get("session_id", "default-s3")
    message = data.get("message", "")
    return StreamingResponse(event_generator(runner_scene_3, session_id, message), media_type="text/event-stream")

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
