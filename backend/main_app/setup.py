import asyncio
import pymilvus
from pymilvus import utility, connections, MilvusClient
print(f"Pymilvus: {pymilvus.__version__}", flush=True)


retries = 0
while True:
    try:
        connection = connections.connect(
            alias="default", 
            host='34.209.51.63', 
            port='19530'
        )
        print(f"Milvus server started: {utility.get_server_version()}", flush=True)
        break
    except Exception as e:
        print(f"Connection failed. Retrying... {e}", flush=True)
        asyncio.sleep(1)  # Properly await the sleep coroutine
        retries += 1
        if retries == 3:
            print("Max retries reached. Exiting...", flush=True)
            break
    

milvus_client = MilvusClient(
    uri="http://34.209.51.63:19530"
)
