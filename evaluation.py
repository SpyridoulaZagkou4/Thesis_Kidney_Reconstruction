import pymeshlab
import vedo

after_isotropic_remeshing = pymeshlab.MeshSet()
after_isotropic_remeshing.load_new_mesh("F:/aadiplwmatikoula/1_final/case_00001/isotropic_remeshing/remeshed.stl")
#after_isotropic_remeshing.load_new_mesh("F:/aadiplwmatikoula/meshes_kits21/case_00001/remeshing/isotropic_remeshing.stl")

after_smoothing = pymeshlab.MeshSet()
after_smoothing.load_new_mesh("F:/aadiplwmatikoula/1_final/case_00001/laplacian_smooth/smoother.stl")
#after_smoothing.load_new_mesh("F:/aadiplwmatikoula/meshes_kits21/case_00001/remeshing/smoother.stl")

taubin_smoothing = pymeshlab.MeshSet()
taubin_smoothing.load_new_mesh("F:/aadiplwmatikoula/meshes_kits21/case_00001/remeshing/taubin_smoother.stl")

repaired_mesh = pymeshlab.MeshSet()
repaired_mesh.load_new_mesh("F:/aadiplwmatikoula/1_final/case_00001/correct_non_manifold/repaired.stl")
#repaired_mesh.load_new_mesh("F:/aadiplwmatikoula/meshes_kits21/case_00001/remeshing/repair.stl")

# repaired_mesh = pymeshlab.MeshSet()
# repaired_mesh.load_new_mesh("F:/aadiplwmatikoula/meshes_kits21/case_00001/nifti/stl_repaired/final_mesh.stl")

# cutted_mesh = pymeshlab.MeshSet()
# cutted_mesh.load_new_mesh("F:/aadiplwmatikoula/1_final/case_00001/cutted_mesh/clipped.stl")
#
# ground_truth=pymeshlab.MeshSet()
# ground_truth.load_new_mesh("F:/aadiplwmatikoula/meshes_kits_19_mc/case00007_ground_truth/stl_seperated/1.stl")
#
# predicted=pymeshlab.MeshSet()
# predicted.load_new_mesh("F:/aadiplwmatikoula/meshes_kits_19_mc/case00007_predicted/stl_seperated/1.0.stl")

# -------------------------------------------  PROBLEMATIC FACES --------------------------------------------------
filter='select_problematic_faces'
after_isotropic_remeshing.apply_filter(filter, usear=False, usenf=True, nfratio=60)

points = after_isotropic_remeshing.current_mesh().vertex_number()
face = after_isotropic_remeshing.current_mesh().face_number()
m = after_isotropic_remeshing.current_mesh()
nf_1 = m.selected_face_number()
vec = m.face_selection_array()

vedo_mesh = vedo.Mesh(m).color('b5').lw(0.1)
vedo.show(vedo_mesh,
          "Applied pymeshlab filter: " + filter + "\nMesh has " + str(points) + " points and " + str(
              face) + " faces " + "\nwith selected " + str(
              nf_1) + "faces with angle normal greater to 60 ", axes=True, bg='green9', bg2='blue9',
          title="Kidney")


filter='select_problematic_faces'
after_smoothing.apply_filter(filter, usear=False, usenf=True, nfratio=30)

points = after_smoothing.current_mesh().vertex_number()
face = after_smoothing.current_mesh().face_number()
m = after_smoothing.current_mesh()
nf_2 = m.selected_face_number()

vedo_mesh = vedo.Mesh(m).color('b5').lw(0.1)
vedo.show(vedo_mesh,
          "Applied pymeshlab filter: " + filter + "\nMesh has " + str(points) + " points and " + str(
              face) + " faces " + "\nwith selected " + str(
              nf_2) + "faces with angle normal greater to 60 ", axes=True, bg='green9', bg2='blue9',
          title="Kidney")


filter='select_problematic_faces'
taubin_smoothing.apply_filter(filter, usear=False, usenf=True, nfratio=30)

