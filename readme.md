# wifi-analyzer

I've isolated the process into 3 distinct steps. They are:

## Step 1:

The first step is to retrieve the necessary emails from a gmail address, all under a specific label. This is done by plugging into gmail's API via readonly authentication and querying for a list of message IDs under that label. A local manifest file is consulted and any missing files are downloaded, saved as .txt files and appended to the manifest.

## Step 2:

Several operations are done to ensure only the desired data is converted and added to the .csv files.

* Since the source XML txt is from an email, any signature is removed
* Certain SSIDs must be ignored. (config.omittedSSIDs)
* Colons are removed from BSSIDs, and the last two characters of the BBSID is replaced with a %
* Finally, only entries with a unique SSID and BSSID are added to the building's .csv file

## Step 3:

???

## Where I am currently

Step 1 and 2 are good to go, save for error handling. Step 3 requires checking in with the client, so waiting on that for now.