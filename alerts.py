import json
import logging
import smtplib
import requests

Url="https://www.avatrade.com/"

def send_alert(message):
    try:
        #define the the email setting like : Email , Password. And starting the SMTP server.
        sender_email = "eyadjbaren99@gmail.com"
        receiver_email = "eyadjb@moovingon.com"
        password = "wsqg rjna qhgn dbtt"  
        logging.info("📩 Attempting to send email...")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)

        #Configure the email content (Title, Text, Body), and sending the email by using .sendmail(....)
        subject = "Selenium Test Failed!".encode("utf-8")  
        body = f"Alert! The Selenium test failed.\n\nError: {message}".encode("utf-8")
        email_text = f"Subject: {subject.decode('utf-8')}\nMIME-Version: 1.0\nContent-Type: text/plain; charset=utf-8\n\n{body.decode('utf-8')}"
        server.sendmail(sender_email, receiver_email, email_text.encode("utf-8"))
        server.quit()
        print("✅ Email sent successfully!")  

    except Exception as e:
        logging.error(f"❌ Error sending email: {e}")  



def send_slack_alert(message):
    slack_webhook_url = "https://hooks.slack.com/services/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"  
    payload = {
        "text": f"🚨 *Login Proactive Failed* 🚨\n*Alert Info:* {message} | {Url} | P1  \n*Priority:* P1\n*Host*: {Url}",  
        "messages": " Test ", 
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(slack_webhook_url, data=json.dumps(payload), headers=headers)  # ✅ Corrected

    if response.status_code == 200:
        print("✅ Slack alert sent successfully!")
    else:
        print(f" Failed to send Slack alert: {response.status_code}, {response.text}")



# Setup Logging log file to monitoring the logs if have any failuer
logging.basicConfig(
    filename="test_log.log",  # Log file name
    level=logging.INFO,  # Log level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
)