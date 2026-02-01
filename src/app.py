"""
Streamlit App - Qlik to Power BI Accelerator
Includes: DAX Converter, Backend Converter, and Visualization Converter
"""
import env_loader  # Load environment variables from .env file
import streamlit as st
import pandas as pd
import os
from pathlib import Path
from validator import SchemaValidator
from converter import QlikToDAXConverter

# Initialize session state
if 'validator' not in st.session_state:
    st.session_state.validator = SchemaValidator()
    st.session_state.schema_loaded = False

st.set_page_config(page_title="Qlik to Power BI Accelerator", page_icon="📊", layout="wide")

st.title("🚀 Qlik to Power BI Accelerator")
st.write("Convert Qlik assets to Power BI: Measures (DAX), Scripts (PySpark), and Dashboards (PBIX)")

tab1, tab2, tab3, tab4 = st.tabs(["📋 Validate Schema", "🔄 Single Convert", "📦 Batch Convert", "🎨 Visualize Dashboard"])

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

# Tab 4: Visualization Converter
with tab4:
    st.header("Step 3: Convert Dashboard to Power BI")
    st.write("Upload a Qlik dashboard screenshot and generate a Power BI (.pbix) file")
    
    # Info box
    st.info("""
    **How it works:**
    1. Upload a screenshot of your Qlik dashboard
    2. AI analyzes the layout and visual elements
    3. Generate a Power BI file with similar visuals
    4. Download and open in Power BI Desktop
    
    **Note:** Generated visuals use sample data. You'll need to connect to your actual data source in Power BI.
    """)
    
    # Hugging Face Vision - 100% FREE, unlimited requests
    st.success("✅ Using Hugging Face Vision (100% FREE, unlimited requests)")
    
    # Dashboard name input
    dashboard_name = st.text_input("Dashboard Name", value="My Dashboard", key="dashboard_name")
    
    # Image upload
    uploaded_image = st.file_uploader(
        "Upload Dashboard Screenshot",
        type=['png', 'jpg', 'jpeg'],
        key='dashboard_image',
        help="Upload a clear screenshot of your Qlik dashboard"
    )
    
    if uploaded_image:
        # Display uploaded image
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📸 Uploaded Dashboard")
            st.image(uploaded_image, use_container_width=True)
        
        # Save uploaded file temporarily
        temp_image_path = Path("temp_dashboard_upload.png")
        with open(temp_image_path, "wb") as f:
            f.write(uploaded_image.getvalue())
        
        # Analyze button
        if st.button("🔍 Analyze Dashboard", type="primary"):
            with st.spinner("Analyzing dashboard... This may take 10-20 seconds"):
                try:
                    from huggingface_vision_analyzer import HuggingFaceVisionAnalyzer
                    
                    # Analyze image using Hugging Face (FREE, no API key needed)
                    analyzer = HuggingFaceVisionAnalyzer()
                    analysis_results = analyzer.analyze_dashboard(str(temp_image_path))
                    
                    # Store in session state
                    st.session_state.analysis_results = analysis_results
                    st.session_state.dashboard_analyzed = True
                    
                    st.success("✅ Analysis complete!")
                    
                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")
                    st.session_state.dashboard_analyzed = False
        
        # Show analysis results if available
        if st.session_state.get('dashboard_analyzed', False):
            with col2:
                st.subheader("📊 Analysis Results")
                
                analysis = st.session_state.analysis_results
                
                # Summary
                from huggingface_vision_analyzer import HuggingFaceVisionAnalyzer
                analyzer = HuggingFaceVisionAnalyzer()
                if analyzer:
                    summary = analyzer.get_layout_summary(analysis)
                    
                    st.metric("Total Pages", summary['total_pages'])
                    st.metric("Total Visuals", summary['total_visuals'])
                    st.metric("Total Slicers", summary['total_slicers'])
                    
                    # Visual types detected
                    visual_types = analyzer.detect_visual_types(analysis)
                    st.write("**Visual Types Detected:**")
                    st.write(", ".join(visual_types))
            
            # Detailed view (expandable)
            with st.expander("🔍 View Detailed Analysis"):
                st.json(analysis)
            
            # Publish to Power BI button
            st.divider()
            st.subheader("📤 Export Dashboard")
            
            st.write("Choose how to export your analyzed dashboard:")
            
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            
            with col_btn1:
                if st.button("⚡ Publish to Power BI Service", type="primary", use_container_width=True):
                    with st.spinner("Publishing to Power BI Service..."):
                        try:
                            from powerbi_publisher import PowerBIPublisher
                            
                            # Publish to Power BI
                            publisher = PowerBIPublisher()
                            result = publisher.publish_dashboard(
                                visual_metadata=analysis,
                                dashboard_name=dashboard_name
                            )
                            
                            st.session_state.pbi_published = True
                            st.session_state.pbi_result = result
                            
                            st.success(f"✅ Published to Power BI: {result['report_name']}")
                            
                        except ValueError as e:
                            st.error(f"❌ Setup required: {str(e)}")
                            st.info("📖 Requires Power BI Pro/Premium account")
                        except Exception as e:
                            st.error(f"Publishing failed: {str(e)}")
                            import traceback
                            st.code(traceback.format_exc())
            
            with col_btn2:
                # Download as JSON
                import json
                analysis_json = json.dumps(analysis, indent=2)
                st.download_button(
                    label="📥 Download JSON",
                    data=analysis_json,
                    file_name=f"{dashboard_name.replace(' ', '_')}_analysis.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            with col_btn3:
                # Generate PBIP file
                if st.button("📦 Generate PBIP File", use_container_width=True):
                    with st.spinner("Generating Power BI file..."):
                        try:
                            from simple_pbip_generator import SimplePBIPGenerator
                            
                            # Save analysis to temp JSON
                            temp_json = Path("temp_analysis.json")
                            with open(temp_json, 'w') as f:
                                json.dump(analysis, f, indent=2)
                            
                            # Generate PBIP
                            generator = SimplePBIPGenerator()
                            zip_path = generator.create_pbip_from_json(str(temp_json))
                            
                            st.session_state.pbip_generated = True
                            st.session_state.pbip_path = zip_path
                            
                            # Cleanup temp file
                            temp_json.unlink()
                            
                            st.success("✅ PBIP file generated!")
                            
                        except Exception as e:
                            st.error(f"Generation failed: {str(e)}")
                            import traceback
                            st.code(traceback.format_exc())
            
            st.info("""
            **Options:**
            - **Publish to Power BI**: Requires Power BI Pro/Premium account
            - **Download JSON**: Get raw analysis data
            - **Generate PBIP**: Create Power BI file to open in Power BI Desktop (FREE)
            """)
            
            # Show published report details
            if st.session_state.get('pbi_published', False):
                result = st.session_state.pbi_result
                
                st.success("🎉 Dashboard published successfully!")
                
                # Display report details
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Report Name", result['report_name'])
                    st.metric("Workspace", result['workspace_name'])
                
                with col2:
                    st.markdown(f"**Report URL:**")
                    st.markdown(f"[Open in Power BI]({result['report_url']})")
                
                st.info("""
                **Next Steps:**
                1. Click the link above to open your report in Power BI
                2. Connect to your actual data sources
                3. Customize visuals as needed
                4. Share with your team!
                """)
            
            # Show PBIP download button
            if st.session_state.get('pbip_generated', False):
                pbip_zip = Path(st.session_state.pbip_path)
                
                if pbip_zip.exists():
                    with open(pbip_zip, 'rb') as f:
                        pbip_data = f.read()
                    
                    st.download_button(
                        label="📥 Download PBIP File (ZIP)",
                        data=pbip_data,
                        file_name=pbip_zip.name,
                        mime="application/zip",
                        type="primary"
                    )
                    
                    st.info("""
                    **How to use:**
                    1. Download the ZIP file above
                    2. Extract the ZIP file
                    3. Open the .pbip file in Power BI Desktop (FREE)
                    4. Your dashboard structure will load!
                    """)
        
        # Cleanup temp file
        if temp_image_path.exists():
            try:
                temp_image_path.unlink()
            except:
                pass
