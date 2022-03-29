from vertex import Vert
from edge import Edge
#   This class represents a face from a mesh in 3d space

class Face:
    def __init__(self, edges):
        self.edges = edges
