from constants import *
from logger import logger, logging
from setup import pc
import json
from chunker import split_markdown_and_prepare_chunks
from pinecone import ServerlessSpec

from embedding import get_embedding

def upsert_to_pinecone(index, records, namespace=NAMESPACE, batch_size=10):
    """
    Upserts records to Pinecone with a progress bar and batching.
    """
    # Calculate total batches for tqdm
    total_batches = (len(records) + batch_size - 1) // batch_size

    dense_embeddings, sparse_embeddings = get_embedding([d['content'] for d in records], "passage")
    
    records_to_upsert = []
    for d, de, se in zip(records, dense_embeddings, sparse_embeddings):
        records_to_upsert.append({
            "id": d['_id'],
            "values": de['values'],
            "sparse_values": {'indices': se['sparse_indices'], 'values': se['sparse_values']},
            "metadata": {'text': d['content']}
        })
    
    logger.log(level=logging.INFO, msg=f"Starting upsert: {len(records)} records in {total_batches} batches.")

    # Upsert the batch
    index.upsert(
        vectors=records_to_upsert, 
        namespace=namespace,
        batch_size=batch_size,
        show_progress=True
    )

if not pc.has_index(INDEX_NAME):
    logger.log(level=logging.INFO, msg=f"creating index: {INDEX_NAME}")
    
    try: 
        pc.create_index(
            name=INDEX_NAME,
            vector_type="dense",
            dimension=VECTOR_DIMENSION,
            metric="dotproduct",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
        )
    )
    except Exception as e:
        logger.log(level=logging.ERROR, msg=f"failed to create index, error: {e}")
        
if pc.has_index(INDEX_NAME):
    logger.log(level=logging.INFO, msg=f"index {INDEX_NAME} already exists, checking if upsert is needed")
    
    # Target the index
    try:
        dense_index = pc.Index(name=INDEX_NAME)

        count = 0
        for page in dense_index.list(namespace=NAMESPACE):
            for item in page.vectors:
                count += 1
        if count == 0:
            logger.log(level=logging.INFO, msg="splitting markdown and preparing chunks")
            records = split_markdown_and_prepare_chunks()
            
            # 6. Preview the result
            logger.log(level=logging.INFO, msg=f"Successfully created {len(records)} context-aware chunks.")
            logger.log(level=logging.INFO, msg="\n--- Example Chunk Metadata ---")
            logger.log(level=logging.INFO, msg=json.dumps(records[5]["metadata"], indent=2))
            logger.log(level=logging.INFO, msg="\n--- Example Chunk Content ---")
            logger.log(level=logging.INFO, msg=records[5]["content"])
            upsert_to_pinecone(dense_index, records, batch_size=10)
        else:
            logger.log(level=logging.INFO, msg=f"index {INDEX_NAME} already has {count} records, skipping upsert")
    
    except Exception as e:
        logger.log(level=logging.ERROR, msg=f"failed to upsert records, error: {e}")
        
