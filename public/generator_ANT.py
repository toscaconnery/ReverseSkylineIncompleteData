import sys
import random
from math import ceil

sys.stdout = open("ANT_D10_N200K.txt", "wt")

random.seed(122)

d = 10
n = 200000
missing_persentage = 20

for i in range(0,n):
    base = random.uniform(0,1)
    basedim = ceil(base / (1/d))-1
    basedata = random.uniform(0, 1)
    row = 'A'
    row += '%d' % (i+1)
    for dim in range(0,d):
        if dim != basedim:
            ran = random.randint(1, 100)
            if ran <= missing_persentage:
                row += ' null'
            else:
                baseotherdim = 1 - basedata
                posneg = random.uniform(0,1)
                if posneg <= 0.5:
                    addsub = -1 * (0.5 - posneg) * 0.2
                else:
                    addsub = (posneg - 0.5) * 0.2
                data = baseotherdim + addsub
                if data < 0:
                    data = 0.0
                elif data > 1:
                    data = 1.0
                row += ' %d' % ceil(data*100)
        else:
            row += ' %d' % ceil(basedata*100)
    print(row)


