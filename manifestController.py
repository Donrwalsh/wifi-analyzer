# -*- coding: utf-8 -*-
import config
import mailController
import os
import csv
import pprint

def compareManifest():
    #TODO: There seems to be a whole host of things that can go wrong here
    list_msg_ids = mailController.getGmailMsgIds()
    mailMsgs = []
    manifestMsgs = []
    output = []
    for msg in list_msg_ids['messages']:
        mailMsgs.append(str(msg['id']))
    if os.path.isfile(os.path.join(config.directory, config.manifest)):
        with open(os.path.join(config.directory, config.manifest), 'r', encoding="utf-8") as manifest:
            mr = csv.reader(manifest)
            for row in mr:
                if row[1] != "id":
                    manifestMsgs.append(row[1])
    for item in mailMsgs:
        if item not in manifestMsgs:
            output.append(item)
    return output

def verifyManifest():
    manifestMsgs = []
    manifestMsgsPass = []
    with open(os.path.join(config.directory, config.manifest), 'r', encoding="utf-8") as manifest:
        mr = csv.reader(manifest)
        for row in mr:
            if row[1] != "id":
                manifestMsgs.append(row[0])
    for mmsg in manifestMsgs:
        if os.path.isfile(os.path.join(config.directory, config.rawFolder, mmsg)):
            manifestMsgsPass.append(mmsg)
    return manifestMsgs == manifestMsgsPass

def writeToManifest(entries):
    if os.path.isfile(os.path.join(config.directory, config.manifest)):
        with open(os.path.join(config.directory, config.manifest), 'a') as manifestFile:
            mw = csv.writer(manifestFile)
            mw.writerow(entries)
    else:
        with open(os.path.join(config.directory, config.manifest), 'w') as manifestFile:
            mw = csv.writer(manifestFile)
            mw.writerow(["filename", "id", "converted"])
            mw.writerow(entries)

def recordConversion(filename):
    r = csv.reader(open(os.path.join(config.directory, config.manifest)))
    lines = [l for l in r]
    for line in lines:
        if line[0] == filename:
            line[2] = "T"
    writer = csv.writer(open(os.path.join(config.directory, config.manifest), 'w'))
    writer.writerows(lines)