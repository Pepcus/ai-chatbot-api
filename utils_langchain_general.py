from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from app_config import local_download_path
import os

def delete_file_from_local(file_name):
    try:
        local_file_path = local_download_path + file_name
        os.remove(local_file_path)
        print(f"Local file {local_file_path} deleted successfully")
    except OSError as e:
        print(f"Error deleting local file: {e}")

## Load the document
def load_doc(directory):
    #Loading the text file data
    loader = DirectoryLoader(directory, glob="./*.txt")
    documents = loader.load()
    return documents

## Divide the docs into chunks
### https://api.python.langchain.com/en/latest/text_splitter/langchain.text_splitter.RecursiveCharacterTextSplitter.html#
def chunk_data(docs,chunk_size=1500,chunk_overlap=200):
    text_splitter = CharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap, length_function=len)
    doc=text_splitter.split_documents(docs)
    return doc