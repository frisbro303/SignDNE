import pytest
import trimesh
import numpy as np

from signDNE import prep
from signDNE import compute_vertex_area
from signDNE import aria_dne
from signDNE import make_watertight

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
    Tests against DNE values computed with the original MATLAB implementation 
    """
    mesh_names = ["normal", "low", "high", "noise1", "noise2", "smooth"]
    expected_dnes = np.loadtxt("signDNE/tests/MATLAB_dnes.txt", delimiter = ",")
    dnes = np.zeros(len(mesh))
    for i in range(len(mesh_names)):
        mesh = trimesh.load(f"signDNE/data/{mesh_names[i]}.ply")
        dne = aria_dne(mesh)[2]
        dnes[i] = dne
        

    assert np.allclose(expected_dnes, dnes)


def test_determine_curvature_orientation():
    pass


def test_centralize():
    pass


def test_make_watertight():
    mesh = trimesh.load("signDNE/data/normal.ply")
    watertight_mesh = make_watertight(mesh)
    assert watertight_mesh.is_watertight == True


def test_rescale():
    pass
