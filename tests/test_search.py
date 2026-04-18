import os
import sys
from dotenv import load_dotenv

# Load environment variables from backend/.env
load_dotenv(os.path.join(os.path.dirname(__file__), "backend", ".env"))

# Ensure the project root is in the python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from backend.ptp_agent.search_util import search_vais

def test_search():
    print("Testing VAIS Search...")
    
    # Test 1: Search with category safety-requirements
    # print("\nTest 1: Searching safety-requirements...")
    # res1 = search_vais("ladder safety", category="safety-requirements")
    #print(f"Result:\n{res1}")
    
    # Test 2: Search with category p6_schedules
    print("\nTest 2: Searching p6_schedules...")
    search_term = "Identify a few scheduling conflicts with Installing Area B of the data hall. We are about to pull low voltage cable in aisle 3."
    res2 = search_vais(search_term, category="p6_schedules")
    print(f"Result:\n{res2}")
    
    # Test 3: Search without category
    # print("\nTest 3: Searching without category...")
    # res3 = search_vais("safety", category=None)
    # print(f"Result:\n{res3}")

if __name__ == "__main__":
    test_search()
