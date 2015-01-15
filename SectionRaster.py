class SectionRaster:
    def __init__(self, bmp, pixelSize):
        self.bmp = bmp
        self.pixelSize = pixelSize
        self.width = self.bmp.width // pixelSize
        self.height = self.bmp.height // pixelSize
        self.minimum = 255
        self.maximum = 0
        self.centerOfMass = (self.width // 2, self.height // 2)
        self.minima = [[255 for y in range(self.height)] for x in range(self.width)]
        self.averages = [[0 for y in range(self.height)] for x in range(self.width)]
        self.threshold = 255
        self.foreground = [[False for y in range(self.height)] for x in range(self.width)]
    
    def calculateMinima(self):
        for i in range(self.bmp.start, self.bmp.start + self.bmp.width * self.bmp.height * self.bmp.bpp, self.bmp.bpp):
            pixelX = (i-self.bmp.start) // self.bmp.bpp % self.bmp.width // self.pixelSize
            pixelY = (i-self.bmp.start) // self.bmp.bpp // (self.bmp.width * self.pixelSize)
            if self.bmp.data[i] < self.minima[pixelX][pixelY]:
                self.minima[pixelX][pixelY] = self.bmp.data[i]
            if self.bmp.data[i] < self.minimum:
                self.minimum = self.bmp.data[i]
            if self.bmp.data[i] > self.maximum:
                self.maximum = self.bmp.data[i]

    def calculateAverages(self):
        for i in range(self.bmp.start, self.bmp.start + self.bmp.width * self.bmp.height * self.bmp.bpp, self.bmp.bpp):
            pixelX = (i-self.bmp.start) // self.bmp.bpp % self.bmp.width // self.pixelSize
            pixelY = (i-self.bmp.start) // self.bmp.bpp // (self.bmp.width * self.pixelSize)
            self.averages[pixelX][pixelY] += self.bmp.data[i]
        for x in range(self.width):
            for y in range(self.height):
                self.averages[x][y] = self.averages[x][y] / self.pixelSize ** 2

    def calculateThreshold(self):
        factorDelta = 10
        minTransitionCount = self.width * self.height
        
        for factor in [x / factorDelta for x in range(factorDelta)]:
            threshold = int(self.minimum + factor * (self.maximum - self.minimum))
            foregroundCount = 0
            transitionCount = 0
            isForeground = None
            
            for i in range(self.width):
                for j in range(self.height):
                    if isForeground not in (True,False):
                        isForeground = self.minima[i][j] <= threshold
                    if isForeground != (self.minima[i][j] <= threshold):
                        transitionCount += 1
                        isForeground = self.minima[i][j] <= threshold
                    if isForeground:
                        foregroundCount += 1
            
            if foregroundCount >= self.width*self.height*0.1 and transitionCount < minTransitionCount:
                self.threshold = threshold
                minTransitionCount = transitionCount

    def findForeground(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.minima[x][y] <= self.threshold:
                    self.foreground[x][y] = True

    def erodeForeground(self):
        newForeground = [[False for y in range(self.height)] for x in range(self.width)]

        for x in range(1, self.width-1):
            for y in range(1, self.height-1):
                if self.foreground[x][y] and self.foreground[x-1][y] and self.foreground[x+1][y]:
                    newForeground[x][y] = True

        self.foreground = newForeground
        
    def findCenterOfMass(self):
        count = 0
        totalX = 0
        totalY = 0
        for x in range(1, self.width-1):
            for y in range(1, self.height-1):
                if self.foreground[x][y]:
                    count += 1
                    totalX += x
                    totalY += y
        self.centerOfMass = (totalX // count, totalY // count)

    def paintBlock(self, x, y, rgb):
        blockStart = self.bmp.start + x * self.pixelSize * self.bmp.bpp + y * self.bmp.width * self.pixelSize * self.bmp.bpp
        for i in range(self.pixelSize):
            for j in range(self.pixelSize):
                idx = blockStart + i * self.bmp.bpp + j * self.bmp.width * self.bmp.bpp
                self.bmp.data[idx:idx+3] = rgb

    def cleanBackground(self):
        for x in range(self.width):
            for y in range(self.height):
                if not self.foreground[x][y]:
                    self.paintBlock(x, y, (255, 255, 255))

