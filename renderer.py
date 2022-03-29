from mesh import Mesh
from BMPreader import Image
#   This class renders a list of meshes

class Renderer:
    def __init__(self, width, hight, meshes = []):
        self.screen = Image.createImage(width, hight)
        self.meshes = meshes
        self.width = width
        self.hight = hight

    def addMesh(self, mesh):    #   This function adds a mesh to the list of meshes
        self.meshes.append(mesh)

    def renderWireFrame(self):  #   Renders a wireframe model of all the meshes in the meshes list
        for mesh in self.meshes:
            for line in mesh.getLines():    #   Calls the getLines function for all of the meshes to get the transformed and projected vertex coördinates
                self.screen.drawLine(self.deNormalise(line[0]), self.deNormalise(line[1]), 4)   # Draws all lines from the funtion getLines on the screen
        self.screen.saveImage("output.bmp")
        print("Saved Image to \"output.bmp\"")

    #   Scales the coördinates to the screen hight and centers the 0,0 point in the middle of the screen.
    def deNormalise(self, point):
        return (self.width/2+point[0]*self.hight/2, self.hight/2+point[1]*self.hight/2)
