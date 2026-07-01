import sqlite3
import requests
import google.generativeai as genai

def get_client_settings(instance_id):
    """Database se client ki API keys aur prompt nikalne ka function bahi"""
    conn = sqlite3.connect('saas_automation.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT gemini_api_key, system_prompt, whatsapp_token, is_active 
        FROM bot_settings 
        WHERE whatsapp_instance_id = ?
    ''', (instance_id,))
    
    result = cursor.fetchone()
    conn.close()
    return result

def send_whatsapp_via_green_api(instance_id, token, to_number, text_message):
    """Green-API ke zariye customer ko actual WhatsApp message bhejne ka function bahi"""
    # Green-API ka official message sending URL format bahi
    url = f"https://api.green-api.com/waInstance{instance_id}/sendMessage/{token}"
    
    # Payload format jo Green-API accept karta hai bahi
    payload = {
        "chatId": f"{to_number.replace('+', '')}@c.us", # Number se '+' hata kar '@c.us' lagana parta hai bahi
        "message": text_message
    }
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"✅ Message successfully delivered via Green-API to {to_number} bahi! 🎉")
        else:
            print(f"❌ Green-API Error: Status {response.status_code} - {response.text} bahi")
    except Exception as e:
        print(f"⚠️ Connection Error while calling Green-API bahi: {e}")

def handle_incoming_whatsapp_webhook(payload):
    """Main router jo message received hone par chalta hai bahi"""
    instance_id = payload.get("instance_id")
    sender_number = payload.get("sender")
    incoming_message = payload.get("message")
    
    print(f"\n📥 Incoming Message! Instance: {instance_id} | From: {sender_number}")
    
    # 1. Database se settings nikalte hain bahi
    client_data = get_client_settings(instance_id)
    
    if not client_data:
        print("⚠️ Error: Yeh Instance ID register nahi hai bahi!")
        return
    
    gemini_key, system_prompt, whatsapp_token, is_active = client_data
    
    if is_active == 0:
        print("🚫 Client account suspended bahi!")
        return
    
    try:
        # 2. Gemini 2.0 Flash configuration bahi
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash-lite",
            system_instruction=system_prompt
        )
        
        print(f"🧠 Generating response using Gemini 2.0 Flash...")
        response = model.generate_content(incoming_message)
        ai_response = response.text
        
        # 3. GREEN-API KE ZARIYE CUSTOMER KO JAWAB BHEJ RAHE HAIN BAHI!
        send_whatsapp_via_green_api(instance_id, whatsapp_token, sender_number, ai_response)
        
    except Exception as e:
        print(f"⚠️ Engine Error bahi: {e}")

if __name__ == "__main__":
    # Test ke liye dummy test code bahi
    fake_webhook_payload = {
        "instance_id": "1101861234",  # Yahan real testing mein client ki Green-API Instance ID aayegi bahi
        "sender": "+923001234567",
        "message": "Hello! What is your burger shop timing?"
    }
    print("--- Running Green-API WhatsApp SaaS Router Suite ---")
    handle_incoming_whatsapp_webhook(fake_webhook_payload)
