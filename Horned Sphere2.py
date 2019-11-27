import bpy
import bmesh
import numpy as np
import json

class HornedSphere():
    
    def __init__(self, src_fn='motif.json'):
        self.src = src_fn
        self.scale = .38
        self.get_motif()
        
    def make_arms(self, verts):
    	'''verts a list of ndarray shape = (3)'''
   
    	RZ = np.array([[0,1,0], [-1,0,0], [0,0,1]])
    	Rz = np.array([[0,1,0], [-1,0,0], [0,0,1]])
    	Ry = np.array([[0,0,-1], [0,-1,0], [1,0,0]])
    	
    	RL = RZ
    	RR = np.dot(Ry,Rz)
    	
    	pts = []
    	pts.extend([ self.scale*np.dot( v-self.Ov, RL) + self.Lv for v in  verts])
    	pts.extend([ self.scale*np.dot( v-self.Ov, RR) + self.Rv for v in verts])
    	return pts

    def get_motif(self):
        with open( self.src, 'r') as fp:
            data = json.load(fp)

        pts = [ np.array(v) for v in data['verts'] ]
        
        Lv = .25*sum( pts[:4])
        Rv = .25*sum( pts[-4:])
        
        #this is bad I sould pass this in the json
        joint = [ pts[j] for j in [20, 21, 24, 25] ]   
        self.Ov = sum(joint)/len(joint)
       
        pts[:5] = [ self.scale*(v- Lv) + Lv for v in pts[:5] ]
        pts[-5:] = [self.scale*(v- Rv) + Rv for v in pts[-5:] ]
        
        self.Lv, self.Rv = Rv, Lv  
        self.pts = pts
        self.face_list = np.array(data['faces'])
                          

model = HornedSphere()       
depth = 3
arm_pts = model.pts[:]
arm_pts.extend(model.make_arms( model.pts))
for k in range(depth-1):
    arm_pts.extend(model.make_arms( arm_pts))


bpy.ops.mesh.primitive_plane_add(location=[0,0,-3]) 
me = bpy.context.object.data
bm = bmesh.new() 

verts = [bm.verts.new(v[:]) for v in arm_pts]
for k in range( 27):
    for L in model.face_list[:] + k*len(model.pts) :
        bm.faces.new([verts[k] for k in L ])
bm.to_mesh(me)
bm.free()  # free and prevent further access

obj = me = bpy.context.object
obj.scale = [5,5,5]
