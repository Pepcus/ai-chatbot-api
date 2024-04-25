from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

load_dotenv()

def delete_file_from_local(file_name):
    try:
        local_file_path = os.environ['LOCAL_DOWNLOAD_PATH'] + file_name
        os.remove(local_file_path)
        print(f"Local file {local_file_path} deleted successfully")
    except OSError as e:
        print(f"Error deleting local file: {e}")

## Read the document
def read_doc(directory):
    file_loader=PyPDFDirectoryLoader(directory)
    documents=file_loader.load()
    return documents

## Divide the docs into chunks
### https://api.python.langchain.com/en/latest/text_splitter/langchain.text_splitter.RecursiveCharacterTextSplitter.html#
def chunk_data(docs,chunk_size=800,chunk_overlap=50):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)
    doc=text_splitter.split_documents(docs)
    return docs