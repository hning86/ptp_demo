import os
import sys
from dotenv import load_dotenv

# Load environment variables from backend/.env
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
backend_env = os.path.join(project_root, "backend", ".env")
load_dotenv(backend_env)

# Ensure the project root is in the python path
sys.path.append(project_root)

from backend.ptp_agent.sub_agents.shared import search_safety_guideline

def test_search_safety():
    print("Testing search_safety_guideline...")
    
    # Query that should return results
    query = "ladder safety"
    print(f"\nQuery: {query}")
    result = search_safety_guideline(query)
    print(f"Result:\n{result}")
    
    # Another query
    query = "scissor lift"
    print(f"\nQuery: {query}")
    result = search_safety_guideline(query)
    print(f"Result:\n{result}")

if __name__ == "__main__":
    test_search_safety()
