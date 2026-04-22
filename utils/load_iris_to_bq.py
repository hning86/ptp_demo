import json
import os
from google.cloud import bigquery

def load_iris_to_bq():
    project_id = "ninghai-ccai"
    dataset_id = "ptp_demo"
    table_id = "iris_incidents"
    
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
    
    # Hardcoded data from learning_resources_provider.py
    rows = [
        {
            "id": "IRIS-2025-0302",
            "date": "2025-03-02 2:39PM",
            "task": "Electrical Work / Scissor Lift Operation",
            "incident": "Electrician was working in the DC1 east zone when his scissor lift came in contact with a nearby ladder crushing the ladder on impact. No worker was using the ladder.",
            "type": "Near Miss",
            "key_focus": "Barricades requirements, Spotters & Banksperson requirements.",
            "suggested_resource": "OSHA Toolbox Talk on working around tight spaces with scissor lifts."
        },
        {
            "id": "IRIS-2024-0623",
            "date": "2024-06-23 3:45PM",
            "task": "Overhead Cable Pulling",
            "incident": "Worker was working on overhead cable pulling when he felt a sharp pain in his left shoulder.",
            "type": "Injury / Ergonomic Hazard",
            "key_focus": "Ergonomics",
            "suggested_resource": "OSHA Worksite Ergonomics Guide (https://www.oshaeducationcenter.com/worksite-ergonomics-guide/)"
        },
        {
            "id": "IRIS-2025-1114",
            "date": "2025-11-14 10:15AM",
            "task": "Hot Work / Welding",
            "incident": "Welder dropped a hot slag spark onto an empty cardboard box causing a small localized fire. Extinguished immediately by fire watch.",
            "type": "Fire Hazard / Near Miss",
            "key_focus": "Fire watch protocol, clearing combustibles from hot work zones.",
            "suggested_resource": "NFPA 51B Standard for Fire Prevention During Welding."
        },
        {
            "id": "IRIS-2025-0822",
            "date": "2025-08-22 1:30PM",
            "task": "Working at Heights",
            "incident": "Ironworker disconnected their safety lanyard temporarily to reach an out-of-bounds tool. Spotted by safety supervisor and corrected.",
            "type": "Safety Violation / Near Miss",
            "key_focus": "100% Tie-off enforcement, harness compliance.",
            "suggested_resource": "OSHA Fall Protection Guidelines."
        },
        {
            "id": "IRIS-2025-0505",
            "date": "2025-05-05 9:00AM",
            "task": "Material Handling",
            "incident": "Reach forklift operator misjudged distance while turning in the staging area, striking a pallet racking unit causing structural bending.",
            "type": "Property Damage",
            "key_focus": "Operator awareness, load management, strict speed limits.",
            "suggested_resource": "OSHA Powered Industrial Trucks Standard."
        },
        {
            "id": "IRIS-2024-1201",
            "date": "2024-12-01 11:00AM",
            "task": "Excavation / Trenching",
            "incident": "Minor trench wall collapse on the perimeter of a 4ft deep utility line trench. No workers were actively deployed inside the zone.",
            "type": "Near Miss",
            "key_focus": "Protective systems, trench shoring evaluation.",
            "suggested_resource": "OSHA Trenching and Excavation Safety."
        },
        {
            "id": "IRIS-2024-0915",
            "date": "2024-09-15 4:00PM",
            "task": "Personal Protective Equipment",
            "incident": "Crew members identified removing mandatory safety eyewear due to fogging in humid staging environments.",
            "type": "Safety Violation",
            "key_focus": "Anti-fog lens alternatives, consistent PPE checks.",
            "suggested_resource": "OSHA Eye and Face Protection."
        }
    ]
        
    # Define schema
    schema = [
        bigquery.SchemaField("id", "STRING"),
        bigquery.SchemaField("date", "STRING"),
        bigquery.SchemaField("task", "STRING"),
        bigquery.SchemaField("incident", "STRING"),
        bigquery.SchemaField("type", "STRING"),
        bigquery.SchemaField("key_focus", "STRING"),
        bigquery.SchemaField("suggested_resource", "STRING"),
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
    load_iris_to_bq()
