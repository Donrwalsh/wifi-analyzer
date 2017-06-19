# wifi-analyzer

I've isolated the process into 3 distinct steps. They are:

## Step 1:

The first step is to retrieve the necessary emails from a gmail address, all under a specific label. This is done by plugging into gmail's API via readonly authentication and querying for a list of message IDs under that label. A local manifest file is consulted and any missing files are downloaded, saved as .txt files and appended to the manifest.

## Step 2:

Several operations are done on the .txt files to convert them into proper .csv files. #TODO: What are these operations? etc. etc.

## Where I am currently

Step 1 is coded as a controller with methods to call, and I'm working on doing the same to Step 2 (should be a lot easier). As of now, it's coded to assume everything runs properly and I'll need to do a pass to catch errors that arise. The current plan is to consolidate at least Step 1 and 2 into a single button action, with Step 3 joining the fun depending on specifics.