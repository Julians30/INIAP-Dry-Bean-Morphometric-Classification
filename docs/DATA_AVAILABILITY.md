# Data Availability

## Repository scope

This repository is intentionally limited to reproducibility materials for the computational analysis reported in the manuscript.

It does **not** contain:

- the original morphometric dataset;
- source grain images;
- raw image-acquisition metadata;
- segmentation masks or contour maps;
- other upstream materials related to external-contour generation;
- model-access credentials or API tokens;
- pretrained TabPFN checkpoint files.

## Original morphometric data

The study dataset contains 4,000 individual dry bean grains from four certified INIAP cultivars, represented by 11 morphometric descriptors used in the primary analysis.

The tabular morphometric dataset is not publicly deposited and is not included in this repository. It may be made available by the corresponding author upon reasonable request, subject to prior authorization and the applicable conditions governing its use.

## Source images and upstream image-processing materials

The source grain images and associated materials related to image acquisition and external-contour generation form part of a separate ongoing doctoral research component. They fall outside the scope of the present classification article, are not included in this repository or in supplementary files, and are not available for redistribution through this article.

The classifiers reported in the manuscript were trained and evaluated exclusively on the finalized tabular morphometric dataset; source images and upstream image-processing materials were not classifier inputs.

## What is public here

The repository provides:

- source code and audited analysis notebooks;
- experimental and validation configurations;
- derived numerical results;
- publication tables and figures;
- statistical-analysis outputs;
- reproducibility and environment documentation.

This separation allows the computational procedure reported in the manuscript to be audited without publicly redistributing the source dataset or upstream doctoral-research materials.

## Supplementary-material boundary

The manuscript does not include supplementary materials. This repository is a standalone public reproducibility resource cited in the Data Availability Statement and should not be interpreted as a supplementary-files package.

## License boundary

The repository's MIT License applies to the software, notebooks, documentation, and other computational materials distributed through this repository. It does not grant rights to the original morphometric dataset, source grain images, raw acquisition metadata, segmentation masks, contour maps, or other upstream materials because those items are not distributed here.

## Manuscript-ready Data Availability Statement

> The tabular morphometric dataset analyzed in this study is not publicly deposited and is not included in the public repository associated with this article. It may be made available by the corresponding author upon reasonable request, subject to prior authorization and the applicable conditions governing its use. The source grain images and associated materials related to image acquisition and external-contour generation are not included in the public repository or supplementary files because they form part of a separate ongoing doctoral research component and fall outside the scope of the present study; they are not available for redistribution through this article. The source code, analysis notebooks, experimental configurations, derived numerical results, tables, figures, and other reproducibility materials required to reproduce the reported computational analyses with the tabular morphometric data are openly available under the MIT License on GitHub at https://github.com/Julians30/INIAP-Dry-Bean-Morphometric-Classification (accessed on 24 September 2026).
