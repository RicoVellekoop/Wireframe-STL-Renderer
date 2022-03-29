from mesh import Mesh
from renderer import Renderer
from vertex import Vert
from edge import Edge
from face import Face

#   If this variable is true it will render a STL file instead of the cube specified in the assignment. This is not part of the assignment, but I've made it for fun so I added this to show it
r = Renderer(1280,720)  #   Creates a renderer object with a resolution of 1280x720

#   Loads the stl file into an object and transformes it
m = Mesh.loadSTL("Susan.stl")
m.scale(0.8)

m.rotate("z", 180)
m.rotate("x", -70)
m.rotate("z", 140)

m.move((0,0,-2))


r.addMesh(m)        #   Adds the mesh in the renderer object
r.renderWireFrame() #   Renders a wireframe model for all of the meshes in the renderer
