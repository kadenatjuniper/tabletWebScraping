import time
from datetime import date
from barcode_giant_web_scrap import barcode_giant_web_scrap
from cdw_web_scrap import cdw_web_scrap, get_total_pages

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

# create one big file
one_file = open("web_scrap_all.csv", "w")
for file in files:
    f = open(file)
    for line in f:
        one_file.write(line)
    f.close()
one_file.close()

total_after =time.time()
print(f"Web Scrapping All Websites took: {total_after - total_before} seconds")


