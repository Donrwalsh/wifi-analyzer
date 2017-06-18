from __future__ import print_function
import httplib2
import os
import pprint
import email
import base64
import requests
from datetime import datetime
import csv
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'wifi-anayzer'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    credential_path = os.path.join(os.getcwd(), 'oauth.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def getMessageBody(service, user_id, msg_id):
    try:
            message = service.users().messages().get(userId=user_id, id=msg_id, format='raw').execute()
            msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
            mime_msg = email.message_from_string(msg_str)
            messageMainType = mime_msg.get_content_maintype()
            if messageMainType == 'multipart':
                    for part in mime_msg.get_payload():
                            if part.get_content_maintype() == 'text':
                                    return part.get_payload()
                    return ""
            elif messageMainType == 'text':
                    return mime_msg.get_payload()
    except requests.HttpError, error:
            print('An error occurred: %s' % error)

def main():
    #Create a Gmail API service object for queries:
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    label_id = 'Label_301'
    folderName = 'raw_data'
    manifest = 'manifest.csv'

    #Download All, create manifest
    list_msg_ids = service.users().messages().list(userId='me', labelIds=label_id, maxResults=500).execute()
    count = len(list_msg_ids['messages'])
    i = 0
    for msg in list_msg_ids['messages']:
        i = i + 1
        message = service.users().messages().get(userId='me', id=msg['id']).execute()
        for item in message['payload']['headers']:
            if item['name'] == "Subject":
                subject = item['value']
            if item['name'] == "Date":
                format_date = datetime.strptime(item['value'][:-6], "%a, %d %b %Y %H:%M:%S")
                date = format_date.strftime("%m-%d %H_%M")
        building = subject.split(' ', 1)[0]
        name = building + " " + date + ".txt"
        print(str(i) + "/" + str(count) + " " + str((i*100)/count) + "% Complete. " + "Creating " + name)
        #Create the file:
        file = open(folderName + "/" + name, "w")
        file.write(getMessageBody(service, 'me', msg['id'])[:-60])
        file.close()
        #If it does not exist, create the manifest. Otherwise, add an entry
        if os.path.isfile(manifest):
            with open(manifest, 'a') as manifestFile:
                mw = csv.writer(manifestFile)
                mw.writerow([name, msg['id']])
        else:
            with open(manifest, 'wb') as manifestFile:
                mw = csv.writer(manifestFile)
                mw.writerow(["filename", "id"])
                mw.writerow([name, msg['id']])



if __name__ == '__main__':
    main()

