# Run Qlik to Power BI Accelerator
# This script sets up the environment and launches the Streamlit app

Write-Host "=" * 60
Write-Host "Qlik to Power BI Accelerator - Launcher"
Write-Host "=" * 60

# Deactivate venv if active (packages are at user level)
if ($env:VIRTUAL_ENV) {
    Write-Host "`n[INFO] Deactivating virtual environment..."
    deactivate
}

# Set Google Gemini API Key (FREE - 1,500 requests/day)
$env:GOOGLE_API_KEY = "AIzaSyAdG7onU0EhA3rqSEGdg7X7nLWhszAZaxg"

Write-Host "`n[OK] Google Gemini API key configured (FREE tier)"
Write-Host "[OK] Starting Streamlit application..."
Write-Host "`nThe app will open in your browser at: http://localhost:8501"
Write-Host "`nPress Ctrl+C to stop the application"
Write-Host "=" * 60
Write-Host ""

# Use system Python (packages installed at user level)
& python -m streamlit run src/app.py
