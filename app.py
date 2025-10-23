import streamlit as st
from chatbot_backend import GeminiChatbot  # Import the backend class

# --- Page Configuration ---
st.set_page_config(
    page_title="🤖 Gemini Chatbot",
    page_icon="🤖",
    layout="centered"
)

# --- Title and Description ---
st.title("🤖 My AI Chatbot")
st.markdown("Welcome! This chatbot uses the Gemini API. To use it, please provide your API key below.")
st.markdown("Get your API key from: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)")

# --- API Key Management ---
# Try to get the API key from Streamlit secrets first
try:
    # This is the recommended way to store secrets in Streamlit
    api_key = st.secrets["GEMINI_API_KEY"]
except (KeyError, FileNotFoundError):
    api_key = None

# If not in secrets, ask the user (less secure, but good for local dev)
if not api_key:
    st.warning("For better security, add your API key to Streamlit's secrets (`.streamlit/secrets.toml`).")
    api_key = st.text_input("Enter your Gemini API key:", type="password", key="api_key_input")

if not api_key:
    st.error("Please provide your Gemini API key to continue.")
    st.stop()

# --- Chatbot Initialization ---
# Initialize the chatbot class
try:
    chatbot = GeminiChatbot(api_key=api_key)
except Exception as e:
    st.error(f"Failed to initialize chatbot: {e}")
    st.stop()

# --- Chat History Management ---
# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [
        # Start with a greeting from the bot
        {"role": "model", "parts": [{"text": "Hello! How can I help you today?"}]}
    ]

# --- Display Chat History ---
# Loop through the existing messages and display them
for message in st.session_state.messages:
    # Use "assistant" for "model" role for st.chat_message
    role = "assistant" if message["role"] == "model" else message["role"]
    with st.chat_message(role):
        st.markdown(message["parts"][0]["text"])

# --- User Input and Response ---
# Get user input from the chat input box
if prompt := st.chat_input("What would you like to ask?"):
    
    # 1. Add user's message to history and display it
    st.session_state.messages.append({"role": "user", "parts": [{"text": prompt}]})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 2. Get bot's response
    with st.chat_message("assistant"):
        # Show a spinner while processing
        with st.spinner("Thinking..."):
            # The backend expects the full chat history
            response_text = chatbot.send_message(st.session_state.messages)
            
            # Display the response
            st.markdown(response_text)
            
    # 3. Add bot's response to history
    st.session_state.messages.append({"role": "model", "parts": [{"text": response_text}]})
