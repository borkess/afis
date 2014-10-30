from sys import argv

from BitmapFile import BitmapFile
from SectionRaster import SectionRaster

script, image = argv
with open(image, "rb") as f:
    bmp = BitmapFile(bytearray(f.read()))


map = SectionRaster(8, bmp.width, bmp.height)

map.minimum = 255
map.maximum = 0
map.minima = [[255 for y in range(map.height)] for x in range(map.width)]

threshold = 181

for i in range(bmp.start, bmp.start + bmp.width * bmp.height * bmp.bpp, bmp.bpp):
    pixelX = (i-bmp.start) // bmp.bpp % bmp.width // map.pixelSize
    pixelY = (i-bmp.start) // bmp.bpp // (bmp.width * map.pixelSize)
    
    if bmp.data[i] < map.minima[pixelX][pixelY]:
        map.minima[pixelX][pixelY] = bmp.data[i]
    if bmp.data[i] < map.minimum:
        map.minimum = bmp.data[i]
    if bmp.data[i] > map.maximum:
        map.maximum = bmp.data[i]

for x in range(map.width):
    for y in range(map.height):
        block = bmp.start + y*bmp.width*map.pixelSize*bmp.bpp + x*map.pixelSize*bmp.bpp
        if map.minima[x][y] > threshold:
            for i in range(map.pixelSize):
                for j in range(map.pixelSize):
                    idx = block + bmp.bpp*i + bmp.width*bmp.bpp*j
                    bmp.data[idx:idx+3] = 255, 255, 255
                    #bmp.data[idx:idx+3] = 0, 0, 255

with open("Rgb_" + str(threshold) + "_" + image, "wb") as f:
    f.write(bmp.data)