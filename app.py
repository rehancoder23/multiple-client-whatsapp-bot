import streamlit as st
import sqlite3
from add_client import register_new_client

# Page config bahi
st.set_page_config(page_title="SaaS Bot Dashboard", page_icon="🤖", layout="wide")

# Session state initialize kar rahe hain taake page track ho sake bahi
if "current_page" not in st.session_state:
    st.session_state.current_page = "registration"

# ==============================================================================
# 🏢 PAGE 1: REGISTRATION FORM (CLIENT VIEW)
# ==============================================================================
if st.session_state.current_page == "registration":
    st.title("🚀 Multi-Client WhatsApp AI SaaS Dashboard")
    st.write("Welcome! Register your business here to activate your automated WhatsApp AI bot bahi.")
    
    st.header("➕ Register New Client Business")
    
    # Main Registration Form bahi
    with st.form("client_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("Username (Unique ID)", placeholder="e.g., burger_king_01")
            business_name = st.text_input("Business / Shop Name", placeholder="e.g., Burger King Pak")
            phone_number = st.text_input("WhatsApp Number", placeholder="e.g., +923001234567")
            client_email = st.text_input("Client Notification Email", placeholder="e.g., owner@gmail.com")
        
        with col2:
            instance_id = st.text_input("WhatsApp Instance ID (Green-API)", placeholder="e.g., 1101861234")
            token = st.text_input("WhatsApp Token / ApiKey", type="password", placeholder="enter green-api token")
            gemini_key = st.text_input("Client's Gemini API Key", type="password", placeholder="AIzaSy...")
            
        shop_address = st.text_input("Shop / Business Physical Address", placeholder="e.g., Shop #4, Main Commercial Market, Lahore")
        system_prompt = st.text_area("AI System Prompt (Bot Persona)", placeholder="You are an AI assistant for a burger shop...")
        
        submit_btn = st.form_submit_button("🔥 Connect & Activate Bot bahi")
    
    if submit_btn:
        if username and business_name and instance_id and token and gemini_key and client_email and shop_address:
            register_new_client(username, business_name, phone_number, instance_id, token, gemini_key, system_prompt, client_email, shop_address)
            st.success(f"⚡ Brilliant! '{business_name}' bot is successfully activated bahi! Alerts will go to {client_email} 🎉")
        else:
            st.error("⚠️ Bahi, please fill in all the fields carefully including the address!")
            
    # --- KHUFIA OWNER LOGIN SECTION ---
    st.markdown("<br><br><hr>", unsafe_allow_html=True)
    
    admin_pass = st.text_input("🔑 Owner Login (Khufia Section) bahi", type="password")
    if admin_pass:
        correct_password = st.secrets.get("ADMIN_PASSWORD")
        
        if correct_password is None:
            st.error("⚠️ Rehan bhai, aapne Streamlit Cloud ke Secrets mein password set nahi kiya bahi!")
        elif admin_pass == correct_password:
            st.success("Password Match! Switching Page... 👑")
            # Daraz style mein current page state change bahi!
            st.session_state.current_page = "admin"
            st.rerun()
        else:
            st.error("❌ Galat password hai bahi!")

# ==============================================================================
# 👑 PAGE 2: ADMIN PANEL (MALIK VIEW ONLY)
# ==============================================================================
elif st.session_state.current_page == "admin":
    st.title("👑 Admin Control Panel (Owner View Only) bahi")
    st.write("Welcome Rehan Bhai! Yahan aapka sara registered data safe hai bahi.")
    
    # Wapas registration form par jaane ka button bahi
    if st.button("⬅️ Back to Registration Form bahi"):
        st.session_state.current_page = "registration"
        st.rerun()
        
    st.subheader("📊 Registered Clients Log")
    
    try:
        conn = sqlite3.connect('saas_automation.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='bot_settings'")
        table_exists = cursor.fetchone()
        
        if table_exists:
            cursor.execute("SELECT username, business_name, whatsapp_number, client_email, shop_address FROM bot_settings")
            data = cursor.fetchall()
            conn.close()
            
            if data:
                for row in data:
                    with st.expander(f"🏢 Client: {row[1]} ({row[0]})"):
                        st.write(f"**📞 WhatsApp:** {row[2]}")
                        st.write(f"**📧 Email:** {row[3]}")
                        st.write(f"**📍 Address:** {row[4]}")
            else:
                st.info("Bahi, abhi tak koi client register nahi hua database mein.")
        else:
            st.info("Bahi, database table abhi tak create nahi hui.")
            
    except Exception as e:
        st.error(f"Database read error bahi: {e}")
