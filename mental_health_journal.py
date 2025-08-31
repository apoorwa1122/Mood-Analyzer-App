import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import re
import random

# Set up the page with custom theme
st.set_page_config(
    page_title="MindCare Journal - Mental Wellness Tracker",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for vibrant design
st.markdown("""
<style>
    .main {
        background-color: #f0f8ff;
    }
    .stApp {
        background: linear-gradient(135deg, #e6f7ff 0%, #f5f5dc 100%);
    }
    .stButton>button {
        background-color: #1e90ff;
        color: white;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0077e6;
        color: white;
    }
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #1e90ff;
    }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-left: 5px solid #1e90ff;
    }
    .highlight {
        background-color: #fffacd;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .resource-box {
        background-color: #e6f7ff;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #1e90ff;
    }
</style>
""", unsafe_allow_html=True)

# Simple emotion detection using keyword matching
def detect_emotion(text):
    text = text.lower()
    
    # Define emotion keywords
    emotion_keywords = {
        'joy': ['happy', 'joy', 'excited', 'great', 'wonderful', 'good', 'love', 'loved', 'amazing', 'fantastic', 'smile', 'laughter'],
        'sadness': ['sad', 'unhappy', 'depressed', 'cry', 'crying', 'tears', 'hopeless', 'lonely', 'grief', 'mourn'],
        'anger': ['angry', 'mad', 'furious', 'hate', 'rage', 'annoyed', 'frustrated', 'irritated', 'outrage'],
        'fear': ['scared', 'afraid', 'fear', 'anxious', 'nervous', 'worried', 'panic', 'terrified', 'apprehensive'],
        'surprise': ['surprised', 'shocked', 'amazed', 'astonished', 'astounded'],
        'neutral': ['okay', 'fine', 'normal', 'alright', 'meh', 'regular', 'usual']
    }
    
    # Count matches for each emotion
    emotion_scores = {}
    for emotion, keywords in emotion_keywords.items():
        count = sum(1 for keyword in keywords if re.search(r'\b' + keyword + r'\b', text))
        emotion_scores[emotion] = count
    
    # Get the emotion with the highest score
    if sum(emotion_scores.values()) == 0:
        return 'neutral', 0.5
    
    dominant_emotion = max(emotion_scores, key=emotion_scores.get)
    confidence = min(0.95, emotion_scores[dominant_emotion] / sum(emotion_scores.values()) + 0.3)
    
    return dominant_emotion, confidence

# Initialize session state for journal entries
if 'entries' not in st.session_state:
    st.session_state.entries = []

# App title and description with vibrant design
st.markdown("<h1 style='text-align: center; color: #1e90ff;'>🧠 MindCare Journal</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #4682b4;'>Your Personal Mental Wellness Tracker</h3>", unsafe_allow_html=True)

st.markdown("""
<div class="card">
    <p>Share your thoughts and feelings in a safe space. Track your emotional patterns and discover insights about your mental wellbeing.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with resources and options
with st.sidebar:
    st.markdown("<h2 style='color: #1e90ff;'>🌱 Resources</h2>", unsafe_allow_html=True)
    
    st.markdown("<div class='resource-box'>", unsafe_allow_html=True)
    st.markdown("**🇮🇳 Indian Helplines**")
    st.markdown("- **Vandrevala Foundation**: 1860-2662-345 / 1800-2333-330")
    st.markdown("- **iCall**: +91-9152987821")
    st.markdown("- **AASRA**: +91-9820466726")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='resource-box'>", unsafe_allow_html=True)
    st.markdown("**🌐 Online Resources**")
    st.markdown("- [MindCare India](https://mindcareindia.org)")
    st.markdown("- [The Live Love Laugh Foundation](https://www.thelivelovelaughfoundation.org)")
    st.markdown("- [YourDOST](https://yourdost.com)")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Quick mood check-in
    st.markdown("<div class='resource-box'>", unsafe_allow_html=True)
    st.markdown("**⚡ Quick Mood Check**")
    quick_mood = st.selectbox("How are you feeling right now?", 
                             ["Select one", "😊 Good", "😐 Okay", "😔 Sad", "😰 Anxious", "😠 Angry"])
    if quick_mood != "Select one":
        st.info(f"Thanks for sharing. Remember, it's okay to feel {quick_mood.split(' ')[1].lower()}.")
    st.markdown("</div>", unsafe_allow_html=True)

# Main content area
tab1, tab2, tab3 = st.tabs(["📝 Journal", "📊 Insights", "ℹ️ Resources"])

with tab1:
    st.markdown("### How are you feeling today?")
    
    journal_input = st.text_area(
        "Share your thoughts:",
        height=150, 
        placeholder="Today I felt...",
        help="Write about your day, your feelings, or anything on your mind."
    )
    
    if st.button("Analyze My Emotions", type="primary"):
        if journal_input:
            with st.spinner("Analyzing your emotions..."):
                # Get prediction using simple emotion detection
                emotion, confidence = detect_emotion(journal_input)
                
                # Save entry with timestamp
                entry = {
                    "date": datetime.now(),
                    "text": journal_input,
                    "emotion": emotion,
                    "confidence": confidence
                }
                st.session_state.entries.append(entry)
                
                # Display result with emoji
                emotion_emojis = {
                    'joy': '😊',
                    'sadness': '😔',
                    'anger': '😠',
                    'fear': '😨',
                    'surprise': '😲',
                    'neutral': '😐'
                }
                
                emoji = emotion_emojis.get(emotion, '😐')
                
                st.markdown(f"""
                <div class="highlight">
                    <h3>{emoji} Detected emotion: <span style="color: #1e90ff;">{emotion.capitalize()}</span></h3>
                    <p>Confidence: {(confidence*100):.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Show appropriate message based on emotion
                if emotion in ['sadness', 'fear', 'anger']:
                    st.info("""
                    **Remember, it's okay to not be okay.** 
                    Consider reaching out to friends, family, or a mental health professional if you need support.
                    """)
                elif emotion == 'joy':
                    st.success("""
                    **It's great to see you're experiencing joy!** 
                    Celebrate these positive moments and acknowledge what's contributing to them.
                    """)
                else:
                    st.info("Thank you for sharing. Self-reflection is an important step in mental wellness.")
        else:
            st.warning("Please write something before analyzing.")

with tab2:
    if st.session_state.entries:
        st.markdown("### Your Emotional Journey")
        
        # Create dataframe from entries
        df = pd.DataFrame(st.session_state.entries)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Display line chart of emotions over time
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Convert emotions to numerical values for plotting
        emotion_map = {'joy': 5, 'surprise': 4, 'neutral': 3, 
                      'fear': 2, 'sadness': 1, 'anger': 0}
        df['emotion_value'] = df['emotion'].map(emotion_map)
        
        ax.plot(df['date'], df['emotion_value'], marker='o', linestyle='-', color='#1e90ff', linewidth=2)
        ax.set_yticks(list(emotion_map.values()))
        ax.set_yticklabels(list(emotion_map.keys()))
        ax.set_xlabel('Date')
        ax.set_ylabel('Emotion')
        ax.set_title('Your Emotional Journey', fontsize=16)
        ax.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        st.pyplot(fig)
        
        # Show statistics in columns
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Entries", len(df))
        with col2:
            most_common = df['emotion'].mode()[0] if not df.empty else "N/A"
            st.metric("Most Common Mood", most_common.capitalize())
        with col3:
            recent_emotion = df.iloc[-1]['emotion'] if not df.empty else "N/A"
            st.metric("Recent Mood", recent_emotion.capitalize())
        
        # Show entries in an expandable section
        with st.expander("View Journal History"):
            for i, entry in enumerate(reversed(st.session_state.entries)):
                emotion_emojis = {
                    'joy': '😊',
                    'sadness': '😔',
                    'anger': '😠',
                    'fear': '😨',
                    'surprise': '😲',
                    'neutral': '😐'
                }
                emoji = emotion_emojis.get(entry['emotion'], '😐')
                
                st.markdown(f"**{entry['date'].strftime('%Y-%m-%d %H:%M')}** {emoji} {entry['emotion'].capitalize()}")
                st.write(entry['text'])
                st.divider()
    else:
        st.info("👆 Write your first journal entry to see insights here!")

with tab3:
    st.markdown("### Mental Health Resources")
    
    st.markdown("""
    <div class="card">
        <h3>🇮🇳 India-Specific Resources</h3>
        <p><b>Emergency Helplines:</b></p>
        <ul>
            <li><b>Vandrevala Foundation</b>: 1860-2662-345 / 1800-2333-330</li>
            <li><b>iCall</b>: +91-9152987821 (Mon-Sat, 10AM-8PM)</li>
            <li><b>AASRA</b>: +91-9820466726 (24x7)</li>
            <li><b>SNEHA</b>: +91-44-24640050 (24x7)</li>
        </ul>
        <p><b>Online Counseling Platforms:</b></p>
        <ul>
            <li><b>YourDOST</b>: <a href="https://yourdost.com">https://yourdost.com</a></li>
            <li><b>InnerHour</b>: <a href="https://theinnerhour.com">https://theinnerhour.com</a></li>
            <li><b>Manas</b>: <a href="https://manas.org.in">https://manas.org.in</a></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <h3>🌐 International Resources</h3>
        <ul>
            <li><b>International Suicide Prevention</b>: <a href="https://www.iasp.info/resources/Crisis_Centres">Crisis Centers Directory</a></li>
            <li><b>7 Cups</b>: <a href="https://www.7cups.com">Free online therapy & counseling</a></li>
            <li><b>Talkspace</b>: <a href="https://www.talkspace.com">Online therapy platform</a></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <h3>📱 Mental Health Apps</h3>
        <ul>
            <li><b>Wysa</b>: AI-powered mental health support</li>
            <li><b>Calm</b>: Meditation and sleep app</li>
            <li><b>Headspace</b>: Mindfulness and meditation</li>
            <li><b>MindDoc</b>: Mental health monitoring</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer with encouragement
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #4682b4;'>
    <p>Remember: Your mental health is just as important as your physical health. 💙</p>
</div>
""", unsafe_allow_html=True)