import sqlite3

def register_new_client(username, business_name, phone_number, instance_id, token, gemini_key, prompt):
    conn = sqlite3.connect('saas_automation.db')
    cursor = conn.cursor()
    
    try:
        # 1. Pehle client ki profile save karte hain bahi
        cursor.execute('''
            INSERT INTO clients (username, business_name, phone_number)
            VALUES (?, ?, ?)
        ''', (username, business_name, phone_number))
        
        # Abhi jo client insert hua uski ID nikalte hain
        client_id = cursor.lastrowid
        
        # 2. Ab us client ki bot settings aur API keys save karte hain bahi
        cursor.execute('''
            INSERT INTO bot_settings (client_id, whatsapp_instance_id, whatsapp_token, gemini_api_key, system_prompt)
            VALUES (?, ?, ?, ?, ?)
        ''', (client_id, instance_id, token, gemini_key, prompt))
        
        conn.commit()
        print(f"🔥 Makkhan bahi! Client '{business_name}' successfully register ho gaya hai! 🎉")
        
    except sqlite3.IntegrityError:
        print("⚠️ Error bahi: Yeh username ya WhatsApp instance pehle se register hai!")
    finally:
        conn.close()

if __name__ == "__main__":
    # Test karne ke liye ek dummy client ka data check karte hain bahi
    # Real system mein yeh data user website ke form se enter karega bahi
    print("--- Naya Client Register Ho Raha Hai bahi ---")
    register_new_client(
        username="burger_house_01",
        business_name="Burger House Pak",
        phone_number="+923001234567",
        instance_id="instance_test_123",
        token="token_xyz_786",
        gemini_api_key="AIzaSy_FakeGeminiKey_Here",
        prompt="Aap ek polite burger shop assistant hain. Urdu mein baat karein aur menu dikhayein bahi."
      )
