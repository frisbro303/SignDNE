import pytest
import trimesh
import numpy as np

from utils import close_holes
from utils import triangulation_to_adjacency_matrix
from utils import compute_face2vertex

def test_close_holes():
    mesh = trimesh.load("signDNE/data/normal.ply")
    watertight_mesh = close_holes(mesh)
    assert watertight_mesh.is_watertight == True


def test_triangulation_to_adjacency_matrix():
    vertices = np.array([[0, 1], [0, 2], [1, 1]])
    faces = np.array([[0, 1, 2]])
    expected_mat = np.array([[0, 1, 1], [1, 0, np.sqrt(2)], [1, np.sqrt(2), 0]])
    adj_mat = triangulation_to_adjacency_matrix(vertices, faces, len(vertices))
    assert np.allclose(expected_mat, adj_mat) == True


def test_compute_face2vertex():
    vertices = np.array([[0, 1], [0, 2], [1, 1]])
    faces = np.array([[0, 1, 2]])
    mesh = trimesh.Trimesh(vertices, faces)
    expected = np.array([[1, 1, 1]])
    f2v = compute_face2vertex(mesh)
    assert np.array_equal(f2v, expected) == True

