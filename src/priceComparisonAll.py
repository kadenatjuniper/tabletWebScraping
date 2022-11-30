import sys
import os

INFOFILE_MODEL = 0
INFOFILE_TITLE = 1
INFOFILE_DESCRIPTION = 2
INFOFILE_SOURCE = 3

PRICEFILE_MODEL = 0
PRICEFILE_DATES = 1
PRICEFILE_PRICE = 2

NEWFILE_TITLE = 0
NEWFILE_DESCRIPTION = 1
NEWFILE_PRICE = 2
NEWFILE_SOURCE = 3
NEWFILE_LINK = 4
NEWFILE_DATE = 5
NEWFILE_MODEL = 6

newFilenames = []

if len(sys.argv) < 4:
    priceFilename = input("What is the path to the file comparing price? ")
    infoFilename = input("What is the path to the file for model information? ")
    newFilename = input("What is the path to the file that is being added to the price comparison? ")
    newFilenames.append(newFilename)
else:
    priceFilename = sys.argv[1]
    infoFilename = sys.argv[2]
    for i in range(3, len(sys.argv)):
        newFilenames.append(sys.argv[i])

print(f"Number of files given: {len(sys.argv) - 3}")

priceFile = open(priceFilename, "a")  # opens the file to be at the end so lines can be written to it

infoFile = open(infoFilename, "r+")  # opens file to read/write with the start at the beginning
infoFile.readline()  # remove header
modelList = []
for line in infoFile:
    modelList.append(line.split(',')[INFOFILE_MODEL].replace(' ', ''))

for newFilename in newFilenames:
    print("--------------------------- Start of a new File ----------------------------------")
    items = {}
    newFile = open(newFilename)
    newFile.readline()  # Remove header
    for line in newFile:
        # Need to remove a potential comma in the price without removing the commas for .csv file format
        # This should be possbile by checking that the char on each side of the comma is a digit
        priceFixedLine = ""
        commaCount = 0
        for i in range(0, len(line)):
            if line[i] == ',':
                commaCount += 1
                if line[i - 1].isnumeric() and line[i + 1].isnumeric() and commaCount == 3:
                    # print("Deleted Comma ***********************************************************************************")
                    a = 1  # Do nothing, we don't want this comma in the line
                else:
                    priceFixedLine += line[i]
            else:
                priceFixedLine += line[i]

        splitLine = priceFixedLine.split(',')
        if len(splitLine) != 7:
            print(f"Error - splitLine is length: {len(splitLine)}")
            print(f"Model: '{splitLine[NEWFILE_MODEL - 1]}' Price: '{splitLine[NEWFILE_PRICE]}' Date: '{splitLine[NEWFILE_DATE - 1]}'")

        if splitLine[NEWFILE_MODEL].strip() == "":
            splitLine[NEWFILE_MODEL] = splitLine[NEWFILE_TITLE]
            print(f"No Model Number Found: {splitLine[NEWFILE_TITLE]}")

        if splitLine[NEWFILE_MODEL] in items:
            items[splitLine[NEWFILE_MODEL]]['price'].append(splitLine[NEWFILE_PRICE].replace('$', '').replace(' ', '').replace('"', '').replace(',', ''))
            items[splitLine[NEWFILE_MODEL]]['source'].append(splitLine[NEWFILE_SOURCE] + ': ' + splitLine[NEWFILE_LINK])

        else:
            item = {'model': splitLine[NEWFILE_MODEL].strip('\n').replace('\n', ''), 'title': splitLine[NEWFILE_TITLE], 'description': splitLine[NEWFILE_DESCRIPTION], 'price': [splitLine[NEWFILE_PRICE].replace('$', '').replace(' ', '').replace('"', '').replace(',', '')], 'source': [splitLine[NEWFILE_SOURCE] + ': ' + splitLine[NEWFILE_LINK]], 'date': splitLine[NEWFILE_DATE]}
            items[splitLine[NEWFILE_MODEL]] = item

    for device in items:
        price = 0.0
        for priceSource in items[device]['price']:
            if priceSource != 'None':
                priceString = ''.join(c for c in priceSource if c.isnumeric() or c == '.')
                price += float(priceString)
            else:
                items[device]['price'].remove('None')
        if len(items[device]['price']) > 0:
            price = price / len(items[device]['price'])
        else:
            price = 0.0
        priceline = items[device]['model'].strip('\n').replace(' ', '') + ',' + items[device]['date'].replace(' ', '') + ',' + str(price).replace(' ', '') + '\n'
        priceFile.write(priceline)

    # TODO: Write the model dictionary to the file
    for device in items:
        if device.strip('\n').replace(' ', '') not in modelList:
            modelList.append(device.strip('\n').replace(' ', ''))
            source = ""
            for eachSource in items[device]['source']:
                source += ' ' + eachSource
            infoline = items[device]['model'].strip('\n').replace(' ', '') + ',' + items[device]['title'] + ',' + items[device]['description'] + ',' + source + ',' + items[device]['date'] +'\n'
            infoFile.write(infoline)

priceFile.close()
infoFile.close()
