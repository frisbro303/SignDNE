# SignDNE
SignDNE is a Python package designed for evolutionary biologists, providing an intuitive tool to robustly calculate the shape complexity metric ariaDNE and its sign-oriented extension. SignDNE can be used as a [Python library](https://github.com/frisbro303/signDNE_Python/blob/main/docs.md#Using-SignDNE-as-a-Python-library) and as a standalone [command line interface](https://github.com/frisbro303/signDNE_Python/blob/main/docs.md#command-line-interface).

See the [arXiv preprint paper](https://arxiv.org/abs/2409.05549) for an exposition and discussion, of our novel robust algorithm for calculating the sign-oriented extension.

Note! To accommodate legacy users, we have updated the original MATLAB implementation of ariaDNE to include the new sign-oriented extension: 
https://github.com/frisbro303/signDNE_MATLAB.

## Installation
![PyPI](https://img.shields.io/pypi/v/signDNE)

The recommended installation method is to install the latest tagged release with `pip`:
```bash
pip install signDNE
```
Alternatively, you can install the latest development version of `SignDNE` by running:
```bash
pip install git+https://github.com/frisbro303/SignDNE
```

## Using `SignDNE` as a Python library
To get started with using `SignDNE` as a library, simply import the `signDNE` function:
```Python
from signDNE import signDNE
```
You are now ready to use the ariaDNE metric and its sign-oriented extension as library in your research. The function is documented below.


The function takes the takes the following inputs:
- Mesh in the format of the Trimesh library. If the mesh is not watertight, a watertight version of the mesh is generated on the fly to use for ray casting.
- Optional bandwidth, for specifying local influence in DNE calculation. Default is set to be $0.08$.
- Optional distance cutoff for the local neighborhoods used to calculate DNE. Default is $0$.
- Optional desired distance metric, either Euclidean or Geodesic. Default is Euclidean.
- Optional pre-computed distances. The format of which should be a symmetric $n times n$  matrix with pairwise distances, where $n$ is the number of points.

With the following outputs:
- *local_curvature*,  which is an ordered list of the signed local bending estimates for each vertex.
- *local_dne*, which is local_curvature weighted by the vertex area. The vertex area is defined as the average area of the adjacent triangular faces.
- *dne*, which is the original DNE value. This is also the sum of *local_dne*.
- *positive_dne*, which is the positive component of DNE.
- *negative_dne*, which is the negative component of DNE.
- *surface_area*, which is the total surface area of the input mesh.
- *positive_surface_area*, which is the surface area of the positive DNE regions.
- *negative_surface_area*, which is the surface area of the negative DNE regions.


The following preprocessing is automatically performed:
- Closing of all holes if given mesh is non-watertight.
- remove degenerate faces
- remove duplicate faces
- remove unreferenced vertices
- remove infinite values from face and vertex data


## Command line interface
Command line interface for `SignDNE`.

### Usage
```
signDNE input [input] [-h] [-v] [-o [OUTPUT]] [-b BANDWIDTH] [-d {Euclidean,Geodesic}] [-c CUTOFF]
```

#### Arguments

- `input`: Path to mesh file(s) or directory containing mesh files. Files should be PLY or OBJ format. 

#### Options

- `-h`, `--help`: Show help message and exit
- `-v`, `--visualize`: Visualize 3d mesh colored by normalized local DNE values (only for single file inputs)
- `-o [OUTPUT]`, `--output [OUTPUT]`: Specify output path for results (default: results.csv).
- `-b BANDWIDTH`, `--bandwidth BANDWIDTH`: Set the bandwidth for DNE calculation (default: 0.08)
- `-d {Euclidean,Geodesic}`, `--distance-type {Euclidean,Geodesic}`: Specify the distance type for calculations (default: Euclidean)
- `-c CUTOFF`, `--cutoff CUTOFF`: Set the cut-off threshold for DNE calculation (default: 0)

### Output

The CLI outputs the following values for each processed mesh as coloumns:

- File name
- DNE
- Positive component of DNE
- Negative component of DNE
- Surface area
- Positive surface area
- Negative surface area

If the `-o` or `--output` flag is off, results will be outputed to STDOUT.

### Visualization

When the `-v` or `--visualize` flag is used with a single input file, the tool will display a 3D visualization of the mesh. The mesh will be colored based on the normalized curvature values, color gradient from blue through white to red. Blue represents low curvature values and red represents high curvature values.

### Examples

1. Calculate signed ariaDNE for a single file and visualize:
   ```
   signDNE path/to/mesh.ply -v
   ```

2. Calculate signed ariaDNE for multiple files and save results to CSV:
   ```
   signDNE path/to/mesh1.obj path/to/mesh2.ply -o results.csv
   ```

3. Calculate signed ariaDNE for all mesh files in a directory with custom bandwidth:
   ```
   signDNE path/to/mesh/directory -b 0.1
   ```


## Dependencies
- scipy
- trimesh
- numpy
- pyvista
- pandas
- networkx
- rtree
- pyglet<2
