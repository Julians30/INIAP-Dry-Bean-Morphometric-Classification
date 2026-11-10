# Study Scope, Limitations, and External-Validation Requirements

This document describes the scientific and operational boundary of the revised *AgriEngineering* manuscript, *Reliability-Oriented Morphometric Classification of INIAP Dry Bean Cultivars Using Artificial Intelligence: TabPFN, Calibration, Selective Prediction, and Redundancy Ablation*. It is a reproducibility and interpretation guide, not evidence of additional experiments.

## Demonstrated task

The analysis concerns **closed-set, grain-level classification** of **4,000 photographed dry bean grains** (1,000 per cultivar) from **INIAP 420, INIAP 425, INIAP 481, and INIAP 485**, using 11 image-derived morphometric descriptors. The reported repeated nested stratified cross-validation has three seeds and five outer folds per seed, with inner-fold model selection where applicable. Performance estimates apply to this analytical dataset and evaluation protocol.

TabPFN achieved mean macro-F1 = **0.9866** on FULL_11; LDA-XGBoost achieved **0.9797**. The six-descriptor sensitivity analysis (STRICT_6) yielded **0.9854** and **0.9796**, respectively. These results describe discrimination among the four modeled classes, not verified generalization to other seed lots or operational facilities.

## Sampling and acquisition boundaries

- Each cultivar was represented by a **single certified seed source** kept in a separate labeled bag; independently sampled seed lots were not available.
- Seed-lot identifiers, production sites, harvest seasons, and **per-grain acquisition dates** were not retained in the modeling table. Accordingly, grain-level splits cannot test generalization across lots, harvests, or acquisition sessions, or rule out acquisition–cultivar confounding.
- Photographs were collected using one smartphone and a fixed LED-light-box setup. No **pixel-to-millimeter physical-scale calibration** or **repeat-imaging quality-control study** was performed. Pixel-based size descriptors may vary with imaging geometry, and measurement repeatability was not established.
- The same 4,000 physical grains appear in the three repeated seed evaluations. Repeated folds and seeds do not create independent biological samples.

## Closed-set classification is not varietal purity certification

The four cultivars have markedly different seed-coat colors, but color was not an input feature. The workflow tests morphometric discrimination among these predefined cultivars; it does not establish a benefit over direct color-based visual identification in routine practice.

The classifier assigns each grain to one of four learned classes. It has **no validated open-set or out-of-distribution detection mechanism** and cannot reliably flag grains from unmodeled cultivars, off-type admixtures, or damaged seeds. Confidence-based abstention selects cases for review but **is not equivalent to off-type detection**. The reported results should **not** be represented as validated operational seed certification or varietal purity testing.

## Small feature sets and computational comparisons

The simple baselines refer to **input features**, not independent physical measurements. For example, the pair **Area and AspectRatio** consists of two input features, but AspectRatio is derived from the major and minor axis lengths. Removing computed descriptors from a single contour reduces input redundancy, not necessarily image-acquisition effort.

Reported TabPFN inference was measured on an **NVIDIA L4 GPU**, while LDA-based inference was measured on a **CPU**. These non-equivalent hardware timings show approximate orders of magnitude only and **cannot establish an overall cost advantage**. A deployment comparison would additionally require matched hardware, throughput, equipment expense, energy use, maintenance, and applicable licensing costs.

## Evidence required before operational use

External validation should include independent certified seed lots, harvests and production sites; acquisition on new dates and devices; documented orientation and physical-scale calibration; repeated imaging to quantify measurement repeatability; and a prespecified open-set evaluation with off-type admixtures and additional cultivars. Probabilistic calibration and selective-rejection thresholds must be re-evaluated for the deployment distribution.

## Reproducibility

The public repository includes code, processed numerical summaries, figures, and supplemental CSV tables, but does **not** redistribute the original morphometric observations, private credentials, or licensed TabPFN weights. See [DATA_AVAILABILITY.md](DATA_AVAILABILITY.md), [REPRODUCIBILITY.md](REPRODUCIBILITY.md), [VALIDATION_PROTOCOL.md](VALIDATION_PROTOCOL.md), and [the supplemental table index](../tables/supplementary/README.md).
