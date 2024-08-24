from pymilvus import FieldSchema, CollectionSchema, DataType, Collection, utility
import connection_setup


# For the paper chunks
COLLECTION_NAME = "paper_chunks"
MAX_LENGTH = 65535
EMBEDDING_DIM = 1024
REF_MAX_CAPACITY = 5
fields = [
    # Use auto generated id as primary key
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True, max_length=10),
    FieldSchema(name="doc", dtype=DataType.VARCHAR, max_length=MAX_LENGTH),
    FieldSchema(name="sparse_vector", dtype=DataType.SPARSE_FLOAT_VECTOR),
    FieldSchema(name="dense_vector", dtype=DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM),
    FieldSchema(name="user_id", dtype=DataType.VARCHAR, max_length=100),
    FieldSchema(name="paper_doi", dtype=DataType.VARCHAR, max_length=MAX_LENGTH),
    FieldSchema(name="paper_arxiv_id", dtype=DataType.VARCHAR, max_length=MAX_LENGTH),
    FieldSchema(name="paper_title", dtype=DataType.VARCHAR, max_length=MAX_LENGTH),
]
schema = CollectionSchema(fields, "")


collection_existed = utility.has_collection(COLLECTION_NAME)
if collection_existed:
    print(f"Collection `{COLLECTION_NAME}` already exists. No collection created.", flush=True)
    # drop_result = utility.drop_collection(COLLECTION_NAME)
    # print(f"Successfully dropped collection: `{COLLECTION_NAME}`", flush=True)
else:
    schema = CollectionSchema(fields, "")
    col = Collection(COLLECTION_NAME, schema, consistency_level="Eventually")

    # Add custom HNSW search index to the collection. M = max number graph connections per layer. Large M = denser graph.
    # Choice of M: 4~64, larger M for larger data and larger embedding lengths.
    M = 16
    # efConstruction = num_candidate_nearest_neighbors per layer. Use Rule of thumb: int. 8~512, efConstruction = M * 2.
    efConstruction = M * 2
    # Create the search index for local Milvus server.
    INDEX_PARAMS = dict({
        'M': M,               
        "efConstruction": efConstruction })

    # Create indices for the vector fields. The indices will pre-load data into memory for efficient search.
    sparse_index = {"index_type": "SPARSE_INVERTED_INDEX", "metric_type": "IP"}
    dense_index = {"index_type": "HNSW", "metric_type": "COSINE", "params": INDEX_PARAMS}
    col.create_index("sparse_vector", sparse_index)
    col.create_index("dense_vector", dense_index)
    col.load()
    print(f"Successfully created collection: `{COLLECTION_NAME}`", flush=True)





# For the reference chunks
COLLECTION_NAME = "ref_chunks"
MAX_LENGTH = 65535
EMBEDDING_DIM = 1024
REF_MAX_CAPACITY = 5
fields = [
    # Use auto generated id as primary key
    FieldSchema(name="cite_id", dtype=DataType.VARCHAR, is_primary=True, max_length=10),
    FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=MAX_LENGTH),
    FieldSchema(name="url", dtype=DataType.VARCHAR, max_length=MAX_LENGTH),
    FieldSchema(name="abstract", dtype=DataType.VARCHAR, max_length=MAX_LENGTH),
    FieldSchema(name="abstract_dense_vector", dtype=DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM),
]
schema = CollectionSchema(fields, "")


collection_existed = utility.has_collection(COLLECTION_NAME)
if collection_existed:
    print(f"Collection `{COLLECTION_NAME}` already exists. No collection created.", flush=True)
    # drop_result = utility.drop_collection(COLLECTION_NAME)
    # print(f"Successfully dropped collection: `{COLLECTION_NAME}`", flush=True)
else:
    schema = CollectionSchema(fields, "")
    col = Collection(COLLECTION_NAME, schema, consistency_level="Eventually")
    
    M = 16
    efConstruction = M * 2
    INDEX_PARAMS = dict({
        'M': M,               
        "efConstruction": efConstruction })
    
    abstract_dense_index = {"index_type": "HNSW", "metric_type": "COSINE", "params": INDEX_PARAMS}
    col.create_index("abstract_dense_vector", abstract_dense_index)
    col.load()
    print(f"Successfully created collection: `{COLLECTION_NAME}`", flush=True)