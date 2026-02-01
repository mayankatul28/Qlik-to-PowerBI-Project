"""
Visual Mappers - Map detected visuals to Power BI configurations
"""

from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class VisualConfig:
    """Configuration for a Power BI visual"""
    visual_type: str
    projections: Dict[str, List[str]]
    objects: Dict[str, Any]
    

class BaseVisualMapper:
    """Base class for visual mappers"""
    
    def __init__(self):
        self.visual_type = "unknown"
    
    def map(self, visual_data: Dict) -> VisualConfig:
        """
        Map visual data to Power BI configuration
        
        Args:
            visual_data: Visual metadata from analysis
            
        Returns:
            VisualConfig object
        """
        raise NotImplementedError("Subclasses must implement map()")
    
    def _create_projection(self, field_name: str, query_ref: str = None) -> Dict:
        """Create a projection object"""
        return {
            "queryRef": query_ref or f"Sample.{field_name}"
        }


class BarChartMapper(BaseVisualMapper):
    """Maps bar/column charts"""
    
    def __init__(self):
        super().__init__()
        self.visual_type = "clusteredBarChart"
    
    def map(self, visual_data: Dict) -> VisualConfig:
        data_fields = visual_data.get('data_fields', ['Category', 'Value'])
        colors = visual_data.get('colors', ['#0078D4'])
        
        # Assume first field is category, rest are values
        category_field = data_fields[0] if len(data_fields) > 0 else "Category"
        value_fields = data_fields[1:] if len(data_fields) > 1 else ["Value"]
        
        projections = {
            "Category": [self._create_projection(category_field)],
            "Values": [self._create_projection(vf) for vf in value_fields]
        }
        
        objects = {
            "dataPoint": {
                "defaultColor": {"solid": {"color": colors[0]}}
            },
            "categoryAxis": {
                "show": True,
                "labelDisplayUnits": 0
            },
            "valueAxis": {
                "show": True,
                "labelDisplayUnits": 0
            }
        }
        
        return VisualConfig(
            visual_type=self.visual_type,
            projections=projections,
            objects=objects
        )


class LineChartMapper(BaseVisualMapper):
    """Maps line charts"""
    
    def __init__(self):
        super().__init__()
        self.visual_type = "lineChart"
    
    def map(self, visual_data: Dict) -> VisualConfig:
        data_fields = visual_data.get('data_fields', ['Date', 'Value'])
        colors = visual_data.get('colors', ['#0078D4'])
        
        category_field = data_fields[0] if len(data_fields) > 0 else "Date"
        value_fields = data_fields[1:] if len(data_fields) > 1 else ["Value"]
        
        projections = {
            "Category": [self._create_projection(category_field)],
            "Values": [self._create_projection(vf) for vf in value_fields]
        }
        
        objects = {
            "dataPoint": {
                "defaultColor": {"solid": {"color": colors[0]}}
            },
            "categoryAxis": {
                "show": True
            },
            "valueAxis": {
                "show": True
            },
            "lineStyles": {
                "strokeWidth": 2
            }
        }
        
        return VisualConfig(
            visual_type=self.visual_type,
            projections=projections,
            objects=objects
        )


class PieChartMapper(BaseVisualMapper):
    """Maps pie/donut charts"""
    
    def __init__(self):
        super().__init__()
        self.visual_type = "pieChart"
    
    def map(self, visual_data: Dict) -> VisualConfig:
        data_fields = visual_data.get('data_fields', ['Category', 'Value'])
        
        category_field = data_fields[0] if len(data_fields) > 0 else "Category"
        value_field = data_fields[1] if len(data_fields) > 1 else "Value"
        
        projections = {
            "Category": [self._create_projection(category_field)],
            "Values": [self._create_projection(value_field)]
        }
        
        objects = {
            "legend": {
                "show": True,
                "position": "Right"
            },
            "labels": {
                "show": True,
                "labelStyle": "Data"
            }
        }
        
        return VisualConfig(
            visual_type=self.visual_type,
            projections=projections,
            objects=objects
        )


