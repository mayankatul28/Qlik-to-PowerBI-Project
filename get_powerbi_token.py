"""
Get Power BI Access Token - Simple Authentication Script
Run this script to get your Power BI access token
"""

from msal import PublicClientApplication
import sys

# Public client ID for Power BI (Microsoft's official app)
CLIENT_ID = "ea0616ba-638b-4df5-95b9-636659ae5121"  # Power BI public client
AUTHORITY = "https://login.microsoftonline.com/organizations"
SCOPES = ["https://analysis.windows.net/powerbi/api/.default"]

def get_powerbi_token():
    """Get Power BI access token using interactive login"""
    
    print("=" * 60)
    print("Power BI Access Token Generator")
    print("=" * 60)
    print("\nThis will open a browser window for you to sign in.")
    print("Please sign in with your Power BI account.\n")
    
    # Create MSAL app
    app = PublicClientApplication(
        client_id=CLIENT_ID,
        authority=AUTHORITY
    )
    
    # Try to get token interactively
    try:
        result = app.acquire_token_interactive(scopes=SCOPES)
        
        if "access_token" in result:
            token = result["access_token"]
            
            print("\n" + "=" * 60)
            print("✅ SUCCESS! Access token obtained")
            print("=" * 60)
            print("\nYour access token:")
            print("-" * 60)
            print(token)
            print("-" * 60)
            
            print("\n📋 Next steps:")
            print("1. Copy the token above")
            print("2. Run this command in PowerShell:")
            print(f'\n   $env:POWERBI_ACCESS_TOKEN = "{token}"\n')
            print("3. Restart the application")
            print("\n⚠️  Note: Token expires in 1 hour\n")
            
            return token
        else:
            print("\n❌ Authentication failed:")
            print(result.get("error_description", "Unknown error"))
            return None
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return None

if __name__ == "__main__":
    get_powerbi_token()
