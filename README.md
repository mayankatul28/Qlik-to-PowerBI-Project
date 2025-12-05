# DAX Converter

A simple web tool that converts Qlik Set Analysis expressions to Power BI DAX formulas.

## Overview

DAX Converter helps data analysts migrate from Qlik to Power BI by automatically translating formula syntax. Upload your data model schema, then convert formulas one at a time or in batch mode. No more manual rewriting.

## Features

- Schema validation with detailed error messages
- Single formula conversion with instant preview
- Batch processing for multiple formulas at once
- Real-time conversion feedback
- CSV export of converted formulas
- Support for filters and aggregations

## Tech Stack

- **Frontend/UI**: Streamlit
- **Data Processing**: Pandas
- **Language**: Python 3.13

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/dax-converter.git
cd "DAX Converter"
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install streamlit pandas openpyxl
```

### 4. Run the application
```bash
streamlit run src/app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

### Step 1: Validate Schema
Upload a CSV file with your data model (columns: table, field, type). The tool validates the schema and shows all available tables.

### Step 2: Single Conversion
Enter a Qlik formula like `Sum({<Year={2023}>} Amount)` and get the DAX equivalent instantly.

### Step 3: Batch Convert
Upload a CSV with multiple formulas (columns: measure_name, qlik_formula). Convert all at once and download results.

## Folder Structure

```
DAX Converter/
├── src/
│   ├── validator.py      # Schema validation logic
│   ├── converter.py      # Qlik to DAX conversion engine
│   └── app.py           # Streamlit UI
├── data/
│   ├── sample_schema.csv
│   └── test_batch.csv
└── README.md
```

## Supported Functions

| Qlik Function | DAX Equivalent |
|--------------|----------------|
| Sum()        | SUM()         |
| Avg()        | AVERAGE()     |
| Count()      | COUNT()       |
| Min()        | MIN()         |
| Max()        | MAX()         |

Supports single and multiple filters with Set Analysis syntax.

## Example

**Input (Qlik):**
```
Sum({<Year={2023}, Region={'North','South'}>} Sales)
```

**Output (DAX):**
```
CALCULATE(SUM(Sales[Sales]), Sales[Year] = 2023, Sales[Region] IN {"North", "South"})
```

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature-name`)
3. Make your changes
4. Commit (`git commit -m "Add feature"`)
5. Push to branch (`git push origin feature-name`)
6. Open a pull request

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Acknowledgments

Built with Streamlit for rapid prototyping and Pandas for robust CSV handling. Inspired by the need to simplify BI tool migrations.
