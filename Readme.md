# Legal Assist-AI
This repository contains the code for a chatbot using `Langchain` and backed by `Meta-Llama-3-8B` by `Meta` using `Huggingface` and `Streamlit` for frontend UI.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)

# Legal-Assist-AI

Legal-Assist-AI is an AI-powered assistant designed to help users navigate and analyze legal documents, leveraging advanced language models and vector search for efficient information retrieval.

## Repository Structure

- `app.py` — Main application entry point.
- `embed.py` — Embedding logic for document processing.
- `langchain_utils.py` — Utilities for integrating with LangChain.
- `visualize.py` — Visualization tools for legal data.
- `requirements.txt` — Python dependencies.
- `Readme.md` — Project documentation.
- `LICENSE` — License information.
- `data_law/` — Collection of legal PDFs and resources.
- `embed_db/` — Vector database files (FAISS, pickle).

## Features

- Search and analyze legal documents.
- Visualize legal data and similarity scores.
- Integrate with LangChain for advanced NLP tasks.
- Modular codebase for easy extension.

## Getting Started

1. Clone the repository:
    ```powershell
    git clone https://github.com/thejatingupta7/Legal-Assist-AI.git
    ```
2. Install dependencies:
    ```powershell
    pip install -r requirements.txt
    ```
3. Run the application:
    ```powershell
    python app.py
    ```

## License

This project is licensed under the terms of the LICENSE file.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Installation
1. Clone the repository
```
git clone https://github.com/thejatingupta7/NyaysathiGPT
```
2. Create a virtual environment
```
python3 -m venv venv
```
3. Activate the virtual environment
```
source venv/bin/activate
```
4. Install the requirements
```
pip install -r requirements.txt
```

## Usage
1. Embedding Knowledge into the Chatbot.
    - Add your pdfs or docx files to the `data_law` folder.
    - Run the following command to ingest the knowledge into the chatbot.
    ```
    python embed.py
    ```
    - This will create a `embed_db/` folder which will contain the embeddings of PDFs i.e. the vectorized information.
2. Running the Chatbot.
    - Run the following command to start the chatbot.
    ```
    python app.py
    ```

