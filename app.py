import streamlit as st
import traceback

from ollama import chat
from langchain_utils import (
    load_embedding_model,
    load_vector_store,
    perform_ocr,
)
from langchain_core.prompts import PromptTemplate

# --- RAG Setup ---
embedding_model = load_embedding_model("all-MiniLM-L6-v2")
retriever = load_vector_store("vectorstore", embedding_model)

rag_prompt_template = PromptTemplate(
    template="""
            You are a Legal Assist AI, a legal expert in Indian Law and Jurisdiction. You are a Legal Assist AI, a legal expert in Indian Law and Jurisdiction. 
            If the question is not legal, respond that you only assist with legal queries.
            
            Use the following retrieved context documents to answer the question. If the context is not relevant, reason and answer using your own knowledge too.
            
            Context:
            {context}
            
            Question:
            {question}
            
            Legal Document uploaded by user (if any):
            {legal_doc_section}
            Answer:
            """,
    input_variables=["context", "question", "legal_doc_section"]
)

# --- Streamlit + Streaming RAG Logic ---
def get_rag_response_stream(query, legal_doc_text=""):
    try:
        # Step 1: Combine query + OCR text for richer retrieval
        if legal_doc_text.strip():
            combined_query = f"{query}\n\n{legal_doc_text}"
        else:
            combined_query = query

        # Step 2: Retrieve documents using combined query
        docs = retriever.get_relevant_documents(combined_query)
        context = "\n\n".join([doc.page_content for doc in docs]) or "No relevant documents found."

        # Step 3: Build optional legal document section for prompt
        if legal_doc_text.strip():
            legal_doc_section = f"Legal Document attached:\n{legal_doc_text}"
        else:
            legal_doc_section = ""

        # Step 4: Format prompt with context
        formatted_prompt = rag_prompt_template.format(
            context=context,
            question=query,
            legal_doc_section=legal_doc_section,
        )

        # Step 5: Stream from model
        stream = chat(
            model='llama3.1:8b',
            messages=[{'role': 'user', 'content': formatted_prompt}],
            stream=True,
        )
        for chunk in stream:
            content = chunk['message']['content']
            yield content

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.error(traceback.format_exc())
        yield "[Error generating response]"

# --- Page setup and styling ---
def configure_page():
    st.set_page_config(page_title="Legal Assist AI", page_icon="⚖️", layout="wide")

def add_custom_css():
    st.markdown("""
    <style>
    .stButton button {
        width: 220px;
        height: 60px;
        font-size: 16px;
        border-radius: 10px;
        background-color: #1E1E2F;
        color: white;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #2C2C3A;
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- Main App ---
def main():
    configure_page()
    add_custom_css()
    st.title("Legal Assist AI ⚖️📜")
    st.subheader("Your AI Assistant for Indian Legal Queries")

    if 'history' not in st.session_state:
        st.session_state['history'] = []

    # Predefined legal questions
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Property Disputes"):
            st.session_state['user_query'] = "What are common legal remedies for property disputes in India?"
    with col2:
        if st.button("Marriage & Divorce Laws"):
            st.session_state['user_query'] = "What is the legal process for divorce under Hindu Marriage Act?"
    with col3:
        if st.button("Contract Enforcement"):
            st.session_state['user_query'] = "How are contracts legally enforced in India?"
    with col4:
        if st.button("Consumer Rights"):
            st.session_state['user_query'] = "What rights does a consumer have under the Consumer Protection Act?"

    # --- Query input + document upload side by side ---
    input_col, upload_col = st.columns([3, 1])
    with input_col:
        user_query = st.text_input(
            "Enter your Legal Query:",
            value=st.session_state.get('user_query', "")
        )
    with upload_col:
        uploaded_file = st.file_uploader(
            "Attach Legal Document (optional)",
            type=["png", "jpg", "jpeg", "tiff", "bmp", "gif", "webp", "pdf"],
            label_visibility="visible",
        )

    # --- OCR processing ---
    ocr_text = ""
    if uploaded_file is not None:
        with st.spinner("Processing document... extracting text via OCR, please wait."):
            try:
                ocr_text = perform_ocr(uploaded_file)
                st.success(f"Document processed successfully ({len(ocr_text)} characters extracted).")
                with st.expander("Preview extracted text"):
                    st.text(ocr_text[:2000] + ("..." if len(ocr_text) > 2000 else ""))
            except Exception as ocr_err:
                st.error(f"OCR failed: {ocr_err}")

    if user_query:
        st.session_state['history'].append({"user": user_query, "response": ""})
        response_container = st.empty()
        full_response = ""
        with st.spinner("Retrieving legal context and generating response..."):
            for chunk in get_rag_response_stream(user_query, legal_doc_text=ocr_text):
                full_response += chunk
                response_container.markdown(f"**Response:** {full_response}▌")
        st.session_state['history'][-1]["response"] = full_response

    # Sidebar history
    with st.sidebar:
        st.header("Conversation History")
        for entry in reversed(st.session_state['history'][-5:]):
            st.markdown(f"*Q:* {entry['user']}")
            st.markdown(f"*A:* {entry['response']}")
            st.markdown("---")

if __name__ == "__main__":
    main()
