#!/usr/bin/env python3

# -*- coding: utf-8 -*-
import base64
from oauth2client import client
from datetime import datetime
from googleapiclient import discovery
import email
import email.message
import httplib2
import os
import requests
from oauth2client.file import Storage
from oauth2client import tools
import manifestController

import config

#TODO: Need to verify that manifest actually matches local files.

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

def gmailAuth():
    credentials = getCredentials()
    http = credentials.authorize(httplib2.Http())
    return discovery.build('gmail', 'v1', http=http)

def getGmailMsgIds():
    return gmailAuth().users().messages().list(userId='me', labelIds=config.labelId, maxResults=1000).execute()

def downloadMessageById(msgId):
    service = gmailAuth()
    message = service.users().messages().get(userId='me', id=msgId).execute()
    for item in message['payload']['headers']:
        if item['name'] == "Subject":
            subject = item['value'].replace('\u200b', '').replace('/', '')
        if item['name'] == "Date":
            format_date = datetime.strptime(item['value'][:-6], "%a, %d %b %Y %H:%M:%S")
            date = format_date.strftime("%m-%d %H_%M")
    building = subject.split(' ', 1)[0]
    name = building + " " + date + ".txt"
    file = open(os.path.join(config.directory, config.rawFolder) + "/" + name, "wb")
    file.write(getMessageBody(service, 'me', msgId).encode('utf-8'))
    file.close()
    # If it does not exist, create the manifest. Otherwise, add an entry
    manifestController.writeToManifest([name, msgId, 'F'])
    return name

def getCredentials():
    credential_path = os.path.join(config.directory, 'oauth.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(config.clientSecretFile, config.scopes)
        flow.user_agent = config.applicationName
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def getMessageBody(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
        if 'parts' in message['payload']:
            message_raw = message['payload']['parts'][0]['body']['data']
        else:
            message_raw = message['payload']['body']['data']
        msg_str = base64.urlsafe_b64decode(message_raw.replace('-_', '+/').encode('utf-8'))
        mime_msg = email.message_from_bytes(msg_str)
        messageMainType = mime_msg.get_content_maintype()
        if messageMainType == 'multipart':
            for part in mime_msg.get_payload():
                    if part.get_content_maintype() == 'text':
                            return part.get_payload()
            return ""
        elif messageMainType == 'text':
            return mime_msg.get_payload()
    except requests.HTTPError as error:
            print('An error occurred: %s' % error)