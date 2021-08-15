#!/usr/bin/python3
import subprocess
import os.path
import fileinput
from datetime import datetime
from dateutil.relativedelta import relativedelta
import twint

# Globale Parameter
actuary = "Fodor"
tableindex = {'AON': 1, 'Heubeck': 2, 'KMKOLL': 3, 'Mercer': 4, 'WTW': 5, 'Fodor': 6}
check = "&#10004;"
cross = "&#10060;"

shot_height = "800"

# Get current date
lastmonth = (datetime.today() - relativedelta(months=1)).strftime('%Y-%m-01')

# Configure
c = twint.Config()
c.Username = "Juergen_Fodor"
c.Search = "discountrate AND model"
c.Since = lastmonth
#c.Since = "2021-01-01"
#c.Until = "2021-05-01"
c.Hide_output = True
c.Pandas = True

# Run
twint.run.Search(c)

tweets = twint.storage.panda.Tweets_df

#print(tweets.keys())
#print(tweets.to_markdown())

for index, row in tweets.iterrows():
    # get tweetdata
    tweet = row['tweet']
    tweetdate = row['date'].split(" ")[0]
    tweetyear = tweetdate.split("-")[0]
    tweetprioryear = str(int(tweetyear)-1)
    tweetlink = row['link']

    # Find reportdate in tweet
    getdate = tweet.split(" #IAS19")[0].split(" ")
    if (tweetyear in getdate):
        yearindex = getdate.index(tweetyear)
        year = getdate[yearindex]
        month = getdate[yearindex-1]
        day = getdate[yearindex-2]
    elif (tweetprioryear in getdate):
        yearindex = getdate.index(tweetprioryear)
        year = getdate[yearindex]
        month = getdate[yearindex-1]
        day = getdate[yearindex-2]
    if month == "January":
        month = "01"
    elif month == "February":
        month = "02"
    elif month == "March":
        month = "03"
    elif month == "April":
        month = "04"
    elif month == "May":
        month = "05"
    elif month == "June":
        month = "06"
    elif month == "July":
        month = "07"
    elif month == "August":
        month = "08"
    elif month == "September":
        month = "09"
    elif month == "October":
        month = "10"
    elif month == "November":
        month = "11"
    elif month == "December":
        month = "12"
    else:
        month = "13"
    reportdate = f"{year}-{month}-{day}"

    # Create dir for reportmonth
    reportmonthdir = f"{year}-{month}"
    if not os.path.exists(reportmonthdir):
        os.mkdir(reportmonthdir)
        # Create new table entry in README.md
        for readmeline in fileinput.FileInput("README.md", inplace=1):
            if readmeline.startswith(':---'):
                newreadmeline = f"{reportmonthdir} | {cross} | {cross} | {cross} | {cross} | {cross} | {cross} |"
                readmeline = readmeline.replace(readmeline,readmeline + newreadmeline + "\n")
            print(readmeline, end='')
        # create README with Download Directory Link
        readmemonth = open(f"{reportmonthdir}/README.md", mode='a')
        readmemonth.write(f"[**Download {reportmonthdir}**](https://downgit.github.io/#/home?url=https://github.com/GeorgGoldbach/Zinsarchiv/tree/master/{reportmonthdir})\n\n")
        readmemonth.write("**Quellen:**\n")
        readmemonth.close()

    # Find model in tweet
    if "ratelink" in tweet.lower():
        model = "RATELink"
    elif "eurozone" in tweet.lower():
        model = "Eurozone"
    else:
        model = "ERROR"
    
    # Set name for outfile
    fileout = f"{reportmonthdir}/WTW-{model}-{reportdate}_Fodor-Tweet-{tweetdate}.png"

    # download files
    if os.path.isfile(fileout):
        print(f"File already exists: {fileout}")
    else:
        subprocess.run(["/usr/bin/chromium", "--headless", "--hide-scrollbars", f"--window-size=1920,{shot_height}", f"--screenshot={fileout}", tweetlink, "--virtual-time-budget=50000"], stderr=subprocess.DEVNULL)
        print(f"File downloaded: {fileout}")

        readmemonth = open(f"{reportmonthdir}/README.md", mode='r+')
        if tweetlink not in readmemonth.read():
            readmemonth.write("* " + tweetlink + "\n")
        readmemonth.close()

        # Check table entry in README.md
        for line in fileinput.FileInput("README.md", inplace=1):
            if line.startswith(reportmonthdir):
                linesplit = line.split('|')
                if cross in linesplit[tableindex[actuary]]:
                    linesplit[tableindex[actuary]] = f" {check} "
                    newline = ""
                    for entry in linesplit[:-1]:
                        newline = newline + entry + "|"
                    line = newline + "\n"
            print(line, end='')