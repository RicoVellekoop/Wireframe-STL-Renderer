import struct   #   This library is used to convert bytes into floats. I use this to load a stl file.
from vector3d import Vec3
from vertex import Vert
from edge import Edge
from face import Face
from matrix import Matrix
#   This class represents a 3d object

class Mesh:
    def __init__(self, faces):
        self.faces = faces              #   This list contains all faces in the object

        self.scalingMatrixes = []       #   This list contains all matrixes used for scaling an object
        self.rotationMatrixes = []      #   This list contains all matrixes used for rotating an object
        self.translationMatrixes = []   #   This list contains all matrixes used for moving an object

    def scale(self, scalar):
        self.scalingMatrixes.append(Matrix.scalingMatrix(scalar))   #   Creates a scaling matrix and adds it to the list

    def move(self, point):
        self.translationMatrixes.append(Matrix.translationMatrix(point))    #   Creates a translation matrix and adds it to the list

    def rotate(self, axis, value):
        self.rotationMatrixes.append(Matrix.rotationMatrix(axis, value))    #   Creates a rotation matrix and adds it to the list

    def getLines(self): #   Applies all transformation matrixes and the projection matrix to all of the vertecies in a mesh and returns a list of 2d coördinates to draw the lines
        lines = []

        #   Combines all transformation matrixes into one matrix in the right order(Scaling -> Rotation -> Translation)
        finalMatrix = Matrix([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
        for matrix in self.translationMatrixes:
            finalMatrix = finalMatrix.mulMatrix(matrix)
        for matrix in self.rotationMatrixes:
            finalMatrix = finalMatrix.mulMatrix(matrix)
        for matrix in self.scalingMatrixes:
            finalMatrix = finalMatrix.mulMatrix(matrix)

        #   Multiplies the projection matrix with the transformation matrix to make the matrix applied to the vertecies
        finalMatrix = Matrix([[-1,0,0,0],[0,-1,0,0],[0,0,-1,0],[0,0,1,0]]).mulMatrix(finalMatrix)

        #   Loops trought lines in all of the faces of the mesh
        for face in self.faces:
            for edge in face.edges:
                lines.append((finalMatrix.project(edge.vert1), finalMatrix.project(edge.vert2))) #  Adds the transformed and projected startpoint and endpoint of each line to the list
        return lines


#   This function here is not needed for the asignment, but I wanted to show something i've tested. This function can create a mesh object using a binary STL file.
    @classmethod
    def loadSTL(cls, path):
        file = open(path, "rb")
        file.read(80)

        faceCount = int.from_bytes(file.read(4), "little")

        faces = [0 for face in range(faceCount)]

        for face in range(faceCount):
            normalvec = Vec3(struct.unpack('<f', file.read(4))[0], struct.unpack('<f', file.read(4))[0], struct.unpack('<f', file.read(4))[0])
            vert1 = Vert.createVert(struct.unpack('<f', file.read(4))[0], struct.unpack('<f', file.read(4))[0], struct.unpack('<f', file.read(4))[0])
            vert2 = Vert.createVert(struct.unpack('<f', file.read(4))[0], struct.unpack('<f', file.read(4))[0], struct.unpack('<f', file.read(4))[0])
            vert3 = Vert.createVert(struct.unpack('<f', file.read(4))[0], struct.unpack('<f', file.read(4))[0], struct.unpack('<f', file.read(4))[0])
            edges = [Edge(vert1,vert2), Edge(vert2,vert3), Edge(vert3,vert1)]
            colorData = file.read(2)

            faces[face] = Face(edges)
        return cls(faces)
