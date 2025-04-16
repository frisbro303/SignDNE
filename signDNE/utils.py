from scipy.sparse import csr_matrix
import numpy as np
import pyvista as pv
import trimesh


def compute_face2vertex(mesh):
    F = mesh.faces.T
    V = mesh.vertices.T
    nf = F.shape[1]
    nv = V.shape[1]
    I = np.hstack((F[0], F[1], F[2]))
    J = np.hstack((np.arange(nf), np.arange(nf), np.arange(nf)))
    S = np.ones(len(I))
    F2V = csr_matrix((S, (J, I)), shape=(nf, nv))
    return F2V


def triangulation_to_adjacency_matrix(vertices, faces, num_points):
    """
    Constructs triangulation matrix to compute geodesic distance using Dijkstra  
    """
    A = np.zeros((num_points, num_points))
    for face in faces:
        for i in range(3):
            j = (i + 1) % 3
            v1 = face[i]
            v2 = face[j]
            dist = np.linalg.norm(vertices[v1] - vertices[v2])
            A[v1, v2] = dist
            A[v2, v1] = dist
    return A


def close_holes(tm_mesh):
    """
    Close all holes in the mesh to make it watertight.
    """
    pv_mesh = pv.wrap(tm_mesh)
    filled_mesh = pv_mesh.fill_holes(hole_size=float('inf'))
    vertices = filled_mesh.points
    faces = filled_mesh.faces.reshape((-1, 4))[:, 1:]
    tm_closed_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    tm_closed_mesh.fix_normals()
    return tm_closed_mesh
