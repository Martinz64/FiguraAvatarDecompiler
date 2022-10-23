import jsonpickle
from classes import *
import json
import uuid
import base64

with open("intermediate_2.json",'r') as f:
    intermediate = jsonpickle.decode(f.read())

hRes = 256
vRes = 256

blockbench_boilerplate = {
    "meta": {
        "format_version": "4.0",
        "creation_time": 1664455679,
        "model_format": "free",
        "box_uv": False
    },
    "name": "test",
    "geometry_name": "",
    "visible_box": [1, 1, 0],
    "variable_placeholders": "",
    "variable_placeholder_buttons": [],
    "timeline_setups": [],
    "resolution": {
        "width": hRes,
        "height": vRes
    },
    "elements": [],
    "outliner": [],
    "textures": [{
        "path": "/home/martinz/FiguraExtractor/texture.png",
        "name": "texture.png",
        "folder": "",
        "namespace": "",
        "id": "0",
        "particle": True,
        "render_mode": "default",
        "visible": True,
        "mode": "bitmap",
        "saved": True,
        "uuid": "972e7a51-8f45-dee1-4d9f-f0527d49f867",
        "relative_path": "../texture.png"
    }]
}

def process_mesh(mesh,visibility):
    print("Mesh Name:", mesh.Name)
    
    base = {
        "name": mesh.Name,
        "color": 0,
        "origin": list(mesh.Pivot),
        "rotation": list(mesh.Rotation),
        "visibility": mesh.Visible & visibility,
        "locked": False,
        "vertices": {},
        "faces": {},
        "type": "mesh",
        "uuid": mesh.UUID
    }
    Faces = {}
    Vertices = {}

    for face in mesh.Faces:
        Faces[face.ID] = {
            "uv": face.UVs,
            "vertices": face.VertexIDs,
            "texture": 0
            #"texture": face.TextureID
        }
        print(face.ID)
    for vtx in mesh.Vertices:
        print(vtx)
        #Vertices[vtx.ID] = list(vtx.Coords)
        Vertices[vtx.ID] = (vtx.Coords[0]-mesh.Pivot[0],vtx.Coords[1]-mesh.Pivot[1],vtx.Coords[2]-mesh.Pivot[2])
    
    base['faces'] = Faces
    base['vertices'] = Vertices


    #print(base['faces'])
    #base['faces'] = Faces


    blockbench_boilerplate['elements'].append(base)
    return mesh.UUID

def process_cube(cube,visibility):
    #print("Cube Name:", cube.Name)
    
    base = {
        "name": cube.Name,
        "rescale": False,
        "locked": False,
        "from": list(cube.From),
        "to": list(cube.To),
        "autouv": 1,
        "color": 2,
        "origin": list(cube.Pivot),
        "visibility": cube.Visible & visibility,
        "inflate": cube.Inflate,
        "faces": {
            "north": {
                "uv": [0, 0, 1, 1]
            },
            "east": {
                "uv": [0, 0, 1, 1]
            },
            "south": {
                "uv": [0, 0, 1, 1]
            },
            "west": {
                "uv": [0, 0, 1, 1]
            },
            "up": {
                "uv": [0, 0, 1, 1]
            },
            "down": {
                "uv": [0, 0, 1, 1]
            }
        },
        "type": "cube",
        "uuid": cube.UUID
    }

    Faces = {}

    for name,face in cube.Faces.items():
        u1 = face.UV[0]# / hRes
        v1 = face.UV[1]# / vRes
        u2 = face.UV[2]# / hRes
        v2 = face.UV[3]# / vRes
        if face.Enabled:
            base['faces'][name.lower()] = {
                "uv": [u1,v1,u2,v2],
                "texture": face.TextureID
            }
        else:
            base['faces'][name.lower()] = {
                "uv": [u1,v1,u2,v2],
                "texture": None
            }
    #print(base['faces'])
    #base['faces'] = Faces


    blockbench_boilerplate['elements'].append(base)
    return cube.UUID

def process_group(grp,visibility):
    base_group ={
        "name": grp.Name,
        "origin": list(grp.Pivot),
        "rotation": list(grp.Rotation),
        "color": 0,
        "uuid": grp.UUID,
        "export": True,
        "isOpen": True,
        "locked": False,
        "visibility": grp.Visible,
        "autouv": 0,
        "children": []
    }

    print("Name:",grp.Name)
    print(grp.Visible)
    Visibility = visibility & grp.Visible
        
    for child in grp.Children:
        if 'Cube' in str(type(child)):
            print("cube")
            base_group['children'].append(process_cube(child,Visibility))
        elif 'Mesh' in str(type(child)):
            print("mesh")
            base_group['children'].append(process_mesh(child,Visibility))
        else:
            base_group['children'].append(process_group(child,Visibility))
    return base_group

def process_textures(textures):
    json_textures = []
    for texture in textures:
        print(texture.Name)
        json_base = {
            "path": "./%s.png" % texture.Name,
            "name": "%s.png" % texture.Name,
            "folder": "",
            "namespace": "",
            "id": texture.ID,
            "particle": True,
            "render_mode": "default",
            "visible": True,
            "mode": "bitmap",
            "saved": True,
            "uuid": str(uuid.uuid4()),
            "relative_path": "./%s.png" % texture.Name,
            "source": "data:image/png;base64," + str(texture.Data.decode())
        }
        #print(texture.Data)
        with open("%s.png" % texture.Name, 'wb') as f:
            f.write(base64.decodebytes(texture.Data))
        json_textures.append(json_base)
    blockbench_boilerplate['textures'] = json_textures

    ""

def process_scripts(scripts):
    for script in scripts:
        print(script.Name)
        with open("%s.lua" % script.Name,'w+') as f:
            f.write(str(script.Content))
            #print(str(script.Content))

blockbench_boilerplate['outliner'].append(process_group(intermediate.Model,True))
process_textures(intermediate.Textures)
process_scripts(intermediate.Scripts)

with open('generated.bbmodel','w+') as f:
    f.write(json.dumps(blockbench_boilerplate))

print(intermediate)