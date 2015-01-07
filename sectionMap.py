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

print("centerOfMass:", map.centerOfMass)

#-------------------------------------------------------------------------------
comX, comY = map.centerOfMass

def findOffsetX(offset, map, comX, comY, sign, limit, bottom, top):
    edge = False
    while not edge:
        offset += 1
        x = comX + offset * sign
        for i in range(offset + 1):
            yBottom = bottom if comY - i < bottom else comY - i
            yTop = top if comY + i > top else comY + i
            if (map.foreground[x][yBottom] or map.foreground[x][yTop]):
                break
            elif i == offset:
                offset -= 1
                edge = True
            elif x == limit:
                edge = True
    return offset
def findOffsetY(offset, map, comX, comY, sign, limit, left, right):
    edge = False
    while not edge:
        offset += 1
        y = comY + offset * sign
        for j in range(offset + 1):
            xLeft = left if comX - j < comX - j else comX - j
            xRight = right if comX + j > right else comX + j
            if (map.foreground[xLeft][y] or
                map.foreground[xRight][y]):
                break
            elif j == offset:
                offset -= 1
                edge = True
            elif y == limit:
                edge = True
    return offset

offsetW = findOffsetX(10, map, comX, comY, -1, 0, 0, map.height - 1)
offsetE = findOffsetX(10, map, comX, comY, 1, map.width - 1, 0, map.height - 1)
offsetS = findOffsetY(2, map, comX, comY, -1, 0, 0, map.width - 1)
offsetN = findOffsetY(10, map, comX, comY, 1, map.height - 1, 0, map.width - 1)

print("offsetW:", offsetW, "offsetE:", offsetE,
    "offsetS:", offsetS, "offsetN:", offsetN)

left = 0 if comX < offsetW else comX - offsetW
right = map.width - 1 if comX + offsetE >= map.width else comX + offsetE
bottom = 0 if comY < offsetS else comY - offsetS
top = map.height - 1 if comY + offsetN >= map.height else comY + offsetN

print("left:", left, "bottom:", bottom, "right:", right, "top:", top)

for x in range(map.width):
    for y in range(map.height):
        if (x < left or  x > right) or (y < bottom or y > top):
            map.foreground[x][y] = False

for y in range(bottom, top + 1):
    xl = right
    xr = left
    xlf = False
    xrf = False
    for x in range(right - left):
        if xlf and xrf:
            break
        if map.foreground[left + x][y] and not xlf:
            xl = left + x
            xlf = True
        if map.foreground[right - x][y] and not xrf:
            xr = right - x
            xrf = True
    for x in range(xl, xr + 1):
        map.foreground[x][y] = True

for x in range(left, right + 1):
    yb = bottom
    yt = top
    ybf = False
    ytf = False
    for y in range(top - bottom):
        if ybf and ytf:
            break
        if map.foreground[x][bottom + y] and not ybf:
            yb = bottom + y
            ybf = True
        if map.foreground[x][top - y] and not ytf:
            yt = top - y
            ytf = True
    for y in range(yb, yt + 1):
        map.foreground[x][y] = True
#-------------------------------------------------------------------------------

map.findCenterOfMass()
comX, comY = map.centerOfMass

print("centerOfMass:", map.centerOfMass)

centerOffsetX = map.width // 2 - comX
centerOffsetY = map.height // 2 - comY

print("centerOffsetX:", centerOffsetX, "centerOffsetY:", centerOffsetY)

#-------------------------------------------------------------------------------

bmp.makeFile(path + image + ".procesada.bmp")

with open(path + image + ".procesada.bmp", "rb") as f:
    bmpCopy = BitmapFile(bytearray(f.read()))

mapCopy = SectionRaster(bmpCopy, 8)

