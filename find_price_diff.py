import sys
from datetime import date

TITLE = 0
DESCRIPTION = 1
PRICE = 2
WEB_SOURCE = 3
LINK = 4
DATE_ACCESSED = 5
MODEL_NUMBER = 6

output_file = open(f"price_diff_{str(date.today())}.csv", "w")

file_name_one = sys.argv[1]
file_name_two = sys.argv[2]

f1 = open(file_name_one)
f2 = open(file_name_two)

# Remove the header
f1.readline()

# create header
output_file.write(f"Title, Description, Date: {file_name_one[-14:-4]}, Date: {file_name_two[-14:-4]}, Source\n")

for f1_line in f1:
    f1_line_split = f1_line.split(',')
    f2.readline()  # remove header
    for f2_line in f2:
        f2_line_split = f2_line.split(',')
        if f1_line_split[TITLE] == f2_line_split[TITLE] and f1_line_split[DESCRIPTION] == f2_line_split[DESCRIPTION] and f1_line_split[PRICE] != f2_line_split[PRICE]:
            output_file.write(f"{f1_line_split[TITLE]}, {f1_line_split[DESCRIPTION]}, {f1_line_split[PRICE]}, {f2_line_split[PRICE]}, {f2_line_split[LINK]}\n")
    f2.seek(0)

f1.close()
f2.close()
