import sqlite3
import requests
import smtplib
from email.mime.text import MIMEText
import google.generativeai as genai

def get_client_settings(instance_id):
    """Database se client ki keys, prompt, email aur SHOP ADDRESS nikalne ka function bahi"""
    conn = sqlite3.connect('saas_automation.db')
    cursor = conn.cursor()
    
    # 🟢 Humne query mein shop_address ko bhi add kar diya hai bahi!
    cursor.execute('''
        SELECT gemini_api_key, system_prompt, whatsapp_token, is_active, client_email, shop_address 
        FROM bot_settings 
        WHERE whatsapp_instance_id = ?
    ''', (instance_id,))
    
    result = cursor.fetchone()
    conn.close()
    return result

def send_order_email_to_client(client_email, order_details):
    """Client ki email par dynamic order alert bhejne ka function bahi"""
    sender_email = "your_saas_system@gmail.com"  
    sender_password = "your_app_password"        

    msg = MIMEText(f"Hello! \n\nA new order has been securely placed via your WhatsApp Bot:\n\n{order_details}\n\nPlease process it immediately bahi!")
    msg['Subject'] = '🚨 New WhatsApp Order Alert!'
    msg['From'] = sender_email
    msg['To'] = client_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, client_email, msg.as_string())
        print(f"📧 Order alert dispatched to registered email ({client_email}) bahi! 🎉")
    except Exception as e:
        print(f"⚠️ Email dispatch failed bahi: {e}")

def send_whatsapp_via_green_api(instance_id, token, to_number, text_message):
    """Green-API sender bahi"""
    url = f"https://api.green-api.com/waInstance{instance_id}/sendMessage/{token}"
    payload = {
        "chatId": f"{to_number.replace('+', '')}@c.us",
        "message": text_message
    }
    headers = {'Content-Type': 'application/json'}
    try:
        requests.post(url, json=payload, headers=headers)
    except Exception as e:
        print(f"⚠️ Green-API Error bahi: {e}")

def handle_incoming_whatsapp_webhook(payload):
    """Main routing engine bahi"""
    instance_id = payload.get("instance_id")
    sender_number = payload.get("sender")
    incoming_message = payload.get("message")
    
    print(f"\n📥 Webhook trigger received for Instance: {instance_id}")
    
    client_data = get_client_settings(instance_id)
    
    if not client_data:
        print("⚠️ Error: Unregistered Instance ID bahi!")
        return
    
    # 🟢 Database se shop_address bhi dynamic mil gayi bahi!
    gemini_key, system_prompt, whatsapp_token, is_active, client_email, shop_address = client_data
    
    if is_active == 0:
        print("🚫 Account is suspended bahi!")
        return
    
    try:
        genai.configure(api_key=gemini_key)
        
        # Shop address ko system instruction ke sath jorh rahe hain bahi taake AI ko shop ka address pata ho!
        full_instruction = f"{system_prompt}\n\nYour shop/business location address is: {shop_address}"
        
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=full_instruction
        )
        
        response = model.generate_content(incoming_message)
        ai_response = response.text
        
        if "[ORDER]" in ai_response:
            send_order_email_to_client(client_email, ai_response)
        
        send_whatsapp_via_green_api(instance_id, whatsapp_token, sender_number, ai_response)
        
    except Exception as e:
        print(f"⚠️ System Engine Error bahi: {e}")
