import streamlit as st
from PyPDF2 import PdfReader
import random

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 Smart AI Chatbot (Offline)")

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "document_text" not in st.session_state:
    st.session_state.document_text = ""

# ---------------- PDF UPLOAD ----------------
uploaded_file = st.file_uploader("Upload a PDF (optional)", type=["pdf"])
if uploaded_file:
    pdf = PdfReader(uploaded_file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text() + "\n"
    st.session_state.document_text = text
    st.success("PDF loaded! Ask questions about it.")

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- CHAT INPUT ----------------
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message instantly
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append({"role": "user", "content": user_input})

    # Bot reply
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤖"):

            user = user_input.lower()

            # ---------------- RESPONSE LOGIC ----------------
            if "hello" in user or "hi" in user:
                reply = "Hey there! 😊 I'm your AI chatbot. Ask me anything!"

            elif "how are you" in user:
                reply = "I'm doing great! 😄"

            elif "your name" in user:
                reply = "I'm your AI chatbot 🤖 built using Streamlit!"

            elif "ai" in user:
                reply = "Artificial Intelligence is about machines that can learn and make decisions like humans."

            elif "python" in user:
                reply = "Python is a powerful programming language used for AI, web apps, and data science."

            elif "what can you do" in user:
                reply = "I can chat with you, answer questions, and even check your uploaded PDF!"

            elif "project" in user:
                reply = "This is an AI chatbot project built using Python and Streamlit. It supports interactive chat and optional PDF analysis."

            elif "bye" in user:
                reply = "Goodbye! 👋 Have a great day!"

            # ---------------- PDF CHECK ---------------
            elif st.session_state.document_text:
                sentences = st.session_state.document_text.split(".")
                best_match = ""

                for sentence in sentences:
                    if user in sentence.lower():
                        best_match = sentence
                        break

                if best_match:
                    reply = f"📄 Answer from your PDF:\n\n{best_match.strip()}."
                else:
                    reply = "❌ I couldn't find a clear answer in the PDF."

            # ---------------- FALLBACK ----------------
            else:
                responses = [
                    "Interesting question! 🤔",
                    "Tell me more about that!",
                    "That sounds cool 😄",
                    "I'm thinking about it...",
                    "Can you explain a bit more?"
                ]
                reply = random.choice(responses)

            # Save and display reply
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.markdown(reply)