---
title: 'SignDNE: A Python package for calculating ariaDNE and its sign-oriented extensions'
tags:
  - Python
  - Morphometrics
  - Biology
  - ariaDNE
  - SignDNE
  - Dirichlet Normal Energy
  - Shape complexity metric
  - Morphology
authors:
  - name: Felix R. Hjerrild
    orcid: 0009-0007-3158-0553
    affiliation: 1
  - name: Shan Shan
    orcid: 0000-0002-2880-0566
    affiliation: 1
  - name: Doug M. Boyer
    orcid: 0000-0002-8697-2999
    affiliation: 2
  - name: Ingrid Daubechies
    orcid: 0000-0002-6472-1056
    affiliation: 3
affiliations:
 - name: Department of Mathematics and Computer Science, University of Southern Denmark
   index: 1
 - name: Department of Evolutionary Anthropology, Duke University
   index: 2
 - name: Department of Mathematics, Duke University
   index: 3
date: 31 March 2025
bibliography: paper.bib
---

# Summary
Biological shapes and anatomical structures are fundamental to the study of evolutionary biology. Numerical descriptors that quantify the overall geometry of biological forms are essential tools for the modeling, analysis, and understanding of evolutionary processes. The Dirichlet Normal Energy (DNE) is a shape complexity metric that addresses this by summarizing the local curvature of surfaces, particularly aiding analytical studies and providing insights into evolutionary and functional adaptations. The sign-oriented DNE is a natural extension of DNE, that distinguishes between the convex and concave regions of a surface by assigning signs to each point. Specifically, it assigns a positive sign when the surface bends outward -- like a cusp or a ridge, and a negative sign when the surface bends inward -- like a valley.

![Visualization of local curvature field on various biological specimens identified by their MorphoSource media identifiers. Positive curvature regions are shaded red, and negative curvature regions are shaded blue.](visualization-demo.png)

`signDNE` is a new Python package for calculating DNE and sign-oriented DNE. The package faithfully reproduces the robust `ariaDNE` algorithm for calculating DNE, and includes a novel algorithm for robustly determining DNE signs. The implementation improves accessibility and usability by providing a visualization tool, aiding evolutionary biologists in their research, along with batch processing features. @visualization-demo illustrates the visualization functionality of the local DNE field on various biological specimens.
Alongside the new Python implementation, the original MATLAB implementation of `ariaDNE` has been updated to include the sign-oriented extension.

# Acknowledgement
DB is supported by NSF BCS 1552848 and NSF DBI 1759839. ID acknowledges the support of the Math+X grant 400837 from the Simons Foundation. 

# References
