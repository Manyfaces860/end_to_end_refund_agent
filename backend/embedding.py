from setup import pc

def get_embedding(inputs, input_type="query"):
    # Convert the query into a dense vector
    dense_query_embedding = pc.inference.embed(
        model="llama-text-embed-v2",
        inputs=inputs,
        parameters={"input_type": input_type, "truncate": "END"}
    )

    # Convert the query into a sparse vector
    sparse_query_embedding = pc.inference.embed(
        model="pinecone-sparse-english-v0",
        inputs=inputs,
        parameters={"input_type": input_type, "truncate": "END"}
    )
    return dense_query_embedding, sparse_query_embedding