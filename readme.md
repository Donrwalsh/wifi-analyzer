# wifi-analyzer

Working with data gathered from a portable wifi analyzer app, the goal of this project is to reduce the amount of manual interaction required to submit discovered data properly to Bastion.

Initially, the wifi-analyzer.gs Google Script will take in a label name, and drive folder ID. It then scans the label for all messages and saves them as text files in the drive folder.

Next, the folder of raw files are parsed by converter.py. It creates or appends to csv files with building names (found from the subject of emails) and parses the XML text into csv files.