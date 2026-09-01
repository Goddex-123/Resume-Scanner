# Data Directory

This directory contains static data assets and configuration files used by the Resume Scanner.

## Core Assets
- `job_keywords.json`: Keyword mappings for categorizing job titles and roles.
- `skills_database.json`: A curated dictionary of technical and soft skills grouped by category, used by the NLP engine for structured extraction.

## Datasets
The training dataset for the ML layer is not stored here statically. Instead, it is generated programmatically using the `ResumeJDDatasetGenerator` located in `resume_scanner/ml/dataset.py`.

The generator creates synthetic resume-JD pairs across 5 professional domains to ensure a balanced, multi-class baseline for model training without leaking proprietary candidate data.
