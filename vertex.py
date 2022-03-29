from vector3d import Vec3
#   This class represents a point in a 3d space which is part of a mesh

class Vert:
    def __init__(self, vec3):   #   This function creates a vertex using a 3d vector as position
        self.vec3 = vec3

    @classmethod
    def createVert(cls, x, y, z):   #   This function creates a vertex using a x, y, and z coördinate as position
        return cls(Vec3(x, y, z))
