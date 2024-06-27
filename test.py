x = -1
y = 2
z = -3

p = ""
if x < 0:
    p += "X: {0}\n".format(x)
if y < 0:
    p += "Y: {0}\n".format(y)
if z < 0:
    p += "Z: {0}\n".format(z)
if p.endswith('\n'):
    p = p[:-1]

print(p)
