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

def removeDuplicates(filename):
    if filename[-4:] != ".csv":
        raise Exception(filename + ' is not a csv file.')
    os.rename(filename, '_' + filename)
    inFile = csv.reader(open("_" + filename))
    with open(filename, "wb") as outFile:
        writeTo = csv.writer(outFile)
        matchPairs = []
        for row in inFile:
            if row[2]+row[3] in matchPairs:
                continue
            else:
                writeTo.writerow(row)
                matchPairs.append(row[2]+row[3])
    os.remove('_' + filename)

list_of_keys = ('Date', 'Time', 'SSID' , 'BSSID' , 'capabilities', 'frequency', 'level', 'centerFreq0',
                'centerFreq1', 'channelWidth', 'operatorFriendlyName',
                'venueName', 'is80211mcResponder', 'isPasspointNetwork')


#Remove all output csv files on start:
filelist = [ f for f in os.listdir(".") if f.endswith(".csv") ]
for f in filelist:
    os.remove(f)

for filename in os.listdir('raw_files'):
    if ".txt" in filename and filename != "Jackson 05-30 15_36.txt":
        omit = 0
        duplicate = 0
        building = filename.split(' ', 1)[0]
        with open('/Users/lfarvour/PycharmProjects/wifi-analyzer/raw_files/' + filename, 'r') as myfile:
            data=myfile.read()
        xmldoc = minidom.parseString(strip_sig(data))
        scan = xmldoc.getElementsByTagName("scanResult")
        date = filename.split(' ', 3)[1]
        time = filename.split(' ', 3)[2][:-4].replace("_", ":")
        for key in scan[0].attributes.keys():
            if key not in list_of_keys:
                raise Exception('The XML source txt file contains incorrect column names. Terminating')
        if not os.path.exists(building + '.csv'):
            with open(building + ".csv",'wb') as resultFile:
                wr = csv.writer(resultFile)
                wr.writerow(list_of_keys)
        else:
            buildingcsv = csv.reader(open(building + '.csv'))
            existingTimes = []
            existingDates = []
            for row in buildingcsv:
                if row[1] not in existingTimes and row[1] != "Time":
                    existingTimes.append(row[1])
                if row[0] not in existingDates and row[0] != "Date":
                    existingDates.append(row[0])
            if date in existingDates and time in existingTimes:
                print(filename + " has already been logged.")
                continue
        with open(building + ".csv",'a') as writeTo:
            wt = csv.writer(writeTo)
            for result in scan:
                if result.attributes['SSID'].value not in ["UofM Secure", "eduroam", "UofM-Guest"]:
                    addList = [date, time]
                    for key in list_of_keys[-12:]:
                        if key == "BSSID": addList.append(result.attributes[key].value.replace(":", "")[:-2] + "%")
                        else: addList.append(write_unicode(result.attributes[key].value))
                    wt.writerow(addList)
                else:
                    omit += 1
        print("Logged " + filename + ", Omitted " + str(omit) + " records.")

filelist = [ f for f in os.listdir(".") if f.endswith(".csv") ]
for f in filelist:
    removeDuplicates(f)