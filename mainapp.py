import streamlit as st
from streamlit_login_auth_ui.widgets import __login__
import os
import json
import PyPDF2
from streamlit_chat import message
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import plotly.express as px
from modules import data
from PIL import Image
from io import BytesIO
import time
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import random
load_dotenv()
# Login UI setup
__login__obj = __login__(auth_token=os.getenv("AUTH_TOKEN"),
                         company_name="Sodacharya",
                         width=200, height=250,
                         logout_button_name='Logout', hide_menu_bool=False,
                         hide_footer_bool=True,
                         lottie_url=os.getenv("LOTTIE_URL"))

LOGGED_IN = __login__obj.build_login_ui()

if LOGGED_IN:
    # Define the CSS for the background color
    page_bg_css = """
    <style>
        .stApp {
            background-color: #000000;
            color :#00ff00;
        }
    </style>
    """
    st.markdown(page_bg_css, unsafe_allow_html=True)

    # Initialize chat open state
    if 'chat_open' not in st.session_state:
        st.session_state['chat_open'] = False

    # Function to toggle chat panel
    def toggle_chat():
        st.session_state['chat_open'] = not st.session_state['chat_open']

    # Sidebar navigation
    st.sidebar.title("Mental Health App")
    nav = st.sidebar.selectbox("Navigation", ["Home", "Resources", "Assistant", "💎 Habit Tracker"])

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
        def animated_section(content_func, alignment):
            container = st.empty()
            with container.container():
                if alignment == "left":
                    st.markdown('<div class="left-section">', unsafe_allow_html=True)
                    content_func()
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="right-section">', unsafe_allow_html=True)
                    content_func()
                    st.markdown('</div>', unsafe_allow_html=True)
            return container
                
        def home_content():
            st.title("Welcome to Our Mental Health App")
            st.write("Your journey to better mental health starts here.")
            st.header("Take Control of Your Mental Health")
            st.write("""
            Our app is designed to help you manage your mental health and wellbeing. With a range of tools and resources, 
            you'll be able to track your progress, set goals, and connect with others who understand what you're going through. 
            Whether you're looking to improve your mood, set and achieve goals, or find community support, our app has something 
            for you.
            """)
            st.write("""
            Mental health is a crucial part of overall well-being, and taking steps to manage it can significantly improve your 
            quality of life. Our app offers features like mood tracking, goal setting, and a community forum to support your journey. 
            By regularly engaging with these tools, you can gain insights into your mental health, identify patterns, and make informed 
            decisions.
            """)
            st.write("""
            We understand that everyone's mental health journey is unique, and our app is designed to be flexible and accommodating 
            to different needs. Whether you're looking for daily journaling, setting specific goals, or finding peer support, our 
            app is here to help. Start today and take the first step towards better mental health with our comprehensive set of tools 
            and resources.
            """)

        def mood_tracking_content():
            st.title("Mood Tracking")
            st.write("""
            Our Mood Tracking feature is designed to help you understand and manage your emotional well-being. With our user-friendly 
            interface, you can easily log your daily moods, thoughts, and experiences. The app provides visual representations of your 
            mood patterns over time, allowing you to identify trends and triggers.
            """)
            st.write("""
            By regularly tracking your mood, you'll gain valuable insights into your emotional health. These insights can help you 
            make informed decisions about your self-care and when to seek additional support. Whether you're experiencing fluctuations 
            in mood due to stress, life changes, or other factors, mood tracking can provide clarity and direction.
            """)
            st.write("""
            In addition to tracking your mood, the app offers personalized insights based on your entries. These insights can guide 
            you in understanding the underlying causes of your emotions and help you develop strategies for managing them effectively. 
            Start using the Mood Tracking feature today and take a proactive step towards better emotional health.
            """)

        def goal_setting_content():
            st.title("Goal Setting")
            st.write("""
            The Goal Setting feature empowers you to take proactive steps towards improving your mental health. We use the SMART 
            (Specific, Measurable, Achievable, Relevant, Time-bound) framework to help you set realistic and attainable goals. Whether 
            it's practicing mindfulness, improving sleep habits, or reducing stress, our app guides you through the process.
            """)
            st.write("""
            You can track your progress with interactive charts and receive timely reminders to keep you motivated and on track towards 
            achieving your mental health objectives. Setting and achieving goals can provide a sense of accomplishment and boost your 
            confidence, contributing positively to your overall well-being.
            """)
            st.write("""
            The app also allows you to adjust your goals as needed, ensuring they remain relevant and achievable. By regularly reviewing 
            and updating your goals, you can maintain a forward momentum in your mental health journey. Start setting your SMART goals 
            today and take control of your mental health with our structured and supportive approach.
            """)

        def community_forum_content():
            st.title("Community Forum")
            st.write("""
            Our Community Forum is a safe and supportive space where you can connect with others on similar mental health journeys. 
            Join discussion groups based on common interests or experiences, share your stories, and offer mutual support. The forum 
            is moderated to ensure a respectful and constructive environment.
            """)
            st.write("""
            Additionally, you'll have access to valuable resources and occasional expert advice from mental health professionals. 
            These resources can provide guidance and support, helping you navigate your mental health journey with more confidence 
            and understanding. Engaging with the community can also reduce feelings of isolation and provide a sense of belonging.
            """)
            st.write("""
            Remember, while peer support can be incredibly helpful, it's not a substitute for professional medical advice or treatment. 
            Our forum is designed to complement your mental health care by providing additional support and connection. Join the 
            Community Forum today and start building meaningful connections with others who understand what you're going through.
            """)

        def cta_content():
            st.title("Get Started Today")
            st.write("""
            Sign up for our app and start your journey to better mental health. Our comprehensive set of tools and resources is designed 
            to support you every step of the way. Whether you're looking to track your mood, set and achieve goals, or find community 
            support, our app has everything you need.
            """)
            st.write("""
            Taking the first step towards better mental health can be daunting, but you're not alone. Our app is here to guide you, 
            providing the structure and support you need to make meaningful progress. With features like daily journaling, interactive 
            goal setting, and a supportive community forum, you'll have all the tools you need to succeed.
            """)
            st.write("""
            Don't wait any longer to take control of your mental health. Sign up today and discover how our app can help you achieve 
            a healthier, happier you. Start your journey now and see the difference that dedicated support and resources can make 
            in your life.
            """)

        def footer_content():
            st.write("Copyright 2023 Mental Health App. All rights reserved.")

        # Display sections with alternating alignment
        animated_section(home_content, alignment="left")
        st.markdown('<div class="fade-in"></div>', unsafe_allow_html=True)
        time.sleep(0.5)

        animated_section(mood_tracking_content, alignment="right")
        st.markdown('<div class="fade-in"></div>', unsafe_allow_html=True)
        time.sleep(0.5)

        animated_section(goal_setting_content, alignment="left")
        st.markdown('<div class="fade-in"></div>', unsafe_allow_html=True)
        time.sleep(0.5)

        animated_section(community_forum_content, alignment="right")
        st.markdown('<div class="fade-in"></div>', unsafe_allow_html=True)
        time.sleep(0.5)

        animated_section(cta_content, alignment="left")
        st.markdown('<div class="fade-in"></div>', unsafe_allow_html=True)
        time.sleep(0.5)

        animated_section(footer_content, alignment="right")

    if nav == "Resources":
        with header_container:
            st.title("Resources for Mental Health")
            st.write("Here are some resources that may be helpful for managing mental health:")
            with hero_container:
                st.header("Mental Health Organizations")
                
                st.write("1. Understanding Mental Health")
                st.write("   - Provides free 24/7 mental health counseling in India")
                st.markdown("[Download](https://www.un.org/en/healthy-workforce/files/Understanding%20Mental%20Health.pdf)", unsafe_allow_html=True)
                
                st.write("2. Mental Health Wellbeing")
                st.write("   - Offers general mental health resources")
                st.markdown("[Download](https://www.education.gov.in/covid-19/assets/img/pdf/CBSE_MH_Manual.pdf)", unsafe_allow_html=True)
                
                st.write("3. Mental Health Resources ")
                st.write("   - Contains all the required mental health resources.")
                st.markdown("[Download](https://iris.who.int/bitstream/handle/10665/42823/9241562579.pdf?sequence=1)", unsafe_allow_html=True)
                
                st.write("4. Mental Health Tips")
                st.write("   - Information on finding help, providers, and treatment for mental health.")
                st.markdown("[Download](https://www.mentalhealth.org.uk/sites/default/files/2022-07/mhf-our-best-ever-mental-health-tips-backed-by-research_0.pdf)", unsafe_allow_html=True)
                
                st.write("5. Tips for improving mental health")
                st.write("   - Contains all the tips related to mental health")
                st.markdown("[Download](https://www.heretohelp.bc.ca/sites/default/files/improving-mental-health.pdf)", unsafe_allow_html=True)
    if nav == "Assistant":
        load_dotenv()
        api_key = os.getenv("GENAI_API_KEY") or st.secrets.get("GENAI_API_KEY")

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

        # Initialize Sentence Transformer model
        sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        
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
            return sentence_model.encode(documents)
        
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
        user_input = st.text_input("You:", key="user_input", placeholder="Type your message...")

        if user_input:
            # Add user message to chat history
            st.session_state['messages'].append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.spinner("Thinking..."):
                if 'documents' in st.session_state and st.session_state['documents']:
                    # Encode query
                    query_embedding = sentence_model.encode([user_input])[0]

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
                    
                    response = model.generate_content(
                        contents=[
                            {"role": "user", "parts": [{"text": context}]},
                            {"role": "user", "parts": [{"text": user_input}]}
                        ]
                    )
                    bot_response = response.text
                else:
                    bot_response = "I'm excited to chat with you! 😊 However, I don't have any mental health information loaded yet. Could you please upload some PDFs using the sidebar? That way, I can provide even better support!"

            # Add assistant response to chat history
            st.session_state['messages'].append({"role": "assistant", "content": bot_response})
            with st.chat_message("assistant"):
                st.markdown(bot_response)

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
    if nav == "💎 Habit Tracker":
            st.title("💎 Habit Tracker")

            dt_now = dt.datetime.now()
            dt_str = dt_now.strftime("%Y-%m-%d")
            dt_weekday = dt_now.strftime("%A")
            dt_day = dt_now.strftime("%d")
            dt_month = dt_now.strftime("%b")

            st.markdown(f"Today is {dt_weekday} - {dt_day}. of {dt_month}.")

            # Sidebar
            st.sidebar.title("Mission Control")

            sidebar_data_container = st.sidebar.expander("💫 Load or Create a file", expanded=True)

            with sidebar_data_container:
                st.markdown("### 🗂 Load data")
                sidebar_uploaded_file = st.file_uploader("Choose your .csv file")

                st.markdown("### ✨ or create a new file")
                sidebar_create_file_name = st.text_input("Choose a file name", value="habit_data.csv")
                sidebar_create_file_button = st.button("* Create new file")

            sidebar_input_container = st.sidebar.expander("💪🏼 How did you do today?", expanded=False)

            with sidebar_input_container:
                sidebar_date = st.date_input("📅 Which day you want to make an entry for?", max_value=dt_now)
                sidebar_sleep = st.slider("😴 How much did you sleep?", min_value=0.0, max_value=12.0, value=8.0, step=0.1)
                sidebar_mood = st.slider("🌈 What mood were you in?", min_value=1, max_value=7, value=5, step=1)
                sidebar_energy = st.slider("⚡️ How energized did you feel?", min_value=1, max_value=7, value=5, step=1)
                sidebar_food = st.radio("🥕 Did you eat healthy?", (0, 1))
                sidebar_exercise = st.radio("🏃‍♀️ Did you exercise?", (0, 1))
                sidebar_meditation = st.radio("🧘‍ Did you meditate?", (0, 1))
                sidebar_reading = st.radio("📖 Did you read?", (0, 1))
                sidebar_journaling = st.radio("✏️ Did you journal?", (0, 1))
                sidebar_learning = st.radio("🎓 Did you learn something new?", (0, 1))
                sidebar_work = st.radio("🏆 Did you work towards your goals?", (0, 1))
                add_row = st.button("➕ Add values")

            @st.cache_resource
            def get_file(input_file):
                HabitData = data.HabitData()
                HabitData.load(file=input_file)
                return HabitData

            @st.cache_resource
            def create_file(filename):
                HabitData = data.HabitData()
                HabitData.create(filename=filename)
                return HabitData

            if sidebar_uploaded_file is not None:
                st.markdown("🔄 Data loaded.")
                HabitData = get_file(sidebar_uploaded_file)
            elif sidebar_create_file_button:
                st.markdown("✨ File created.")
                HabitData = create_file(sidebar_create_file_name)
            else:
                st.markdown("### Create or load a file to continue.")
                st.stop()

            if add_row:
                if sidebar_date in HabitData.data["date"].values:
                    st.warning("Data for this date already exists.")
                else:
                    append_dict = {
                        "date": [sidebar_date],
                        "sleep": [sidebar_sleep],
                        "mood": [sidebar_mood],
                        "energy": [sidebar_energy],
                        "food": [sidebar_food],
                        "exercise": [sidebar_exercise],
                        "meditation": [sidebar_meditation],
                        "reading": [sidebar_reading],
                        "journaling": [sidebar_journaling],
                        "learning": [sidebar_learning],
                        "work": [sidebar_work],
                    }
                    append_df = pd.DataFrame(append_dict)
                    HabitData.data = pd.concat([HabitData.data, append_df], ignore_index=True)

            sidebar_remove_data_container = st.sidebar.expander("🗑 Delete data", expanded=False)

            with sidebar_remove_data_container:
                try:
                    opt = HabitData.data.date.unique()
                except AttributeError:
                    opt = [None]

                selectbox_remove_date = st.selectbox("Remove data:", options=opt)
                drop_row = st.button("➖ Remove values")

            if drop_row:
                HabitData.drop(date_index=selectbox_remove_date)

            sidebar_download_data = st.sidebar.button("⬇️ Download data")

            if sidebar_download_data:
                st.sidebar.markdown(HabitData.download(), unsafe_allow_html=True)

            HabitData.data["avg_performance"] = HabitData.data.set_index("date").sum(axis=1).div(28).values

            data_container = st.expander("Display your data", expanded=True)
            with data_container:
                dataframe = st.dataframe(HabitData.data)

            st.markdown("### Plot your habits over time")

            plot_container, info_container = st.columns([8, 2])

            with info_container:
                opt = HabitData.data.columns.to_list()
                opt.remove("date")
                selectbox_columns = st.selectbox("Select which column to plot:", options=opt)

                m = round(HabitData.data[selectbox_columns].mean(), 2)
                metric_dict = {
                    "mood": "lvl",
                    "energy": "lvl",
                    "sleep": "h",
                    "food": "%",
                    "exercise": "%",
                    "meditation": "%",
                    "reading": "%",
                    "journaling": "%",
                    "learning": "%",
                    "work": "%",
                }
                st.markdown(f"""# avg // {m}""")

            with plot_container:
                px_chart = px.bar(HabitData.data, x="date", y=selectbox_columns)
                st.plotly_chart(px_chart, use_container_width=True)
