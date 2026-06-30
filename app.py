import streamlit as st
import sqlite3
from add_client import register_new_client

# Page Title aur UI Formatting bahi
st.set_page_config(page_title="SaaS Bot Dashboard", page_icon="🤖", layout="wide")

st.title("🚀 Multi-Client WhatsApp AI SaaS Dashboard")
st.write("Welcome, Rehan Bhai! Apne clients ko yahan se manage aur register karein bahi.")

# Ek pyara sa form naye client ke liye bahi
st.header("➕ Register New Client Business")

with st.form("client_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        username = st.text_input("Username (Unique ID)", placeholder="e.g., burger_king_01")
        business_name = st.text_input("Business / Shop Name", placeholder="e.g., Burger King Pak")
        phone_number = st.text_input("WhatsApp Number", placeholder="e.g., +923001234567")
    
    with col2:
        instance_id = st.text_input("WhatsApp Instance ID (Evolution/Baileys)", placeholder="instance_123")
        token = st.text_input("WhatsApp Token / ApiKey", type="password", placeholder="enter token here")
        gemini_key = st.text_input("Client's Gemini API Key", type="password", placeholder="AIzaSy...")
        
    system_prompt = st.text_area("AI System Prompt (Bot Persona)", placeholder="Aap ek burger shop assistant hain...")
    
    submit_btn = st.form_submit_with_rows = st.form_submit_button("🔥 Connect & Activate Bot bahi")

# Jab button dabaein toh database mein data save ho bahi
if submit_btn:
    if username and business_name and instance_id and token and gemini_key:
        # Hum apni 'add_client.py' wali script ka function use kar rahe hain bahi
        register_new_client(username, business_name, phone_number, instance_id, token, gemini_key, system_prompt)
        st.success(f"⚡ Makkhan! '{business_name}' ka bot successfully active ho gaya hai bahi! 🎉")
    else:
        st.error("⚠️ Bahi, saari fields laazmi bharein!")
