import time
import os
from datetime import date
from barcodeGiant import barcodeGiant
from cdw import cdw
from allterra import allterra
from barcodesInc import barcodesInc

total_before = time.time()
files = []

# scrap BarcodeGiant.com
before = time.time()
files.append(barcodeGiant())
after = time.time()
print(f"Scrapping BarcodeGiant.com took: {after-before} seconds")

# scrap CDW.com
before = time.time()
files.append(cdw())
after = time.time()
print(f"Scrapping CDW.com took: {after-before} seconds")

# scrap Allterra.com
before = time.time()
files.append(allterra())
after = time.time()
print(f"Scrapping Allterra.com took: {after-before} seconds")

# scrap BarcodesInc.com
before = time.time()
files.append(barcodesInc())
after = time.time()
print(f"Scrapping BarcodesInc.com took: {after-before} seconds")

# create one big file
one_file = open(f"web_scrap_all_{str(date.today())}.csv", "w")
one_file.write("Title, Description, Price, Web_source, Link, Date_Accessed, Model #\n")
for file in files:
    f = open(file, 'r')
    f.readline() # remove the header
    for line in f:
        one_file.write(line)
    f.close()
    os.remove(file)
one_file.close()

total_after = time.time()
print(f"Web Scrapping All Websites took: {total_after - total_before} seconds")


def scrape(scrapeModule, websiteName):
    before = time.time()
    files.append(scrapeModule())
    after = time.time()
    print(f"Scrapping {websiteName} took: {after - before} seconds")

