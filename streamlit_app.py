import streamlit as st
import requests
import datetime

BASE_URL = "http://localhost:8000"  # FastAPI backend endpoint

# Page configuration
st.set_page_config(
    page_title="🌍 UNO-AI Travel Planner",
    page_icon="🌍",
    layout="wide"
)

# Custom CSS with the new image URL and updated bot message background color
st.markdown("""
<style>
.stApp {
    background-image: url('https://damoclesjournal.com/wp-content/uploads/2022/02/0x0.jpg');
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    color: #f5f5f5; /* Adjust text color for better contrast */
}
.chat-container {
    background-color: rgba(14, 17, 23, 0.8); /* Semi-transparent background for readability */
    border-radius: 10px;
    padding: 20px;
    max-height: 70vh;
    overflow-y: auto;
}
.user-msg {
    background-color: #1f77b4;
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
    max-width: 70%;
}
.bot-msg {
    background-color: #add8e6; /* Light Sky Blue */
    color: #0e1117; /* Dark text for contrast on light background */
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
    max-width: 70%;
}
.timestamp {
    font-size: 10px;
    color: gray;
}
.stTextInput>div>div>input {
    border-radius: 12px;
    padding: 12px;
    font-size: 16px;
}
h2 {
    color: #f5f5f5; /* Ensure title is visible on background */
}
</style>
""", unsafe_allow_html=True)

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title
st.markdown("## 🌍 UNO-AI TRAVEL PLANNER")

# Display chat messages
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["sender"] == "user":
        st.markdown(f'<div class="user-msg">{msg["text"]}<div class="timestamp">{msg["time"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-msg">{msg["text"]}<div class="timestamp">{msg["time"]}</div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Chat input form
with st.form(key="query_form", clear_on_submit=True):
    user_input = st.text_input("",
                                placeholder="✈️ e.g., Trip to Jaipur for 3 days with family",
                                key="user_input_text")
    submit_button = st.form_submit_button("Send")

if submit_button and st.session_state.user_input_text.strip():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_message = st.session_state.user_input_text.strip()

    # Add user message
    st.session_state.messages.append({"sender": "user", "text": user_message, "time": timestamp})

    try:
        # Bot response
        with st.spinner("Bot is thinking..."):
            payload = {"question": user_message}
            response = requests.post(f"{BASE_URL}/query", json=payload)

        if response.status_code == 200:
            answer = response.json().get("answer", "No answer returned.")
        else:
            answer = "Bot failed to respond: " + response.text

    except Exception as e:
        answer = f"Bot response failed: {e}"

    # Add bot message
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.messages.append({"sender": "bot", "text": answer, "time": timestamp})
    
    st.rerun()