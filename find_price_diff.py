import sys
from datetime import date

output_file = open(f"price_diff_{str(date.today())}.csv")

file_name_one = sys.argv[1]
file_name_two = sys.argv[2]

f1 = open(file_name_one)
f2 = open(file_name_two)

# Remove the header
f1.readline()

# create header
output_file.write(f"Title, Description, Date: {file_name_one[-10:-1]}, Date: {file_name_two[-10:-1]}, Source")

for f1_line in f1:
    f1_line_split = f1_line.split(',')
    f2.readline()  # remove header
    for f2_line in f2:
        f2_line_split = f2_line.split(',')
        if f1_line_split[0] == f2_line_split[0] and f1_line_split[1] == f2_line_split[1]:


f1.close()
f2.close()
