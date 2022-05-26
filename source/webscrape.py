import time
import os
import traceback
from datetime import date
from barcodeGiant import barcodeGiant
from cdw import cdw
from allterra import allterra
from barcodesInc import barcodesInc
from fondriestGNSS import fondriestGNSS

total_before = time.time()
files = []


def scrape(scrapeModule, websiteName):
    try:
        before = time.time()
        files.append(scrapeModule())
        after = time.time()
        print(f"Scrapping {websiteName} took: {after - before} seconds")
    except Exception as e:
        print(f"Error scraping {websiteName}.\n   {e}")
        traceback.print_exc()


scrape(fondriestGNSS, "Fondriest.com for GNSS")
scrape(cdw, "CDW.com")
scrape(allterra, "Allterra.com")
scrape(barcodesInc, "BarcodesInc.com")
scrape(barcodeGiant, "BarcodeGiant.com")

# create one big file
one_file = open(f"web_scrap_all_{str(date.today())}.csv", "w")
one_file.write("Title, Description, Price, Web_source, Link, Date_Accessed, Model #\n")
for file in files:
    f = open(file, 'r')
    f.readline()  # remove the header
    for line in f:
        one_file.write(line)
    f.close()
    os.remove(file)
one_file.close()

total_after = time.time()
print(f"Web Scrapping All Websites took: {total_after - total_before} seconds")


