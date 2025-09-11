# Import necessary modules from LangChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Path to PDF documents
DATASET = "data_law/"

# Path to save the FAISS index
FAISS_INDEX = "embed_db/"                # folder containing embeddings (vectorised information)

# Function to embed all files in the dataset directory
def embed_all():

    # Initialize the document loader to load PDFs from the directory
    loader = DirectoryLoader(DATASET, glob="*.pdf", loader_cls=PyPDFLoader)
    print("Loader ready-----------------------------------------------------------------")
    
    # Load the PDF documents
    documents = loader.load()
    print("Loaded-----------------------------------------------------------------------")

    # Initialize the text splitter to create chunks of the documents
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200)
    print("Splitter ready---------------------------------------------------------------")

    # Split the documents into chunks
    chunks = splitter.split_documents(documents)
    print("Splitted---------------------------------------------------------------------")

    # Initialize the embeddings generator
    embeddings = HuggingFaceEmbeddings()
    print("embedding ready--------------------------------------------------------------")
    
    # Create the vector store using FAISS with the document chunks and their embeddings
    vector_store = FAISS.from_documents(chunks, embeddings)
    print("embed done-------------------------------------------------------------------")

    # Save the vector store locally
    vector_store.save_local(FAISS_INDEX)
    print("==================================Saved======================================")

# Execute the embedding function if the script is run directly
if __name__ == "__main__":
    embed_all()