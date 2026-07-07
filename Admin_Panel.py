import streamlit as st
import sqlite3

# Hide sidebar on this page too bahi
st.set_page_config(page_title="Admin Panel", page_icon="👑", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none !important;}
        [data-testid="collapsedControl"] {display: none !important;}
    </style>
""", unsafe_allow_html=True)

st.title("👑 Admin Control Panel (Owner View Only) bahi")
st.write("Welcome Rehan Bhai! Yahan aapka sara registered data safe hai bahi.")

# Wapas homepage par jane ka button bahi
if st.button("⬅️ Back to Registration Form bahi"):
    st.switch_page("app.py")

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
