# -*- coding: utf-8 -*-
import config
import csv
import os
import pprint
import manifestController
from xml.dom import minidom

def addToBldgCsv(_filename, listOfLists):
    building = _filename.split(' ', 1)[0]
    filename = os.path.join(config.directory, config.bldgFolder, building + '.csv')
    if not os.path.exists(filename):
        with open(filename, 'w') as resultFile:
            wr = csv.writer(resultFile)
            wr.writerow(config.list_of_keys)
    bldgFile = csv.reader(open(filename))
    existingEntries = []
    for row in bldgFile:
        existingEntries.append(row[2]+row[3])
    with open(filename, "a") as outFile:
        w = csv.writer(outFile)
        for list in listOfLists:
            if list[2]+list[3] in existingEntries:
                continue
            else:
                w.writerow(list)
                existingEntries.append(list[2]+list[3])
    manifestController.recordConversion(_filename)

def convertFile(filename):
    #Converts file from .txt to a list of lists ready for potential addition to building csv.
    txtXmlString = ""
    with open(config.directory + "/" + config.rawFolder + "/" + filename, 'r', encoding="utf-8") as lines_file:
        csvR = csv.reader(lines_file)
        for row in csvR:
            txtXmlString = txtXmlString + str(row[0]) + " "
    xmldoc = minidom.parseString(strip_sig(txtXmlString).replace("�", "").replace('\n', ''))
    scan = xmldoc.getElementsByTagName("scanResult")
    date = filename.split(' ', 3)[1]
    time = filename.split(' ', 3)[2][:-4].replace("_", ":")
    for key in scan[0].attributes.keys():
        if key not in config.list_of_keys:
            print('Note: The XML source txt file contains incorrect column names.')

    output = []
    for item in scan:
        if item.attributes['SSID'].value not in config.omittedSSIDs:
            output.append([date, time, item.attributes['SSID'].value,
                          item.attributes['BSSID'].value.replace(":", "")[:-2] + "%",
                          item.attributes['capabilities'].value,
                          item.attributes['frequency'].value,
                          item.attributes['level'].value,
                          item.attributes['centerFreq0'].value,
                          item.attributes['centerFreq1'].value,
                          item.attributes['channelWidth'].value,
                          item.attributes['operatorFriendlyName'].value,
                          item.attributes['venueName'].value,
                          item.attributes['is80211mcResponder'].value,
                          item.attributes['isPasspointNetwork'].value
                          ])
    return output
    #Perform conversion from raw_txt files to parsed csv files.

def strip_sig(str):
    loc = str.find("</wifiScanResults>")
    return str[0:loc+18]
