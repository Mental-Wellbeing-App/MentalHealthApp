import streamlit as st
import base64
import time

# Function to add custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Encode the local image in base64
def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Path to your local image
image_path = "C:/Users/amith/OneDrive/Desktop/mini project/Mental-Wellbeing-App\mental health.png"
base64_image = get_base64_encoded_image(image_path)

# Custom CSS for animations and alternating sections
st.markdown(f"""
<style>
body {{
    background-image: url("data:image/jpeg;base64,{base64_image}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
@keyframes fadeIn {{
    0% {{ opacity: 0; }}
    100% {{ opacity: 1; }}
}}
.fade-in {{
    animation: fadeIn 0.5s ease-in-out;
}}
.left-section {{
    text-align: left;
    background-color: rgba(255, 255, 255, 0.8);
    padding: 20px;
    border-radius: 10px;
}}
.right-section {{
    text-align: right;
    background-color: rgba(255, 255, 255, 0.8);
    padding: 20px;
    border-radius: 10px;
}}
</style>
""", unsafe_allow_html=True)

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
