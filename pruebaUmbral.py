from sys import argv

from BitmapFile import BitmapFile
from SectionRaster import SectionRaster

script, path, image = argv

with open(path + image, "rb") as f:
    bmp = BitmapFile(bytearray(f.read()))

map = SectionRaster(bmp, 8)

map.calculateMinima()

map.threshold = 160

for x in range(map.width):
    for y in range(map.height):
        if map.minima[x][y] > map.threshold:
            map.paintBlock(x, y, (255, 255, 255)) # (0, 0, 255)

with open(path + "Rgb_" + str(map.threshold) + "_" + image, "wb") as f:
    f.write(bmp.data)