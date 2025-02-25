import streamlit as st
from datetime import datetime
import random
import time
import requests
class ChatBot:
    def __init__(self):
        # Initialize session state for message history if it doesn't exist
        if 'messages' not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Hello! How can I help you today?"}
            ]

    def simulate_response(self, user_message):
        """Simulate a bot response - replace with actual bot logic"""
        responses = [
            f"I understand you said: '{user_message}'. Here's a simulated response.",
            "That's an interesting point. Could you tell me more?",
            "I'm processing your message and formulating a response...",
            f"Thank you for sharing that. Let me think about '{user_message}'."
        ]
        # Simulate thinking
        url = 'http://localhost:6000/query'
        myobj = {'prompt': user_message}

        x = requests.post(url, json = myobj)
        print(x.text)
        position = x.text.find("###")
        if position != -1:
            answer = x.text[position + len("###"):].strip()
            return answer
        else:
            return "No answer found."


        #return x.text.split("The answer is:")[1].strip()

    def display_messages(self):
        """Display all messages in the chat history"""
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                # Add timestamp in smaller, gray text
                st.caption(f"Sent at {datetime.now().strftime('%H:%M')}")

    def handle_input(self):
        """Handle user input and generate response"""
        if prompt := st.chat_input("What's on your mind?"):
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.write(prompt)
                st.caption(f"Sent at {datetime.now().strftime('%H:%M')}")

            # Generate and display assistant response
            response = self.simulate_response(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            with st.chat_message("assistant"):
                st.write(response)
                st.caption(f"Sent at {datetime.now().strftime('%H:%M')}")

def main():
    # Set up page configuration
    st.set_page_config(
        page_title="Streamlit Chatbot",
        page_icon="💬",
        layout="wide"
    )

    # Add custom CSS for styling
    st.markdown("""
        <style>
        .stTextInput>div>div>input {
            border-radius: 20px;
        }
        .stButton>button {
            border-radius: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Create sidebar with settings
    with st.sidebar:
        st.title("💬 Chat Settings")
        if st.button("Clear Chat History"):
            st.session_state.messages = [
                {"role": "assistant", "content": "Hello! How can I help you today?"}
            ]
        
        st.divider()
        st.markdown("### About")
        st.markdown("""
        MBCET Chatbot
        """)

    # Main chat interface
    st.title("MBCET Chatbot")
    
    # Initialize and run chatbot
    chatbot = ChatBot()
    chatbot.display_messages()
    chatbot.handle_input()

if __name__ == "__main__":
    main()