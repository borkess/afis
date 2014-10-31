from sys import argv

from BitmapFile import BitmapFile
from SectionRaster import SectionRaster

script, path, image = argv

with open(path + image, "rb") as f:
    bmp = BitmapFile(bytearray(f.read()))

map = SectionRaster(bmp, 8)
print("map.width:", map.width, "map.height:", map.height)

map.calculateMinima()

print("map.minimum", map.minimum)
print("map.maximum", map.maximum)
print("map.minima.19.19", map.minima[19][19])

factorDelta = 10
minTransitionCount = map.width * map.height

for factor in [x / factorDelta for x in range(factorDelta)]:
    threshold = int(map.minimum + factor * (map.maximum - map.minimum))
    
    foregroundCount = 0
    transitionCount = 0
    isForeground = None
    
    for i in range(map.width):
        for j in range(map.height):
            if isForeground not in (True,False):
                isForeground = map.minima[i][j] <= threshold
                
            if isForeground != (map.minima[i][j] <= threshold):
                transitionCount += 1
                isForeground = map.minima[i][j] <= threshold
            
            if isForeground:
                foregroundCount += 1
    
    if foregroundCount >= map.width*map.height*0.1 and transitionCount < minTransitionCount:
        map.threshold = threshold
        minTransitionCount = transitionCount
    
    print("factor:", factor, "threshold:", threshold, 
        "foregroundCount:", foregroundCount, "transitionCount:", transitionCount)

print("map.threshold:", map.threshold)

for x in range(map.width):
    for y in range(map.height):
        if map.minima[x][y] > map.threshold:
            map.foreground = True
            map.paintBlock(x, y, (255, 255, 255))

with open(path + image + "." + str(map.threshold) + ".bmp", "wb") as f:
    f.write(bmp.data)