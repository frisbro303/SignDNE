import pytest
import trimesh
from utils import close_holes

def test_close_holes():
    mesh = trimesh.load("signDNE/normal.ply")
    watertight_mesh = close_holes(mesh)
    assert mesh.is_watertight()

