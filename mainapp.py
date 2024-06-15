import streamlit as st
from streamlit_login_auth_ui.widgets import __login__
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import pickle
import os
import json
from streamlit_chat import message, _streamlit_chat
from dotenv import load_dotenv
import google.generativeai as genai
import base64
from PIL import Image
from io import BytesIO
from io import BytesIO

# Login UI setup
__login__obj = __login__(auth_token="pk_prod_M8EH5F9J4W48J9NQ0E3YAA4XEJN8",
                         company_name="Sodacharya",
                         width=200, height=250,
                         logout_button_name='Logout', hide_menu_bool=False,
                         hide_footer_bool=True,
                         lottie_url='https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

LOGGED_IN = __login__obj.build_login_ui()

if LOGGED_IN:
    # Initialize chat open state
    if 'chat_open' not in st.session_state:
        st.session_state['chat_open'] = False

    # Function to toggle chat panel
    def toggle_chat():
        st.session_state['chat_open'] = not st.session_state['chat_open']

    # Sidebar navigation
    st.sidebar.title("Mental Health App")
    nav = st.sidebar.selectbox("Navigation", ["Home", "Resources", "Assistant", "Profile"])

    # Main container
    main_container = st.container()

    # Containers for different sections
    header_container = main_container.container()
    hero_container = main_container.container()
    features_container = main_container.container()
    call_to_action_container = main_container.container()
    footer_container = main_container.container()

    # Content for Home navigation
    if nav == "Home":
        with header_container:
            st.title("Welcome to Our Mental Health App")
            st.write("Your journey to better mental health starts here.")

        with hero_container:
            st.header("Take Control of Your Mental Health")
            st.write("Our app is designed to help you manage your mental health and wellbeing. With a range of tools and resources, you'll be able to track your progress, set goals, and connect with others who understand what you're going through.")

        with features_container:
            st.header("Our Features")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader("Mood Tracking")
                st.write("""
                - *Daily Journal:* Log your feelings and experiences daily.
                - *Mood Graphs:* Visualize your mood patterns over time.
                - *Insights:* Get personalized insights based on your entries.
                """)
            with col2:
                st.subheader("Goal Setting")
                st.write("""
                - *SMART Goals:* Set Specific, Measurable, Achievable, Relevant, and Time-bound goals.
                - *Progress Tracker:* Monitor your progress with interactive charts.
                - *Reminders:* Receive timely reminders to stay on track.
                """)
            with col3:
                st.subheader("Community Forum")
                st.write("""
                - *Discussion Groups:* Join groups based on common interests or experiences.
                - *Peer Support:* Connect with peers for mutual support.
                - *Expert Advice:* Access advice from mental health professionals.
                """)

        with call_to_action_container:
            st.header("Get Started Today")
            st.write("Sign up for our app and start your journey to better mental health.")

        with footer_container:
            st.write("Copyright 2023 Mental Health App. All rights reserved.")

    if nav == "Assistant":
        load_dotenv()
        api_key = os.getenv("GENAI_API_KEY")

        if not api_key:
            api_key = st.secrets["GENAI_API_KEY"]
            if not api_key:
                st.error("Please set the GENAI_API_KEY environment variable.")
                st.stop()

        genai.configure(api_key=api_key)

        # Set up the model
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 32,
            "max_output_tokens": 8192,
        }

        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]

        model = genai.GenerativeModel(
            model_name="gemini-pro",
            generation_config=generation_config,
            safety_settings=safety_settings,
        )

        # Load conversation history from file
        with open("conversation_history.json", "r") as file:
            conversation_history = json.load(file)

        # Start a chat with a greeting and initial information
        convo = model.start_chat(history=conversation_history)

        st.title("Mental Support Chatbot")

        # Get user input
        user_input = st.text_input("You:", key="user_input", placeholder="Type your message...")

        if user_input:
            with st.spinner("Thinking..."):
                convo.send_message(user_input)
                bot_response = convo.last.text

            # Display user message on the right
            message(user_input, is_user=True, key="user_message")

            # Display bot response on the left
            message(bot_response, is_user=False, key="bot_message")