from math import *

h = 3 * 10**8
t = [185, 254, 365, 436, 546, 615]
t = [x * 10**-9 for x in t]
tprime = [(h/x, log(h/x)/log(10)) for x in t]
print(tprime)
