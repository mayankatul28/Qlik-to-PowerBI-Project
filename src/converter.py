"""
Converter Module - Converts Qlik expressions to DAX
"""
import re

class QlikToDAXConverter:
    def __init__(self, validator):
        self.validator = validator
        
        self.functions = {
            'Sum': 'SUM',
            'Avg': 'AVERAGE',
            'Count': 'COUNT',
            'Min': 'MIN',
            'Max': 'MAX'
        }
    
    def convert(self, qlik_formula):
        """Convert Qlik formula to DAX"""
        qlik_formula = qlik_formula.strip()
        
        if not qlik_formula:
            raise ValueError("Empty formula")
        
        pattern = r'(\w+)\(\s*(?:\{<([^>]+)>\}\s*)?(\w+)\s*\)'
        match = re.match(pattern, qlik_formula)
        
        if not match:
            raise ValueError("Invalid Qlik syntax")
        
        func_name = match.group(1)
        filters_str = match.group(2)
        field_name = match.group(3)
        
        if func_name not in self.functions:
            raise ValueError(f"Unsupported function: {func_name}")
        
        table_name = self.validator.get_table_for_field(field_name)
        if not table_name:
            raise ValueError(f"Field '{field_name}' not found in schema")
        
        dax_func = self.functions[func_name]
        dax_field = f"{table_name}[{field_name}]"
        
        if not filters_str:
            return f"{dax_func}({dax_field})"
        
        filters = self._parse_filters(filters_str)
        dax_filters = []
        
        for filter_field, filter_values in filters.items():
            filter_table = self.validator.get_table_for_field(filter_field)
            if not filter_table:
                raise ValueError(f"Filter field '{filter_field}' not found in schema")
            
            if len(filter_values) == 1:
                value = filter_values[0]
                if value.isdigit():
                    dax_filters.append(f"{filter_table}[{filter_field}] = {value}")
                else:
                    dax_filters.append(f'{filter_table}[{filter_field}] = "{value}"')
            else:
                formatted_values = [f'"{v}"' if not v.isdigit() else v for v in filter_values]
                values_str = ", ".join(formatted_values)
                dax_filters.append(f"{filter_table}[{filter_field}] IN {{{values_str}}}")
        
        all_filters = ", ".join(dax_filters)
        return f"CALCULATE({dax_func}({dax_field}), {all_filters})"
    
    def _parse_filters(self, filters_str):
        """Parse filter string into dictionary"""
        filters = {}
        filter_parts = filters_str.split(',')
        
        for part in filter_parts:
            part = part.strip()
            match = re.match(r'(\w+)=\{([^}]+)\}', part)
            if match:
                field = match.group(1)
                values_str = match.group(2)
                values = [v.strip().strip("'\"") for v in values_str.split(',')]
                filters[field] = values
        
        return filters