for x in range(map.width):
    for y in range(map.height):
        if map.foreground[x][y]:
            mapCopy.foreground[x+centerOffsetX][y+centerOffsetY] = True
            blockStart = (mapCopy.bmp.start +
                x * mapCopy.pixelSize * mapCopy.bmp.bpp +
                y * mapCopy.bmp.width * mapCopy.pixelSize * mapCopy.bmp.bpp)
            for i in range(mapCopy.pixelSize):
                for j in range(mapCopy.pixelSize):
                    idx = (blockStart +
                        i * mapCopy.bmp.bpp +
                        j * mapCopy.bmp.width * mapCopy.bmp.bpp)
                    idxCopy = (idx +
                        centerOffsetX * mapCopy.pixelSize * mapCopy.bmp.bpp +
                        centerOffsetY * mapCopy.pixelSize * mapCopy.bmp.width * mapCopy.bmp.bpp)
                    mapCopy.bmp.data[idxCopy:idxCopy+3] = map.bmp.data[idx:idx+3]
        if not mapCopy.foreground[x][y]:
            mapCopy.paintBlock(x, y, (255, 255, 255))

map = mapCopy
bmp = bmpCopy
map.centerOfMass = (map.width // 2, map.height // 2)
comX, comY = map.centerOfMass

#-------------------------------------------------------------------------------

middleLeftmost = comX
while map.foreground[middleLeftmost-1][comY]:
    middleLeftmost -= 1

print("middleLeftmost:", middleLeftmost)

leftEdge = [(middleLeftmost, comY)]

initX, initY = (middleLeftmost, comY)
while True:
    initY += 1
    initValue = map.foreground[initX][initY]
    
    x, y = (initX, initY)
    while initValue == map.foreground[x][y] and not abs(initX - x) > 1:
        if not map.foreground[x][y]:
            x += 1
        elif map.foreground[x-1][y]:
            x -= 1
        else:
            break
    if abs(initX - x) > 1:
        break
    else:
        leftEdge.append((x, y))
        initX, initY = (x, y)
#
initX, initY = (middleLeftmost, comY)
while True:
    initY -= 1
    initValue = map.foreground[initX][initY]
    
    x, y = (initX, initY)
    while initValue == map.foreground[x][y] and not abs(initX - x) > 1:
        if not map.foreground[x][y]:
            x += 1
        elif map.foreground[x-1][y]:
            x -= 1
        else:
            break
    if abs(initX - x) > 1:
        break
    else:
        leftEdge.append((x, y))
        initX, initY = (x, y)
#
#
middleRightmost = comX
while map.foreground[middleRightmost+1][comY]:
    middleRightmost += 1

print("middleRightmost:", middleRightmost)

rightEdge = [(middleRightmost, comY)]

initX, initY = (middleRightmost, comY)
while True:
    initY += 1
    initValue = map.foreground[initX][initY]
    
    x, y = (initX, initY)
    while initValue == map.foreground[x][y] and not abs(initX - x) > 1:
        if not map.foreground[x][y]:
            x -= 1
        elif map.foreground[x+1][y]:
            x += 1
        else:
            break
    if abs(initX - x) > 1:
        break
    else:
        rightEdge.append((x, y))
        initX, initY = (x, y)
#
initX, initY = (middleRightmost, comY)
while True:
    initY -= 1
    initValue = map.foreground[initX][initY]
    
    x, y = (initX, initY)
    while initValue == map.foreground[x][y] and not abs(initX - x) > 1:
        if not map.foreground[x][y]:
            x -= 1
        elif map.foreground[x+1][y]:
            x += 1
        else:
            break
    if abs(initX - x) > 1:
        break
    else:
        rightEdge.append((x, y))
        initX, initY = (x, y)
#
for i in range(len(leftEdge)):
    x, y = leftEdge[i]
    map.paintBlock(x, y, (0, 0, 255))
#
for i in range(len(rightEdge)):
    x, y = rightEdge[i]
    map.paintBlock(x, y, (0, 0, 255))

#-------------------------------------------------------------------------------

#bmpCopy.makeFile(path + image + ".procesada.bmp")
bmp.makeFile(path + image + ".procesada.bmp")
print(path + image + ".procesada.bmp")
