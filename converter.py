import os
import csv
from xml.dom import minidom
#Update the .gs to move things to raw_files
#Also if there's any work to be done on the timestamp, I'm using raw '_' files.

def strip_sig(str):
    loc = str.find("</wifiScanResults>")
    return str[0:loc+18]

def write_unicode(text, charset='utf-8'):
    return text.encode(charset)

list_of_keys = ('SSID' , 'BSSID' , 'capabilities', 'frequency', 'level', 'centerFreq0',
                'centerFreq1', 'channelWidth', 'operatorFriendlyName',
                'venueName', 'is80211mcResponder', 'isPasspointNetwork')

for filename in os.listdir('raw_files'):
    if ".txt" in filename:
        print("Now working on " + filename)
        building = filename.split(' ', 1)[0]
        with open('/Users/lfarvour/PycharmProjects/wifi-analyzer/raw_files/' + filename, 'r') as myfile:
            data=myfile.read()
        xmldoc = minidom.parseString(strip_sig(data))
        scan = xmldoc.getElementsByTagName("scanResult")
        for key in scan[0].attributes.keys():
            if key not in list_of_keys:
                raise Exception('The XML source txt file contains incorrect column names. Terminating')
        if not os.path.exists(building + '.csv'):
            with open(building + ".csv",'wb') as resultFile:
                wr = csv.writer(resultFile)
                wr.writerow(list_of_keys)
        with open(building + ".csv",'a') as writeTo:
            wt = csv.writer(writeTo)
            for result in scan:
                addList = []
                for key in list_of_keys:
                    addList.append(write_unicode(result.attributes[key].value))
                wt.writerow(addList)