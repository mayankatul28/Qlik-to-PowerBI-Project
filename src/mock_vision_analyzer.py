"""
Mock Vision Analyzer - For testing without OpenAI API credits
"""

import json
from typing import Dict
from pathlib import Path


class MockVisionAnalyzer:
    """Mock analyzer that returns sample data for testing"""
    
    def __init__(self, api_key=None):
        """Initialize mock analyzer"""
        self.api_key = api_key
    
    def analyze_dashboard(self, image_path: str) -> Dict:
        """
        Return mock analysis data for testing
        
        Args:
            image_path: Path to dashboard image (not actually analyzed)
            
        Returns:
            Mock analysis results
        """
        # Return sample dashboard analysis
        mock_analysis = {
            "pages": [
                {
                    "name": "Sales Dashboard",
                    "visuals": [
                        {
                            "id": "visual_1",
                            "type": "bar_chart",
                            "position": {"x": 5, "y": 10, "width": 40, "height": 30},
                            "title": "Sales by Region",
                            "data_fields": ["Region", "Sales Amount"],
                            "colors": ["#0078D4"]
                        },
                        {
                            "id": "visual_2",
                            "type": "line_chart",
                            "position": {"x": 50, "y": 10, "width": 40, "height": 30},
                            "title": "Sales Trend",
                            "data_fields": ["Date", "Sales Amount"],
                            "colors": ["#50E6FF"]
                        },
                        {
                            "id": "visual_3",
                            "type": "card",
                            "position": {"x": 5, "y": 45, "width": 20, "height": 15},
                            "title": "Total Sales",
                            "data_fields": ["Total Sales"],
                            "colors": ["#107C10"]
                        },
                        {
                            "id": "visual_4",
                            "type": "pie_chart",
                            "position": {"x": 30, "y": 45, "width": 25, "height": 25},
                            "title": "Sales by Category",
                            "data_fields": ["Category", "Sales"],
                            "colors": ["#FFB900", "#E74856", "#0078D4"]
                        },
                        {
                            "id": "visual_5",
                            "type": "table",
                            "position": {"x": 60, "y": 45, "width": 35, "height": 25},
                            "title": "Top Products",
                            "data_fields": ["Product", "Sales", "Quantity"],
                            "colors": []
                        }
                    ],
                    "slicers": [
                        {
                            "name": "Year Slicer",
                            "position": {"x": 5, "y": 2, "width": 15, "height": 6},
                            "field": "Year"
                        },
                        {
                            "name": "Region Filter",
                            "position": {"x": 25, "y": 2, "width": 15, "height": 6},
                            "field": "Region"
                        }
                    ],
                    "filters": []
                }
            ],
            "theme": "light",
            "total_visuals": 5
        }
        
        return mock_analysis
    
    def detect_visual_types(self, analysis: Dict) -> list:
        """Extract visual types from analysis"""
        visual_types = set()
        for page in analysis.get('pages', []):
            for visual in page.get('visuals', []):
                visual_types.add(visual.get('type', 'unknown'))
        return sorted(list(visual_types))
    
    def get_layout_summary(self, analysis: Dict) -> Dict:
        """Get layout summary"""
        total_visuals = 0
        total_slicers = 0
        pages = []
        
        for page in analysis.get('pages', []):
            page_info = {
                'name': page.get('name', 'Unnamed'),
                'visual_count': len(page.get('visuals', [])),
                'slicer_count': len(page.get('slicers', [])),
                'filter_count': len(page.get('filters', []))
            }
            pages.append(page_info)
            total_visuals += page_info['visual_count']
            total_slicers += page_info['slicer_count']
        
        return {
            'total_pages': len(pages),
            'total_visuals': total_visuals,
            'total_slicers': total_slicers,
            'pages': pages,
            'theme': analysis.get('theme', 'light')
        }
