# AI DATASET CLEANER

## Project Overview

ai-dataset-cleaner is a Streamlit-based web application designed to streamline the process of cleaning and analyzing datasets. It provides an intuitive interface for users to handle common data quality issues like missing values, duplicates, outliers, and inconsistencies, while offering insights and visualization tools to support data preprocessing tasks.

## Key Features

- Data Exploration: Comprehensive overview of dataset structure, including shape, column statistics, and missing value patterns.
- Automated Cleaning: Tools to detect and correct duplicates, handle missing data through various imputation strategies, and identify/remove outliers.
- Visualization: Interactive charts and graphs to visualize data distributions and cleaning results.
- Session Persistence: Maintains session state between browser refreshes to avoid redundant data uploads.
- Export Capabilities: Export cleaned datasets in multiple formats (CSV, Excel, Parquet).
- Recommendation Engine: Suggests data cleaning strategies based on dataset characteristics and quality metrics.

## Installation

1. Install Python 3.8+
2. Install required packages:
pip install -r requir
4. Run the application:
streamlit run app.py

## Usage

1. Launch the app via browser at http://localhost:8501
2. Upload a dataset (CSV/Excel/Parquet)
3. Navigate through the interface:
  - Home: Quick dataset summary
  - Overview: Detailed statistics and visualization
  - Explorer: Interactive exploration of data elements
  - Cleaning: Apply deduplication, outlier removal, and missing value handling
  - Export: Save cleaned dataset in preferred format
4. Use session persistence to resume work after browser refresh
