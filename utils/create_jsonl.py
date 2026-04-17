import json

files = [
    "gs://ninghai-bucket-0/ptp_demo/Energy Wheel.pdf",
    "gs://ninghai-bucket-0/ptp_demo/P6_Schedules.pdf",
    "gs://ninghai-bucket-0/ptp_demo/safety_requirements/Construction Barriers, Barricades, and Tagging Usage CON-EHS-TSS-020.00.pdf",
    "gs://ninghai-bucket-0/ptp_demo/safety_requirements/Construction Cutting Tool Use CON-EHS-TSS-008.00.pdf",
    "gs://ninghai-bucket-0/ptp_demo/safety_requirements/Construction Ladder Usage CON-EHS-TSS-012.00.pdf",
    "gs://ninghai-bucket-0/ptp_demo/safety_requirements/Contractor Safety Improvement Plan CON-EHS-TSS-019.00 (1).pdf",
    "gs://ninghai-bucket-0/ptp_demo/safety_requirements/Copy of Risk Assessment Program CON-EHS-TSS-015.00.pdf",
    "gs://ninghai-bucket-0/ptp_demo/safety_requirements/Crane and Rigging Usage CON-EHS-TSS-010.00.pdf",
    "gs://ninghai-bucket-0/ptp_demo/safety_requirements/Excavation and Trenching CON-EHS-TSS-005.00.pdf",
    "gs://ninghai-bucket-0/ptp_demo/safety_requirements/Permit To Work Systems CON-EHS-TSS-018.00.pdf",
    "gs://ninghai-bucket-0/ptp_demo/safety_requirements/Risk Assessment Program CON-EHS-TSS-015.00.pdf"
]

with open("scratch/documents.jsonl", "w") as f:
    for uri in files:
        filename = uri.split("/")[-1]
        doc_id = filename.replace(" ", "_").replace(".", "_").replace(",", "").replace("(", "").replace(")", "").lower()
        # Ensure ID contains only valid characters (a-z, 0-9, -, _)
        doc_id = "".join([c if c.isalnum() or c in ["-", "_"] else "_" for c in doc_id])
        category = "safety-requirements" if "safety_requirements" in uri else filename.split(".")[0].replace(" ", "-").lower()
        doc = {
            "id": doc_id,
            "content": {"mimeType": "application/pdf", "uri": uri},
            "structData": {"title": filename, "fileName": filename, "category": category}
        }
        f.write(json.dumps(doc) + "\n")

print("Created scratch/documents.jsonl")
