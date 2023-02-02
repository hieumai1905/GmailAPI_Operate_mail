import base64
import json
from email.mime.text import MIMEText

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def send_email_via_gmail(to, subject, body):
    credentials = None
    # Load the credentials from the token.json file
    with open("token.json") as f:
        token_info = json.load(f)
        credentials = Credentials.from_authorized_user_info(info=token_info, scopes=token_info['scopes'])

    # Use the Gmail API
    service = build('gmail', 'v1', credentials=credentials)
    message = create_message(to, subject, body)
    send_message(service, "me", message, to)


def create_message(to, subject, body):
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


def send_message(service, user_id, message, send_to):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print(F'Email sent to {send_to} with email Id: {message["id"]}')
        print('Sent mail successfully!')
    except Exception as error:
        print(F'An error occurred: {error}')


if __name__ == '__main__':
    to = 'hieumai1905it@gmail.com'
    subject = 'Test Email using Gmail API'
    body = 'This is content of mail.'
    send_email_via_gmail(to, subject, body)
