import asyncio
import json
import os
import sys
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types

from dotenv import load_dotenv
# Load environment variables from backend/.env
load_dotenv(os.path.join(os.path.dirname(__file__), "backend", ".env"))

# Ensure the project root is in the python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import the agent
from backend.ptp_agent.agent import root_agent

async def test_agent():
    session_service = InMemorySessionService()
    runner = Runner(
        app_name="ptp_test_app",
        agent=root_agent,
        session_service=session_service,
        auto_create_session=True
    )
    
    session_id = "test-session-1"
    
    turns = [
        "Hello! I am a new crew member. I need help with Pre-Task Planning.",
        "We are at the UNO3 campus, Area B of the data hall. We are about to pull low voltage cable in aisle 3. The cable trays are already installed. I have a crew of 3 people today and we have 10 hours to get the work done.",
        "Yes, please analyze hazards of the task you found that conflicts with my main task today.",
        # "Great, now please generate the PTP v1."
    ]
    
    for message in turns:
        print(f"\n{'='*20}")
        print(f"User: {message}")
        print(f"{'='*20}")
        print("Agent: ", end="", flush=True)
        
        try:
            agen = runner.run_async(
                user_id="test_user",
                session_id=session_id,
                new_message=types.Content(parts=[types.Part.from_text(text=message)])
            )
            async for event in agen:
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            print(part.text, end="", flush=True)
                        elif part.function_call:
                            print(f"\n[Function Call: {part.function_call.name} with args {part.function_call.args}]", end="", flush=True)
            print()
        except Exception as e:
            print(f"\nError during turn: {e}")

if __name__ == "__main__":
    # Run the async test
    asyncio.run(test_agent())
