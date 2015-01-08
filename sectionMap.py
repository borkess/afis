from sys import argv

from BitmapFile import BitmapFile
from SectionRaster import SectionRaster

script, path, image = argv

with open(path + image, "rb") as f:
    bmp = BitmapFile(bytearray(f.read()))

mapa = SectionRaster(bmp, 8)
print("map.width:", mapa.width, "map.height:", mapa.height)

mapa.calculateMinima()

print("map.minimum:", mapa.minimum, "map.maximum:", mapa.maximum)

mapa.calculateThreshold()

print("map.threshold:", mapa.threshold)

mapa.findForeground()

mapa.erodeForeground()
mapa.erodeForeground()
mapa.erodeForeground()

mapa.findCenterOfMass()

print("centerOfMass:", mapa.centerOfMass)

#-------------------------------------------------------------------------------
comX, comY = mapa.centerOfMass

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

offsetW = findOffsetX(10, mapa, comX, comY, -1, 0, 0, mapa.height - 1)
offsetE = findOffsetX(10, mapa, comX, comY, 1, mapa.width - 1, 0, mapa.height - 1)
offsetS = findOffsetY(2, mapa, comX, comY, -1, 0, 0, mapa.width - 1)
offsetN = findOffsetY(10, mapa, comX, comY, 1, mapa.height - 1, 0, mapa.width - 1)

print("offsetW:", offsetW, "offsetE:", offsetE,
    "offsetS:", offsetS, "offsetN:", offsetN)

left = 0 if comX < offsetW else comX - offsetW
right = mapa.width - 1 if comX + offsetE >= mapa.width else comX + offsetE
bottom = 0 if comY < offsetS else comY - offsetS
top = mapa.height - 1 if comY + offsetN >= mapa.height else comY + offsetN

print("left:", left, "bottom:", bottom, "right:", right, "top:", top)

for x in range(mapa.width):
    for y in range(mapa.height):
        if (x < left or  x > right) or (y < bottom or y > top):
            mapa.foreground[x][y] = False

for y in range(bottom, top + 1):
    xl = right
    xr = left
    xlf = False
    xrf = False
    for x in range(right - left):
        if xlf and xrf:
            break
        if mapa.foreground[left + x][y] and not xlf:
            xl = left + x
            xlf = True
        if mapa.foreground[right - x][y] and not xrf:
            xr = right - x
            xrf = True
    for x in range(xl, xr + 1):
        mapa.foreground[x][y] = True

for x in range(left, right + 1):
    yb = bottom
    yt = top
    ybf = False
    ytf = False
    for y in range(top - bottom):
        if ybf and ytf:
            break
        if mapa.foreground[x][bottom + y] and not ybf:
            yb = bottom + y
            ybf = True
        if mapa.foreground[x][top - y] and not ytf:
            yt = top - y
            ytf = True
    for y in range(yb, yt + 1):
        mapa.foreground[x][y] = True
#-------------------------------------------------------------------------------

mapa.findCenterOfMass()
comX, comY = mapa.centerOfMass

print("centerOfMass:", mapa.centerOfMass)

centerOffsetX = mapa.width // 2 - comX
centerOffsetY = mapa.height // 2 - comY

print("centerOffsetX:", centerOffsetX, "centerOffsetY:", centerOffsetY)

#-------------------------------------------------------------------------------

bmp.makeFile(path + image + ".procesada.bmp")

with open(path + image + ".procesada.bmp", "rb") as f:
    bmpCopy = BitmapFile(bytearray(f.read()))

mapCopy = SectionRaster(bmpCopy, 8)

for x in range(mapa.width):
    for y in range(mapa.height):
        if mapa.foreground[x][y]:
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
                    mapCopy.bmp.data[idxCopy:idxCopy+3] = mapa.bmp.data[idx:idx+3]
        if not mapCopy.foreground[x][y]:
            mapCopy.paintBlock(x, y, (255, 255, 255))

