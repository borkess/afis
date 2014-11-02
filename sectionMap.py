from sys import argv

from BitmapFile import BitmapFile
from SectionRaster import SectionRaster

script, path, image = argv

with open(path + image, "rb") as f:
    bmp = BitmapFile(bytearray(f.read()))

map = SectionRaster(bmp, 8)
print("map.width:", map.width, "map.height:", map.height)

map.calculateMinima()

print("map.minimum:", map.minimum, "map.maximum:", map.maximum)

map.calculateThreshold()

print("map.threshold:", map.threshold)

map.findForeground()

map.erodeForeground()
map.erodeForeground()
map.erodeForeground()

map.cleanBackground()

bmp.makeFile(path + image + "." + str(map.threshold) + ".bmp")