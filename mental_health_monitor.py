# Install required libraries
# (In your terminal or Colab: pip install streamlit requests)

import streamlit as st
import requests
import random
import time

# --- Configuration ---
THINGSPEAK_API_KEY = 'YOUR_READ_API_KEY'  # <-- optional if fetching from ThinkSpeak
CHANNEL_ID = 'YOUR_CHANNEL_ID'

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

# --- Streamlit App ---

st.title("💖 Smart Mental Health Monitoring System")

# Option to choose simulation or ThinkSpeak
mode = st.radio("Choose Data Source:", ("Simulated Data", "ThingSpeak Live Data"))

if st.button("Monitor Now"):

    if mode == "Simulated Data":
        heart_rate, temperature, gsr, activity = generate_sensor_data()
    else:
        heart_rate, temperature, gsr, activity = fetch_thingspeak_data()

    st.subheader("📈 Live Sensor Readings")
    st.metric("Heart Rate (bpm)", heart_rate)
    st.metric("Body Temperature (°C)", temperature)
    st.metric("GSR Value", gsr)
    st.metric("Activity Level", activity)

    # Stress Detection
    if detect_stress(heart_rate, gsr):
        st.error("⚠️ Stress Detected!")
        st.success(f"💬 Relaxation Suggestion: {suggest_relaxation()}")
    else:
        st.success("😊 You are Relaxed!")

    st.caption("🔄 Click 'Monitor Now' again to refresh.")

