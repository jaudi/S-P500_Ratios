import streamlit as st
import pandas as pd

# --- Load the data ---
@st.cache_data
def load_data():
    df = pd.read_csv('S&P500.csv')
    df['PER'] = pd.to_numeric(df['PER'], errors='coerce')  # Make sure PER is numeric
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header('Filter Options')

# Filter by sector
sectors = df['Sector'].dropna().unique()
selected_sector = st.sidebar.multiselect('Select Sector(s):', sectors, default=sectors)

# Filter by recommendation (REC)
recs = df['REC'].dropna().unique()
selected_recs = st.sidebar.multiselect('Select Recommendation(s):', recs, default=recs)

# Safe min and max values for PER
per_min_value = df['PER'].min()
per_max_value = df['PER'].max()

if pd.isna(per_min_value) or pd.isna(per_max_value):
    per_min_value, per_max_value = 0.0, 200.0  # Default values if data is missing

# PER Range (slider)
per_min, per_max = st.sidebar.slider(
    'Select PER range (from data)', 
    min_value=float(per_min_value), 
    max_value=float(per_max_value), 
    value=(float(per_min_value), float(per_max_value))
)

# Manual PER filter (optional)
st.sidebar.subheader('Manual PER Filter (0-200)')
manual_per_min = st.sidebar.number_input('Manual PER Minimum:', min_value=0.0, max_value=200.0, value=0.0)
manual_per_max = st.sidebar.number_input('Manual PER Maximum:', min_value=0.0, max_value=200.0, value=200.0)

# --- Apply Filters ---
filtered_df = df[
    (df['Sector'].isin(selected_sector)) &
    (df['REC'].isin(selected_recs)) &
    (df['PER'] >= per_min) & (df['PER'] <= per_max) &
    (df['PER'] >= manual_per_min) & (df['PER'] <= manual_per_max)
]

# --- Main Page ---

# Title
st.title('S&P500 Company Explorer')

# Display filtered data
st.subheader('Filtered Companies')
st.dataframe(filtered_df)

# Search for a specific company symbol
st.subheader('Search by Symbol')
symbol_search = st.text_input('Enter Symbol (e.g., AAPL):').upper()

if symbol_search:
    result = df[df['

