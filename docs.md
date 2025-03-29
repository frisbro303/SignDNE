## signDNE library
In order to acess the ariaDNE function add `from signDNE import aria_dne` to your script.

The function will calculate local DNE, local curvature values, DNE, positiveDNE component, and negativeDNE component.

The following preprocessing is automatically performed:
- Closing of all holes if given mesh is non-watertight.
- remove degenerate faces
- remove duplicate faces
- remove unreferenced vertices
- remove infinite values from face and vertex data
  
## Installation
## Command line interface
Command line interface for the `ariaDNE` function.

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


Note! To accommodate legacy users, we have updated the original MATLAB implementation of ariaDNE to include the new sign-oriented extension: 
https://github.com/frisbro303/signDNE_MATLAB.

