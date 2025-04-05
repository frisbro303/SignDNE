import pytest
import trimesh
import numpy as np

from signDNE import prep, compute_vertex_area, aria_dne
from utils import compute_face2vertex


def test_prep():
    mesh = trimesh.load("signDNE/data/normal.ply")
    prep(mesh)
    assert not mesh.is_empty
    assert np.all(np.isfinite(mesh.vertices))
    assert np.all(np.isfinite(mesh.faces))
    assert len(mesh.faces) > 0


# def test_compute_vertex_area():
#     """
#     """
#     mesh = trimesh.primitives.Box()
#     expected = np.repeat([1/3], 8)
#     f2v = compute_face2vertex(mesh)
#     vertex_area = compute_vertex_area(mesh, f2v)
#     assert np.allclose(vertex_area, 1/3) == True


def test_signDNE():
    """
    Expected values are copied from the original MATLAB implementation
    """
    mesh = trimesh.load("signDNE/data/normal.ply")
    results = aria_dne(mesh)

    assert round(results[2], 4) == 0.1190


