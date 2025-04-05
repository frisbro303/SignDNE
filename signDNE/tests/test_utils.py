import pytest
import trimesh
from utils import close_holes

def test_close_holes():
    mesh = trimesh.load("signDNE/data/normal.ply")
    watertight_mesh = close_holes(mesh)
    assert watertight_mesh.is_watertight == True

