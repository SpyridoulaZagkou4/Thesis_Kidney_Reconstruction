import pymeshlab
import vedo
# after_isotropic_remeshing = pymeshlab.MeshSet()
# after_isotropic_remeshing.load_new_mesh("F:/aadiplwmatikoula/1_final/case_00001/isotropic_remeshing/remeshed.stl")
# after_isotropic_remeshing.load_new_mesh("F:/aadiplwmatikoula/meshes_kits21/case_00001/remeshing/isotropic_remeshing.stl")

after_isotropic_remeshing = pymeshlab.MeshSet()
after_isotropic_remeshing.load_new_mesh("F:/aadiplwmatikoula/1_final/case_00001/isotropic_remeshing/remeshed.stl")
#after_isotropic_remeshing=vedo.Mesh("F:/aadiplwmatikoula/1_final/case_00001/isotropic_remeshing/remeshed.stl").computeNormals()

after_smoothing = pymeshlab.MeshSet()
after_smoothing.load_new_mesh("F:/aadiplwmatikoula/1_final/case_00001/laplacian_smooth/smoother.stl")
# after_smoothing.load_new_mesh("F:/aadiplwmatikoula/meshes_kits21/case_00001/remeshing/smoother.stl")


# ----------------------------------- BEFORE SMOOTHING  --------------------------------------------------
filter = 'select_problematic_faces'
after_isotropic_remeshing.apply_filter(filter, usear=False, usenf=True, nfratio=60)

m = after_isotropic_remeshing.current_mesh()
points = m.vertex_number()
face = m.face_number()
korufes= m.vertex_matrix()
triangles = m.face_matrix()
norms = m.face_normal_matrix()
#
nf_1 = m.selected_face_number()
#vec = m.face_selection_array()


# Triangles Centers of mass
cms=[]
for i in range(len(triangles)):
    cm=0
    for j in triangles[i]:
        cm = (cm + korufes[j])
    cms.append(cm/3)

# Remove normals accordind to center of mass of triangles
for i in range(len(norms)):
    norms[i]=norms[i]+cms[i]
normal_mesh=vedo.Mesh(norms)

# Visualize normals
arrows = []
for i in range(len(norms)):
    arrows.append(vedo.shapes.Line(cms[i], norms[i], c=(1,0,0)))

kidney=vedo.Mesh(after_isotropic_remeshing).color('b5').lw(0.1)
vedo.show(kidney, arrows, normal_mesh)


# -----------------,----------------- AFTER SMOOTHING --------------------------------------------
filter = 'select_problematic_faces'
after_smoothing.apply_filter(filter, usear=False, usenf=True, nfratio=60)

m = after_smoothing.current_mesh()
points = m.vertex_number()
face = m.face_number()
korufes= m.vertex_matrix()
triangles = m.face_matrix()
norms = m.face_normal_matrix()
#
nf_1 = m.selected_face_number()
#vec = m.face_selection_array()


# Triangles Centers of mass
cms=[]
for i in range(len(triangles)):
    cm=0
    for j in triangles[i]:
        cm = (cm + korufes[j])
    cms.append(cm/3)

# Remove normals accordind to center of mass of triangles
for i in range(len(norms)):
    norms[i]=norms[i]+cms[i]
normal_mesh=vedo.Mesh(norms)

# Visualize normals
arrows = []
for i in range(len(norms)):
    arrows.append(vedo.shapes.Line(cms[i], norms[i], c=(1,0,0)))

kidney=vedo.Mesh(after_smoothing).color('b5').lw(0.1)
vedo.show(kidney, arrows, normal_mesh)


