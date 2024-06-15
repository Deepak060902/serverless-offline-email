import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import ssl

def send_email(event, context):
    try:
        # Check if body is present in the event
        if 'body' not in event or not event['body']:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Body is missing"})
            }

        try:
            # Parse the JSON body of the request
            body = json.loads(event['body'])
            print(f"Parsed body: {body}")
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {str(e)}")
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Invalid JSON format", "error": str(e)})
            }

        receiver_email = body.get('receiver_email')
        subject = body.get('subject')
        body_text = body.get('body_text')
        if not receiver_email or not subject or not body_text:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Missing required fields"})
            }

        sender_email = os.getenv('GMAIL_USER')
        sender_password = os.getenv('GMAIL_PASS')

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body_text, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465,) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Email sent"})
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal Server Error", "error": str(e)})
        }
