import math
from vertex import Vert
#   This class is used to do math using matrixes

class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix

    @classmethod                    #   This function makes a scaling matrix for the values given
    def scalingMatrix(cls, scalar):
        if type(scalar) != tuple:   #   If only a single value is given it will convert that value in a truple with each value being that value
            scalar = (scalar,scalar,scalar)

        return cls([[scalar[0],0,0,0],[0,scalar[1],0,0],[0,0,scalar[2],0],[0,0,0,1]])

    @classmethod                        #   This function makes a translation matrix for the values given
    def translationMatrix(cls, pos):
        if type(pos) != tuple:          #   If only a single value is given it will convert that value in a truple with each value being that value
            pos = (pos,pos,pos)

        return cls([[1,0,0,pos[0]],[0,1,0,pos[1]],[0,0,1,pos[2]],[0,0,0,1]])

    @classmethod     #   This function makes a rotation matrix for a given angle around a given axis
    def rotationMatrix(cls, axis, value):
        angle = value/180*math.pi   #   converts the angle from degrees to radians
        if axis == "x":     #   Returns a rotation matrix around the X axis if that axis is specified
            return cls([[1,0,0,0],[0,math.cos(angle),-math.sin(angle),0],[0,math.sin(angle),math.cos(angle),0],[0,0,0,1]])
        elif axis == "y":   #   Returns a rotation matrix around the Y axis if that axis is specified
            return cls([[math.cos(angle),0,math.sin(angle),0],[0,1,0,0],[-math.sin(angle),0,math.cos(angle),0],[0,0,0,1]])
        elif axis == "z":   #   Returns a rotation matrix around the Z axis if that axis is specified
            return cls([[math.cos(angle),-math.sin(angle),0,0],[math.sin(angle),math.cos(angle),0,0],[0,0,1,0],[0,0,0,1]])
        else:
            raise Exception('Axis not found')

    def mulMatrix(self, other):     #   Multiplies this matrix with an other matrix
        if len(self.matrix[0]) == len(other.matrix):
            result = [[0 for col in range(len(other.matrix[0]))] for row in range(len(self.matrix))]
            for row in range(len(result)):
                for col in range(len(result[0])):
                    for val in range(len(self.matrix[0])):
                        result[row][col] += self.matrix[row][val]*other.matrix[val][col]
            return Matrix(result)
        else:
            raise Exception('These matrixes can not be multiplied')

    def project(self, vert):    #   Multiplies the is matrix with the coördinates of a vertex, and returns the projected X and Y coördinate as a truple
        vec = [vert.vec3.x, vert.vec3.y, vert.vec3.z, 1]
        result = 4*[0]
        if len(self.matrix[0]) == len(vec):
            for col in range(len(self.matrix)):
                for val in range(len(self.matrix[0])):
                    result[col] += self.matrix[col][val]*vec[val]
            return (result[0]/result[3], result[1]/result[3])
        else:
            raise Exception('These maxrix can not be multiplied with this vertex')
