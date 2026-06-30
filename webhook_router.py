import sqlite3
import requests

def get_client_settings(instance_id):
    """Database se client ki API keys aur prompt nikalne ka function bahi"""
    conn = sqlite3.connect('saas_automation.db')
    cursor = conn.cursor()
    
    # Query chala kar check karte hain ke instance_id database mein hai ya nahi bahi
    cursor.execute('''
        SELECT gemini_api_key, system_prompt, whatsapp_token, is_active 
        FROM bot_settings 
        WHERE whatsapp_instance_id = ?
    ''', (instance_id,))
    
    result = cursor.fetchone()
    conn.close()
    return result

def handle_incoming_whatsapp_webhook(payload):
    """WhatsApp se aane wale message ko route karne ka main function bahi"""
    
    # Webhook ke payload se instance_id aur message nikalte hain bahi
    # (Yeh structure Evolution-API/Baileys ke mutabiq thoda change ho sakta hai)
    instance_id = payload.get("instance_id")
    sender_number = payload.get("sender")
    incoming_message = payload.get("message")
    
    print(f"\n📥 Naya Message Aaya! Instance: {instance_id} | From: {sender_number}")
    
    # 1. Database se client ki settings uthayein bahi
    client_data = get_client_settings(instance_id)
    
    if not client_data:
        print("⚠️ Error: Yeh instance ID hamare database mein register nahi hai bahi!")
        return
    
    gemini_key, system_prompt, whatsapp_token, is_active = client_data
    
    # 2. Check karein ke client active hai ya uska account block hai bahi
    if is_active == 0:
        print("🚫 Account Suspended: Is client ka bot disabled hai bahi!")
        return
    
    print(f"🎯 Client Mil Gaya! Custom Prompt Use Ho Raha Hai: '{system_prompt[:30]}...'")
    
    # 3. Yahan hum Gemini API ko call karenge bahi (Aapka purana Gemini logic)
    # AI Key: gemini_key aur Prompt: system_prompt use hoga bahi.
    ai_response = f"(AI Jawab) Shukriya message karne ka! Aapne poocha: {incoming_message}" 
    
    # 4. Phir Evolution-API / Baileys ke zariye customer ko reply bheinjein ge bahi
    print(f"📤 Replying to {sender_number} via WhatsApp API... Makkhan! 🚀")
    print(f"💬 Response: {ai_response}")

if __name__ == "__main__":
    # Test karne ke liye ek fake webhook data chalate hain bahi
    # Yeh wahi instance_id hai jo humne 'add_client.py' mein register ki thi bahi!
    fake_webhook_payload = {
        "instance_id": "instance_test_123",
        "sender": "+923219999999",
        "message": "Burger ki delivery charges kya hain bahi?"
    }
    
    print("--- Testing Dynamic Webhook Router ---")
    handle_incoming_whatsapp_webhook(fake_webhook_payload)
