import vertexai
from vertexai.preview import rag

def import_safety():
    vertexai.init(project="ninghai-ccai", location="us-east5")
    
    corpus_name = "projects/ninghai-ccai/locations/us-east5/ragCorpora/4611686018427387904"
    
    uris = [
        "gs://ninghai-bucket-0/ptp_demo/Energy Wheel.pdf",
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
    
    print(f"Importing files to {corpus_name}...")
    try:
        response = rag.import_files(
            corpus_name=corpus_name,
            paths=uris,
        )
        print(f"Import response: {response}")
    except Exception as e:
        print(f"Error importing files: {e}")

if __name__ == "__main__":
    import_safety()
