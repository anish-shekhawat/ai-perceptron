import math

c = 4
k = float(1) / float(2 * c)
delta = float(1)/float(1000)
epsilon = 0.2

delta = float(1) / float(1000)
n = 5

m1 = (144 * (n + 1) ** 2) / (25 * (k * float(epsilon)) ** 2)

m = max((-144 * math.log(delta / float(2))), m1)

print "Value of m: " + str(int(m))
print "2m/epsilon: " + str(2*m/epsilon)