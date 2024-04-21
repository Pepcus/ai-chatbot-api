from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.retrievers import VectorIndexRetriever
from pinecone import ServerlessSpec
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core.ingestion import IngestionPipeline
import nest_asyncio

load_dotenv()
nest_asyncio.apply()

def build_pinecone_index(
    pc,    
    documents,
    index_name,
    embed_model
):
    pc.create_index(
        index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    pinecone_index = pc.Index(index_name)
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    pipeline = IngestionPipeline(
    transformations=[
        SemanticSplitterNodeParser(
            buffer_size=1,
            breakpoint_percentile_threshold=95, 
            embed_model=embed_model,
            ),
        embed_model,
        ],
        vector_store=vector_store
    )
    pipeline.run(documents=documents)

def get_pinecone_query_engine(pc, index_name):
    try:
        automerging_index = pc.Index(index_name)
        print(automerging_index.describe_index_stats())
        vector_store = PineconeVectorStore(pinecone_index=automerging_index)
        vector_index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        retriever = VectorIndexRetriever(index=vector_index, similarity_top_k=5)
        query_engine = RetrieverQueryEngine(retriever=retriever)
    except Exception as re:
        print(re)
    return query_engine