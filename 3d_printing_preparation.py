import pymeshlab
import vedo
import os
import vtk
import SimpleITK as sitk
import numpy as np
import json
import nibabel as nib
import matplotlib.pyplot as plt

first_time = False
# --------------------    CHOOSE ISOCONTOURING ALGORITHM ------------------------------
# method = 'marching_cubes'
method = 'flying_edges'
# method='synchronized templates'
# --------------------------------------------------------------------------------------

with open("paths.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()


def read_nifti_labelmap(filename_nii):
    filename = filename_nii.split(".")[0]

    # read all the labels present in the file
    multi_label_image = sitk.ReadImage(filename_nii)
    img_npy = sitk.GetArrayFromImage(multi_label_image)
    labels = np.unique(img_npy)

    # read the file
    reader = vtk.vtkNIFTIImageReader()
    reader.SetFileName(filename_nii)
    reader.Update()

    return labels, reader


def convert_to_stl(reader):
    # apply vtk flying edges
    if method == 'flying_edges':
        surfaces = vtk.vtkDiscreteFlyingEdges3D()
    if method == 'marching_cubes':
        surfaces = vtk.vtkDiscreteMarchingCubes()
    if method == 'synchronized templates':
        surfaces = vtk.vtkSynchronizedTemplates3D()

    surfaces.SetInputConnection(reader.GetOutputPort())
    surfaces.SetValue(0, int(
        label))  # use surf.GenerateValues function if more than one contour is available in the file
    surfaces.Update()

    return surfaces


def smooth(surf):
    # smoothing the mesh
    smoother = vtk.vtkWindowedSincPolyDataFilter()
    if vtk.VTK_MAJOR_VERSION <= 5:
        smoother.SetInput(surf.GetOutput())
    else:
        smoother.SetInputConnection(surf.GetOutputPort())

    # increase this integer set number of iterations if smoother surface wanted
    smoother.SetNumberOfIterations(30)
    smoother.NonManifoldSmoothingOn()
    smoother.NormalizeCoordinatesOn()  # The positions can be translated and scaled such that they fit within a range of [-1, 1] prior to the smoothing computation
    smoother.GenerateErrorScalarsOn()
    smoother.Update()

    return smoother


def save_output(smoother, label):
    # save the output
    writer = vtk.vtkSTLWriter()
    writer.SetInputConnection(smoother.GetOutputPort())
    writer.SetFileTypeToASCII()

    # file name need to be changed
    # save as the .stl file, can be changed to other surface mesh file
    # out_path = jsonObject["separated_stl"]
    out_path = jsonObject["classes_surfaces"]
    path = out_path + f'{label}.stl'
    # path = f'{filename}_{label}.stl'
    writer.SetFileName(path)
    writer.Write()


# return out_path
def merge_stl_files(path):
    stl_files = os.listdir(path)
    meshes = []
    for name in stl_files:
        meshes.append(vedo.Mesh(path + name))
    return vedo.merge(meshes)


def cut_mesh(organs):
    plt = vedo.show(organs, __doc__, bg='black', bg2='bb', interactive=False)
    plt.addCutterTool(organs, mode='plane')  # modes= sphere, plane, box
    plt.close()


def fill_holes(vedo_mesh):
    vedo_mesh.fillHoles(30)


def apply_filters(ms):
    filters = []
    filters.append('remeshing_isotropic_explicit_remeshing')
    #filters.append('select_problematic_faces')
    filters.append('laplacian_smooth')
    #filters.append('select_problematic_faces')

    filters.append('select_non_manifold_edges_')
    filters.append('select_non_manifold_vertices')

    filters.append('normalize_face_normals')
    filters.append('normalize_vertex_normals')
    filters.append('remove_zero_area_faces')
    filters.append('remove_duplicate_faces')
    filters.append('remove_duplicate_vertices')
    filters.append('remove_isolated_folded_faces_by_edge_flip')
    filters.append('repair_non_manifold_edges_by_removing_faces')

    filters.append('select_non_manifold_edges_')
    filters.append('select_non_manifold_vertices')

    filters.append('repair_non_manifold_edges_by_splitting_vertices')
    filters.append('repair_non_manifold_vertices_by_splitting')
    filters.append('close_holes')

    for filter in filters:

        if filter == 'merge_close_vertices':
            ms.apply_filter(filter, threshold=1)
        elif filter == 'remeshing_isotropic_explicit_remeshing':
            ms.apply_filter(filter, iterations=3, smoothflag=False)
            remeshed_1 = vedo.Mesh(ms)
            vedo.write(remeshed_1, "F:/aadiplwmatikoula/1_final/case_00001/isotropic_remeshing/remeshed.stl")
        elif filter == 'laplacian_smooth':
            ms.apply_filter(filter, stepsmoothnum=1)
            remeshed_2 = vedo.Mesh(ms)
            vedo.write(remeshed_2, "F:/aadiplwmatikoula/1_final/case_00001/laplacian_smooth/smoother.stl")
        elif filter == 'repair_non_manifold_edges_by_removing_faces':
            ms.apply_filter(filter)
            remeshed_3 = vedo.Mesh(ms)
            vedo.write(remeshed_3, "F:/aadiplwmatikoula/1_final/case_00001/correct_non_manifold/repaired.stl")
        elif filter == 'close_holes':
            ms.apply_filter(filter, maxholesize=150)
        elif filter == 'compute_planar_section':
            ms.apply_filter(filter, planeaxis=1)
        # elif filter == 'select_problematic_faces':
        #     ms.apply_filter(filter, usear=False, usenf=True, nfratio=60)
        #     ms.apply_filter(filter)
        #     m = ms.current_mesh()
        #     nf = m.selected_face_number()
        #     print("Selected %d problematic adjacent faces with normal angle greater than 60" % nf)
        elif filter == 'select_non_manifold_edges_':
            ms.apply_filter(filter)
            m = ms.current_mesh()
            nf = m.selected_face_number()
            print("Selected %d non manifold edges" % nf)
        else:
            ms.apply_filter(filter)

        points = ms.current_mesh().vertex_number()
        face = ms.current_mesh().face_number()
        print('After ' + filter + ' has points: ' + str(points) + ' and faces ' + str(face))
        mesh = ms.current_mesh()
        vedo_mesh = vedo.Mesh(mesh).color('b5').lw(0.1)
        vedo.show(vedo_mesh, "Applied pymeshlab filter: " + filter + "\nMesh has " + str(points) + " points and " + str(
            face) + " faces ", axes=True, bg='green9', bg2='blue9', title="Kidney")


if __name__ == '__main__':
    if first_time is True:
        # Convert to stl
        labels, reader = read_nifti_labelmap(jsonObject["read_labelmap"])

        # can be done in a loop if you have multiple files to be processed, speed is guaranteed if GPU is used:)
        # for all labels presented in the segmented file
        for label in labels:
            if int(label) != 0:
                surf = convert_to_stl(reader)
                smoother = smooth(surf)
                save_output(smoother, label)

        # Merge stl organs
        merged_organs = merge_stl_files(jsonObject["classes_surfaces"])
        vedo.write(merged_organs, jsonObject["merged_surfaces"])

    # Show different organs surfaces
    organs = os.listdir(jsonObject["classes_surfaces"])
    for organ in organs:
        anatomy = vedo.Mesh(jsonObject["classes_surfaces"] + organ)
        vedo.show(anatomy)

    # Show merged file
    merged_mesh = vedo.Mesh(jsonObject["merged_surfaces"])
    vedo.show(merged_mesh)

    # Cut merged mesh to select the region of interest
    cut_mesh(merged_mesh)

    # Show cutted mesh before hole filling
    cutted_mesh = vedo.Mesh(jsonObject["cropped_mesh"])
    points = len(cutted_mesh.vertices())
    face = len(cutted_mesh.faces())
    vedo.show(cutted_mesh, "Before hole fill" + "\nMesh has " + str(points) + " points and " + str(
        face) + " faces ",
              axes=True, bg='green9', bg2='blue9', title="Kidney")

    # Hole Filling
    fill_holes(cutted_mesh)

    # Show mesh after hole filling
    hole_filled_mesh = vedo.Mesh(cutted_mesh).computeNormals().lighting('glossy')
    points = len(hole_filled_mesh.vertices())
    face = len(hole_filled_mesh.faces())
    vedo.show(hole_filled_mesh, "After hole fill" + "\nMesh has " + str(points) + " points and " + str(
        face) + " faces ",
              axes=True, bg='green9', bg2='blue9', title="Kidney")

    vedo.write(hole_filled_mesh, jsonObject["hole_filled_mesh"])

    mesh_before_preprocessing = vedo.Mesh(hole_filled_mesh).color('b5').lw(0.1)
    vedo.show(mesh_before_preprocessing,
              "Before apply any filter " + "\nMesh has " + str(points) + " points and " + str(
                  face) + " faces ", axes=True, bg='green9', bg2='blue9', title="Kidney")

    # Apply all filters
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(jsonObject["hole_filled_mesh"])
    apply_filters(ms)
    ms.save_current_mesh(jsonObject["final_repaired_stl"])
