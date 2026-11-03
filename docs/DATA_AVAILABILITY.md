# Data Availability

## Repository scope

This repository provides the reproducibility materials for the computational analyses reported in the manuscript.

Public materials include:

- source code and audited analysis notebooks;
- experimental and validation configurations;
- derived numerical results;
- statistical-analysis outputs;
- publication tables and figures;
- reproducibility and environment documentation.

## Original morphometric data

The analytical dataset contains 4,000 individual dry bean grains from four certified INIAP cultivars represented by 11 morphometric descriptors.

The morphometric dataset is **not publicly deposited** and is not included in this repository. It may be made available by the corresponding author upon reasonable request, subject to prior authorization and the applicable conditions governing its use.

## Reproducibility boundary

The public repository allows the complete computational design, model definitions, validation logic, statistical analyses, calibration procedure, selective-prediction analysis, tables, and figures to be audited. Full rerunning from raw observations requires authorized access to the source morphometric dataset.

Private access credentials, API tokens, and pretrained TabPFN checkpoint files are not distributed.

## License boundary

The MIT License applies to the software, notebooks, documentation, and computational materials distributed through this repository. It does not grant rights to the original morphometric dataset because the dataset is not distributed here.

## Manuscript-aligned Data Availability Statement

> The morphometric dataset analyzed in this study is not publicly deposited and may be made available by the corresponding author upon reasonable request, subject to prior authorization and the applicable conditions governing its use. The source code, analysis notebooks, experimental configurations, derived numerical results, tables, figures, and reproducibility documentation are openly available under the MIT License at https://github.com/Julians30/INIAP-Dry-Bean-Morphometric-Classification (accessed on 28 September 2026). The morphometric table forms part of an ongoing doctoral research program, which is why it is not publicly deposited; when made available under the conditions stated above, it allows the complete re-execution of all reported analyses. The repository documents the notebook execution order, the generation of outer and inner folds (stratified K-fold with shuffling, outer seeds 2026–2028 and inner seeds equal to the outer seed plus the fold index), the exact software versions, and the procedure for obtaining the pretrained TabPFN weights through the tabpfn package after registration with Prior Labs; the weights themselves are not redistributed.