mapa = mapCopy
bmp = bmpCopy
mapa.centerOfMass = (mapa.width // 2, mapa.height // 2)
comX, comY = mapa.centerOfMass

#-------------------------------------------------------------------------------

middleLeftmost = comX
while mapa.foreground[middleLeftmost-1][comY]:
    middleLeftmost -= 1

print("middleLeftmost:", middleLeftmost)

leftEdge = [(middleLeftmost, comY)]

initX, initY = (middleLeftmost, comY)
while True:
    initY += 1
    initValue = mapa.foreground[initX][initY]
    
    x, y = (initX, initY)
    while initValue == mapa.foreground[x][y] and not abs(initX - x) > 1:
        if not mapa.foreground[x][y]:
            x += 1
        elif mapa.foreground[x-1][y]:
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
    initValue = mapa.foreground[initX][initY]
    
    x, y = (initX, initY)
    while initValue == mapa.foreground[x][y] and not abs(initX - x) > 1:
        if not mapa.foreground[x][y]:
            x += 1
        elif mapa.foreground[x-1][y]:
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
while mapa.foreground[middleRightmost+1][comY]:
    middleRightmost += 1

print("middleRightmost:", middleRightmost)

rightEdge = [(middleRightmost, comY)]

initX, initY = (middleRightmost, comY)
while True:
    initY += 1
    initValue = mapa.foreground[initX][initY]
    
    x, y = (initX, initY)
    while initValue == mapa.foreground[x][y] and not abs(initX - x) > 1:
        if not mapa.foreground[x][y]:
            x -= 1
        elif mapa.foreground[x+1][y]:
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
    initValue = mapa.foreground[initX][initY]
    
    x, y = (initX, initY)
    while initValue == mapa.foreground[x][y] and not abs(initX - x) > 1:
        if not mapa.foreground[x][y]:
            x -= 1
        elif mapa.foreground[x+1][y]:
            x += 1
        else:
            break
    if abs(initX - x) > 1:
        break
    else:
        rightEdge.append((x, y))
        initX, initY = (x, y)
#
#
middleTopmost = comY
while mapa.foreground[comX][middleTopmost+1]:
    middleTopmost += 1

print("middleTopmost:", middleTopmost)

topEdge = [(comX, middleTopmost)]

initX, initY = (comX, middleTopmost)
while True:
    initX += 1
    initValue = mapa.foreground[initX][initY]

    x, y = (initX, initY)
    while initValue == mapa.foreground[x][y] and not abs(initY - y) > 1:
        if not mapa.foreground[x][y]:
            y -= 1
        elif mapa.foreground[x][y+1]:
            y += 1
        else:
            break
    if abs(initY - y) > 1:
        break
    else:
        topEdge.append((x, y))
        initX, initY = (x, y)
#
initX, initY = (comX, middleTopmost)
while True:
    initX -= 1
    initValue = mapa.foreground[initX][initY]

    x, y = (initX, initY)
    while initValue == mapa.foreground[x][y] and not abs(initY - y) > 1:
        if not mapa.foreground[x][y]:
            y -= 1
        elif mapa.foreground[x][y+1]:
            y += 1
        else:
            break
    if abs(initY - y) > 1:
        break
    else:
        topEdge.append((x, y))
        initX, initY = (x, y)
#
for i in range(len(leftEdge)):
    x, y = leftEdge[i]
    mapa.paintBlock(x, y, (0, 0, 255))
#
for i in range(len(rightEdge)):
    x, y = rightEdge[i]
    mapa.paintBlock(x, y, (0, 255, 0))
#
for i in range(len(topEdge)):
    x, y = topEdge[i]
    mapa.paintBlock(x, y, (255, 0, 0))

#-------------------------------------------------------------------------------

#bmpCopy.makeFile(path + image + ".procesada.bmp")
bmp.makeFile(path + image + ".procesada.bmp")
print(path + image + ".procesada.bmp")
