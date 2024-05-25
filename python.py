import pandas as pd
import streamlit as st
# pip install openpyxl
import openpyxl

# Set the title of the main page
st.title("Movie Project")

# Add items to the sidebar
with st.sidebar:
    st.header("Getting started")
    st.write("Demo: Survey")
    st.write("Demo: User management")
   
# Load data
file_path = 'Moive_Boxoffice.xlsx'
data = pd.read_excel(file_path)

