import json
import os
from google.cloud import bigquery
from dotenv import load_dotenv

# Load .env from backend directory
script_dir = os.path.dirname(os.path.abspath(__file__))
backend_env = os.path.join(os.path.dirname(script_dir), 'backend', '.env')
load_dotenv(backend_env)

def load_to_bq():
    project_id = os.environ.get("BQ_PROJECT_ID", "ninghai-ccai")
    dataset_id = os.environ.get("BQ_DATASET_ID", "ptp_demo")
    table_id = os.environ.get("BQ_SCHEDULE_TABLE_ID", "simulated_schedule")
    
    client = bigquery.Client(project=project_id)
    
    # Create dataset if not exists
    dataset_ref = bigquery.DatasetReference(project_id, dataset_id)
    try:
        client.get_dataset(dataset_ref)
        print(f"Dataset {dataset_id} already exists.")
    except Exception:
        print(f"Creating dataset {dataset_id}...")
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "us-east5" # Using same location as RAG
        try:
            client.create_dataset(dataset)
            print(f"Dataset {dataset_id} created.")
        except Exception as e:
            print(f"Failed to create dataset: {e}")
            return
        
    table_ref = dataset_ref.table(table_id)
    
    # Load data from file
    file_path = "/Users/ninghai/projects/craft-ptp-demo-v2/scratch/simulated_schedule.json"
    with open(file_path, "r") as f:
        rows = json.load(f)
        
    # Define schema
    schema = [
        bigquery.SchemaField("task_id", "STRING"),
        bigquery.SchemaField("description", "STRING"),
        bigquery.SchemaField("start_date", "STRING"),
        bigquery.SchemaField("end_date", "STRING"),
        bigquery.SchemaField("location", "STRING"),
        bigquery.SchemaField("crew_foreperson", "STRING"),
    ]
    
    # Create table if not exists
    try:
        client.get_table(table_ref)
        print(f"Table {table_id} already exists. Deleting to refresh data...")
        client.delete_table(table_ref)
        # Wait a bit for deletion to propagate
        import time
        time.sleep(2)
    except Exception:
        pass
        
    print(f"Creating table {table_id}...")
    table = bigquery.Table(table_ref, schema=schema)
    client.create_table(table)
    print(f"Table {table_id} created.")
        
    # Insert rows
    print(f"Inserting {len(rows)} rows into {table_id}...")
    errors = client.insert_rows_json(table_ref, rows)
    if errors == []:
        print("New rows have been added.")
    else:
        print(f"Encountered errors while inserting rows: {errors}")

if __name__ == "__main__":
    load_to_bq()
