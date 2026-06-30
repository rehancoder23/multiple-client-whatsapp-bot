import sqlite3

def init_saas_database():
    conn = sqlite3.connect('saas_automation.db')
    cursor = conn.cursor()
    
    # 1. Clients Table: Profiles store karne ke liye
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            client_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            business_name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 2. Bot Settings Table: API credentials aur prompt store karne ke liye
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bot_settings (
            setting_id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            whatsapp_instance_id TEXT UNIQUE NOT NULL,
            whatsapp_token TEXT NOT NULL,
            gemini_api_key TEXT NOT NULL,
            system_prompt TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            FOREIGN KEY (client_id) REFERENCES clients (client_id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("⚡ Makkhan! SaaS Database aur Tables successfully ban gayi hain bahi! 🚀")

if __name__ == "__main__":
    init_saas_database()
