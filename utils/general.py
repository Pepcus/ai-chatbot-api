from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config.config import local_download_path
from utils.logs import logger
import os

def delete_file_from_local(file_name):
    try:
        local_file_path = local_download_path + file_name
        os.remove(local_file_path)
        logger.info(f"Local file {local_file_path} deleted successfully")
    except OSError as e:
        logger.error(f"Error deleting local file: {e}")

## Load the document
def load_doc(directory):
    try:
        # Attempt to load the document
        loader = PyPDFLoader(directory)
        documents = loader.load()
        return documents
    except Exception as e:
        logger.error(f"An error occurred while loading the document: {e}")
        return None

## Divide the docs into chunks
### https://api.python.langchain.com/en/latest/text_splitter/langchain.text_splitter.RecursiveCharacterTextSplitter.html#
def chunk_data(docs, chunk_size=1500, chunk_overlap=200):
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len)
        doc = text_splitter.split_documents(docs)
        return doc
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None