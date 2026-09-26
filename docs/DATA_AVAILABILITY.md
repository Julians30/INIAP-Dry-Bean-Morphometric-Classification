# Data Availability

## Repository scope

This repository is intentionally limited to reproducibility materials for the computational analysis reported in the manuscript.

It does **not** contain:

- the original morphometric dataset;
- raw grain photographs;
- raw image-acquisition metadata;
- segmentation masks or contour maps;
- model-access credentials or API tokens;
- pretrained TabPFN checkpoint files.

## Original morphometric data

The study dataset contains 4,000 individual dry bean grains from four certified INIAP cultivars, represented by 11 morphometric descriptors used in the primary analysis.

The tabular morphometric dataset is not publicly redistributed through GitHub. Access may be considered for qualified researchers upon reasonable request to the corresponding author and is subject to the applicable authorization conditions.

## Raw images and upstream image-processing materials

The source grain images, raw acquisition metadata, segmentation masks, contour maps, and related upstream image-processing materials form part of a separate ongoing doctoral research component. They are outside the analytical scope of the present classification article and are not included in this repository or its public supplementary package.

The classifiers reported in the manuscript were trained and evaluated exclusively on the finalized tabular morphometric dataset; raw images, masks, and contour maps were not classifier inputs.

## What is public here

The repository is designed to provide:

- analysis notebooks;
- model and validation configuration;
- selected derived results;
- publication tables and figures;
- statistical-analysis workflow;
- reproducibility documentation.

This separation allows the computational procedure reported in the manuscript to be audited without publicly redistributing restricted source data.

## License boundary

The repository's MIT License applies to the software, notebooks, documentation, and other computational materials distributed through this repository. It does not grant rights to the original morphometric dataset, raw photographs, raw acquisition metadata, segmentation masks, or contour maps because those materials are not distributed here.

## Manuscript-ready Data Availability Statement

> The tabular morphometric dataset analyzed in this study is available on reasonable request from the corresponding author, subject to prior authorization and the applicable conditions governing its use. It is not publicly deposited because it forms part of an ongoing research program. The source grain images and upstream image-processing materials are not publicly available with this article because they form part of a separate ongoing doctoral research component and were not used as classifier inputs in the analyses reported here. The analysis code, audited notebooks, selected derived results, statistical outputs, publication figures, and reproducibility documentation are publicly available at https://github.com/Julians30/INIAP-Dry-Bean-Morphometric-Classification under the MIT License.
