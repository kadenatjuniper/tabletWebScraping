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

priceFilename = input("What is the path to the file comparing price? ")
infoFilename = input("What is the path to the file for model information? ")
newFilename = input("What is the path to the file that is being added to the price comparison? ")

priceFile = open(priceFilename, "a") # opens the file to be at the end so lines can be written to it

infoFile = open(infoFilename, "w+") # opens file to read/write with the start at the beginning
infoFile.readline() # remove header
modelDict = []
for line in infoFile:
    modelDict.append(line.split(',')[INFOFILE_MODEL])

items = {}
newFile = open(newFilename)
for line in newFile:
    splitLine = line.split(',')
    if splitLine[NEWFILE_MODEL] in items:
        items[splitLine[NEWFILE_MODEL]][] # DO MORE STUFF HERE
    else:
        item = {'title': splitLine[NEWFILE_TITLE], 'description': splitLine[NEWFILE_DESCRIPTION], 'price': list(splitLine[NEWFILE_PRICE]), 'source': list(splitLine[NEWFILE_SOURCE] + ': ' + splitLine[NEWFILE_LINK]), 'date': splitLine[NEWFILE_DATE]}
        items[splitLine[NEWFILE_MODEL]] = item




priceFile.close()
infoFile.close()
