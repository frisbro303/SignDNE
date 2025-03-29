# SignDNE
SignDNE is a Python package for calculating the shape complexity metric ariaDNE and its sign-oriented extension.

## Documentation
Documentation for `SignDNE` is found in [docs.md](docs.md).

## Installation
The recommended installation method is with `pip`:
```bash
pip install git+https://github.com/frisbro303/signDNE_python.git
```

A guide to installing from source is detailed in the [installation section](docs.md) of the [documentation](docs.md).

## Examples

1. Calculate signed ariaDNE for a single file and visualize:
   ```bash
   signDNE path/to/mesh.ply -v
   ```

2. Calculate signed ariaDNE for multiple files and save results to CSV:
   ```bash
   signDNE path/to/mesh1.obj path/to/mesh2.ply -o results.csv
   ```

3. Calculate signed ariaDNE for all mesh files in a directory with custom bandwidth:
   ```bash
   signDNE path/to/mesh/directory -b 0.1
   ```

## Contributors 

