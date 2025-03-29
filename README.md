# SignDNE
SignDNE is a Python package for calculating the shape complexity metric ariaDNE and its sign-oriented extension.

## Documentation
The documentation `signDNE` is found 

## Installation
The package is installed by running the following command:
```
$ pip install git+https://github.com/frisbro303/signDNE_python.git
```

### Examples

1. Calculate signed ariaDNE for a single file and visualize:
   ```bash
   $ signDNE path/to/mesh.ply -v
   ```

2. Calculate signed ariaDNE for multiple files and save results to CSV:
   ```bash
   $ signDNE path/to/mesh1.obj path/to/mesh2.ply -o results.csv
   ```

3. Calculate signed ariaDNE for all mesh files in a directory with custom bandwidth:
   ```bash
   $ signDNE path/to/mesh/directory -b 0.1
   ```

## Contributors 

