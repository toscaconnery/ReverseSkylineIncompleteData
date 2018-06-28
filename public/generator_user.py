import sys
import random
from math import ceil

d = 4
n = 100

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

sys.stdout = open("user_preference_D" + str(d) + "_N" + str(data_number_on_title) + ".txt", "wt")
random.seed(122)

missing_persentage = 20

for i in range(0,n):
    # base = random.uniform(0,1)
    # basedim = ceil(base / (1/d))-1
    # basedata = random.uniform(0, 1)
    row = ''

    base = random.randint(0,8)
    base = base * 10

    row += '%d' % (base + random.randint(0,15))

    for dim in range(0,d-1):
       # row += ' %d' % base + random.randint(0,15)
        row += ' %d' % (base + random.randint(0,15))

    print(row)