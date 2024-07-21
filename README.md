# Document QA System with Vector Store and Chat Interface

This repository contains a Streamlit application that facilitates a Question and Answer (QA) system utilizing a vector store and a chat interface. The system processes PDF documents, converts them into embeddings, and enables querying these documents to retrieve relevant information. The application leverages OpenAI's GPT-4o-mini model for answering questions based on the document content.

## Features

- Upload PDF documents and convert them into embeddings
- Store and manage document embeddings using a vector store
- Query the document content via a chat interface
- Retrieve and display answers based on the provided context

## Requirements

- Python 3.8+
- Streamlit
- OpenAI API Key
- Additional Python packages listed in `requirements.txt`

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/akssnr/document-qa-system.git
    cd document-qa-system
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the environment variable:**
    ```sh
    export OPENAI_API_KEY="your-openai-api-key"  # On Windows, use `set OPENAI_API_KEY="your-openai-api-key"`
    ```

## Usage

1. **Run the Streamlit application:**
    ```sh
    streamlit run app.py
    ```

2. **Upload and process documents:**
    - Navigate to the "Upload and Process Documents" section in the app.
    - Upload a PDF file and click the "Load PDF Documents" button.
    - The system will load, split, and create a vector store from the document.

3. **Ask questions:**
    - Navigate to the "Question and Answer Response" section.
    - Enter a question related to the uploaded document and click the "Get Answer" button.
    - The system will retrieve and display the answer based on the document content.

## Code Explanation

### Importing Libraries
The necessary libraries for building the application are imported, including Streamlit for the web interface, and various LangChain and OpenAI components for text processing and querying.

### Streamlit App Initialization
The app title is set, and the OpenAI API key is retrieved from the environment variables.

### Loading and Splitting PDF Documents
Functions to load and split PDF documents into chunks are defined.

### Creating Vector Store
A function to create a vector store from document embeddings is defined.

### Main App Code
The main sections of the Streamlit app for uploading documents and retrieving answers are implemented.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with your suggestions or improvements.

## License

This project is licensed under the MIT License.
