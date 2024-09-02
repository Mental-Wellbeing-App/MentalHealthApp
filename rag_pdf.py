import streamlit as st
import PyPDF2
import os
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai
import random

# Initialize Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize Gemini API (replace with your actual API key)
genai.configure(api_key='YOUR_GEMINI_API_KEY')
model_gemini = genai.GenerativeModel('gemini-pro')

# Function to extract text from PDF
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to process uploaded PDFs
def process_pdfs(uploaded_files):
    all_text = []
    for file in uploaded_files:
        text = extract_text_from_pdf(file)
        all_text.append(text)
    return all_text

# Function to get embeddings for documents
def get_embeddings(documents):
    return model.encode(documents)

# Streamlit app
st.title("🌟 Cheerful Mental Health Buddy 🌈")

# Sidebar for PDF uploads
with st.sidebar:
    st.header("📚 Upload Mental Health Resources")
    uploaded_files = st.file_uploader("Choose PDF files", accept_multiple_files=True, type="pdf")
    
    if uploaded_files:
        documents = process_pdfs(uploaded_files)
        document_embeddings = get_embeddings(documents)
        st.session_state['documents'] = documents
        st.session_state['document_embeddings'] = document_embeddings
        st.success(f"Yay! Processed {len(documents)} documents. 🎉")

# Main chat interface
greeting_messages = [
    "Hello there! I'm your friendly Mental Health Buddy. How can I brighten your day? 😊",
    "Welcome! I'm here to chat and support you. What's on your mind today? 🌟",
    "Hi friend! It's great to see you. How about we start with something positive? 🌈",
    "Greetings! I'm your cheerful chat companion. Ready for an uplifting conversation? 🌞"
]

if 'greeted' not in st.session_state:
    st.session_state['greeted'] = False

if not st.session_state['greeted']:
    st.write(random.choice(greeting_messages))
    st.session_state['greeted'] = True

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Display chat history
for message in st.session_state['messages']:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Your message"):
    # Add user message to chat history
    st.session_state['messages'].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    if 'documents' in st.session_state and st.session_state['documents']:
        # Encode query
        query_embedding = model.encode([prompt])[0]

        # Calculate similarities
        similarities = cosine_similarity([query_embedding], st.session_state['document_embeddings'])[0]

        # Get the most similar document
        most_similar_idx = np.argmax(similarities)
        most_similar_doc = st.session_state['documents'][most_similar_idx]

        # Generate response using Gemini
        context = f"""You are a cheerful and supportive mental health chatbot named Cheerful Mental Health Buddy. 
        Use the following context to answer the user's question. If the context doesn't contain relevant information, 
        use your general knowledge about mental health to provide a helpful and supportive response. 
        Always maintain a compassionate, professional, and upbeat tone. Start your responses with a brief 
        positive affirmation or encouragement when appropriate. Remember to use emojis occasionally to add warmth to your messages.

        Context: {most_similar_doc[:2000]}"""
        
        response = model_gemini.generate_content(
            contents=[
                {"role": "user", "parts": [{"text": context}]},
                {"role": "user", "parts": [{"text": prompt}]}
            ]
        )
        assistant_response = response.text
    else:
        assistant_response = "I'm excited to chat with you! 😊 However, I don't have any mental health information loaded yet. Could you please upload some PDFs using the sidebar? That way, I can provide even better support!"

    # Add assistant response to chat history
    st.session_state['messages'].append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

# Clear chat history button
if st.button("Start Fresh 🌱"):
    st.session_state['messages'] = []
    st.session_state['greeted'] = False
    st.success("Chat history cleared. Let's start anew with positivity! 🌟")

# Motivational message
st.markdown("---")
motivational_messages = [
    "Remember, every step forward is progress. You're doing great! 🌟",
    "Your mental health matters. Be kind to yourself today. 🌸",
    "You have the strength within you to overcome any challenge. Believe in yourself! 💪",
    "Taking care of your mind is a beautiful act of self-love. Keep it up! 💖"
]
st.markdown(f"*{random.choice(motivational_messages)}*")