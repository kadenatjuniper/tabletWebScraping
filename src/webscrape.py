import time
import os
import traceback
from datetime import date
from barcodeGiant import barcodeGiant
from cdw import cdw
from allterra import allterra
from barcodesInc import barcodesInc
from fondriestGNSS import fondriestGNSS
from rjm import rjm
from waypointtech import waypointtech

total_before = time.time()
files = []

error = 0

def scrape(scrapeModule, websiteName):
    try:
        before = time.time()
        files.append(scrapeModule())
        after = time.time()
        print(f"Scrapping {websiteName} took: {after - before} seconds")
        return 0
    except Exception as e:
        print(f"Error scraping {websiteName}.\n   {e}")
        traceback.print_exc()
        return 1

def createOneFile(files):
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


error = error + scrape(rjm, "RJMPrecision.com")
error = error + scrape(fondriestGNSS, "Fondriest.com for GNSS")
error = error + scrape(cdw, "CDW.com")
error = error + scrape(allterra, "Allterra.com")
error = error + scrape(barcodesInc, "BarcodesInc.com")
error = error + scrape(barcodeGiant, "BarcodeGiant.com")
error = error + scrape(waypointtech, "WaypointTech.com")

createOneFile(files)

total_after = time.time()
print(f"Web Scrapping All Websites took: {total_after - total_before} seconds")
if error:
    print(f"----------- An error occurred While scraping one of the websites --------------")


