# -*- coding: utf-8 -*-
import config
import os
import sys
import mailController
import pprint
import conversionController
import manifestController
import csv

def sprint(string):
    print(string)
    sys.stdout.flush()

def spprint(thing):
    pprint.pprint(thing)
    sys.stdout.flush()

#Step 1
if os.path.exists(os.path.join(config.directory, config.manifest)):
    sprint("Manifest exists")
    sprint("Verifying manifest")
    if (manifestController.verifyManifest()):
        sprint("Manifest matches local files.")
    else:
        sprint("Manifest does not match local files. Exiting")
        exit()
else:
    sprint("Manifest does not exist. It will be created")
sprint("Getting a list of Gmail messages")
new_ids = manifestController.compareManifest()
if len(new_ids) > 0:
    sprint("Found " + str(len(new_ids)) + " new messages:")
    spprint(new_ids)
else:
    sprint("No new messages found")
i = 0
for message in new_ids:
    i = i + 1
    sprint("Downloading message ID: " + message + ", " + str(i) + "/" + str(len(new_ids)))
    sprint("Succesfully created " + mailController.downloadMessageById(message))

#Step 2
r = csv.reader(open(os.path.join(config.directory, config.manifest)))
conversionToDo = []
toConvert = 0
for row in r:
    if row[0] not in config.skipTxt:
        if row[2] == "F":
            toConvert += 0
            conversionToDo.append(row[0])
j = 0
if len(conversionToDo) != 0:
    for filename in conversionToDo:
        if filename not in config.skipTxt:
            j = j + 1
            sprint("Converting file " + filename + ", " + str(j) + "/" + str(len(conversionToDo)))
            conversionController.addToBldgCsv(filename, conversionController.convertFile(filename))
    sprint("Finished converting " + str(len(conversionToDo)) + " txt files.")
else:
    sprint("There were no files to convert")