class SectionRaster:
    def __init__(self, bmp, pixelSize):
        self.bmp = bmp
        self.pixelSize = pixelSize
        self.width = self.bmp.width // pixelSize
        self.height = self.bmp.height // pixelSize
        self.minimum = 255
        self.maximum = 0
        self.minima = [[255 for y in range(self.height)] for x in range(self.width)]
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

    def paintBlock(self, x, y, rgb):
        blockStart = self.bmp.start + x * self.pixelSize * self.bmp.bpp + y * self.bmp.width * self.pixelSize * self.bmp.bpp
        for i in range(self.pixelSize):
            for j in range(self.pixelSize):
                idx = blockStart + i * self.bmp.bpp + j * self.bmp.width * self.bmp.bpp
                self.bmp.data[idx:idx+3] = rgb