xarray = [1, 2, 3, 4, 5]
yarray = [5, 5, 5, 6.8, 9]
x2 = 0
y = 0
x = 0
xy = 0
n = len(xarray)

for i in range(n):
    x2 += xarray[i] ** 2
    y += yarray[i]
    x += xarray[i]
    xy += xarray[i] * yarray[i]

a = (xy * n - x * y) / (x2 * n - x * x)
b = (x2 * y - xy * x) / (x2 * n - x * x)

print("y =", a, "x", "+", b)
