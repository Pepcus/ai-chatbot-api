from llama_index.core import ServiceContext, VectorStoreIndex, StorageContext
from llama_index.core.indices.postprocessor import MetadataReplacementPostProcessor
from llama_index.core.indices.postprocessor import SentenceTransformerRerank
from pinecone import ServerlessSpec
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine

def build_direct_query_index(
    pc,document, llm, embed_model, index_name
):
    
    pc.create_index(
        index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    pinecone_index = pc.Index(index_name)
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    service_context = ServiceContext.from_defaults(
        llm=llm, embed_model=embed_model
    )
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents([document],
                                        service_context=service_context, storage_context=storage_context)
    return index


def get_direct_query_engine(
    pc,     
    index_name,
    similarity_top_k=6,
    rerank_top_n=2,
):
    # define postprocessors
    postproc = MetadataReplacementPostProcessor(target_metadata_key="window")
    rerank = SentenceTransformerRerank(
        top_n=rerank_top_n, model="BAAI/bge-reranker-base"
    )

    pinecone_index = pc.Index(index_name)
    print(pinecone_index.describe_index_stats())
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    vector_index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    retriever = VectorIndexRetriever(index=vector_index, similarity_top_k=5, node_postprocessors=[postproc, rerank])
    query_engine = RetrieverQueryEngine(retriever=retriever)
    return query_engine