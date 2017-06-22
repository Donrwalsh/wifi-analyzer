# -*- coding: utf-8 -*-
import config
import os
import sys
import mailController



def sprint(string):
    print(string)
    sys.stdout.flush()

if os.path.exists(os.path.join(config.directory, config.manifest)):
    sprint("Manifest exists")
    sprint("Verifying manifest")
    #TODO: Verify manifest
    sprint("Manifest verified")
else:
    sprint("Manifest does not exist. It will be created")
sprint("Getting a list of Gmail messages")
new_ids = mailController.compareManifest()
if len(new_ids) > 0:
    sprint("Found " + str(len(new_ids)) + " new messages:")
    sprint(new_ids)
else:
    sprint("No new messages found")

for message in new_ids:
    sprint("Downloading message ID: " + message)
    sprint("Succesfully created " + mailController.downloadMessageById(message))
