import sys
import random
from math import ceil

d = 3
n = 200

#title
data_number_on_title = ""
thousands = False
number = n
if(n >= 1000):
    thousands = True
    number = int(n / 1000)
data_number_on_title = str(number)
if(thousands == True):
    data_number_on_title += "K"

sys.stdout = open("TESTING_USER_D" + str(d) + "_N" + str(data_number_on_title) + ".txt", "wt")
random.seed(122)

missing_persentage = 20

for i in range(0,n):
    row = ''

    base = random.randint(1,9)
    base = base * 10

    for dimension in range(0, d):
        last_digit = random.randint(0,9)
        number = base + last_digit
        if(dimension == 0):
            row += '%d' % (number)
        else:
            row += ' %d' % (number)
    print(row)