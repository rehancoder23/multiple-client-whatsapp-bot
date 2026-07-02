import sqlite3
import requests
import smtplib
from email.mime.text import MIMEText
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

def send_order_email_to_client(client_email, order_details):
    """Client ko naye order ki email automatic bhejne ka function bahi"""
    sender_email = "your_saas_system@gmail.com"  # Aapki main system email bahi
    sender_password = "your_app_password"        # Gmail ka App Password bahi

    # Email ka content set kar rahe hain bahi
    msg = MIMEText(f"Hello Client! \n\nA new order has been placed via WhatsApp Bot:\n\n{order_details}\n\nPlease prepare the order bahi!")
    msg['Subject'] = '🚨 New WhatsApp Order Received!'
    msg['From'] = sender_email
    msg['To'] = client_email

    try:
        # Gmail SMTP server se connect kar rahe hain bahi
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, client_email, msg.as_string())
        print(f"📧 Notification Email successfully sent to client ({client_email}) bahi! 🎉")
    except Exception as e:
        print(f"⚠️ Email sending failed bahi: {e}")

def send_whatsapp_via_green_api(instance_id, token, to_number, text_message):
    """Green-API ke zariye customer ko actual WhatsApp message bhejne ka function bahi"""
    url = f"https://api.green-api.com/waInstance{instance_id}/sendMessage/{token}"
    payload = {
        "chatId": f"{to_number.replace('+', '')}@c.us",
        "message": text_message
    }
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"✅ Message successfully delivered via Green-API to {to_number} bahi!")
        else:
            print(f"❌ Green-API Error: {response.text} bahi")
    except Exception as e:
        print(f"⚠️ Connection Error: {e} bahi")

def handle_incoming_whatsapp_webhook(payload):
    """Main router jo message received hone par chalta hai bahi"""
    instance_id = payload.get("instance_id")
    sender_number = payload.get("sender")
    incoming_message = payload.get("message")
    
    print(f"\n📥 Incoming Message! Instance: {instance_id} | From: {sender_number}")
    
    client_data = get_client_settings(instance_id)
    
    if not client_data:
        print("⚠️ Error: Yeh Instance ID register nahi hai bahi!")
        return
    
    gemini_key, system_prompt, whatsapp_token, is_active = client_data
    
    if is_active == 0:
        print("🚫 Client account suspended bahi!")
        return
    
    try:
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=system_prompt
        )
        
        print(f"🧠 Generating response using Gemini 2.0 Flash...")
        response = model.generate_content(incoming_message)
        ai_response = response.text
        
        # 🟢 CHECK KARTE HAIN KE KYA AI NE ORDER RECOGNIZE KIYA HAI BAHI?
        if "[ORDER]" in ai_response:
            # Fake testing ke liye hum abhi ek static email address par notifications bhej rahe hain bahi
            test_client_email = "client_test_email@gmail.com" 
            send_order_email_to_client(test_client_email, ai_response)
        
        # Green-API se reply WhatsApp par bhejte hain bahi
        send_whatsapp_via_green_api(instance_id, whatsapp_token, sender_number, ai_response)
        
    except Exception as e:
        print(f"⚠️ Engine Error bahi: {e}")

if __name__ == "__main__":
    # Test karne ke liye ek fake payload chalate hain bahi
    # Is baar payload aisa bhejenge ke Gemini order detect kare bahi!
    fake_webhook_payload = {
        "instance_id": "1101861234",
        "sender": "+923001234567",
        "message": "Mera order confirm kar do bahi, 2 Zinger burger chahiye!"
    }
    print("--- Running Green-API WhatsApp SaaS Router with Order Email System ---")
    handle_incoming_whatsapp_webhook(fake_webhook_payload)
