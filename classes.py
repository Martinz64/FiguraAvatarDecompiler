from pyexpat import model
from unicodedata import name
import uuid
import string
import random

class Element:
    Name = ""
    Children = []
    UUID = ""
    def __init__(self, name, children = []) -> None:
        self.Name = name
        self.Children = children
        self.UUID = str(uuid.uuid4())

class Group(Element):
    AnchorType = None
    Pivot = (0,0,0)
    Rotation = (0,0,0)
    Visible = True
    def __init__(self, name, anchor, pivot, rotation, visible, children=[]) -> None:
        super().__init__(name, children)
        self.AnchorType = anchor
        self.Pivot = pivot
        self.Visible = visible
        self.Rotation = rotation

class Cube(Element):
    From = (0,0,0)
    To = (0,0,0)
    Pivot = (0,0,0)
    Rotation = (0,0,0)
    Inflate = 0
    Visible = True
    Faces = []
    def __init__(self, name, from_c, to, pivot, rotation, inflate, visible, faces) -> None:
        super().__init__(name, [])
        self.From = from_c
        self.To = to
        self.Pivot = pivot
        self.Rotation = rotation
        self.Inflate = inflate
        self.Visible = visible
        self.Faces = faces

class CubeFace:
    UV = (0,0,0,0)
    Rotation = 0
    TextureID = 0
    Enabled = True
    def __init__(self,enabled,texture,rotation,uv) -> None:
        self.Enabled = enabled
        self.TextureID = texture
        self.Rotation = rotation
        self.UV = uv

class Mesh(Element):
    Pivot = (0,0,0)
    Rotation = (0,0,0)
    Inflate = 0
    Visible = True
    Faces = []
    Vertices = []
    def __init__(self, name, pivot, rotation, visible, vertices, faces) -> None:
        super().__init__(name, [])
        self.Pivot = pivot
        self.Rotation = rotation
        self.Visible = visible
        self.Faces = faces
        self.Vertices = vertices

class MeshFace:
    ""
    VertexIDs = []
    UVs = []
    ID = ""
    TextureID = 0
    def __init__(self,vIDs,uvs,texID) -> None:
        self.VertexIDs = vIDs
        self.UVs = uvs
        self.TextureID = texID
        self.ID = ''.join(random.sample(string.ascii_letters,6))


class MeshVertex:
    Coords = (0,0,0)
    ID = ""
    def __init__(self,coords) -> None:
        self.Coords = coords
        self.ID = ''.join(random.sample(string.ascii_letters,6))

class Texture:
    ID = 0
    Name = ""
    Data = bytearray()
    def __init__(self,id,name,data) -> None:
        self.ID = id
        self.Name = name
        self.Data = data

class Script:
    Name = ""
    Content = ""
    def __init__(self,name,content) -> None:
        self.Name = name
        self.Content = content

class Avatar:
    Model = None
    Textures = []
    Scripts = []
    def __init__(self,model,textures,scripts) -> None:
        self.Model = model
        self.Textures = textures
        self.Scripts = scripts