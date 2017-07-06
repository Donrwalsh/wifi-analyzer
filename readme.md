# wifi-analyzer

App that parses wifi-analyzer data from xml emails and outputs specialized results. This app has a single use-case, and so is tailored for that environment.

## Step 1:

Retrieve all emails from a gmail address that have the given label. Messages are retrieved with Google's Gmail API, and saved as text files while retaining the XML formatting.

## Step 2:

Several operations are done to ensure only the desired data is converted and added to the .csv files.

* Since the source XML txt is from an email, any signature is removed
* Certain SSIDs must be ignored. (config.omittedSSIDs)
* Colons are removed from BSSIDs, and the last two characters of the BBSID is replaced with a %
* Finally, only entries with a unique SSID and BSSID are added to the building's .csv file

## Step 3:

???

## Where I am currently

Step 1 & 2 are complete. App is working on client machine.