# Data Utilities

Scripts for working with structured data formats such as CSV and Excel.

These utilities are designed to be simple, reusable, and easy to run from the command line.

## Scripts

### csv_to_excel.py
Converts a CSV file into an Excel (.xlsx) file.
Note:
Although some scraping scripts already produce well-structured CSV files,
the `clean_csv.py` utility is designed as a universal post-processing tool.

It is useful when:
- working with multiple data sources
- handling messy or user-generated content
- removing duplicates after merging datasets
- normalizing text before analysis or storage

In simple scraping cases (like books.toscrape.com), cleaning may not be required,
but the tool becomes essential in real-world data pipelines.


**Features**
- Reads CSV files using the standard library
- Creates Excel files using `openpyxl`
- Automatically names the output file if not provided

**Usage**
```bash
python data_utils/csv_to_excel.py input.csv
