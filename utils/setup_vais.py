import os
from google.cloud import discoveryengine

project_id = "ninghai-ccai"
location = "global"
data_store_id = "ptp-docs-store"
engine_id = "ptp-search-app"

# 1. Create Datastore
ds_client = discoveryengine.DataStoreServiceClient()
parent = f"projects/{project_id}/locations/{location}/collections/default_collection"

try:
    ds = discoveryengine.DataStore(
        display_name="ptp_docs_store",
        industry_vertical=discoveryengine.IndustryVertical.GENERIC,
        content_config=discoveryengine.DataStore.ContentConfig.CONTENT_REQUIRED
    )
    op = ds_client.create_data_store(parent=parent, data_store=ds, data_store_id=data_store_id)
    print("Creating Datastore...")
    res = op.result()
    print(f"Created Datastore: {res.name}")
except Exception as e:
    print(f"Datastore creation status/error: {e}")

# 2. Import documents from GCS
doc_client = discoveryengine.DocumentServiceClient()
branch_parent = f"{parent}/dataStores/{data_store_id}/branches/0"

try:
    request = discoveryengine.ImportDocumentsRequest(
        parent=branch_parent,
        gcs_source=discoveryengine.GcsSource(
            input_uris=["gs://ninghai-bucket-0/ptp_demo/documents.jsonl"]
        ),
    )
    print("Importing documents from GCS...")
    op = doc_client.import_documents(request=request)
    res = op.result()
    print(f"Import completed: {res}")
except Exception as e:
    print(f"Import failed: {e}")

# 3. Create Search App (Engine)
engine_client = discoveryengine.EngineServiceClient()

try:
    # SolutionType and IndustryVertical might need to be referenced correctly
    # Let's try to use the enums if available, or raw ints/strings if not
    # Generic vertical is standard for search on unstructured data
    
    engine = discoveryengine.Engine(
        display_name="ptp_search_app",
        solution_type="SOLUTION_TYPE_SEARCH",
        industry_vertical="GENERIC",
        data_store_ids=[data_store_id]
    )
    print("Creating Search App...")
    op = engine_client.create_engine(parent=parent, engine=engine, engine_id=engine_id)
    res = op.result()
    print(f"Created Search App: {res.name}")
except Exception as e:
    print(f"Search App creation failed: {e}")
