"""Metrics of quality for
the cells of a triangular mesh
(zoom to see cell label values)"""
from vedo import *
from vedo.pyplot import histogram
from vedo.pyplot import whisker

# mesh = Mesh("C:/Users/Dell/PycharmProjects/pythonProject17/clipped.stl").computeNormals().lineWidth(0.1)
#mesh = Mesh(
#    "F:/aadiplwmatikoula/meshes_kits21/case_00001/remeshing/isotropic_remeshing.stl").computeNormals().lineWidth(0.1)
mesh = Mesh("F:/aadiplwmatikoula/meshes_kits21/case_00001/remeshing/smoother.stl").computeNormals().lineWidth(0.1)
# mesh.threshold(above=5,below= 10,scalars=mesh)

# generate a numpy array for mesh quality
mesh.addQuality(measure=1).printInfo().cmap('RdYlBu', on='cells', vmin=1, vmax=3)

# make it smaller and position it, useBounds makes the cam
# ignore the object when resetting the 3d qscene
#hist.scale(10).pos(40,-53,0).useBounds(False)
hist = histogram(mesh.getCellArray("Quality"), xtitle='mesh quality', bc='w', logscale=False, xlim=[1, 3])
cm = mesh.centerOfMass()
hist.scale(20).pos(cm + 70).useBounds(False)

box_plot = whisker(mesh.getCellArray("Quality"), r=1, s=1)
#cm=mesh.centerOfMass()
# box_plot.pos(cm+70).useBounds(False)

# add a scalar bar for the active scalars
# mesh.addScalarBar3D(c='w', title='triangle quality by min(\alpha_i )')
mesh.addScalarBar3D(c='w', title='triangle quality by aspect_ratio')

# create numeric labels of active scalar on top of cells
labs = mesh.labels(cells=True,
                   precision=3,
                   scale=0.4,
                   font='Quikhand',
                   c='black',
                   )

# cam = dict(pos=(59.8, -191, 78.9),
#            focalPoint=(27.9, -2.94, 3.33),
#            viewup=(-0.0170, 0.370, 0.929),
#            distance=205,
#            clippingRange=(87.8, 355))

cam = dict(pos=cm,
           focalPoint=(27.9, -2.94, 3.33),
           viewup=(-0.0170, 0.370, 0.929),
           distance=205,
           clippingRange=(87.8, 355))

# build custom axes
axes = Axes(box_plot,
            yrange=[1, 4]
            )

show(mesh, labs, hist, __doc__, bg='bb', camera=cam, axes=11).close()
# show(mesh, labs, box_plot, __doc__, bg='bb', camera=cam, axes=11).close()
show(box_plot, __doc__, axes).close()
# show(box_plot,axes, __doc__, bg='bb', camera=cam).close()
# show(hist, interactorStyle="Image").close()
