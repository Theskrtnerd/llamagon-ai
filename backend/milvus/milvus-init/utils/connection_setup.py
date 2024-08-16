import asyncio
import pymilvus
from pymilvus import (
    MilvusClient, utility, connections,
)
print(f"Pymilvus: {pymilvus.__version__}")


# Connect to the local server
while True:
    try:
        connection = connections.connect(
            alias="default", 
            host='localhost', # or '0.0.0.0' or 'localhost'
            port='19530'
        )
        # Get server version.
        print(f"Milvus: {utility.get_server_version()}")
        # Check the collection using MilvusClient.
        mc = MilvusClient(connections=connection)
        break
    except:
        print("Connection failed. Retrying...")
        asyncio.sleep(1)
        continue