class TableMapper(BaseVisualMapper):
    """Maps tables and matrices"""
    
    def __init__(self):
        super().__init__()
        self.visual_type = "tableEx"
    
    def map(self, visual_data: Dict) -> VisualConfig:
        data_fields = visual_data.get('data_fields', ['Column1', 'Column2'])
        
        projections = {
            "Values": [self._create_projection(field) for field in data_fields]
        }
        
        objects = {
            "grid": {
                "gridVertical": True,
                "gridHorizontal": True
            },
            "columnHeaders": {
                "fontColor": {"solid": {"color": "#000000"}},
                "fontSize": 11
            }
        }
        
        return VisualConfig(
            visual_type=self.visual_type,
            projections=projections,
            objects=objects
        )


class CardMapper(BaseVisualMapper):
    """Maps KPI cards"""
    
    def __init__(self):
        super().__init__()
        self.visual_type = "card"
    
    def map(self, visual_data: Dict) -> VisualConfig:
        data_fields = visual_data.get('data_fields', ['Value'])
        value_field = data_fields[0] if len(data_fields) > 0 else "Value"
        
        projections = {
            "Values": [self._create_projection(value_field)]
        }
        
        objects = {
            "labels": {
                "fontSize": 24,
                "fontColor": {"solid": {"color": "#000000"}}
            },
            "categoryLabels": {
                "show": True,
                "fontSize": 12
            }
        }
        
        return VisualConfig(
            visual_type=self.visual_type,
            projections=projections,
            objects=objects
        )


class SlicerMapper(BaseVisualMapper):
    """Maps slicers"""
    
    def __init__(self):
        super().__init__()
        self.visual_type = "slicer"
    
    def map(self, visual_data: Dict) -> VisualConfig:
        field = visual_data.get('field', 'Category')
        
        projections = {
            "Values": [self._create_projection(field)]
        }
        
        objects = {
            "general": {
                "orientation": 1  # Vertical
            },
            "selection": {
                "selectAllCheckboxEnabled": True,
                "singleSelect": False
            },
            "header": {
                "show": True,
                "fontColor": {"solid": {"color": "#000000"}}
            }
        }
        
        return VisualConfig(
            visual_type=self.visual_type,
            projections=projections,
            objects=objects
        )


class VisualMapperFactory:
    """Factory to get appropriate mapper for visual type"""
    
    MAPPERS = {
        'bar_chart': BarChartMapper,
        'column_chart': BarChartMapper,
        'clustered_bar': BarChartMapper,
        'line_chart': LineChartMapper,
        'line': LineChartMapper,
        'pie_chart': PieChartMapper,
        'pie': PieChartMapper,
        'donut': PieChartMapper,
        'table': TableMapper,
        'matrix': TableMapper,
        'card': CardMapper,
        'kpi': CardMapper,
        'slicer': SlicerMapper,
        'filter': SlicerMapper
    }
    
    @classmethod
    def get_mapper(cls, visual_type: str) -> BaseVisualMapper:
        """
        Get appropriate mapper for visual type
        
        Args:
            visual_type: Type of visual
            
        Returns:
            Mapper instance
        """
        # Normalize visual type
        normalized_type = visual_type.lower().replace(' ', '_')
        
        mapper_class = cls.MAPPERS.get(normalized_type, BarChartMapper)
        return mapper_class()
    
    @classmethod
    def map_visual(cls, visual_data: Dict) -> VisualConfig:
        """
        Map visual data to Power BI configuration
        
        Args:
            visual_data: Visual metadata
            
        Returns:
            VisualConfig object
        """
        visual_type = visual_data.get('type', 'bar_chart')
        mapper = cls.get_mapper(visual_type)
        return mapper.map(visual_data)


# Example usage
if __name__ == "__main__":
    # Example visual data
    sample_visual = {
        'type': 'bar_chart',
        'title': 'Sales by Region',
        'data_fields': ['Region', 'Sales Amount'],
        'colors': ['#0078D4', '#50E6FF']
    }
    
    # Map to Power BI configuration
    config = VisualMapperFactory.map_visual(sample_visual)
    
    print(f"Visual Type: {config.visual_type}")
    print(f"Projections: {config.projections}")
    print(f"Objects: {config.objects}")
