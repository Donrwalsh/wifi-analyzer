#Gmail Label ID
labelId = 'Label_301'

#Local System:
clientSecretFile = 'client_secret.json'
manifest = 'manifest.csv'
rawFolder = 'raw_data'
bldgFolder = 'bldg_csv'

#API Information:
applicationName = 'wifi-analyzer'
scopes = 'https://www.googleapis.com/auth/gmail.readonly'

#csv format:
list_of_keys = ('Date', 'Time', 'SSID' , 'BSSID' , 'capabilities', 'frequency', 'level', 'centerFreq0',
                'centerFreq1', 'channelWidth', 'operatorFriendlyName',
                'venueName', 'is80211mcResponder', 'isPasspointNetwork')
omittedSSIDs = ("UofM Secure", "eduroam", "UofM-Guest")

#Enter the name of .txt files to skip in conversion
skipTxt = ('Hhh 05-25 15_01.txt', 'Re: 05-30 10_36.txt', '.gitkeep')

directory = ('/Users/lfarvour/Desktop/potato/')