import asyncio
import pymilvus
from pymilvus import utility, connections
print(f"Pymilvus: {pymilvus.__version__}", flush=True)

async def wait_for_milvus():
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
            await asyncio.sleep(1)  # Properly await the sleep coroutine

# Run the wait_for_milvus function
asyncio.run(wait_for_milvus())
