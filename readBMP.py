from sys import argv

from BitmapFile import BitmapFile

script, image = argv
with open(image, "rb") as f:
    bmp = BitmapFile(bytearray(f.read()))
    
print("size: ", bmp.size)
print("start: ", bmp.start)
print("width: ", bmp.width)
print("height: ", bmp.height)
print("depth: ", bmp.depth)
print("bpp: ", bmp.bpp)