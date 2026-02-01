"""
PBIX Generator - Creates Power BI (.pbix) files from visual metadata
"""

import json
import zipfile
import shutil
from pathlib import Path
from typing import Dict, List
from datetime import datetime
import uuid


class PBIXGenerator:
    """Generates Power BI .pbix files from dashboard metadata"""
    
    def __init__(self, template_dir: str = "src/pbix_templates"):
        """
        Initialize PBIX Generator
        
        Args:
            template_dir: Directory containing PBIX template files
        """
        self.template_dir = Path(template_dir)
        self.temp_dir = Path("temp_pbix_generation")
    
    def create_pbix(self, visual_metadata: Dict, output_path: str, dashboard_name: str = "Dashboard") -> str:
        """
        Create a .pbix file from visual metadata
        
        Args:
            visual_metadata: Structured visual data from analysis
            output_path: Path where .pbix file will be saved
            dashboard_name: Name of the dashboard
            
        Returns:
            Path to generated .pbix file
        """
        print(f"Generating Power BI file: {dashboard_name}")
        
        # Create temp directory
        self.temp_dir.mkdir(exist_ok=True)
        
        try:
            # Step 1: Create base structure
            self._create_base_structure()
            
            # Step 2: Generate report layout
            self._generate_report_layout(visual_metadata, dashboard_name)
            
            # Step 3: Generate data model schema
            self._generate_data_model(visual_metadata)
            
            # Step 4: Package as .pbix
            pbix_path = self._package_pbix(output_path)
            
            print(f"Successfully generated: {pbix_path}")
            return pbix_path
            
        finally:
            # Cleanup temp directory
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
    
    def _create_base_structure(self):
        """Create base PBIX directory structure"""
        # Create required directories
        (self.temp_dir / "Report").mkdir(exist_ok=True)
        (self.temp_dir / "Metadata").mkdir(exist_ok=True)
        
        # Create [Content_Types].xml with UTF-8 encoding
        content_types = '''<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="json" ContentType="application/json" />
  <Override PartName="/Report/Layout" ContentType="application/json" />
  <Override PartName="/DataModelSchema" ContentType="application/xml" />
</Types>'''
        
        (self.temp_dir / "[Content_Types].xml").write_bytes(content_types.encode('utf-8'))
        
        # Create metadata.json
        metadata = {
            "name": "PowerBIReport",
            "id": str(uuid.uuid4()),
            "version": "1.0",
            "createdDateTime": datetime.now().isoformat()
        }
        
        (self.temp_dir / "Metadata" / "metadata.json").write_bytes(
            json.dumps(metadata, indent=2).encode('utf-8')
        )
    
    def _generate_report_layout(self, visual_metadata: Dict, dashboard_name: str):
        """Generate Report/Layout file"""
        from visual_mappers import VisualMapperFactory
        
        sections = []
        
        for page_idx, page_data in enumerate(visual_metadata.get('pages', [])):
            visual_containers = []
            
            # Add regular visuals
            for visual_idx, visual in enumerate(page_data.get('visuals', [])):
                container = self._create_visual_container(
                    visual, 
                    f"visual_{page_idx}_{visual_idx}"
                )
                visual_containers.append(container)
            
            # Add slicers
            for slicer_idx, slicer in enumerate(page_data.get('slicers', [])):
                slicer['type'] = 'slicer'  # Ensure type is set
                container = self._create_visual_container(
                    slicer,
                    f"slicer_{page_idx}_{slicer_idx}"
                )
                visual_containers.append(container)
            
            # Create section
            section = {
                "id": page_idx,
                "displayName": page_data.get('name', f'Page {page_idx + 1}'),
                "filters": "[]",
                "visualContainers": visual_containers,
                "config": "{}"
            }
            
            sections.append(section)
        
        # Create layout structure
        layout = {
            "id": 0,
            "resourcePackages": [
                {
                    "name": "SharedResources",
                    "type": 3,
                    "items": []
                }
            ],
            "config": json.dumps({
                "name": dashboard_name,
                "layouts": [
                    {
                        "id": 0,
                        "displayName": "Default"
                    }
                ]
            }),
            "layoutOptimization": 0,
            "sections": sections
        }
        
        # Write layout file with UTF-8 encoding (Power BI accepts UTF-8)
        layout_path = self.temp_dir / "Report" / "Layout"
        layout_path.write_bytes(
            json.dumps(layout, indent=2).encode('utf-8')
        )
    
    def _create_visual_container(self, visual: Dict, visual_id: str) -> Dict:
        """Create a visual container configuration"""
        from visual_mappers import VisualMapperFactory
        
        # Get position (convert percentages to pixels, assuming 1280x720 canvas)
        position = visual.get('position', {})
        x = position.get('x', 0) * 12.8  # Convert % to pixels
        y = position.get('y', 0) * 7.2
        width = position.get('width', 30) * 12.8
        height = position.get('height', 20) * 7.2
        
        # Map visual to Power BI configuration
        visual_config = VisualMapperFactory.map_visual(visual)
        
        # Create visual configuration JSON
        config = {
            "name": visual_id,
            "layouts": [
                {
                    "id": 0,
                    "position": {
                        "x": x,
                        "y": y,
                        "z": 0,
                        "width": width,
                        "height": height
                    }
                }
            ],
            "singleVisual": {
                "visualType": visual_config.visual_type,
                "projections": visual_config.projections,
                "prototypeQuery": {
                    "Version": 2,
                    "From": [
                        {
                            "Name": "s",
                            "Entity": "SampleData"
                        }
                    ],
                    "Select": []
                },
                "objects": visual_config.objects
            }
        }
        
        # Add title if present
        title = visual.get('title', '')
        if title:
            config['singleVisual']['vcObjects'] = {
                "title": [
                    {
                        "properties": {
                            "text": {
                                "expr": {
                                    "Literal": {
                                        "Value": f"'{title}'"
                                    }
                                }
                            },
                            "show": {
                                "expr": {
                                    "Literal": {
                                        "Value": "true"
                                    }
                                }
                            }
                        }
                    }
                ]
            }
        
        return {
            "x": x,
            "y": y,
            "z": 0,
            "width": width,
            "height": height,
            "config": json.dumps(config),
            "filters": "[]",
            "query": "{}"
        }
    
    def _generate_data_model(self, visual_metadata: Dict):
        """Generate DataModelSchema file"""
        # Create a simple data model with sample table
        data_model = '''<?xml version="1.0" encoding="utf-8"?>
<DataModelSchema xmlns="http://schemas.microsoft.com/analysisservices/2003/engine">
  <Model>
    <Name>Model</Name>
    <Tables>
      <Table>
        <Name>SampleData</Name>
        <Columns>
          <Column>
            <Name>Category</Name>
            <DataType>String</DataType>
          </Column>
          <Column>
            <Name>Value</Name>
            <DataType>Int64</DataType>
          </Column>
          <Column>
            <Name>Date</Name>
            <DataType>DateTime</DataType>
          </Column>
        </Columns>
      </Table>
    </Tables>
  </Model>
</DataModelSchema>'''
        
        (self.temp_dir / "DataModelSchema").write_bytes(data_model.encode('utf-8'))
    
    def _package_pbix(self, output_path: str) -> str:
        """Package directory as .pbix file (ZIP format)"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create ZIP file
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in self.temp_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(self.temp_dir)
                    zipf.write(file_path, arcname)
        
        return str(output_path)


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
                        "title": "Sales by Region",
                        "data_fields": ["Region", "Sales Amount"],
                        "colors": ["#0078D4"]
                    },
                    {
                        "type": "line_chart",
                        "position": {"x": 50, "y": 10, "width": 40, "height": 30},
                        "title": "Sales Trend",
                        "data_fields": ["Date", "Sales Amount"],
                        "colors": ["#50E6FF"]
                    },
                    {
                        "type": "card",
                        "position": {"x": 5, "y": 45, "width": 20, "height": 15},
                        "title": "Total Sales",
                        "data_fields": ["Total Sales"]
                    }
                ],
                "slicers": [
                    {
                        "name": "Year",
                        "position": {"x": 5, "y": 2, "width": 15, "height": 6},
                        "field": "Year"
                    }
                ]
            }
        ],
        "theme": "light"
    }
    
    # Generate PBIX
    generator = PBIXGenerator()
    pbix_path = generator.create_pbix(
        visual_metadata=sample_metadata,
        output_path="output/sample_dashboard.pbix",
        dashboard_name="Sample Sales Dashboard"
    )
    
    print(f"Generated PBIX: {pbix_path}")