points = taubin_smoothing.current_mesh().vertex_number()
face = taubin_smoothing.current_mesh().face_number()
m = taubin_smoothing.current_mesh()
nf_2 = m.selected_face_number()

vedo_mesh = vedo.Mesh(m).color('b5').lw(0.1)
vedo.show(vedo_mesh,
          "Applied pymeshlab filter: " + filter + "\nMesh has " + str(points) + " points and " + str(
              face) + " faces " + "\nwith selected " + str(
              nf_2) + "faces with angle normal greater to 60 ", axes=True, bg='green9', bg2='blue9',
          title="Kidney")


# ----------------------------------------- NON MANIFOLD -------------------------------------------------------

filter='select_non_manifold_edges_'
after_smoothing.apply_filter(filter)

points = after_smoothing.current_mesh().vertex_number()
face = after_smoothing.current_mesh().face_number()
m = after_smoothing.current_mesh()
nf_2 = m.selected_face_number()

vedo_mesh = vedo.Mesh(m).color('b5').lw(0.1)
vedo.show(vedo_mesh,
          "Applied pymeshlab filter: " + filter + "\nMesh has " + str(points) + " points and " + str(
              face) + " faces " + "\nwith selected " + str(
              nf_2) + "non-manifold faces ", axes=True, bg='green9', bg2='blue9',
          title="Kidney")


filter='select_non_manifold_edges_'
repaired_mesh.apply_filter(filter)

points = repaired_mesh.current_mesh().vertex_number()
face = repaired_mesh.current_mesh().face_number()
m = repaired_mesh.current_mesh()
nf_3 = m.selected_face_number()

vedo_mesh = vedo.Mesh(m).color('b5').lw(0.1)
vedo.show(vedo_mesh,
          "Applied pymeshlab filter: " + filter + "\nMesh has " + str(points) + " points and " + str(
              face) + " faces " + "\nwith selected " + str(
              nf_3) + "non_manifold_edges ", axes=True, bg='green9', bg2='blue9',
          title="Kidney")


# filter='select_non_manifold_edges_'
# cutted_mesh.apply_filter(filter)
#
# points = cutted_mesh.current_mesh().vertex_number()
# face = cutted_mesh.current_mesh().face_number()
# m = cutted_mesh.current_mesh()
# nf_4 = m.selected_face_number()
#
# vedo_mesh = vedo.Mesh(m).color('b5').lw(0.1)
# vedo.show(vedo_mesh,
#           "Applied pymeshlab filter: " + filter + "\nMesh has " + str(points) + " points and " + str(
#               face) + " faces " + "\nwith selected " + str(
#               nf_4) + "non_manifold_edges ", axes=True, bg='green9', bg2='blue9',
#           title="Kidney")
#
# # -------------------------------------------------------------------------------------------------------
# filter='select_non_manifold_edges_'
# ground_truth.apply_filter(filter)
#
# points = ground_truth.current_mesh().vertex_number()
# face = ground_truth.current_mesh().face_number()
# m = ground_truth.current_mesh()
# nf_4 = m.selected_face_number()
#
# vedo_mesh = vedo.Mesh(m).color('b5').lw(0.1)
# vedo.show(vedo_mesh,
#           "Applied pymeshlab filter: " + filter + "\nMesh ground truth has " + str(points) + " points and " + str(
#               face) + " faces " + "\nwith selected " + str(
#               nf_4) + "non_manifold_edges ", axes=True, bg='green9', bg2='blue9',
#           title="Kidney")
#
# filter='select_non_manifold_edges_'
# predicted.apply_filter(filter)
#
# points = predicted.current_mesh().vertex_number()
# face = predicted.current_mesh().face_number()
# m = predicted.current_mesh()
# nf_4 = m.selected_face_number()
#
# vedo_mesh = vedo.Mesh(m).color('b5').lw(0.1)
# vedo.show(vedo_mesh,
#           "Applied pymeshlab filter: " + filter + "\nMesh predicted has " + str(points) + " points and " + str(
#               face) + " faces " + "\nwith selected " + str(
#               nf_4) + "non_manifold_edges ", axes=True, bg='green9', bg2='blue9',
#           title="Kidney")