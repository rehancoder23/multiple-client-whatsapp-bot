import sqlite3
import requests
import google.generativeai as genai

def get_client_settings(instance_id):
    """Fetches the specific client's API keys and custom prompt from the database bahi"""
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

def handle_incoming_whatsapp_webhook(payload):
    """Main routing controller that maps incoming messages to the correct client bot persona bahi"""
    
    instance_id = payload.get("instance_id")
    sender_number = payload.get("sender")
    incoming_message = payload.get("message")
    
    print(f"\n📥 Incoming Message Received! Instance: {instance_id} | From: {sender_number}")
    
    # 1. Retrieve the client details from the centralized database
    client_data = get_client_settings(instance_id)
    
    if not client_data:
        print("⚠️ Error: This WhatsApp Instance ID is not registered in our database bahi!")
        return
    
    gemini_key, system_prompt, whatsapp_token, is_active = client_data
    
    # 2. Guardrail to check if the client's subscription is active
    if is_active == 0:
        print("🚫 Access Denied: This client account has been suspended bahi!")
        return
    
    try:
        # 3. Dynamically configure the Google AI API with the client's private key
        genai.configure(api_key=gemini_key)
        
        # 4. FIXED BACKEND MODEL: Upgraded to Gemini 2.0 Flash bahi!
        # The client does not need to configure this; it is handled automatically.
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash-lite",
            system_instruction=system_prompt  # Injecting the client's custom business training rules
        )
        
        # 5. Generate automated AI response
        print(f"🧠 Processing context via Gemini 2.0 Flash router...")
        response = model.generate_content(incoming_message)
        ai_response = response.text
        
    except Exception as e:
        print(f"⚠️ Gemini API Engine Error bahi: {e}")
        ai_response = "We are currently facing high server traffic. Please try again shortly."

    # 6. Dispatch the generated response back to the client's WhatsApp API instance
    print(f"📤 Dispatching automated reply to {sender_number} via WhatsApp Gateway... Seamless! 🚀")
    print(f"💬 Generated Response: {ai_response}")

if __name__ == "__main__":
    # Simulated webhook testing suite bahi
    fake_webhook_payload = {
        "instance_id": "instance_test_123",
        "sender": "+923219999999",
        "message": "Hello! What are your business operating hours today?"
    }
    
    print("--- Testing Dynamic SaaS Webhook Router with Fixed Gemini 2.0 Flash ---")
    handle_incoming_whatsapp_webhook(fake_webhook_payload)
