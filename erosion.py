from sys import argv

from BitmapFile import BitmapFile
from SectionRaster import SectionRaster

script, path, image = argv

with open(path + image, "rb") as f:
    bmp = BitmapFile(bytearray(f.read()))

map = SectionRaster(bmp, 8)

map.calculateMinima()

map.calculateThreshold()

map.findForeground()

map.erodeForeground()
map.erodeForeground()
map.erodeForeground()

map.findCenterOfMass()

comX, comY = map.centerOfMass

map.cleanBackground()

map.paintBlock(comX, comY, (0, 0, 255))

bmp.makeFile(path + image + ".eroded.bmp")


