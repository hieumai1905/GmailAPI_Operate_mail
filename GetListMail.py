from __future__ import print_function
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        result = service.users().messages().list(userId='me').execute()
        messages = result.get('messages')

        if not messages:
            print('No messages found.')
            return

        print('Messages:')
        for message in messages:
            if not os.path.exists('email.txt'):
                with open('email.txt', 'w') as f:
                    f.write(message['id'] + ' ')
            else:  # neu file da ton tai thi kiem tra xem email da ton tai trong file chua
                with open('email.txt', 'r') as f:
                    data = f.read()
                    if message['id'] not in data:
                        with open('email.txt', 'a') as f:
                            f.write(message['id'] + ' ')

            message = service.users().messages().get(userId='me', id=message['id']).execute()

            # lay dia chi nguoi nhan va chu de cua email
            print(message['id'])
            print(message['payload']['headers'][4])
            print(message['payload']['headers'][5])
    except HttpError as error:
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()
