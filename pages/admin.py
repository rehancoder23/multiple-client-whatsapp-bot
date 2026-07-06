import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Admin Panel", page_icon="👑", layout="wide")

st.title("👑 Admin Control Panel (Owner View Only) bahi")
st.write("Welcome Rehan Bhai! Yahan aap apne saare registered clients ka data dekh sakte hain bahi.")

# Secrets se password uthana bahi (GitHub par leak nahi hoga!)
correct_password = st.secrets["ADMIN_PASSWORD"]

# Password input field bahi
admin_password = st.text_input("Enter Admin Password to access data bahi", type="password")

if admin_password == correct_password:
    st.success("Access Granted! Welcome Back Rehan Bhai! 🔥")
    st.subheader("📊 Registered Clients Log")
    
    try:
        conn = sqlite3.connect('saas_automation.db')
        cursor = conn.cursor()
        
        # Check kar rahe hain ke table bani hui hai ya nahi bahi
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='bot_settings'")
        table_exists = cursor.fetchone()
        
        if table_exists:
            cursor.execute("SELECT username, business_name, whatsapp_number, client_email, shop_address FROM bot_settings")
            data = cursor.fetchall()
            conn.close()
            
            if data:
                # Loops chala kar data expanders mein dikhana bahi
                for row in data:
                    with st.expander(f"🏢 Client: {row[1]} ({row[0]})"):
                        st.write(f"**📞 WhatsApp:** {row[2]}")
                        st.write(f"**📧 Email:** {row[3]}")
                        st.write(f"**📍 Address:** {row[4]}")
            else:
                st.info("Bahi, abhi tak koi client register nahi hua database mein.")
        else:
            st.info("Bahi, abhi tak database table create nahi hui.")
            
    except Exception as e:
        st.error(f"Database read error bahi: {e}")
elif admin_password:
    st.error("❌ Galat password hai Rehan bhai! Chori nahi chalegi bahi.")
