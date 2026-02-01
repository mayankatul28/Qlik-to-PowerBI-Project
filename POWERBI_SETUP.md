# Power BI REST API Setup Guide

## Quick Setup (5 minutes)

### Step 1: Create Azure AD App Registration

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** → **App registrations**
3. Click **New registration**
4. Enter name: `DAX-Converter-PowerBI`
5. Select **Accounts in this organizational directory only**
6. Click **Register**

### Step 2: Configure API Permissions

1. In your app, go to **API permissions**
2. Click **Add a permission**
3. Select **Power BI Service**
4. Choose **Delegated permissions**
5. Select these permissions:
   - `Dataset.ReadWrite.All`
   - `Report.ReadWrite.All`
   - `Workspace.ReadWrite.All`
6. Click **Add permissions**
7. Click **Grant admin consent** (requires admin)

### Step 3: Get Access Token

**Option A: Using Azure CLI (Easiest)**

```bash
# Install Azure CLI if not installed
# https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

# Login
az login

# Get token
az account get-access-token --resource https://analysis.windows.net/powerbi/api
```

Copy the `accessToken` value.

**Option B: Using Python Script**

```python
from msal import PublicClientApplication

app = PublicClientApplication(
    client_id="YOUR_APP_CLIENT_ID",
    authority="https://login.microsoftonline.com/YOUR_TENANT_ID"
)

result = app.acquire_token_interactive(
    scopes=["https://analysis.windows.net/powerbi/api/.default"]
)

print(result["access_token"])
```

### Step 4: Set Environment Variable

**Windows PowerShell:**
```powershell
$env:POWERBI_ACCESS_TOKEN = "YOUR_ACCESS_TOKEN_HERE"
```

**Or add to `.env` file:**
```
POWERBI_ACCESS_TOKEN=YOUR_ACCESS_TOKEN_HERE
```

### Step 5: Run the Application

```powershell
powershell -ExecutionPolicy Bypass -File run_app.ps1
```

## Usage

1. Open the app at http://localhost:8501
2. Go to **Tab 4: Visualize Dashboard**
3. Upload a Qlik dashboard screenshot
4. Click **Analyze Dashboard**
5. Click **Publish to Power BI**
6. Report will be created in your Power BI workspace!

## Troubleshooting

### Error: "Power BI access token not found"
- Make sure you set the `POWERBI_ACCESS_TOKEN` environment variable
- Token expires after 1 hour - get a new one if needed

### Error: "No Power BI workspaces found"
- Create a workspace in Power BI Service first
- Go to https://app.powerbi.com → Workspaces → Create workspace

### Error: "Insufficient permissions"
- Make sure admin consent was granted for API permissions
- Check that your account has Power BI Pro license

## Notes

- Access tokens expire after 1 hour
- For production, use service principal authentication
- Reports are published to your first available workspace
