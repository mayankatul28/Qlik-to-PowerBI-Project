# Qlik to Power BI Accelerator

A comprehensive tool that converts Qlik assets to Power BI: Measures (DAX), Scripts (PySpark), and Dashboards (PBIP/PBIX).

## 🌟 Features

### 1. **DAX Converter**
- Convert Qlik Set Analysis expressions to Power BI DAX formulas
- Schema validation with detailed error messages
- Single formula conversion with instant preview
- Batch processing for multiple formulas at once
- CSV export of converted formulas

### 2. **Visualization Converter**
- Upload Qlik dashboard screenshots
- AI-powered analysis using **Hugging Face Vision** (100% FREE, unlimited requests)
- Extract visual elements, chart types, and layout information
- Generate Power BI Project (.pbip) files
- Publish directly to Power BI Service (requires Pro/Premium account)

### 3. **Backend Converter**
- Convert Qlik scripts to PySpark (coming soon)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Power BI Desktop (for opening generated .pbip files)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/DAX-Converter.git
cd DAX-Converter
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Mac/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Copy the example file
copy .env.example .env  # Windows
# or
cp .env.example .env  # Mac/Linux

# Edit .env and add your API keys (optional for basic DAX conversion)
```

5. **Run the application**
```bash
python -m streamlit run src/app.py
```

The app will open in your browser at `http://localhost:8501`

## 🔑 API Key Setup (Optional)

### For Visualization Converter

**Option 1: Hugging Face Vision (Recommended - 100% FREE)**
- No API key required!
- Unlimited requests
- Already configured in the app

**Option 2: Google Gemini Vision (FREE - 1,500 requests/day)**
1. Get your free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add to `.env`: `GOOGLE_API_KEY=your_key_here`

**Option 3: OpenAI GPT-4 Vision (Paid)**
1. Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Add to `.env`: `OPENAI_API_KEY=your_key_here`

### For Power BI Publishing (Optional)
Requires Power BI Pro/Premium account. See [POWERBI_SETUP.md](POWERBI_SETUP.md) for details.

## 📖 Usage

### DAX Converter

#### Step 1: Validate Schema
Upload a CSV file with your data model (columns: `table`, `field`, `type`). The tool validates the schema and shows all available tables.

#### Step 2: Single Conversion
Enter a Qlik formula like `Sum({<Year={2023}> Amount)` and get the DAX equivalent instantly.

#### Step 3: Batch Convert
Upload a CSV with multiple formulas (columns: `measure_name`, `qlik_formula`). Convert all at once and download results.

### Visualization Converter

1. **Upload Dashboard Screenshot**: Upload a clear screenshot of your Qlik dashboard
2. **Analyze**: Click "Analyze Dashboard" to extract visual elements using AI
3. **Export Options**:
   - **Generate PBIP File**: Download a Power BI Project file (FREE - opens in Power BI Desktop)
   - **Publish to Power BI**: Publish directly to Power BI Service (requires Pro/Premium)
   - **Download JSON**: Get raw analysis data

## 📁 Project Structure

```
DAX-Converter/
├── src/
│   ├── app.py                      # Main Streamlit application
│   ├── validator.py                # Schema validation logic
│   ├── converter.py                # Qlik to DAX conversion engine
│   ├── huggingface_vision_analyzer.py  # AI vision analysis
│   ├── simple_pbip_generator.py    # Power BI file generator
│   ├── powerbi_publisher.py        # Power BI Service publisher
│   └── env_loader.py               # Environment variable loader
├── data/
│   ├── sample_schema.csv           # Example schema file
│   └── test_batch.csv              # Example batch conversion file
├── examples/                       # Example files and screenshots
├── tests/                          # Unit tests
├── .env.example                    # Environment variables template
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🔄 Supported Conversions

### Qlik Functions → DAX

| Qlik Function | DAX Equivalent |
|--------------|----------------|
| Sum()        | SUM()         |
| Avg()        | AVERAGE()     |
| Count()      | COUNT()       |
| Min()        | MIN()         |
| Max()        | MAX()         |

Supports single and multiple filters with Set Analysis syntax.

### Example Conversion

**Input (Qlik):**
```qlik
Sum({<Year={2023}, Region={'North','South'}> Sales)
```

**Output (DAX):**
```dax
CALCULATE(SUM(Sales[Sales]), Sales[Year] = 2023, Sales[Region] IN {"North", "South"})
```

## 🛠️ Tech Stack

- **Frontend/UI**: Streamlit
- **Data Processing**: Pandas
- **AI Vision**: Hugging Face Transformers (FREE)
- **Power BI Integration**: MSAL, Power BI REST API
- **Backend**: FastAPI, PySpark
- **Language**: Python 3.8+

## 📚 Documentation

- [Installation Guide](INSTALLATION_SUMMARY.md)
- [How to Use](HOW_TO_USE.md)
- [Visualization Quickstart](VISUALIZATION_QUICKSTART.md)
- [Power BI Setup](POWERBI_SETUP.md)
- [API Key Setup](API_KEY_SETUP.md)
- [Project Structure](PROJECT_STRUCTURE.md)

## 🤝 Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature-name`)
3. Make your changes
4. Commit (`git commit -m "Add feature"`)
5. Push to branch (`git push origin feature-name`)
6. Open a pull request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Built with Streamlit for rapid prototyping
- Powered by Hugging Face for free AI vision analysis
- Inspired by the need to simplify BI tool migrations

## 👥 Contributors

- [sabareeshsp7](https://github.com/sabareeshsp7) - Co-creator
- [mayankatul28](https://github.com/mayankatul28) - Co-creator

---
**Made with ❤️ for the BI community**
