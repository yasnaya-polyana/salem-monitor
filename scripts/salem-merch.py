import requests
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

def get_page_content():
    url = "https://s4lem.myshopify.com/"
    try:
        response = requests.get(url)
        return response.text
    except Exception as e:
        return f"Error fetching page: {str(e)}"

def get_content_hash(content):
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def send_email(changes):
    sender_email = os.environ.get('EMAIL_ADDRESS')
    sender_password = os.environ.get('EMAIL_PASSWORD')
    receiver_email = "oscarlinehan@gmail.com"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "S4LEM Website Update Detected!"

    body = f"Changes detected on S4LEM website at {datetime.now()}\nCheck: https://s4lem.myshopify.com/"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("Email notification sent successfully")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

def check_for_updates():
    try:
        content = get_page_content()
        new_hash = get_content_hash(content)
        
        hash_file = 'last_hash.txt'
        
        if os.path.exists(hash_file):
            with open(hash_file, 'r') as f:
                old_hash = f.read().strip()
        else:
            old_hash = new_hash
            
        if new_hash != old_hash:
            print("Changes detected!")
            send_email(content)
            
            with open(hash_file, 'w') as f:
                f.write(new_hash)
        else:
            print("No changes detected")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    check_for_updates()