from google.cloud import discoveryengine
client = discoveryengine.EngineServiceClient()
with open("scratch/output.txt", "w") as f:
    f.write(str([attr for attr in dir(client) if "create" in attr.lower()]))
