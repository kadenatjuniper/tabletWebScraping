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


if len(sys.argv) < 4:
    priceFilename = input("What is the path to the file comparing price? ")
    infoFilename = input("What is the path to the file for model information? ")
    newFilename = input("What is the path to the file that is being added to the price comparison? ")
else:
    priceFilename = sys.argv[1]
    infoFilename = sys.argv[2]
    newFilename = sys.argv[3]

priceFile = open(priceFilename, "a")  # opens the file to be at the end so lines can be written to it

infoFile = open(infoFilename, "r+")  # opens file to read/write with the start at the beginning
infoFile.readline()  # remove header
modelList = []
for line in infoFile:
    modelList.append(line.split(',')[INFOFILE_MODEL].replace(' ', ''))


items = {}
newFile = open(newFilename)
newFile.readline()  # Remove header
for line in newFile:
    splitLine = line.split(',')
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
            price += float(priceSource)
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
        modelList.append(device)
        source = ""
        for eachSource in items[device]['source']:
            source += ' ' + eachSource
        infoline = items[device]['model'].strip('\n').replace(' ', '') + ',' + items[device]['title'] + ',' + items[device]['description'] + ',' + source + ',' + items[device]['date'] +'\n'
        infoFile.write(infoline)

priceFile.close()
infoFile.close()
