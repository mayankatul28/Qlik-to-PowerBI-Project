"""
Simple PBIP Generator - Creates Power BI Project files from JSON analysis
"""

import json
import zipfile
from pathlib import Path
from typing import Dict


class SimplePBIPGenerator:
    """Generates PBIP (Power BI Project) files from dashboard analysis JSON"""
    
    def create_pbip_from_json(self, json_path: str, output_dir: str = "output") -> str:
        """
        Create PBIP folder from JSON analysis file
        
        Args:
            json_path: Path to the JSON analysis file
            output_dir: Directory to create PBIP folder
            
        Returns:
            Path to created PBIP folder (as ZIP)
        """
        # Load JSON
        with open(json_path, 'r') as f:
            analysis = json.load(f)
        
        # Get dashboard name from JSON or use default
        dashboard_name = "Dashboard"
        if analysis.get('pages') and len(analysis['pages']) > 0:
            dashboard_name = analysis['pages'][0].get('name', 'Dashboard')
        
        # Clean name for file system
        clean_name = dashboard_name.replace(' ', '_').replace('/', '_')
        
        # Create PBIP folder structure
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        pbip_folder = output_path / clean_name
        pbip_folder.mkdir(exist_ok=True)
        
        # Create .pbip file (main project file)
        self._create_pbip_file(pbip_folder, clean_name, analysis)
        
        # Create Report folder
        report_folder = pbip_folder / f"{clean_name}.Report"
        report_folder.mkdir(exist_ok=True)
        self._create_report_definition(report_folder, analysis)
        
        # Zip the folder for download
        zip_path = output_path / f"{clean_name}.zip"
        self._zip_folder(pbip_folder, zip_path)
        
        print(f"✅ Created PBIP: {zip_path}")
        return str(zip_path)
    
    def _create_pbip_file(self, folder: Path, name: str, analysis: Dict):
        """Create main .pbip project file with minimal valid schema"""
        # Minimal valid PBIP structure - just the report
        pbip_content = {
            "version": "1.0",
            "artifacts": [
                {
                    "report": {
                        "path": f"{name}.Report"
                    }
                }
            ]
        }
        
        pbip_file = folder / f"{name}.pbip"
        with open(pbip_file, 'w') as f:
            json.dump(pbip_content, f, indent=2)
    
    def _create_report_definition(self, folder: Path, analysis: Dict):
        """Create report definition file"""
        # Simple report definition
        report_def = {
            "version": "5.0",
            "dataModelRefs": [
                {
                    "name": "SampleModel"
                }
            ],
            "pages": []
        }
        
        # Add pages from analysis
        for page in analysis.get('pages', []):
            page_def = {
                "name": page.get('name', 'Page 1'),
                "displayName": page.get('name', 'Page 1'),
                "width": 1280,
                "height": 720,
                "visualContainers": []
            }
            report_def['pages'].append(page_def)
        
        # Write definition.pbir
        pbir_file = folder / "definition.pbir"
        with open(pbir_file, 'w') as f:
            json.dump(report_def, f, indent=2)
    
    def _create_semantic_model(self, folder: Path):
        """Create semantic model definition"""
        # Simple TMDL model
        tmdl_content = """model Model
  culture: en-US

  table SampleData
    lineageTag: sample-data

    column Category
      dataType: string
      lineageTag: category

    column Value
      dataType: int64
      lineageTag: value

    column Date
      dataType: dateTime
      lineageTag: date
"""
        
        # Write definition.tmdl
        tmdl_file = folder / "definition.tmdl"
        with open(tmdl_file, 'w') as f:
            f.write(tmdl_content)
    
    def _zip_folder(self, folder: Path, zip_path: Path):
        """Zip the PBIP folder for download"""
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in folder.rglob('*'):
                if file.is_file():
                    arcname = file.relative_to(folder.parent)
                    zipf.write(file, arcname)


# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python simple_pbip_generator.py <json_file>")
        print("Example: python simple_pbip_generator.py My_Dashboard_analysis.json")
        sys.exit(1)
    
    json_file = sys.argv[1]
    
    if not Path(json_file).exists():
        print(f"❌ File not found: {json_file}")
        sys.exit(1)
    
    generator = SimplePBIPGenerator()
    output = generator.create_pbip_from_json(json_file)
    
    print(f"\n✅ PBIP file created: {output}")
    print("\nNext steps:")
    print("1. Extract the ZIP file")
    print("2. Open the .pbip file in Power BI Desktop")
    print("3. The dashboard structure will be loaded!")
