import streamlit as st
import json
import os
from Chatbot import ChatBot   # Import your backend function

# ---------------------- Page Config ----------------------
st.set_page_config(
    page_title="AI Assistant | Professional Chat Interface",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------- Custom CSS ----------------------
st.markdown(
    """
    <style>
    :root {
        --primary: #2563eb;
        --primary-light: #dbeafe;
        --secondary: #475569;
        --background: #f8fafc;
        --surface: #ffffff;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --success: #10b981;
        --border: #e2e8f0;
    }
    
    body {
        background-color: var(--background);
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, var(--primary) 0%, #1d4ed8 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 0 0 12px 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    .chat-container {
        background-color: var(--surface);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        height: 10vh;
        overflow-y: auto;
        margin-bottom: 1.5rem;
        border: 1px solid var(--border);
    }
    
    .chat-bubble-user {
        background-color: var(--primary);
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 4px 18px;
        margin: 10px 0;
        max-width: 75%;
        margin-left: auto;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        line-height: 1.5;
    }
    
    .chat-bubble-assistant {
        background-color: var(--primary-light);
        color: var(--text-primary);
        padding: 12px 16px;
        border-radius: 18px 18px 18px 4px;
        margin: 10px 0;
        max-width: 75%;
        margin-right: auto;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        border: 1px solid var(--border);
        line-height: 1.5;
    }
    
    .stButton button {
        background-color: var(--primary);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stButton button:hover {
        background-color: #1d4ed8;
        color: white;
    }
    
    .sidebar .sidebar-content {
        background-color: var(--surface);
        border-right: 1px solid var(--border);
    }
    
    .input-box {
        background-color: var(--surface);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid var(--border);
    }
    
    .logo-text {
        font-weight: 700;
        font-size: 1.5rem;
        margin-bottom: 0;
    }
    
    .tagline {
        color: #bfdbfe;
        font-size: 0.9rem;
        margin-top: 0;
    }
    
    .message-timestamp {
        font-size: 0.7rem;
        color: var(--text-secondary);
        margin-top: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------- Chat State ----------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ---------------------- Sidebar ----------------------
with st.sidebar:
    st.markdown('<p class="logo-text">🤖 AI Assistant</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.subheader("Conversation Settings")
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state["messages"] = []
        st.success("Conversation cleared!")
    
    st.markdown("---")
    st.subheader("About")
    st.markdown("""
    This AI assistant uses advanced natural language processing 
    to provide helpful and accurate responses to your questions.
    
    **Features:**
    - Real-time information access
    - Context-aware conversations
    - Professional interface
    """)
    
    st.markdown("---")
    st.caption("v1.0 | Professional Edition")

# ---------------------- Header ----------------------
st.markdown(
    """
    <div class="main-header">
        <h1>AI Assistant</h1>
        <p class="tagline">Your professional intelligent assistant with real-time knowledge</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# ---------------------- Chat Display ----------------------
chat_container = st.container()
with chat_container:
    # st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if not st.session_state["messages"]:
        st.info("💡 Start a conversation by typing a message below. I can help with information, ideas, and more!")
    
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.markdown(f'''
            <div class="chat-bubble-user">
                {msg["content"]}
                <div class="message-timestamp">You</div>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div class="chat-bubble-assistant">
                {msg["content"]}
                <div class="message-timestamp">Assistant</div>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------- Input Section ----------------------
# st.markdown('<div class="input-box">', unsafe_allow_html=True)
with st.form("chat_input_form", clear_on_submit=True):
    col1, col2 = st.columns([6, 1])
    with col1:
        user_input = st.text_input(
            "Type your message:", 
            placeholder="Ask me anything...", 
            label_visibility="collapsed"
        )
    with col2:
        submit_button = st.form_submit_button("Send →")
st.markdown('</div>', unsafe_allow_html=True)

if submit_button and user_input:
    # Save user message
    st.session_state["messages"].append({"role": "user", "content": user_input})
    
    # Show a spinner while processing
    with st.spinner("Thinking..."):
        # Get response from backend
        response = ChatBot(user_input)
    
    # Save assistant message
    st.session_state["messages"].append({"role": "assistant", "content": response})
    
    st.rerun()
