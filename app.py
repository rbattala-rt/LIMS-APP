import streamlit as st
import os
from groq import Groq

# Set page config
st.set_page_config(
    page_title=" LIMS Chat",
    page_icon="🤖",
    layout="centered"
)

# App title and description
st.title("🤖 LIMS Chat")
#st.markdown("Chat with powerful language models using Groq's fast inference API")

# Sidebar for API key and model selection
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter API Key", type="password")
    model = st.selectbox(
        "Select Model",
        ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768", "gemma-7b-it"]
    )
    
    #st.markdown("---")
    #st.markdown("### About")
    #st.markdown("""
    #This app uses Groq's API to access various large language models.
    #Groq provides fast inference for popular open models.
    #""")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("What's on your mind?")

# Process the user input
if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response with a spinner while loading
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        if not api_key:
            message_placeholder.error("Please enter your  API key in the sidebar.")
        else:
            try:
                with st.spinner("Thinking..."):
                    # Initialize Groq client
                    client = Groq(api_key=api_key)
                    
                    # Prepare chat completion request
                    response = client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": m["role"], "content": m["content"]} 
                            for m in st.session_state.messages
                        ],
                        temperature=0.7,
                        max_tokens=1024
                    )
                    
                    # Extract and display the response
                    assistant_response = response.choices[0].message.content
                    message_placeholder.markdown(assistant_response)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
            except Exception as e:
                message_placeholder.error(f"Error: {str(e)}")

# Add clear chat button
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()