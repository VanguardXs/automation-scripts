# Data Utilities

Scripts for working with structured data formats such as CSV and Excel.

These utilities are designed to be simple, reusable, and easy to run from the command line.

## Scripts

### csv_to_excel.py
Converts a CSV file into an Excel (.xlsx) file.

**Features**
- Reads CSV files using the standard library
- Creates Excel files using `openpyxl`
- Automatically names the output file if not provided

**Usage**
```bash
python data_utils/csv_to_excel.py input.csv
