import os
from google.adk.agents import Agent
from google.cloud import bigquery
from .shared import transfer_action, common_instruction, DEFAULT_MODEL
import json

def get_past_incidents(task: str) -> str:
    """
    Retrieve relevant past incidents from BigQuery for a given task.
    """
    project_id = os.environ.get("BQ_PROJECT_ID", "ninghai-ccai")
    dataset_id = os.environ.get("BQ_DATASET_ID", "ptp_demo")
    table_id = os.environ.get("BQ_IRIS_TABLE_ID", "iris_incidents")
    
    client = bigquery.Client(project=project_id)
    
    # If task is provided, try to filter by task or incident content
    # Otherwise return all
    if task and task != "General":
        query_str = f"""
            SELECT * FROM `{project_id}.{dataset_id}.{table_id}`
            WHERE LOWER(task) LIKE LOWER('%{task}%') 
               OR LOWER(incident) LIKE LOWER('%{task}%')
               OR LOWER(type) LIKE LOWER('%{task}%')
        """
    else:
        query_str = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"
        
    try:
        query_job = client.query(query_str)
        results = query_job.result()
        
        rows = []
        for row in results:
            rows.append(dict(row))
            
        # If no results found with filter, fallback to all records
        if not rows and task and task != "General":
            query_all = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"
            query_job = client.query(query_all)
            results = query_job.result()
            for row in results:
                rows.append(dict(row))
                
        return json.dumps(rows, indent=2)
    except Exception as e:
        print(f"Error querying BigQuery: {e}")
        return json.dumps([], indent=2)

def get_scissor_lift_video_link() -> str:
    """
    Retrieve the scissor lift safety video link.
    """
    return "https://www.youtube.com/watch?v=coYQOu2Y1pI"

learning_resources_provider = Agent(
    name="learning_resources_provider",
    model=DEFAULT_MODEL,
    instruction=f"""
    {common_instruction}
    Provide learning resources for the safety topic, which are related to the task. First, use the get_past_incidents tool to retrieve past incidents for the task. Also use get_scissor_lift_video_link to get the video link. Then display the following as a list of resources: 
    - [Toolbox doc](https://examples.com/doc_place_holder.docx)
    - Training video (Provide the link retrieved by get_scissor_lift_video_link)
    - List past incidents (from the get_past_incidents tool in simple one-line-bullet-points format. No more than one sentence per line with a link to the full report)

    Stops and ask user to take some time to review the above materials. Once the user is ready, continue with the next step by using transfer action.
        
    {transfer_action}
    """,
    tools=[get_past_incidents, get_scissor_lift_video_link]
)
