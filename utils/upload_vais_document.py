import os
from google.cloud import discoveryengine

project_id = "ninghai-ccai"
location = "global"
data_store_id = "ptp-demo-store"

client = discoveryengine.DocumentServiceClient()
parent = f"projects/{project_id}/locations/{location}/collections/default_collection/dataStores/{data_store_id}/branches/0"

pdf_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "docs", "Energy Wheel.pdf"))

try:
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    doc = discoveryengine.Document(
        id="energy-wheel-document",
        struct_data={
            "title": "Energy Wheel Risk Assessment PDF",
            "document_type": "safety_guideline"
        },
        content=discoveryengine.Document.Content(
            mime_type="application/pdf",
            raw_bytes=pdf_bytes
        )
    )
    
    req = discoveryengine.CreateDocumentRequest(
        parent=parent,
        document=doc,
        document_id="energy-wheel-document"
    )
    
    print(f"Directly creating document via DocumentServiceClient in {parent}...")
    try:
        client.delete_document(name=f"{parent}/documents/energy-wheel-document")
    except Exception:
        pass
        
    res = client.create_document(request=req)
    print(f"Import completed successfully! Uploaded Resource: {res.id}")
except Exception as e:
    print(f"Import failed: {e}")
