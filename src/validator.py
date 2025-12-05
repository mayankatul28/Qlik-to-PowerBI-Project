"""
Validator Module - Handles schema validation and field lookup
"""
import pandas as pd

class SchemaValidator:
    def __init__(self):
        self.schema = {}
    
    def clear_schema(self):
        self.schema = {}
    
    def load_schema(self, file_path):
        self.clear_schema()
        df = pd.read_csv(file_path)
        
        required_columns = ['table', 'field', 'type']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"CSV must have columns: table, field, type. Missing: {', '.join(missing_columns)}")
        
        if len(df.columns) > 3:
            extra_cols = [col for col in df.columns if col not in required_columns]
            unnamed_cols = [col for col in extra_cols if str(col).startswith('Unnamed:')]
            
            if unnamed_cols:
                raise ValueError(f"Malformed CSV: found {len(df.columns)} columns, expected 3. This is likely caused by trailing commas at the end of lines. Remove any extra commas.")
            else:
                raise ValueError(f"Malformed CSV: found {len(df.columns)} columns, expected 3. Extra columns: {', '.join(extra_cols)}")
        
        for idx, row in df.iterrows():
            row_num = idx + 2
            
            if pd.isna(row['table']) or str(row['table']).strip() == '':
                raise ValueError(f"Row {row_num}: Missing value in 'table' column")
            
            if pd.isna(row['field']) or str(row['field']).strip() == '':
                raise ValueError(f"Row {row_num}: Missing value in 'field' column")
            
            if pd.isna(row['type']) or str(row['type']).strip() == '':
                raise ValueError(f"Row {row_num}: Missing value in 'type' column")
        
        seen_fields = {}
        
        for idx, row in df.iterrows():
            row_num = idx + 2
            field = str(row['field']).strip()
            table = str(row['table']).strip()
            field_type = str(row['type']).strip()
            
            if field in seen_fields:
                prev_table, prev_row = seen_fields[field]
                if prev_table == table:
                    raise ValueError(f"Duplicate field detected: '{field}' already exists in table '{table}' (first defined in row {prev_row}, duplicate in row {row_num})")
            
            seen_fields[field] = (table, row_num)
            self.schema[field] = {
                'table': table,
                'type': field_type
            }
        
        return len(df)
    
    def get_table_for_field(self, field_name):
        if field_name in self.schema:
            return self.schema[field_name]['table']
        return None
    
    def get_all_tables(self):
        """Get list of all unique tables"""
        tables = set()
        for field_info in self.schema.values():
            tables.add(field_info['table'])
        return sorted(list(tables))
