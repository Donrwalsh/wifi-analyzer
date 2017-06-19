from __future__ import print_function
import httplib2
import os
from datetime import datetime
import csv
from apiclient import discovery
from oauth2client import tools


import mailController



# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json

def main():
    #Create a Gmail API service object for queries:
    credentials = mailController.getCredentials()
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
        file.write(mailController.getMessageBody(service, 'me', msg['id'])[:-60])
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

