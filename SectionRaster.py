class SectionRaster:
    def __init__(self, pixelSize, originalWidth, originalHeight):
        self.pixelSize = pixelSize
        self.width = originalWidth // pixelSize
        self.height = originalHeight // pixelSize
        self.minimum = 255
        self.maximum = 0
        self.minima = [[255 for y in range(self.height)] for x in range(self.width)]