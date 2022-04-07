import time
import os
from datetime import date
from barcode_giant_web_scrap import barcode_giant_web_scrap
from cdw_web_scrap import cdw_web_scrap
from allterra_web_scrap import allterra_web_scrap

total_before = time.time()
files = []

# scrap BarcodeGiant.com
before = time.time()
files.append(barcode_giant_web_scrap())
after = time.time()
print(f"Scrapping BarcodeGiant.com took: {after-before} seconds")

# scrap CDW.com
before = time.time()
files.append(cdw_web_scrap())
after = time.time()
print(f"Scrapping CDW.com took: {after-before} seconds")

# scrap Allterra.com
before = time.time()
files.append(allterra_web_scrap())
after = time.time()
print(f"Scrapping Allterra.com took: {after-before} seconds")

# create one big file
one_file = open(f"web_scrap_all_{str(date.today())}.csv", "w")
one_file.write("Title, Description, Price, Web_source, Link, Date_Accessed, Part/Item #, MFG #, SKU, CDW #\n")
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


