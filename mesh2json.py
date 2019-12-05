import bpy
import json

bpy.ops.object.mode_set(mode="OBJECT")
me = bpy.context.object.data

pts = [ v.co[:] for v in me.vertices]

selected = [ v.index for v in me.vertices if v.select]


face_list = [ list(ff.vertices) 
                          for ff in me.polygons]
                 
with open('motif.json','w') as fp:         
    json.dump({ "verts" : pts,   
                "selected" : selected,
              "faces" : face_list},
               fp)
                          