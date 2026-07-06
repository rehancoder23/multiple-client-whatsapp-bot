import sqlite3

def register_new_client(username, business_name, phone_number, instance_id, token, gemini_key, system_prompt, client_email, shop_address):
    """Database ke andar naye client ka mukammal data save karne ka function bahi"""
    conn = sqlite3.connect('saas_automation.db')
    cursor = conn.cursor()
    
    # Pehle table bana rahe hain agar nahi bani hui, naye columns ke sath bahi!
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bot_settings (
            username TEXT PRIMARY KEY,
            business_name TEXT,
            whatsapp_number TEXT,
            whatsapp_instance_id TEXT,
            whatsapp_token TEXT,
            gemini_api_key TEXT,
            system_prompt TEXT,
            client_email TEXT,
            shop_address TEXT,
            is_active INTEGER DEFAULT 1
        )
    ''')
    
    # Naya data insert ya replace kar rahe hain bahi
    cursor.execute('''
        INSERT OR REPLACE INTO bot_settings 
        (username, business_name, whatsapp_number, whatsapp_instance_id, whatsapp_token, gemini_api_key, system_prompt, client_email, shop_address, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
    ''', (username, business_name, phone_number, instance_id, token, gemini_key, system_prompt, client_email, shop_address))
    
    conn.commit()
    conn.close()
    print(f"✅ Database updated successfully for {business_name} bahi!")
