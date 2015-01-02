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

map.findCenterOfMass()

#-------------------------------------------------------------------------------
comX, comY = map.centerOfMass

def encontrarOffsetX(offset, map, comX, comY, sign, limit):
    edge = False
    while not edge:
        offset += 1
        for i in range(offset + 1):
            if (map.foreground[comX+offset*sign][comY-i] or
                map.foreground[comX+offset*sign][comY+i]):
                break
            elif comX+offset*sign == limit:
                edge = True
            elif i == offset:
                offset -= 1
                edge = True
    return offset
def encontrarOffsetY(offset, map, comX, comY, sign, limit):
    edge = False
    while not edge:
        offset += 1
        for j in range(offset + 1):
            if (map.foreground[comX-j][comY+offset*sign] or
                map.foreground[comX+j][comY+offset*sign]):
                break
            elif comX+offset*sign == limit:
                edge = True
            elif j == offset:
                offset -= 1
                edge = True
    return offset
    

offsetW = encontrarOffsetX(10, map, comX, comY, -1, 0)
offsetE = encontrarOffsetX(10, map, comX, comY, 1, map.width-1)
offsetS = encontrarOffsetY(2, map, comX, comY, -1, 0)
offsetN = encontrarOffsetY(10, map, comX, comY, 1, map.height-1)

left = 0 if comX < offsetW else comX-offsetW
right = map.width-1 if comX+offsetE >= map.width else comX+offsetE
bottom = 0 if comY < offsetS else comY-offsetS
top = map.height-1 if comY+offsetN >= map.height else comY+offsetN

#"""
for x in range(map.width):
    for y in range(map.height):
        if x not in range(left, right) or y not in range(bottom, top):
            map.foreground[x][y] = False

for y in range(bottom, top):
    xl = left
    xr = right
    xlf = False
    xrf = False
    for x in range(right-left):
        if map.foreground[left+x][y] and not xlf:
            xl = left+x
            xlf = True
        if map.foreground[right-x][y] and not xrf:
            xr = right-x
            xrf = True
        if xlf and xrf:
            break
    for x in range(xl, xr+1):
        map.foreground[x][y] = True

for x in range(left, right):
    yb = bottom
    yt = top
    ybf = False
    ytf = False
    for y in range(top-bottom):
        if map.foreground[x][bottom+y] and not ybf:
            yb = bottom+y
            ybf = True
        if map.foreground[x][top-y] and not ytf:
            yt = top-y
            ytf = True
        if ybf and ytf:
            break
    for y in range(yb, yt+1):
        map.foreground[x][y] = True
"""
for x in range(map.width):
    for y in range(map.height):
        map.foreground[x][y] = (
                                #map.minima[x][y] <= map.threshold and
                                x in range(left+1, right) and
                                y in range(bottom+1, top)
                                )
#"""
#-------------------------------------------------------------------------------

map.cleanBackground()

#-------------------------------------------------------------------------------
print("centerOfMass: ", map.centerOfMass)
map.paintBlock(comX, comY, (0, 0, 255))

print("offsetW: ", offsetW, "offsetE: ", offsetE, "offsetS: ", offsetS, "offsetN: ", offsetN)
print("left: ", left, "bottom: ", bottom, "right: ", right, "top: ", top)
map.paintBlock(left, bottom, (0, 0, 255))
map.paintBlock(right, bottom, (0, 0, 255))
map.paintBlock(left, top, (0, 0, 255))
map.paintBlock(right, top, (0, 0, 255))
#-------------------------------------------------------------------------------

bmp.makeFile(path + image + "." + str(map.threshold) + ".bmp")


