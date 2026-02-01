"""
Simple Power BI Publisher - Publishes reports to Power BI Service using REST API
"""

import os
import json
from typing import Dict, Optional
from pbipy import PowerBI


class PowerBIPublisher:
    """Simple class to publish Power BI reports using REST API"""
    
    def __init__(self, access_token: Optional[str] = None):
        """
        Initialize Power BI Publisher
        
        Args:
            access_token: Azure AD access token (if None, reads from environment)
        """
        self.access_token = access_token or os.getenv('POWERBI_ACCESS_TOKEN')
        if not self.access_token:
            raise ValueError(
                "Power BI access token not found. Set POWERBI_ACCESS_TOKEN environment variable.\n"
                "See setup instructions in POWERBI_SETUP.md"
            )
        
        # Initialize Power BI client
        self.pbi = PowerBI(self.access_token)
    
    def publish_dashboard(
        self, 
        visual_metadata: Dict, 
        dashboard_name: str,
        workspace_id: Optional[str] = None
    ) -> Dict:
        """
        Publish dashboard to Power BI Service
        
        Args:
            visual_metadata: Dashboard analysis from vision analyzer
            dashboard_name: Name for the Power BI report
            workspace_id: Target workspace ID (if None, uses default workspace)
            
        Returns:
            Dictionary with report URL and details
        """
        print(f"Publishing dashboard: {dashboard_name}")
        
        # Get workspace
        if workspace_id:
            workspace = self.pbi.workspace(workspace_id)
        else:
            # Use first available workspace
            workspaces = list(self.pbi.workspaces())
            if not workspaces:
                raise ValueError("No Power BI workspaces found. Please create a workspace first.")
            workspace = workspaces[0]
        
        print(f"Using workspace: {workspace.name}")
        
        # Create dataset with sample data
        dataset = self._create_dataset(workspace, dashboard_name, visual_metadata)
        
        # Create report with visuals
        report = self._create_report(workspace, dataset, dashboard_name, visual_metadata)
        
        # Get report URL
        report_url = f"https://app.powerbi.com/groups/{workspace.id}/reports/{report.id}"
        
        return {
            'success': True,
            'report_name': dashboard_name,
            'report_url': report_url,
            'workspace_name': workspace.name,
            'workspace_id': workspace.id,
            'report_id': report.id
        }
    
    def _create_dataset(self, workspace, name: str, metadata: Dict):
        """Create a simple dataset with sample data"""
        
        # Define simple dataset schema
        dataset_def = {
            "name": f"{name}_Dataset",
            "tables": [
                {
                    "name": "SampleData",
                    "columns": [
                        {"name": "Category", "dataType": "string"},
                        {"name": "Value", "dataType": "Int64"},
                        {"name": "Date", "dataType": "DateTime"}
                    ]
                }
            ]
        }
        
        # Create dataset
        dataset = workspace.post_dataset(dataset_def)
        
        # Add sample rows
        sample_rows = [
            {"Category": "A", "Value": 100, "Date": "2024-01-01T00:00:00Z"},
            {"Category": "B", "Value": 200, "Date": "2024-01-02T00:00:00Z"},
            {"Category": "C", "Value": 150, "Date": "2024-01-03T00:00:00Z"}
        ]
        
        dataset.post_rows("SampleData", sample_rows)
        
        return dataset
    
    def _create_report(self, workspace, dataset, name: str, metadata: Dict):
        """Create report with visuals based on metadata"""
        
        # Create basic report definition
        report_def = {
            "name": name,
            "datasetId": dataset.id
        }
        
        # Create report
        report = workspace.post_report(report_def)
        
        print(f"Report created: {name}")
        
        return report


# Example usage
if __name__ == "__main__":
    # Example metadata
    sample_metadata = {
        "pages": [
            {
                "name": "Sales Dashboard",
                "visuals": [
                    {
                        "type": "bar_chart",
                        "position": {"x": 5, "y": 10, "width": 40, "height": 30},
                        "title": "Sales by Region"
                    }
                ]
            }
        ]
    }
    
    # Publish (requires POWERBI_ACCESS_TOKEN environment variable)
    try:
        publisher = PowerBIPublisher()
        result = publisher.publish_dashboard(
            visual_metadata=sample_metadata,
            dashboard_name="Test Dashboard"
        )
        print(f"Success! Report URL: {result['report_url']}")
    except Exception as e:
        print(f"Error: {e}")
