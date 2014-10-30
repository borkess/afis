from sys import argv

from BitmapFile import BitmapFile
from SectionRaster import SectionRaster

script, image = argv

with open(image, "rb") as f:
    bmp = BitmapFile(bytearray(f.read()))

map = SectionRaster(8, bmp.width, bmp.height)
print("map.width:", map.width, "map.height:", map.height)

for i in range(bmp.start, bmp.start + bmp.width * bmp.height, bmp.bpp):
    pixelX = (i-bmp.start) // bmp.bpp % bmp.width // map.pixelSize
    pixelY = (i-bmp.start) // bmp.bpp // (bmp.width * map.pixelSize)
    
    if bmp.data[i] < map.minima[pixelX][pixelY]:
        map.minima[pixelX][pixelY] = bmp.data[i]
    if bmp.data[i] < map.minimum:
        map.minimum = bmp.data[i]
    if bmp.data[i] > map.maximum:
        map.maximum = bmp.data[i]

print("map.minimum", map.minimum)
print("map.maximum", map.maximum)
print("map.minima.19.19", map.minima[19][19])

factorDelta = 10
finalThreshold = 255
finalTransitionCount = map.width * map.height

for factor in [x / factorDelta for x in range(factorDelta)]:
    threshold = int(map.minimum + factor * (map.maximum - map.minimum))
    
    foregroundCount = 0
    transitionCount = 0
    isForeground = 0
    
    for i in range(map.width):
        for j in range(map.height):
            if isForeground not in (True,False):
                isForeground = map.minima[i][j] <= threshold
                
            if isForeground != (map.minima[i][j] <= threshold):
                transitionCount += 1
                isForeground = map.minima[i][j] <= threshold
            
            if isForeground:
                foregroundCount += 1
    
    if foregroundCount >= map.width*map.height*0.1 and transitionCount < finalTransitionCount:
        finalThreshold = threshold
        finalTransitionCount = transitionCount
    
    print("factor:", factor, "threshold:", threshold, 
        "foregroundCount:", foregroundCount, "transitionCount:", transitionCount)

print("finalThreshold:", finalThreshold)