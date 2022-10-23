from pynbt import NBTFile
from classes import *
import base64
import sys

def print_metadata(nbt):
  meta = nbt['metadata']
  name = str(meta['name'].value)
  color = str(meta['color'].value)
  authors = str(meta['authors'].value)
  version = str(meta['ver'].value)
  print("Name: "+name)
  print("Color: "+color)
  print("Author(s): "+authors)
  print("Figura version: "+version)

def process_scripts(nbt):
  Scripts = []
  for name,script in nbt.items():
    Scripts.append(Script(name,str(script.value.decode('utf-8'))))
  return Scripts


def process_textures(nbt):
  textures = nbt['textures']
  #print(textures)
  Textures = []

  texture_counter = 0
  for texture in textures:
    texture_data = base64.encodebytes(texture['default'].value)
    #print(texture['name'].value)
    Textures.append(Texture(texture_counter,texture['name'].value,texture_data))
    texture_counter += 1
  return Textures

#Aqui es donde me volvi loco (en el mal sentido)
#NO LO TOQUES
def process_mesh(nbt):
  #print("mesh")
  
  Pivot = (0,0,0)
  if 'piv' in nbt:
    Pivot = (nbt['piv'][0].value,nbt['piv'][1].value,nbt['piv'][2].value)
  
  Rotation = (0,0,0)
  if 'rot' in nbt:
    Rotation = (nbt['rot'][0].value,nbt['rot'][1].value,nbt['rot'][2].value)
  
  #print("Pivot:",Pivot," Rotation:",Rotation)

  mesh_data = nbt['mesh_data']
  
  Vertices = []
  vertex_data = mesh_data['vtx']
  for vtx in zip(vertex_data[::3],vertex_data[1::3],vertex_data[2::3]):
    vertex = MeshVertex((vtx[0].value,vtx[1].value, vtx[2].value))
    Vertices.append(vertex)
    #print(vertex.ID)
  
  UVs = []
  uv_data = mesh_data['uvs']
  for uv in zip(uv_data[::2],uv_data[1::2]):
    
    UVs.append((uv[0].value,uv[1].value))
    #print(vertex.ID)
  
  fac_data_index = []
  fac_data = mesh_data['fac']
  for fac in fac_data:
    fac_data_index.append(fac.value)
  #print(fac_data_index)
  
  Faces = []
  vertex_counter = 0
  #QUE COJONES??!!💀💀
  tex_data = mesh_data['tex']
  for tex in tex_data:
    packed = tex.value
    num_verts = packed & 0xf
    tex_id = packed >> 4
    #print("tex_id:", packed >> 4)
    #print("num_verts:",packed & 0xf)

    face_vertex_ids = []
    vertex_uvs = {}
    for i in range(vertex_counter,vertex_counter+num_verts,1):
      #print(i)
      #print(len(Vertices))
      face_vertex_ids.append(Vertices[fac_data_index[i]].ID)
      vertex_uvs[Vertices[fac_data_index[i]].ID] = UVs[i]
      #vertex_uvs[Vertices[fac_data_index[i]].ID] = [0,0]
      #no cago hace un mes
    #print(face_vertex_ids)
    Faces.append(MeshFace(face_vertex_ids,vertex_uvs,tex_id))
    vertex_counter += num_verts
 

  Name = nbt['name'].value

  Visibility = True
  if 'vsb' in nbt:
    Visibility = nbt['vsb'].value == 1

  return Mesh(Name,Pivot,Rotation,Visibility,Vertices,Faces)

def process_cube_face(nbt):
  TextureID = nbt['tex'].value
  UV = (
    nbt['uv'][0].value,
    nbt['uv'][1].value,
    nbt['uv'][2].value,
    nbt['uv'][3].value
  )
  Rotation = nbt['rot'].value if 'rot' in nbt else 0
  return CubeFace(True,TextureID,Rotation,UV)

def process_cube(nbt):
  #print("cube")
  From = (nbt['f'][0].value,nbt['f'][1].value,nbt['f'][2].value)
  To = (nbt['t'][0].value,nbt['t'][1].value,nbt['t'][2].value)
  #print("From:",From, " To:",To)
  Inflate = nbt['inf'].value if 'inf' in nbt else 0
  #print("Inflate:",Inflate)
  
  Pivot = (0,0,0)
  if 'piv' in nbt:
    Pivot = (nbt['piv'][0].value,nbt['piv'][1].value,nbt['piv'][2].value)
  
  Rotation = (0,0,0)
  if 'rot' in nbt:
    Rotation = (nbt['rot'][0].value,nbt['rot'][1].value,nbt['rot'][2].value)
  
  #print("Pivot:",Pivot," Rotation:",Rotation)

  cube_data = nbt['cube_data']

  Faces = {}
  #for f in ['UP','DOWN','LEFT','RIGHT','SOUTH','NORTH']: Cagada canal sur
  for f in ['NORTH','EAST','SOUTH','WEST','UP','DOWN']:
    facename = f[0].lower()
    if facename in cube_data:
      Faces[f] = (process_cube_face(cube_data[facename]))
    else:
      Faces[f] = CubeFace(False,0,0,(0,0,0,0))
  Name = nbt['name'].value

  Visibility = True
  if 'vsb' in nbt:
    Visibility = nbt['vsb'].value == 1

  return Cube(Name,From,To,Pivot,Rotation,Inflate,Visibility,Faces)

def process_children(nbt):
  #print()
  #print("Name: " + nbt['name'].value)
  Name = nbt['name'].value
  
  AnchorType = None
  if 'pt' in nbt:
    #print("Anchor Type: "+nbt['pt'].value)
    AnchorType = nbt['pt'].value

  Pivot = (0,0,0)
  if 'piv' in nbt:
    Pivot = (nbt['piv'][0].value,nbt['piv'][1].value,nbt['piv'][2].value)
  
  Rotation = (0,0,0)
  if 'rot' in nbt:
    Rotation = (nbt['rot'][0].value,nbt['rot'][1].value,nbt['rot'][2].value)
  
  Visibility = True
  if 'vsb' in nbt:
    Visibility = nbt['vsb'].value == 1
  
  #print("Pivot:",Pivot," Rotation:",Rotation)

  
  Children = []
  if 'chld' in nbt:
    #print("[")
    for child in nbt['chld']:
      if 'cube_data' in child:
        Children.append(process_cube(child))
      elif 'mesh_data' in child:
        Children.append(process_mesh(child))
      else:
        Children.append(process_children(child))
    #print("]")
  
  return Group(Name,AnchorType,Pivot,Rotation,Visibility,Children)

with open(sys.argv[1], 'rb') as io:
  nbt = NBTFile(io)
  #print(nbt.pretty())
  texture = nbt['textures'][0]['default'].value
  with open('texture.png', 'wb') as f:
    f.write(texture)
  print_metadata(nbt)

  Textures = process_textures(nbt)
  Model = process_children(nbt['models'])
  Scripts = process_scripts(nbt['scripts'])

  import jsonpickle
  frozen = jsonpickle.encode(Model)
  with open("model_intermediate.json","w+") as f:
    f.write(frozen)
  
  Avatar_final = Avatar(Model, Textures, Scripts)
  final = jsonpickle.encode(Avatar_final)
  with open("intermediate_2.json","w+") as f:
    f.write(final)



