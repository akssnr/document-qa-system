# Importing Libraries
import streamlit as st
import os
import pandas as pd
from rich import print
import warnings
warnings.filterwarnings("ignore")

# Initialize LangChain components
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter


# Initialize Streamlit app title
st.title("Document QA System with Vector Store and Chat Interface")

# Initialize OpenAI API key from environment variable
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    st.error("Please set the OPENAI_API_KEY environment variable.")
else:
    # Initialize the OpenAI model
    llm = ChatOpenAI(model = "gpt-4o-mini", openai_api_key = openai_api_key)

    # Initialize the embedding model
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small", chunk_size = 1000)

    # Function to load and split PDF documents
    def load_pdf_documents(file):
        pdf_loader = PyPDFLoader(file)
        pdf_pages = pdf_loader.load_and_split()
        return pdf_pages

    # Function to split documents into chunks
    def split_documents(pages):
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.split_documents(pages)
        # texts = [d.page_content for d in docs]
        return docs

    # Function to create vector store from documents
    def create_vector_store(docs, embeddings):
        db = FAISS.from_documents(docs, embeddings)
        return db

    # Main Streamlit app code
    st.header("Upload and Process Documents")

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    if uploaded_file:
        # Process PDF documents
        with st.spinner("Loading, splitting document, and creating vector database..."):
            if st.button("Load PDF Documents"):
                try:
                    # Read the file content
                    file_content = uploaded_file.read()
                    
                    # Save the file content to a temporary file
                    with open("temp.pdf", "wb") as temp_file:
                        temp_file.write(file_content)
                    
                    # Load and split the PDF document
                    pdf_pages = load_pdf_documents("temp.pdf")
                    docs = split_documents(pdf_pages)
                    db = create_vector_store(docs, embedding_model)
                    db.save_local("PDF_Vector_Database")
                    st.success("PDF documents loaded and vector store created.")
                except Exception as e:
                    st.error(f"Error processing PDF: {e}")

    # QA System Section
    st.header("Question and Answer Response")

    question = st.text_input("Enter your question:")
    if st.button("Get Answer"):
        with st.spinner("Retrieving the answer..."):
            try:
                new_db = FAISS.load_local("PDF_Vector_Database", embedding_model, allow_dangerous_deserialization=True)
                retriever = new_db.as_retriever()
                system_prompt = (
                "You are an assistant for question answering tasks. "
                "Fetch the relevant context from the provided document and answer the best you can only from the document provided"
                "If the context does not provide enough information, say you don't know. "
                "Provide a concise answer based on the context. "
                "Context: {context}"
                )
                prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", system_prompt),
                    ("human", "{input}"),
                ]
                )
                qa_chain = create_stuff_documents_chain(llm, prompt)
                chain = create_retrieval_chain(retriever, qa_chain)
                result = chain.invoke({"input": question})
                st.write("**Answer:**", result["answer"])
                # st.write(result)
            except Exception as e:
                st.error(f"Error retrieving answer: {e}")
