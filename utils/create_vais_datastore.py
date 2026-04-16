import os
from google.cloud import discoveryengine

project_id = "ninghai-ccai"
location = "global"
data_store_id = "ptp-demo-store"

client = discoveryengine.DataStoreServiceClient()
parent = f"projects/{project_id}/locations/{location}/collections/default_collection"

try:
    ds = discoveryengine.DataStore(
        display_name="ptp_demo_store",
        industry_vertical=discoveryengine.IndustryVertical.GENERIC,
        content_config=discoveryengine.DataStore.ContentConfig.CONTENT_REQUIRED
    )
    op = client.create_data_store(parent=parent, data_store=ds, data_store_id=data_store_id)
    print("Creating Datastore...")
    res = op.result()
    print(f"Created: {res.name}")
except Exception as e:
    print(f"Datastore info/status: {e}")
