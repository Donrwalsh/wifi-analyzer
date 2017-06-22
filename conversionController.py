import config
import csv
import os
import pprint
from xml.dom import minidom

def addToBldgCsv(filename, listOfLists):
    building = filename.split(' ', 1)[0]
    filename = config.bldgFolder + '/' + building + '.csv'
    if not os.path.exists(filename):
        with open(filename, 'wb') as resultFile:
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

def convertFile(filename):
    #Converts file from .txt to a list of lists ready for potential addition to building csv.
    with open(config.directory + "/" + config.rawFolder + "/" + filename, 'r') as txtXmlFile:
        data=txtXmlFile.read()
    pprint.pprint(data)
    xmldoc = minidom.parseString(strip_sig(data))
    scan = xmldoc.getElementsByTagName("scanResult")
    date = filename.split(' ', 3)[1]
    time = filename.split(' ', 3)[2][:-4].replace("_", ":")
    for key in scan[0].attributes.keys():
        if key not in config.list_of_keys:
            raise Exception('The XML source txt file contains incorrect column names. Terminating')

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

convertFile('Microbiology​ 06-19 11_09.txt')

for filename in os.listdir('raw_data'):
    if filename not in config.skipTxt:
        print("Working on " + filename)
        addToBldgCsv(filename, convertFile(filename))
    else:
        print("Skipping " + filename)

convertFile('Microbiology​ 06-19 11_09.txt')