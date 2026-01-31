# fkh-7 Analysis

This repository contains the analysis, visualization, and image-processing code
used in:

**<The forkhead transcription factor FKH-7/FOXP acts in C. elegans chemosensory neurons to shape a life history strategy>**  
Chai et al., <2026>

---

## Overview

This repository accompanies the above manuscript and includes:

- **Python analysis and plotting code** used to process quantitative data and
  generate preliminary figures
- **A Fiji/ImageJ Jython script** used for automated image processing and
  fluorescence quantification

The code is provided to support transparency, reproducibility, and reuse of the
analysis pipeline described in the manuscript.

## Fiji / ImageJ Jython script

The Jython script performs automated image processing steps including:

- Channel selection and separation
- Z-projection
- ROI-based fluorescence quantification
- Batch processing of image stacks

The script is intended to be run interactively within Fiji and assumes image
inputs are selected manually by the user.

## AI-assisted code development statement

Portions of the code in this repository were developed with the assistance of
large language models.

- The Python-based analysis and plotting scripts were developed with the aid of
  ChatGPT (OpenAI), which was used to assist with code structure, debugging, and
  refactoring. All scripts were reviewed, tested, and modified by the authors.

- The Fiji/ImageJ Jython script was developed with assistance from both ChatGPT
  (OpenAI) and Gemini (Google), which were used to suggest code patterns and
  implementation strategies. The final script was written, validated, and
  executed by the authors.

No AI system was used to generate or interpret biological data, select regions
of interest, or draw scientific conclusions.

