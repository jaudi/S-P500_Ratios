import streamlit as st
import pandas as pd

# Load the data
@st.cache_data

def load_data():
    df = pd.read_csv('S&P500.csv')
    return df

df = load_data()

# Title
st.title('S&P500 Company Explorer')

# Sidebar filters
st.sidebar.header('Filter Options')

# Filter by sector
sectors = df['Sector'].dropna().unique()
selected_sector = st.sidebar.multiselect('Select Sector(s):', sectors, default=sectors)

# Filter by Recommendation (REC)
recs = df['REC'].dropna().unique()
selected_recs = st.sidebar.multiselect('Select Recommendation(s):', recs, default=recs)

# Filter by PER range
df = load_data()
st.sidebar.subheader('Manual PER Filter')

manual_per_min = st.sidebar.number_input('PER Minimum:', min_value=0.0, max_value=200.0, value=0.0)
manual_per_max = st.sidebar.number_input('PER Maximum:', min_value=0.0, max_value=200.0, value=200.0)
# Apply filters
filtered_df = df[
    (df['Sector'].isin(selected_sector)) &
    (df['REC'].isin(selected_recs)) &
    (df['PER'] >= per_min) & (df['PER'] <= per_max)
]

# Display data
st.subheader('Filtered Companies')
st.dataframe(filtered_df)

# Search for a specific company symbol
st.subheader('Search by Symbol')
symbol_search = st.text_input('Enter Symbol (e.g., AAPL):').upper()

if symbol_search:
    result = df[df['Symbol'] == symbol_search]
    if not result.empty:
        st.write(result)
    else:
        st.warning('Symbol not found.')

# Quick Stats
st.subheader('Quick Stats')
st.metric('Total Companies', len(df))
st.metric('Companies After Filter', len(filtered_df))

# Allow download of filtered data
st.subheader('Download Filtered Data')
@st.cache_data

def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

downloadable_csv = convert_df_to_csv(filtered_df)
st.download_button('Download CSV', data=downloadable_csv, file_name='filtered_sp500.csv', mime='text/csv')
