import streamlit as st
import streamlit.components.v1 as components
import os
import requests
import datetime
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="🌍 BREVO - Smart Travel Planner",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to hide Streamlit elements and make it full-screen
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {
        padding: 0;
        margin: 0;
    }
    .main .block-container {
        padding: 0;
        margin: 0;
        max-width: 100%;
    }
    .stButton > button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Function to read HTML file
def read_html_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return f"<h1>Error: {file_path} not found</h1>"

# Function to serve static files
def serve_static_file(file_path, mime_type):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return ""

# Main app
def main():
    # Check if HTML file exists
    html_file_path = "templates/index.html"
    css_file_path = "static/styles.css"
    js_file_path = "static/script.js"
    
    if not os.path.exists(html_file_path):
        st.error("HTML file not found. Please ensure the templates/index.html file exists.")
        return
    
    # Create tabs for different interfaces
    tab1, tab2 = st.tabs(["🌐 Web Interface", "💬 Streamlit Chat"])
    
    with tab1:
        st.markdown("## 🌍 BREVO - Smart Travel Planner")
        st.markdown("Experience our beautiful web interface below:")
        
        # Read and display HTML content
        html_content = read_html_file(html_file_path)
        
        # Create a container for the HTML
        st.markdown("---")
        
        # Display the HTML interface
        components.html(
            html_content,
            height=800,
            scrolling=True
        )
        
        # Add download links for the files
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📥 Download HTML"):
                st.download_button(
                    label="Download HTML File",
                    data=html_content,
                    file_name="index.html",
                    mime="text/html"
                )
        
        with col2:
            if st.button("📥 Download CSS"):
                css_content = serve_static_file(css_file_path, "text/css")
                st.download_button(
                    label="Download CSS File",
                    data=css_content,
                    file_name="styles.css",
                    mime="text/css"
                )
        
        with col3:
            if st.button("📥 Download JavaScript"):
                js_content = serve_static_file(js_file_path, "application/javascript")
                st.download_button(
                    label="Download JavaScript File",
                    data=js_content,
                    file_name="script.js",
                    mime="application/javascript"
                )
    
    with tab2:
        st.markdown("## 💬 AI Travel Assistant Chat")
        st.markdown("Chat with our AI assistant for travel planning:")
        
        # Initialize session state for messages
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat messages
        for msg in st.session_state.messages:
            with st.chat_message(msg["sender"]):
                st.write(msg["text"])
                st.caption(msg["time"])
        
        # Chat input
        if prompt := st.chat_input("Ask me about travel planning..."):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Add user message
            st.session_state.messages.append({"sender": "user", "text": prompt, "time": timestamp})
            with st.chat_message("user"):
                st.write(prompt)
                st.caption(timestamp)
            
            # Simulate AI response (you can integrate with your actual backend here)
            with st.chat_message("assistant"):
                with st.spinner("AI is thinking..."):
                    # Here you can integrate with your actual AI backend
                    ai_response = generate_ai_response(prompt)
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    st.session_state.messages.append({"sender": "assistant", "text": ai_response, "time": timestamp})
                    st.write(ai_response)
                    st.caption(timestamp)

def generate_ai_response(user_message):
    """Generate AI response based on user message"""
    # This is a simple response generator - you can replace this with your actual AI backend
    responses = {
        'paris': "Paris is a beautiful city! Here are some recommendations:\n\n• Best time to visit: April-June or September-October\n• Must-see attractions: Eiffel Tower, Louvre Museum, Notre-Dame Cathedral\n• Budget: $150-300 per day for mid-range travel\n• Weather: Check current conditions before booking",
        'budget': "I can help you plan your travel budget! Here's what to consider:\n\n• Transportation (flights, local transport)\n• Accommodation (hotels, hostels, vacation rentals)\n• Food and dining\n• Activities and attractions\n• Emergency fund\n\nWhat type of trip are you planning?",
        'weather': "I can help you check weather conditions for your destination! Just let me know:\n\n• City and country\n• Travel dates\n• What activities you're planning\n\nThis will help me give you the most relevant weather information.",
        'japan': "Japan is amazing! Here are the best times to visit:\n\n• Spring (March-May): Cherry blossoms, mild weather\n• Summer (June-August): Festivals, but hot and humid\n• Fall (September-November): Beautiful autumn colors\n• Winter (December-February): Snow, hot springs, skiing\n\nWhat interests you most about Japan?"
    }
    
    user_message_lower = user_message.lower()
    
    for keyword, response in responses.items():
        if keyword in user_message_lower:
            return response
    
    # Default response
    return "I'd love to help you plan your trip! I can assist with:\n\n• Destination recommendations\n• Budget planning\n• Weather information\n• Travel tips and advice\n\nWhat specific aspect of travel planning would you like help with?"

if __name__ == "__main__":
    main()

