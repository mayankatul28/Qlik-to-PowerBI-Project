"""
Gemini Vision Analyzer - FREE alternative using Google's Gemini API
Offers generous free tier: 60 requests/minute
"""

import os
import json
from typing import Dict, Optional
from pathlib import Path
from PIL import Image
import google.generativeai as genai


class GeminiVisionAnalyzer:
    """Analyzes dashboard images using Google Gemini Vision (FREE)"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini Vision Analyzer
        
        Args:
            api_key: Google API key (if None, reads from environment)
        """
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError(
                "Google API key not found. Set GOOGLE_API_KEY environment variable "
                "or pass api_key parameter. Get free key at: https://makersuite.google.com/app/apikey"
            )
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('models/gemini-2.5-pro')  # Gemini 2.5 Pro - More powerful reasoning
    
    def analyze_dashboard(self, image_path: str) -> Dict:
        """
        Analyze dashboard image using Gemini Vision
        
        Args:
            image_path: Path to dashboard image
            
        Returns:
            Dictionary containing visual metadata
        """
        if not Path(image_path).exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        # Load image
        img = Image.open(image_path)
        
        # Create prompt
        prompt = """Analyze this dashboard image in detail and provide a structured JSON response.

Identify and describe:
1. All visual elements (charts, tables, cards, slicers, filters)
2. For each visual:
   - Type (bar_chart, line_chart, pie_chart, table, card, slicer, etc.)
   - Approximate position (x, y as percentage of image width/height)
   - Approximate size (width, height as percentage)
   - Title or label
   - Data fields visible (axis labels, column names, etc.)
   - Colors used
3. Page information (if multiple pages visible, tab names)
4. Any filters or slicers
5. Overall layout and theme

Return ONLY valid JSON in this exact format:
{
  "pages": [
    {
      "name": "Page 1",
      "visuals": [
        {
          "id": "visual_1",
          "type": "bar_chart",
          "position": {"x": 10, "y": 10, "width": 40, "height": 30},
          "title": "Sales by Region",
          "data_fields": ["Region", "Sales Amount"],
          "colors": ["#0078D4", "#50E6FF"]
        }
      ],
      "slicers": [
        {
          "name": "Year Slicer",
          "position": {"x": 5, "y": 5, "width": 15, "height": 10},
          "field": "Year"
        }
      ],
      "filters": []
    }
  ],
  "theme": "light",
  "total_visuals": 5
}"""
        
        try:
            # Generate response
            response = self.model.generate_content([prompt, img])
            analysis_text = response.text
            
            # Parse JSON
            structured_data = self._structure_analysis(analysis_text)
            
            return structured_data
            
        except Exception as e:
            raise Exception(f"Gemini Vision analysis failed: {str(e)}")
    
    def _structure_analysis(self, analysis_text: str) -> Dict:
        """Parse and structure the analysis results"""
        try:
            # Extract JSON from response
            json_start = analysis_text.find('{')
            json_end = analysis_text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = analysis_text[json_start:json_end]
            data = json.loads(json_str)
            
            # Validate structure
            self._validate_structure(data)
            
            return data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON: {str(e)}\nResponse: {analysis_text}")
    
    def _validate_structure(self, data: Dict) -> None:
        """Validate analysis data structure"""
        if 'pages' not in data:
            raise ValueError("Missing required key: pages")
        
        if not isinstance(data['pages'], list) or len(data['pages']) == 0:
            raise ValueError("Pages must be a non-empty list")
        
        for page in data['pages']:
            if 'visuals' not in page:
                page['visuals'] = []
            if 'slicers' not in page:
                page['slicers'] = []
            if 'filters' not in page:
                page['filters'] = []
    
    def detect_visual_types(self, analysis: Dict) -> list:
        """Extract list of visual types detected"""
        visual_types = set()
        for page in analysis.get('pages', []):
            for visual in page.get('visuals', []):
                visual_types.add(visual.get('type', 'unknown'))
        return sorted(list(visual_types))
    
    def get_layout_summary(self, analysis: Dict) -> Dict:
        """Get summary of layout information"""
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
            'theme': analysis.get('theme', 'unknown')
        }


# Example usage
if __name__ == "__main__":
    analyzer = GeminiVisionAnalyzer()
    
    image_path = "examples/sample_dashboard.png"
    if Path(image_path).exists():
        print("Analyzing with Gemini Vision (FREE)...")
        results = analyzer.analyze_dashboard(image_path)
        print(json.dumps(results, indent=2))
    else:
        print("Image not found. Please provide a dashboard screenshot.")
