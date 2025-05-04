import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embeddings_model = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory="chroma_db", embedding_function = embeddings_model)


class DocumentHandler(FileSystemEventHandler):
    
    def on_created(self, event):
        """
        Triggered when a new file is added to the watched directory.
        Processes the document if it is a .txt or .pdf.

        Args:
            event (FileSystemEvent): Event object containing file path and type.
        """
        if event.is_directory:
            return 
        
        ext = os.path.splitext(event.src_path)[-1].lower()

        if ext in [".txt", ".pdf"]:
            print(f"🆕 New file detected: {event.src_path}")
            self.process(event.src_path, ext)


    def process(self, file_path, ext):
        """
        Process a document and store its chunks in ChromaDB.

        Args:
            file_path (str): Path to the file.
            ext (str): File extension (e.g., '.txt', '.pdf').

        Returns:
            None
        """
        if ext == ".txt":
            loader  = TextLoader(file_path)
        elif ext == ".pdf":
            loader  = PyPDFLoader(file_path)
        else:
            print(f"Unsupport file type: {file_path}")
            return 

        try:
            ## Document to load
            docs = loader.load()
            ## Splits document into 500 char chunks
            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
            chunks = splitter.split_documents(docs)
            ## Stores it in ChromaDB as a vector embedding
            vectorstore.add_documents(chunks)
            print(f"✅ Indexed and stored: {file_path}")
        except Exception as e:
            print(f"⚠️ Error processing {file_path}: {e}")


if __name__ == "__main__":
    ## Creates a directory named "documents" to actively listen to any new files added
    path = "documents"
    os.makedirs(path, exist_ok=True)

    ## Starts listening to changes in "documents" directory
    event_handler = DocumentHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    print(f"👀 Watching folder: {path}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()