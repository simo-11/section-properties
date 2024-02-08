# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 19:42:59 2023

This file is used to speedup testing of various fragments of code
known as cells e.g. in Spyder which provides means to run and debug cells.
Matlab has quite similar feature for matlab-scripts but uses
%% as cell separator


@author: snikula
"""
# %% rectangle
runfile('primitive.py',#noqa
  args="""-A -W 0.085 -H 0.118 --mesh_size=0.00003 --primitive=rectangle""")
# %% rectangle 1-1
runfile('primitive.py',#noqa
  args="""-A -W=1 -H=1 --mesh_size=0.003 --primitive=rectangle""")
# %% circle
runfile('primitive.py',#noqa
  args="""-A --diameter 1 --mesh_size=0.05 --primitive=circular""")
# %% rhs
runfile('primitive.py',#noqa
  args="""-A -W 1 -H 1 --thickness=0.03 --mesh_size=0.05 --primitive=rhs
  --radius=0 --n_r=0""")
# %% Timo's rhs
# On the distortion and warping of cantilever beams with hollow section
runfile('primitive.py',#noqa
  args="""-A -W 0.1 -H 0.1 --thickness=0.004 --mesh_size=1e-5
  --primitive=rhs --n_r=0""")
# %% chs
runfile('primitive.py',#noqa
  args="""-A --diameter 1 --thickness 0.03 --mesh_size=0.2 --primitive=chs
   --count=105""")
# %% cold-formed-u
runfile('cold-formed-u.py',#noqa
  args="""-A -W 0.05 -H 0.1 --thickness=0.004 --n_r=0 --mesh_size=0.05""")
# %% plot_geometry
section.geometry.plot_geometry()#noqa
# %% plot_mesh
import matplotlib.pyplot as plt
s=section#noqa
w=s.args.width
h=s.args.height
alpha=0.5
mask=None
x=s._mesh_nodes[:,0]
y=s._mesh_nodes[:,1]
t=s._mesh_elements[:, 0:3]
fig, ax = plt.subplots()
s.set_box_aspect(ax)
ax.triplot(x,y,t,lw=0.5,color="black",alpha=alpha,mask=mask)
axins = ax.inset_axes([0.1, 0.1, 0.7, 0.7])
s.set_box_aspect(axins)
axins.triplot(x,y,t,lw=0.5,color="black",alpha=alpha,mask=mask)
# subregion of the original image
if min(x)<0 and min(y)<0:
    x1, x2, y1, y2 = -0.1*w, 0.05*w, 0.36*h, 0.51*h
else:
    x1, x2, y1, y2 = 0.45*w, 0.56*w, 0.9*h, 1.01*h
els=s.find_elements_in_region(x1,x2,y1,y2)
print(els)
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
axins.set_xticklabels([])
axins.set_yticklabels([])
ax.indicate_inset_zoom(axins, edgecolor="black")
plt.show()
# %% plot_warping_values
section.plot_warping_values()#noqa
# %% contour_warping_values
section.contour_warping_values(levels=51)#noqa
# %% write_warping_csv
section.write_warping_csv()#noqa
# %% write_warping_gltf
# can be moved to dev.DecSection
import pygltflib
import numpy as np
def write_warping_gltf(self,fn=None):
    if fn==None:
        fn=self.default_filename(suffix='.glb',use_case='warping')
    ps=len(self._mesh_nodes)
    points=np.empty((ps,3),dtype="float32")
    points[:,0]=self._mesh_nodes[:,0]
    points[:,1]=self._mesh_nodes[:,1]
    points[:,2]=self.section_props.omega
    triangles=self.get_triangles()
    triangles_binary_blob = triangles.flatten().tobytes()
    points_binary_blob = points.tobytes()
    n_times=31
    d=n_times-1
    times=np.empty(n_times,dtype="float32")
    scales=np.ones((n_times,3),dtype="float32")
    scaler=0.4*self.get_box_aspect()[2]/max(self.section_props.omega)
    for i in range(0,n_times):
        times[i]=i
        scales[i,2]=math.sin(times[i]/d*2*math.pi)*scaler
    flat_scales=np.ones((n_times,3),dtype="float32")
    flat_scales[:,2]=0
    times_blob=times.tobytes()
    scales_blob=scales.tobytes()
    gltf = pygltflib.GLTF2(
    scene=0,
    scenes=[pygltflib.Scene(nodes=[0])],
    nodes=[pygltflib.Node(children=[1,2])
           ,pygltflib.Node(mesh=0,name="cross-section with warping")
           ,pygltflib.Node(mesh=1,name="undeformed cross-section",
                           scale=[1,1,0])
           ],
    meshes=[
        pygltflib.Mesh(
            primitives=[
                pygltflib.Primitive(
                    attributes=pygltflib.Attributes(POSITION=1),
                    indices=0,
                    material=0
                )])
        ,pygltflib.Mesh(
            primitives=[
                pygltflib.Primitive(
                    attributes=pygltflib.Attributes(POSITION=1),
                    indices=0,
                    material=1
                )])
    ],
    materials=[
        pygltflib.Material(pbrMetallicRoughness=
                           pygltflib.PbrMetallicRoughness(
                               baseColorFactor=[0.2,0.2,0.2,0.85]),
                           doubleSided=True,
                           alphaCutoff=None,
                           name='cross-section with warping',
                           alphaMode='BLEND')
        ,pygltflib.Material(pbrMetallicRoughness=
                           pygltflib.PbrMetallicRoughness(
                               baseColorFactor=[0.5,0.1,0.1,0.]),
                           doubleSided=True,
                           alphaCutoff=None,
                           name='undeformed cross-section',
                           alphaMode='OPAQUE')
    ],
    accessors=[
        pygltflib.Accessor(
            bufferView=0,
            componentType=pygltflib.UNSIGNED_SHORT,
            count=triangles.size,
            type=pygltflib.SCALAR,
            max=[int(triangles.max())],
            min=[int(triangles.min())],
        ),
        pygltflib.Accessor(
            bufferView=1,
            componentType=pygltflib.FLOAT,
            count=len(points),
            type=pygltflib.VEC3,
            max=points.max(axis=0).tolist(),
            min=points.min(axis=0).tolist(),
        ),
        pygltflib.Accessor(
            bufferView=2,
            componentType=pygltflib.FLOAT,
            count=n_times,
            type=pygltflib.SCALAR,
            max=[times.max().item()],
            min=[0],
        ),
        pygltflib.Accessor(
            bufferView=3,
            componentType=pygltflib.FLOAT,
            count=n_times,
            type=pygltflib.VEC3,
            max=scales.max(axis=0).tolist(),
            min=scales.min(axis=0).tolist(),
        ),
    ],
    bufferViews=[
        pygltflib.BufferView(
            buffer=0,
            byteLength=len(triangles_binary_blob),
            target=pygltflib.ELEMENT_ARRAY_BUFFER,
            name='triangles',
        ),
        pygltflib.BufferView(
            buffer=0,
            byteLength=len(points_binary_blob),
            byteOffset=len(triangles_binary_blob),
            target=pygltflib.ARRAY_BUFFER,
            name='points',
        ),
        pygltflib.BufferView(
            buffer=0,
            byteLength=len(times_blob),
            byteOffset=len(triangles_binary_blob)
                +len(points_binary_blob)
            ,name='times',
        ),
        pygltflib.BufferView(
            buffer=0,
            byteLength=len(scales_blob),
            byteOffset=len(triangles_binary_blob)
                +len(points_binary_blob)
                +len(times_blob)
            ,name='scales',
        ),
    ],
    buffers=[
        pygltflib.Buffer(byteLength=len(triangles_binary_blob)
                         +len(points_binary_blob)
                         +len(times_blob)
                         +len(scales_blob)
                         )
    ],
    animations=[
        pygltflib.Animation(name="warping",
                            channels=[pygltflib.AnimationChannel(
                                sampler=0,
                                target=pygltflib.AnimationChannelTarget(
                                    node=0,path='scale')
                                )],
                            samplers=[pygltflib.AnimationSampler(
                                input=2,output=3),
                                ]),
    ]
    )
    gltf.set_binary_blob(triangles_binary_blob + points_binary_blob+
                         times_blob+scales_blob)
    #
    #
    gfn=self.gfn(fn)
    gltf.save(gfn)

write_warping_gltf(section)#noqa
# %% torsion stress plots from upstream
"""
Note to myself, figure details on how warping function values (at nodes)
are used with shape function derivates (at gauss integration points)
to get correct shear stresses.
https://sectionproperties.readthedocs.io/en/latest/rst/theory.html
refers to usage of smoothing matrix.
fea.py:element_stress
              sig_zxy_mzz_gp[i, :] = (
                  self.material.elastic_modulus
                  * Mzz
                  / j
                  * (B.dot(omega) - np.array([Ny, -Nx]))

"""
stress_post = section.calculate_stress(Mzz=1e6)#noqa
#ax_v=stress_post.plot_vector_mzz_zxy()
ax_c_xy=stress_post.plot_stress_mzz_zxy(normalize=False)
#ax_c_x=stress_post.plot_stress_mzz_zx()
#ax_c_y=stress_post.plot_stress_mzz_zy()
# %% analytic for circular, diameter=1: 5.09 MPa
# section-properties: 5.16 MPa (+ 1 %)
import math
d=1
r=d/2
Mzz=1e6
It=math.pi*math.pow(d,4)/32
tau=Mzz/It*r
print("d={0}, It={1:.3g}, Mzz={2:.3g}, tau={3:.3g}".format(d,It,Mzz,tau))
# %% analytic for chs, outer diameter=1, t=0.03: 23.2 MPa, It=0.0215
# section-properties(n=32), 965 elements: 24.3 MPa (+ 5 %), It=0.0212 (- 1 %)
# section-properties(n=64): 128-1023 elemenets 23.8 MPa (+ 3 %), It=0.0215
# section-properties(n=128): 256-512 elements 23.2 MPa It=0.0215
import math
d=1
t=0.03
d2=d-2*t
r=d/2
Mzz=1e6
It=math.pi*(math.pow(d,4)-math.pow(d2,4))/32
tau=Mzz/It*r
print("d={0}, It={1:.3g}, Mzz={2:.3g}, tau={3:.3g}".format(d,It,Mzz,tau))
# %% inset axes for contour_warping_values
import matplotlib.pyplot as plt
levels=51
fn=None
title=None
s=section#noqa
w=s.args.width#noqa
h=s.args.height#noqa
if s.is_shs():#noqa
    fn='warping-of-shs.pdf'
    title='Warping distribution of SHS using section properties'
(fig,ax)=s.contour_warping_values(levels=levels)#noqa
if title:
    ax.set_title(title)
axins = ax.inset_axes([0.1, 0.1, 0.7, 0.7])
s.set_box_aspect(axins)
x=s._mesh_nodes[:,0]
y=s._mesh_nodes[:,1]
triangles=s.get_triangles()#noqa
z=s.section_props.omega#noqa
trictr = axins.tricontourf(x, y, triangles, z,levels=levels)
# subregion of the original image
if s.args.primitive in ['circular','chs']:
    x1, x2, y1, y2 = -0.1*w, 0.05*w, 0.36*h, 0.51*h
else:
     x1, x2, y1, y2 = 0.92*w, 1.0*w, 0.92*h, 1.0*h
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
axins.set_xticklabels([])
axins.set_yticklabels([])
ax.indicate_inset_zoom(axins, edgecolor="black")
if fn!=None:
    plt.savefig(fn)
    print('Wrote {0}'.format(fn))
plt.show()
