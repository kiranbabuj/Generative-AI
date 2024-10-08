# streamlit_app.py
import streamlit as st
import getpass
import os
from llama_index.llms.openai import OpenAI
from llama_index.core.llms import ChatMessage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader

# Streamlit UI for OpenAI API key input
st.title("Virtual Customer")

# Input API Key
api_key = st.text_input("Enter your OpenAI API key", type="password")

if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
    st.success("API Key set successfully.")

    # Choose the LLM model
    model_choice = st.selectbox("Select an LLM model", ["gpt-3.5-turbo", "gpt-4o-mini"])

    # Initialize the LLM
    st.write("Initializing LLM model...")
    llm = OpenAI(model=model_choice)

    # Query interaction using LLM
    st.write("Chat with the LLM")
    user_input = st.text_input("Ask your question:")

    if user_input:
        messages = [
            ChatMessage(role="system", content="You are a virtual customer designed to help upskill and train bank employees. Your role is to provide realistic banking scenarios, respond as a customer would, and evaluate the employees based on their responses. Some times you are angry, short tempered & in a hurry"),
            ChatMessage(role="user", content=user_input),
        ]
        response = llm.chat(messages)
        st.write(f"LLM Response: {response}")

    # Embeddings section
    st.write("## Embeddings Section")
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    Settings.llm = OpenAI(model="gpt-4o-mini", max_tokens=300)

    # Document loading and querying
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        # Save the uploaded PDF locally
        with open("uploaded_file.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Load documents and create an index
        documents = SimpleDirectoryReader("./").load_data()
        index = VectorStoreIndex.from_documents(documents)

        # Query engine
        query = st.text_input(" Good morning! Welcome to Canara Bank. How can I assist you today?:")
        if query:
            query_engine = index.as_query_engine()
            response = query_engine.query(query)
            st.write(f"Document Response: {response}")
else:
    st.warning("Please enter your OpenAI API key to continue.")
