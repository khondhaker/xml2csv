import streamlit as st
import pandas as pd
import os
import tempfile
import subprocess

# Streamlit App Title
st.title("XML to CSV Converter")
st.caption("For the amazing students of CEES 3883 Transportation Engineering")

# File uploader
uploaded_file = st.file_uploader("Upload an XML file", type=["xml"])

if uploaded_file is not None:
    st.success("File uploaded successfully!")
    
    # Save the uploaded XML file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as temp_xml:
        temp_xml.write(uploaded_file.read())
        temp_xml_path = temp_xml.name
    
    # Define the output CSV file path
    temp_csv_path = temp_xml_path.replace(".xml", ".csv")
    
    # Run the existing xml2csv.py script
    try:
        result = subprocess.run(["python", "xml2csv.py", temp_xml_path, "-o", temp_csv_path], capture_output=True, text=True)
        if result.returncode == 0:
            st.success("Conversion successful!")
        else:
            st.error(f"Error: {result.stderr}")
    except Exception as e:
        st.error(f"Failed to run conversion script: {e}")
    
    # Provide a download button for the converted CSV
    if os.path.exists(temp_csv_path):
        with open(temp_csv_path, "rb") as file:
            st.download_button(label="Download CSV File", data=file, file_name="Converted.csv", mime="text/csv")
    
    # Clean up temporary files
    os.remove(temp_xml_path)
    if os.path.exists(temp_csv_path):
        os.remove(temp_csv_path)
