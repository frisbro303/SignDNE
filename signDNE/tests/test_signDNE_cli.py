import pytest
from unittest.mock import patch

from _signDNE_cli import parse_arguments
from _signDNE_cli import visualize_mesh
from _signDNE_cli import safe_load
from _signDNE_cli import get_file_names
from _signDNE_cli import main


def test_get_file_names(tmp_path):
    file = tmp_path / "file.obj"
    file.write_text("dummy")
    subdir = tmp_path / "folder"
    subdir.mkdir()
    nested_file = subdir / "nested.obj"
    nested_file.write_text("data")

    files = get_file_names([str(tmp_path)])
    assert len(files) == 2
    assert all(f.is_file() for f in files)


@patch("trimesh.Scene.show")
def test_visualize_mesh(mock_show):
    mesh = trimesh.creation.icosphere()
    local_dne = np.random.rand(len(mesh.vertices))
    visualize_mesh(mesh, local_dne)
    mock_show.assert_called_once()

    
def test_parse_arguments():
    test_args = ["prog", "mesh.obj", "-v", "-b", "0.05", "-d", "Geodesic", "-c", "0.1"]
    with patch("sys.argv", test_args):
        args = parse_arguments()
        assert args.visualize
        assert args.bandwidth == 0.05
        assert args.distance_type == "Geodesic"
        assert args.cutoff == 0.1


def test_safe_load_success():
    file_path = "signDNE/data/normal.ply"
    mesh, path = safe_load(file_path)
    assert isinstance(mesh, trimesh.Trimesh)
    assert path == file_path


def test_safe_load_failure():
    result = safe_load("bad_file.obj")
    assert result is None



# @patch("src.your_module.aria_dne")
# @patch("src.your_module.safe_load")
# @patch("src.your_module.get_file_names")
# @patch("src.your_module.output_results")
def test_main_logic(capsys):
    mock_args = ["prog", "signDNE/data/normal.ply"]

    with patch("sys.argv", mock_args):
        main()
        captured = capsys.readouterr()
        
        assert captured == True
