

# Install required libraries
# (pip install streamlit requests)

import streamlit as st
import requests
import random
import time
import pandas as pd

# --- Configuration ---
THINGSPEAK_API_KEY = '4MNC2JYMQJQLKSSB'  # <-- Your Read API Key
CHANNEL_ID = '2939269'

# --- Functions ---

def generate_sensor_data():
    heart_rate = random.randint(65, 120)
    temperature = round(random.uniform(36.0, 37.5), 2)
    gsr = random.randint(400, 1000)
    activity = random.randint(1, 3)
    return heart_rate, temperature, gsr, activity

def detect_stress(heart_rate, gsr):
    return heart_rate > 100 and gsr > 700

def suggest_relaxation():
    suggestions = [
        "Take deep breaths for 2 minutes.",
        "Listen to calming music 🎵.",
        "Drink a glass of water slowly 🥤.",
        "Do a short stretching exercise 🤸‍♀️.",
        "Watch a feel-good short video 🎬."
    ]
    return random.choice(suggestions)

def fetch_thingspeak_data():
    url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={THINGSPEAK_API_KEY}&results=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        feeds = data['feeds'][0]
        heart_rate = int(feeds['field1'])
        temperature = float(feeds['field2'])
        gsr = int(feeds['field3'])
        activity = int(feeds['field4'])
        return heart_rate, temperature, gsr, activity
    else:
        st.error("Failed to fetch data from ThingSpeak.")
        return generate_sensor_data()

# --- App Starts Here ---

st.set_page_config(page_title="Smart Mental Health Dashboard", layout="wide")

st.title("💖 Smart Mental Health Monitoring Dashboard")

# Option to choose data source
mode = st.radio("Choose Data Source:", ("Simulated Data", "ThingSpeak Live Data"))

# Initialize a list to store heart rate history
if 'heart_rate_history' not in st.session_state:
    st.session_state.heart_rate_history = []

if st.button("Monitor Now"):

    # Get data
    if mode == "Simulated Data":
        heart_rate, temperature, gsr, activity = generate_sensor_data()
    else:
        heart_rate, temperature, gsr, activity = fetch_thingspeak_data()

    # Save heart rate history
    st.session_state.heart_rate_history.append(heart_rate)

    # --- Layout: 3 Columns ---
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("❤️ Heart Rate (bpm)", heart_rate)
        st.metric("🌡️ Temperature (°C)", temperature)

    with col2:
        st.metric("🧠 GSR Value", gsr)
        st.metric("🏃‍♂️ Activity Level", activity)

    with col3:
        if detect_stress(heart_rate, gsr):
            st.error("⚠️ Stress Detected!")
            st.success(f"💬 {suggest_relaxation()}")
        else:
            st.success("😊 You are Relaxed!")

    st.markdown("---")

    # --- Heart Rate Chart ---
    st.subheader("📈 Heart Rate Over Time")
    hr_df = pd.DataFrame({'Heart Rate': st.session_state.heart_rate_history})
    st.line_chart(hr_df)

    st.caption("🔄 Click 'Monitor Now' every few seconds to update live data.")


