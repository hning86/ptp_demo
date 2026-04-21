import os
import vertexai
from vertexai.preview import rag

DEFAULT_MODEL = os.environ.get("GEMINI_MODEL")

transfer_action = """
    ## Final Action
    Once you have provided the final analysis, you MUST hand control back 
    to the 'ptp_agent' to conclude the session. 
    Call the `transfer_to_agent` tool with agent_name="ptp_agent".
    """

common_instruction = """
    ## Common Rules
    - DO NOT greet the user.
    - DO NOT introduce yourself.
    - DO NOT repeat what was just said by the user or previous agents.
    """

def search_safety_guideline(query: str) -> str:
    """
    Search the Safety Requirements document for safety guidelines and hazard mitigations.
    Use this tool to find specific hazards and controls from the Safety Requirements document.
    """
    rag_corpus_name = os.environ.get("RAG_CORPUS_NAME")
    
    # Extract project and location
    parts = rag_corpus_name.split("/")
    project = parts[1]
    location = parts[3]
    
    vertexai.init(project=project, location=location)
    
    try:
        response = rag.retrieval_query(
            text=query,
            rag_resources=[rag.RagResource(rag_corpus=rag_corpus_name)],
            similarity_top_k=5
        )
        
        contexts = []
        if hasattr(response, 'contexts') and hasattr(response.contexts, 'contexts'):
            for context in response.contexts.contexts:
                contexts.append(context.text)
        elif hasattr(response, 'contexts'):
            for context in response.contexts:
                contexts.append(context.text)
        
        if not contexts:
            return "No relevant safety contexts found."
            
        return "\n".join(contexts)
    except Exception as e:
        print(f"Rag Engine error: {e}")
        return f"Error retrieving from Rag Engine: {e}"

def get_current_weather():
    """
    Get the current weather for a given location.
    """
    return "Weather advisory: Dark clouds are rolling in with scattered light rain. Temperature is 52°F and humidity is 75%. Winds are steady at 25 mph with occasional gusts up to 35 mph."
