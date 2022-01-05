"""Isolate points of intersection and Generate the silhouette of a mesh
as seen along a specified direction
"""
from vedo import *
import vedo
import numpy as np
import math
import matplotlib.pyplot as plt

kidney = Mesh("F:/aadiplwmatikoula/data/case_00003/cutted_seperated/kidney.stl", computeNormals=True).alpha(
    0.4).c('violet').rotateX(20)

cancer = Mesh("F:/aadiplwmatikoula/data/case_00003/seperated_stl/2.stl", computeNormals=True).alpha(
    0.4).rotateX(20)

# ------------------------------------------------------------------------------------------------------------
#                                          PROJECTIONS
# ------------------------------------------------------------------------------------------------------------
kidney_points = kidney.points()
m = len(kidney_points)

cancer_points = cancer.points()
n = len(cancer_points)

cm_kidney = kidney.centerOfMass()

# orthogonal projection ###############################
plane1 = Plane(pos=(cm_kidney * (0, 1, 1)), normal=(1, 0, 0), sx=200).alpha(0.2)
so_1 = cancer.clone().projectOnPlane(plane1).c('y')
si_1 = kidney.clone().projectOnPlane(plane1).c('y')
pts1 = so_1.silhouette('2d').points()
lts1 = si_1.silhouette('2d').points()

plane2 = Plane(pos=(cm_kidney * (1, 0, 1)), normal=(0, 1, 0), sx=200).alpha(0.2)
so_2 = cancer.clone().projectOnPlane(plane2).c('y')
si_2 = kidney.clone().projectOnPlane(plane2).c('y')
pts2 = so_2.silhouette('2d').points()
lts2 = si_2.silhouette('2d').points()

plane3 = Plane(pos=(cm_kidney * (1, 1, 0)), normal=(0, 0, 1), sx=200).alpha(0.2)
so_3 = cancer.clone().projectOnPlane(plane3).c('y')
si_3 = kidney.clone().projectOnPlane(plane3).c('y')
pts3 = so_3.silhouette('2d').points()
lts3 = si_3.silhouette('2d').points()

# draw the lines
lines = []
for i in range(0, len(cancer_points), int(len(cancer_points) / 20)):
    lines.append(Line(pts1[i], cancer_points[i], c='k', alpha=0.3))  # megalo
    lines.append(Line(pts2[i], cancer_points[i], c='k', alpha=0.3))  # den fainetai
    lines.append(Line(pts3[i], cancer_points[i], c='k', alpha=0.3))  # mikro

for i in range(0, len(kidney_points), int(len(kidney_points) / 20)):
    lines.append(Line(lts1[i], kidney_points[i], c='k', alpha=0.3))  # megalo
    lines.append(Line(lts2[i], kidney_points[i], c='k', alpha=0.3))  # den fainetai
    lines.append(Line(lts3[i], kidney_points[i], c='k', alpha=0.3))  # mikro

# ------------------------------------------------------------------------------------------------------------
#                                          INTERSECTIONS
# ------------------------------------------------------------------------------------------------------------
# Cut mesh with other mesh
cutted_mesh = kidney.cutWithMesh(cancer, invert=True)
cutted_mesh.computeNormals().clean().lw(0.1)

# Find mesh boundaries (holes)
pids = cutted_mesh.boundaries(returnPointIds=True)
bpts = cutted_mesh.points()[pids]
new = Mesh(bpts)
new.pointSize(8).c('red')

# Cluster boundary points
cl = cluster(bpts, radius=5)
bounds = cl.unpack(0).c('red')
bounds.pointSize(8)

# Fit a plane to these points
fit_Plane = vedo.pointcloud.fitPlane(bounds)
fit_Plane.pos(fit_Plane.center - 6 * fit_Plane.normal)

cut_points_mesh = vedo.Mesh(bounds)

# Project to this plane the clustered points
projection = cut_points_mesh.projectOnPlane(fit_Plane).c('y')
projected_points = projection.silhouette('2d').points()
projected_points_mesh = vedo.Mesh(projected_points)

# Make a mesh with clustered points
cut_points = vedo.Mesh(bounds).points()

projected_size = int(projected_points.size / 3)
quantized_points = []

