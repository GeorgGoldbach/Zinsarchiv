#!/usr/bin/python3
import subprocess
import os.path
import re
import fileinput

def search_string_in_file(filename, searchstring):
    """Search for given string in file and return lines containing that string
    (source: https://thispointer.com/python-search-strings-in-a-file-and-get-line-numbers-of-lines-containing-the-string/)"""
    linenumber = 0
    resultlist = []
    # Opem file in read only mode
    with open(filename, 'r') as file:
        # Real all line in the file one by one
        for line in file:
            # For each line, check if line contains the strin
            linenumber += 1
            if searchstring in line:
                # If yes, then add the line in the list
                resultlist.append(line.rstrip())
    # Return list of tuples containing line numbers and lines where string is found
    return resultlist

# Globale Parameter
tableindex = {'AON': 1, 'Heubeck': 2, 'KMKOLL': 3, 'Mercer': 4, 'WTW': 5, 'Fodor': 6}
check = "&#10004;"
cross = "&#10060;"
useragent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.101 Safari/537.36"

# Mercer
# ======

for actuary in ["Mercer", "AON", "KMKOLL", "WTW", "Heubeck"]:

    if actuary == "Mercer":
        actuaryurl = 'https://www.mercer.de/our-thinking/rechnungszins-fuer-ifrs-us-gaap-bilmog-bewertungen.html'

        # Indicators for reportdate
        standindicator = '(Stand '
        cutstandindicatorleft = '(Stand '

        # Indicators for fileurl
        fileurlbeginning = 'https://www.mercer.de'
        fileurlindicator = 'src="/content/dam/mercer/attachments/europe/Germany/'
        cutindicatorleft = 'src="'
        cutindicatorright = '.png'

    elif actuary == "AON":
        actuaryurl = 'https://www.aon.com/germany/publikationen/human-resources/rechnungszins.jsp'

        # Indicators for reportdate
        standindicator = '(Stand '
        cutstandindicatorleft = '(Stand '

        # Indicators for fileurl
        fileurlbeginning = 'https://www.aon.com'
        fileurlindicator = 'Rechnungszinsinformation'
        cutindicatorleft = 'href="'
        cutindicatorright = '.pdf'

    elif actuary == "KMKOLL":
        actuaryurl = 'https://www.kmkoll.de/IFRS-Zinsermittlung.aspx'

        # Indicators for reportdate
        standindicator = 'Stichtag">'
        cutstandindicatorleft = 'Stichtag">'

        # Indicators for fileurl
        fileurlbeginning = 'https://www.kmkoll.de/'
        fileurlindicator = '.pdf'
        cutindicatorleft = 'href="'
        cutindicatorright = '.pdf'

    elif actuary == "WTW":
        actuaryurl = 'https://www.willistowerswatson.com/de-DE/Insights/campaigns/rechnungszins-nach-ifrs-us-gaap-und-hgb'

        # Indicators for reportdate
        standindicator = '/Rechnungszins/Rechnungszins-'
        cutstandindicatorleft = '/Rechnungszins/Rechnungszins-'

        # Indicators for fileurl
        fileurlbeginning = ''
        fileurlindicator = '/Rechnungszins/Rechnungszins-'
        cutindicatorleft = 'href="'
        cutindicatorright = '.pdf'

    elif actuary == "Heubeck":
        actuaryurl = 'https://www.heubeck.de/aktuelles/informationen/zinsinfo'

        # Indicators for reportdate
        standindicator = ''
        cutstandindicatorleft = ''

        # Indicators for fileurl
        fileurlbeginning = 'https://www.heubeck.de/assets/Download/HI_Zinsinfo/'
        fileurlindicator = '.pdf'
        cutindicatorleft = 'href="/assets/Download/HI_Zinsinfo/'
        cutindicatorright = '.pdf'

    # START
    print(actuary)
    print("=" * len(actuary))

    actuaryfile = f"{actuary}.txt"
    subprocess.run(["wget", "--no-check-certificate", "--user-agent", useragent, actuaryurl, "-O", actuaryfile], stderr=subprocess.DEVNULL)

    # Search for reportdate 
    searchstand = search_string_in_file(actuaryfile, standindicator)

    # Search for fileurl
    if actuary == "Heubeck":
        searchfileurl = []
        results = search_string_in_file(actuaryfile, fileurlindicator)
        for result in results:
            for href in result.split(cutindicatorleft)[1:]:
                href = href.replace(".PDF", ".pdf")
                href = href.split(cutindicatorright, 1)[0] + cutindicatorright
                if "IFRS" in href:
                    searchfileurl.append(cutindicatorleft + href)
    else:
        searchfileurl = search_string_in_file(actuaryfile, fileurlindicator)

    i = 0
    for line in searchfileurl:

        if actuary in ["Mercer", "KMKOLL"]:
            stand = searchstand[0].split(cutstandindicatorleft)[1]
            year = stand.split('.')[2][0:4]
            month = stand.split('.')[1]
            day = stand.split('.')[0]
            reportdate = f"{year}-{month}-{day}"
        elif actuary == "AON":
            stand = searchstand[i].split(cutstandindicatorleft)[1]
            year = stand.split('.')[2][0:4]
            month = stand.split('.')[1]
            day = stand.split('.')[0]
            reportdate = f"{year}-{month}-{day}"
        elif actuary == "WTW":
            stand = searchstand[i].split(cutstandindicatorleft)[1]
            year = stand.split('-')[1][0:4]
            month = stand.split('-')[0]
            if month == "Januar":
                month = "01"
            elif month == "Februar":
                month = "02"
            elif month in ["Mrz", "Maerz"]:
                month = "03"
            elif month == "April":
                month = "04"
            elif month == "Mai":
                month = "05"
            elif month == "Juni":
                month = "06"
            elif month == "Juli":
                month = "07"
            elif month == "August":
                month = "08"
            elif month == "September":
                month = "09"
            elif month == "Oktober":
                month = "10"
            elif month == "November":
                month = "11"
            elif month == "Dezember":
                month = "12"
            else:
                month = "13"
            reportdate = f"{year}-{month}"
        elif actuary == "Heubeck":
            reportdate = re.search(r'\d+-\d+-\d+', line).group()
            year = reportdate.split('-')[0][0:4]
            month = reportdate.split('-')[1]
            day = reportdate.split('-')[2]
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

        line = line.split(cutindicatorleft)[1]
        fileurlending = line.split(cutindicatorright, 1)[0] + cutindicatorright

        fileurl = fileurlbeginning + fileurlending
        filename = fileurl.split('/')[-1]
        fileout = f"{reportmonthdir}/{actuary}-{reportdate}_{filename}"

        # download files
        if os.path.isfile(fileout):
            print(f"File already exists: {fileout}")
        else:
            subprocess.run(["wget", "--no-check-certificate", "--user-agent", useragent, fileurl, "-O", fileout], stderr=subprocess.DEVNULL)
            print(f"File downloaded: {fileout}")

            readmemonth = open(f"{reportmonthdir}/README.md", mode='r+')
            if fileurl not in readmemonth.read():
                readmemonth.write("* " + fileurl + "\n")
            readmemonth.close()

            # Read image (OCR), in other words: convert png to csv
            if actuary == "Mercer" and i == 2:
                fileoutname = fileout.split('.')[0]
                subprocess.run(["tesseract", "-l", "deu+eng", fileout, fileoutname])
                subprocess.run(["mv", fileoutname + ".txt", fileoutname + "_OCR.csv"])

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

        i += 1

    os.remove(actuaryfile)
