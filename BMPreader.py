import math

class Image:
    def __init__(self, data):
        self.imageData = data;
        self.width = len(data)
        self.hight = len(data[0])


    @classmethod
    def loadBMP(cls, filename):
        file = open(filename, "rb")
        if file.read(2).decode("utf-8") != "BM":
            raise Exception("This is not a vallid BMP file.")
        file.read(8)

        if int.from_bytes(file.read(4), "little") != 54:
            raise Exception("This bmp format is not supported")
        file.read(4)

        width = int.from_bytes(file.read(4), "little")
        hight = int.from_bytes(file.read(4), "little")

        file.read(2)

        if int.from_bytes(file.read(2), "little") != 24 or int.from_bytes(file.read(4), "little") != 0:
            raise Exception("This bmp format is not supported")

        file.read(20)

        imageData = [[[0 for rgb in range(3)] for y in range(hight)] for x in range(width)]
        padding = (4 - (width * 3) % 4) % 4

        for y in range(hight):
            for x in range(width):
                for rgb in range(3):
                    imageData[x][hight-y-1][2-rgb] = file.read(1)[0]
            file.read(padding)

        file.close()

        return cls(imageData)

    @classmethod
    def createImage(cls, width, hight):
        imageData = [[[0 for rgb in range(3)] for y in range(hight)] for x in range(width)]
        return cls(imageData)

    def getWidth(self):
        return self.width

    def getHight(self):
        return self.hight

    def getPixel(self, x, y):
        return (self.imageData[x][y][0]/255.0,self.imageData[x][y][1]/255.0,self.imageData[x][y][2]/255.0)

    def setPixel(self, x, y, c = 1):
        if type(c) != tuple:
            c = (c,c,c)
        for rgb in range(3):
            if 0 <= x < self.width and 0 <= y < self.hight:
                self.imageData[x][y][rgb] = max(min(round(c[rgb]*255), 255), 0)

    # This is the code to draw a line without anti-aliasing. The code with anti-aliasing is based on this code.
    def drawLineWithoutAntiAliasing(self, p0, p1):
        x0 = round(p0[0])
        y0 = round(p0[1])
        x1 = round(p1[0])
        y1 = round(p1[1])

        if x0 != x1: # Checks if the line is vertical, becouse this would result in a 0 devision and a line with an infinite slope
            a = (y0-y1)/(x0-x1)     # Calculates the slope of the line
            b = y0 - a*x0           # Calculates the starting position of the line

            if abs(a) < 1: #  Checks if the difference in Y value is smaller than the difference in x value. If it is it will draw a pixel in every column, otherwise in every line.
                for x in range(min(x0,x1), max(x0,x1)+1):   # Loops trought all x values from the smallest to the largest
                    self.setPixel(x, round(a*x + b))           # Calculates the Y value for each x value, and adds a point to the grid on that coördinate
            else:
                for y in range(min(y0,y1), max(y0,y1)+1):   # Same code as above, but loops trought Y values and calculates x
                    self.setPixel(round((y-b)/a), y)

        else:   # If the line is vertical this loop will draw a vertical line
            for y in range(min(y0,y1), max(y0,y1)+1):
                self.setPixel(x0, y)

    def drawLine(self, p0, p1, AAscale = 1):
        # Largely the same as the function above
        x0 = round(p0[0])
        y0 = round(p0[1])
        x1 = round(p1[0])
        y1 = round(p1[1])

        AAscale = round(AAscale)    # the folowing lines make sure the scale is a round, positive number to fix faulty inputs
        if AAscale < 1:
            AAscale = 1

        if x0 != x1:
            a = (y0-y1)/(x0-x1)
            b = y0 - a*x0


            if abs(a) < 1:
                lastValue = round(a*min(x0,x1) + b)             # This variable is used to detect when the line enters a new pixel
                for xBase in range(min(x0,x1), max(x0,x1)+1):   # Loops trought all x values from the smallest to the largest
                    counter = 0                                 # This variable keeps track of how many times the line has been in a pixel before leaving the pixel
                    for s in range(AAscale):                    # In this loop the Y coördinates for the X coördinates between the current xBase and the next xBase are calculated
                                                                # The amount of X coördinates calculated is the value of AAscale
                        x = xBase + s/AAscale                   # Calculates a fractional x coördinate between the current xBase and the next xBase
                        if round(a*x + b) == lastValue:         # If the line is still in the same pixel for the fractional x coördinate the counter gets incremented
                            counter += 1
                        else:   # If the line goes one pixel up or down the last pixel is drawn with a color based on the counter, the counter is reset, and the lastValue is set to the new value
                            self.setPixel(xBase, lastValue, counter/AAscale)
                            counter = 1
                            lastValue = round(a*x + b)
                    self.setPixel(xBase, lastValue, counter/AAscale)   # Adds the point to the grid when going to the next xBase coördinate
            else:   # Works the same way as above, but with Y instead of X
                lastValue = round((min(y0,y1)-b)/a)

                for yBase in range(min(y0,y1), max(y0,y1)+1):
                    counter = 0
                    for s in range(AAscale):
                        y = yBase + s/AAscale
                        if round((y-b)/a) == lastValue:
                            counter += 1
                        else:
                            self.setPixel(lastValue, yBase, counter/AAscale)
                            counter = 1
                            lastValue = round((y-b)/a)
                    self.setPixel(lastValue, yBase, counter/AAscale)
        else:
            for y in range(min(y0,y1), max(y0,y1)+1):
                self.setPixel(x0, y)


    def saveImage(self, path):  #   Saves the image as a BMP file
        #   This uses code from an older project of mine where I've made a program to read and write BMP files
        #   Create a byte array with the right header information
        bHight = self.hight.to_bytes(4, 'little')
        bWidth = self.width.to_bytes(4, 'little')
        header = b'BMF\x00\x00\x00\x00\x00\x00\x006\x00\x00\x00(\x00\x00\x00' + bWidth + bHight + b'\x01\x00\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

        file = open(path, "wb")
        file.write(header)

        padding = (4 - (self.width * 3) % 4) % 4    #   This calculates how many empty bytes should be after a row of pixels due to the bmp format

        #   Writes all the color information to the bmp file
        for y in range(self.hight):
            for x in range(self.width):
                file.write(bytes(self.imageData[x][self.hight-y-1])[::-1])
            for pad in range(padding):
                file.write(bytes(0))

        file.close()
