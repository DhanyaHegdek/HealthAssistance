def retrieve(query, top_k=3):
    # No Pinecone? No stress.
    # Return simple fallback context.
    return [{"text": "Breathing exercises can reduce stress."}]
