from scipy.spatial.distance import pdist, squareform
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
import numpy as np
import trimesh
from src.utils import compute_face2vertex, triangulation_to_adjacency_matrix, close_holes


def prep(mesh):
    """
    Prepare mesh by simple preprocesing
    """
    mesh.fill_holes()
    mesh.update_faces(mesh.nondegenerate_faces(height=1e-08))
    mesh.update_faces(mesh.unique_faces())
    mesh.remove_infinite_values()
    mesh.remove_unreferenced_vertices()


def compute_vertex_area(mesh, f2v):
    face_area = mesh.area_faces
    vertex_area= (face_area.T @ f2v) / 3
    return vertex_area


def make_watertight(mesh):
    if mesh.is_watertight:
        watertight_mesh = mesh
    else:
        watertight_mesh = close_holes(mesh)
    return watertight_mesh


def centralize(mesh):
    center = np.sum(mesh.vertices, 0) / mesh.vertices.shape[0]
    mesh.vertices -= center


def rescale(mesh):
    scale_factor = np.sqrt(1 / mesh.area)
    mesh.vertices *= scale_factor
        

def compute_vertex_normals(mesh):
    """
    Calculate non-weighted vertex normals 
    """
    face_normals = mesh.face_normals
    vertex_normals = np.zeros(mesh.vertices.shape)

    for i, face in enumerate(mesh.faces):
        for vertex in face:
            vertex_normals[vertex] += face_normals[i]
    vertex_normals = trimesh.util.unitize(vertex_normals)

    return vertex_normals


def get_dists(precomputed_dist, points, faces, num_points, distance_type):
    if precomputed_dist is not None:
        if isinstance(precomputed_dist, np.ndarray) and precomputed_dist.shape == (num_points, num_points):
            d_dist = precomputed_dist
        else:
            raise TypeError(
                "Variable precomputed_dist must be a square numpy array "
                "with size equal to the number of points"
            )
    elif distance_type == 'Geodesic':
        d_dist = dijkstra(triangulation_to_adjacency_matrix(points, faces, num_points), directed=False)
    elif distance_type == 'Euclidean':
        d_dist = squareform(pdist(points))
    else:
        raise NameError(
            "Provide valid precomputed_dist or set distance_type to either "
            "'Geodesic' or 'Euclidean'"
        )
    return d_dist


def build_covariance_matrix(p, w):
    cov = np.zeros((6,))
    cov[0] = np.sum(p[:, 0] * w.T * p[:, 0], axis=0)
    cov[1] = np.sum(p[:, 0] * w.T * p[:, 1], axis=0)
    cov[2] = np.sum(p[:, 0] * w.T * p[:, 2], axis=0)
    cov[3] = np.sum(p[:, 1] * w.T * p[:, 1], axis=0)
    cov[4] = np.sum(p[:, 1] * w.T * p[:, 2], axis=0)
    cov[5] = np.sum(p[:, 2] * w.T * p[:, 2], axis=0)
    cov /= np.sum(w)

    cov_mat = np.array([
        [cov[0], cov[1], cov[2]],
        [cov[1], cov[3], cov[4]],
        [cov[2], cov[4], cov[5]]
    ])
    return cov_mat


def determine_curvature_orientation(points, neighbour, weight, watertight_mesh):
    # Calculate weighted neighborhood centroid
    neighbour_centroid = np.sum(points[neighbour, :] * weight.T[:, np.newaxis], axis=0) / np.sum(weight)

    # Determine if the centroid is inside or not to find the sign of curvature
    inside = watertight_mesh.ray.contains_points([neighbour_centroid])
    sign = int(inside) * 2 - 1
    return sign


def choose_arg_eig(normals, v, jj, vertex_normals):
    v_aug = np.hstack([v, -v])
    diff = v_aug - np.tile(vertex_normals[jj, :], (6, 1)).T
    q = np.sum(diff ** 2, axis=0)
    k = np.argmin(q)
    normals[jj, :] = v_aug[:, k]
    k %= 3
    return k


def aria_dne(
    mesh, bandwidth=0.08, cutoff=0, distance_type='Euclidean',
    precomputed_dist=None):
    """
    Compute the ariaDNE and signed ariaDNE values of a mesh surface.

    Parameters:
    mesh : trimesh.Trimesh
        The mesh to be analyzed.
    bandwidth : float, optional
        The epsilon value in the weight function (default is 0.08).
    cutoff : float, optional
        The cutoff distance for neighbors (default is 0).
    distance_type : str, optional
        Type of distance metric ('Euclidean' or 'Geodesic', default is 'Euclidean').
    precomputed_dist : numpy.ndarray, optional
        Precomputed distance matrix.

    Returns:
        local DNE, local curvature, DNE, positive DNE, negative DNE,
        surface area, positive surface area, and negative surface area.
    """

    if not isinstance(mesh, trimesh.base.Trimesh):
        raise TypeError("mesh must be an instance of trimesh.base.Trimesh")

    prep(mesh)
    centralize(mesh)

    face2vertex = compute_face2vertex(mesh)

    unnormalized_vertex_area = compute_vertex_area(mesh, face2vertex)
    rescale(mesh)
    vertex_area = compute_vertex_area(mesh, face2vertex)

    watertight_mesh = make_watertight(mesh)

    vertex_normals = compute_vertex_normals(mesh)

    num_points = np.shape(mesh.vertices)[0]
    normals = np.zeros((num_points, 3))
    local_curvature = np.zeros(num_points)

    d_dist = get_dists(precomputed_dist, mesh.vertices, mesh.faces, num_points, distance_type)
    kernel = np.exp(-d_dist ** 2 / bandwidth ** 2)

    # Estimate curvature via PCA for each vertex in the mesh
    for jj in range(num_points):
        neighbour = np.where(kernel[jj, :] > cutoff)[0]
        num_neighbours = len(neighbour)
        if num_neighbours <= 3:
            print(f'aria_dne: Too few neighbors on vertex {jj}.')
        p = np.tile(mesh.vertices[jj, :3], (num_neighbours, 1)) - mesh.vertices[neighbour, :3]
        weights = kernel[jj, neighbour]

        cov_mat = build_covariance_matrix(p, weights)

        # Compute eigenvalues and eigenvectors
        eigvals, eigvecs = np.linalg.eig(cov_mat)

        chosen_eigvec = choose_arg_eig(normals, eigvecs, jj, vertex_normals)
        # Update the vertex normal using chosen eigenvector

        orientation_sign = determine_curvature_orientation(mesh.vertices, neighbour, weights, watertight_mesh)

        # Estimate curvature using the eigenvalue
        lambda_ = eigvals[chosen_eigvec]
        local_curvature[jj] = (lambda_ / np.sum(eigvals)) * orientation_sign

    # Save the outputs
    local_dne = np.multiply(local_curvature, vertex_area)
    dne = np.sum(np.abs(local_dne))

    positive_indices = np.where(local_dne >= 0)
    negative_indices = np.where(local_dne < 0)

    positive_dne = np.sum(local_dne[positive_indices])
    negative_dne = np.abs(np.sum(local_dne[negative_indices]))

    surface_area = np.sum(unnormalized_vertex_area)
    positive_surface_area = np.sum(unnormalized_vertex_area[positive_indices])
    negative_surface_area = np.sum(unnormalized_vertex_area[negative_indices])

    return (
        local_dne, local_curvature, dne, positive_dne, negative_dne,
        surface_area, positive_surface_area, negative_surface_area
    )