quantized_points.append(vedo.pointcloud.Point(projected_points_mesh.centerOfMass(), c=(1, 1, 1)))
list = []
for i in range(projected_size):
    # Move points at the start of coordinate system (0,0,0)
    temp_point = projected_points_mesh.points()[i] - projected_points_mesh.centerOfMass()
    # Convert cartesian to spherical coordinates (r,θ,φ)
    rho, theta, phi = vedo.utils.cart2spher(temp_point[0], temp_point[1], temp_point[2])

    # Normalize values to range [0,1]
    phi = (phi + math.pi) / (2 * math.pi)  # oi times tou phi einai  -p ews p edw to pame sto diastima 0-1
    phi = np.round(phi, decimals=3)  # round to first decimal
    # Quantizate phi values with step 0.05
    phi = 0.05 * math.floor(((phi / 0.05) + 0.5))
    phi = np.round(phi, decimals=2)

    # We want to extract points with the min distance, so we create a line from the projected point to intersection
    dist = vedo.shapes.Line(projected_points[i], cut_points[i]).length()
    # we create a list with intersection point, projected point,phi, distance
    list.append({'phi': phi, 'point': projected_points[i], 'cut_points': cut_points[i], 'dist': dist})

    # visualisation
    rgba = plt.cm.jet(phi)

    quantized_points.append(vedo.pointcloud.Point(projected_points_mesh.points()[i], c=(rgba[0], rgba[1], rgba[2])))

# sort list according to phi
sorted_by_phi = sorted(list, key=lambda k: k['phi'])

step_phi = 0.0
miden = []

step_phi = 0
grouped_points_by_phi = []

# Sampling points with phi
for i in range(20):
    onetime = 0
    miden = []
    for element in sorted_by_phi:
        if element['phi'] == step_phi:
            miden.append(element)

    grouped_points_by_phi.append(miden)
    step_phi += 0.05
    step_phi = np.round(step_phi, decimals=2)

# -------------------------------------------------------------------------------------------------------------
points_of_interest = []  # ta ekswterika simeia
for point in grouped_points_by_phi:
    # ta kanoyme sort ws pros tin apostasi kai pratame to simeio me thn elaxisti apostasi
    points_of_interest.append(
        vedo.pointcloud.Point(sorted(point, key=lambda k: k['dist'])[0]['cut_points'], c=(0, 1, 0)))

# Create arrows from projected points and points of intersection (clustered)
ars = Arrows(cut_points, projected_points, s=0.5).c('k').alpha(0.5)

# Create spheres at points of interest
spheres = []
for point in points_of_interest:
    print(point.pos())
    spheres.append(vedo.shapes.Sphere(pos=point.pos(), r=1.8, c='r5', alpha=1, res=5, quads=False))

# ______________________________________________________________________________________________________________
#                                           SHOW ALL
# ---------------------------------------------------------------------------------------------------------------

show(kidney, cancer, new, __doc__, axes=1, viewup='z')
show(kidney, cancer, bounds, __doc__, axes=1, viewup='z').close()
show(fit_Plane, bounds, __doc__, axes=1, viewup='z')
show(fit_Plane, bounds, quantized_points, points_of_interest, ars, __doc__, axes=1, viewup='z')
show(fit_Plane, bounds, points_of_interest, __doc__, axes=1, viewup='z')
# show(kidney,cancer, final_points, __doc__, axes=1, viewup='z')
show(kidney, cancer, spheres, __doc__, axes=1, viewup='z').close()

# ------------------------------------------------------------------------------------------------------------------------------------------

show(kidney, cancer, spheres, plane1, so_1, so_1.silhouette('2d').c('red'), si_1, si_1.silhouette('2d').c('yellow'),
     plane2, so_2, so_2.silhouette('2d').c('red'), si_2, si_2.silhouette('2d').c('yellow'),
     plane3, so_3, so_3.silhouette('2d').c('red'), si_3, si_3.silhouette('2d').c('yellow'),
     lines, axes=1).close()

show(so_1.silhouette('2d').c('red').rotateY(90), si_1.silhouette('2d').c('yellow').rotateY(90), interactorStyle="Image")
show(so_2.silhouette('2d').c('red').rotateX(90), si_2.silhouette('2d').c('yellow').rotateX(90), interactorStyle="Image")
show(so_3.silhouette('2d').c('red').rotateZ(90), si_3.silhouette('2d').c('yellow').rotateZ(90), interactorStyle="Image")
# ------------------------------------------------------------------------------------------------------------------------------------------
# Save final mesh
# meshes = []
# # meshes.append(Mesh("F:/aadiplwmatikoula/data/case_00003/cutted_seperated/kidney.stl", computeNormals=True).alpha(
# #     0.4).c('violet'))
# meshes.append(Mesh("F:/aadiplwmatikoula/data/case_00003/cutted_seperated/kidney.stl", computeNormals=True).c('violet'))
# #meshes.append(cancer.c('yellow'))
# meshes.append(Mesh("F:/aadiplwmatikoula/data/case_00003/seperated_stl/2.stl", computeNormals=True))
# meshes.append(spheres)
# fin = vedo.merge(meshes)
# show(fin, __doc__, axes=1, viewup='z').close()
# vedo.write(fin, "F:/aadiplwmatikoula/data/case_00003/final_mesh/final.stl")
