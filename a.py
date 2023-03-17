from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Authenticate the API client
creds = Credentials.from_authorized_user_file('credentials.json', scopes=['https://www.googleapis.com/auth/gmail.compose'])

# Compose the email
message = MIMEMultipart()
message['to'] = 'akhilpatel2121@gmail.com'
message['subject'] = 'My APK file'
body = 'Here is my APK file'
message.attach(MIMEText(body))

# Attach the APK file
with open('my-app.apk', 'rb') as f:
    attachment = MIMEApplication(f.read(), _subtype='apk')
    attachment.add_header('Content-Disposition', 'attachment', filename='my-app.apk')
    message.attach(attachment)

# Send the email
try:
    service = build('gmail', 'v1', credentials=creds)
    message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
    send_message = (service.users().messages().send(userId="me", body=message).execute())
    print(F'sent message to {message["to"]}, Message Id: {send_message["id"]}')
except HttpError as error:
    print(F'An error occurred: {error}')
    send_message = None
