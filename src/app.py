"""
Streamlit App - DAX Converter UI
"""
import streamlit as st
import pandas as pd
from validator import SchemaValidator
from converter import QlikToDAXConverter

if 'validator' not in st.session_state:
    st.session_state.validator = SchemaValidator()
    st.session_state.schema_loaded = False

st.title("DAX Converter")
st.write("Convert Qlik Set Analysis to Power BI DAX")

tab1, tab2, tab3 = st.tabs(["Validate", "Single Convert", "Batch Convert"])

with tab1:
    st.header("Step 1: Validate Data Model")
    st.write("Upload a CSV file with your table and field definitions")
    
    uploaded_file = st.file_uploader("Upload Schema CSV", type=['csv'], key='schema')
    
    if uploaded_file:
        try:
            temp_path = "data/temp_schema.csv"
            with open(temp_path, 'wb') as f:
                f.write(uploaded_file.getvalue())
            
            count = st.session_state.validator.load_schema(temp_path)
            st.session_state.schema_loaded = True
            
            st.success(f"Schema loaded! Found {count} fields")
            
            tables = st.session_state.validator.get_all_tables()
            st.write(f"**Tables found:** {', '.join(tables)}")
            
        except Exception as e:
            st.error(f"Error loading schema: {str(e)}")

with tab2:
    st.header("Step 2: Single Convert")
    
    if not st.session_state.schema_loaded:
        st.warning("Please upload schema in the Validate tab first!")
    else:
        st.write("Enter a Qlik formula to convert")
        
        qlik_input = st.text_area("Qlik Formula", height=100, 
                                   placeholder="Example: Sum({<Year={2023}>} Amount)")
        
        if st.button("Convert", type="primary"):
            if qlik_input:
                try:
                    converter = QlikToDAXConverter(st.session_state.validator)
                    dax_output = converter.convert(qlik_input)
                    
                    st.success("Conversion successful!")
                    st.code(dax_output, language="dax")
                    
                except Exception as e:
                    st.error(f"Conversion failed: {str(e)}")
            else:
                st.warning("Please enter a Qlik formula")


with tab3:
    st.header("Step 3: Batch Convert")
    
    if not st.session_state.schema_loaded:
        st.warning("Please upload schema in the Validate tab first!")
    else:
        st.write("Upload a CSV with multiple formulas to convert")
        st.info("CSV must have columns: measure_name, qlik_formula")
        
        batch_file = st.file_uploader("Upload Batch CSV", type=['csv'], key='batch')
        
        if batch_file:
            try:
                df = pd.read_csv(batch_file)
                
                if 'measure_name' not in df.columns or 'qlik_formula' not in df.columns:
                    st.error("CSV must have columns: measure_name, qlik_formula")
                else:
                    st.write(f"Found {len(df)} formulas to convert")
                    st.dataframe(df.head())
                    
                    if st.button("Convert All", type="primary"):
                        converter = QlikToDAXConverter(st.session_state.validator)
                        results = []
                        
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        for idx, row in df.iterrows():
                            status_text.text(f"Converting {idx + 1} of {len(df)}...")
                            
                            try:
                                dax = converter.convert(row['qlik_formula'])
                                results.append({
                                    'measure_name': row['measure_name'],
                                    'qlik_formula': row['qlik_formula'],
                                    'dax_formula': dax,
                                    'status': 'Success',
                                    'error_message': ''
                                })
                            except Exception as e:
                                results.append({
                                    'measure_name': row['measure_name'],
                                    'qlik_formula': row['qlik_formula'],
                                    'dax_formula': '',
                                    'status': 'Failed',
                                    'error_message': str(e)
                                })
                            
                            progress_bar.progress((idx + 1) / len(df))
                        
                        status_text.text("Conversion complete!")
                        
                        results_df = pd.DataFrame(results)
                        st.dataframe(results_df)
                        
                        csv = results_df.to_csv(index=False)
                        st.download_button(
                            label="Download Results",
                            data=csv,
                            file_name="dax_conversions.csv",
                            mime="text/csv"
                        )
                        
            except Exception as e:
                st.error(f"Error: {str(e)}")
