# Setup Guide for AI Market Intelligence Dashboard

## Python Installation Required

Your system doesn't have Python installed. Here's how to set it up:

### Option 1: Install Python from Microsoft Store (Recommended)
1. Open Microsoft Store
2. Search for "Python 3.11" or "Python 3.12"
3. Click "Install"
4. This will install Python and add it to your PATH automatically

### Option 2: Install Python from python.org
1. Go to https://www.python.org/downloads/
2. Download Python 3.11 or 3.12 for Windows
3. **IMPORTANT**: During installation, check "Add Python to PATH"
4. Complete the installation

### Option 3: Install via Chocolatey (if you have it)
```powershell
choco install python
```

## After Python Installation

1. **Restart your terminal/PowerShell**
2. **Verify installation**:
   ```bash
   python --version
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Dashboard

Once Python is installed, you can run:

```bash
# Collect all data
python src/fetch_market.py
python src/fetch_hyperscalers.py
python src/fetch_context.py

# Build Excel dashboard
python src/build_workbook.py
```

## Alternative: Use Sample Data

If you want to see the project structure without installing Python, I can create sample CSV files and an Excel workbook for you to explore the data format and dashboard structure.

Would you like me to:
1. Wait for you to install Python, or
2. Create sample data files so you can see the project structure immediately?
