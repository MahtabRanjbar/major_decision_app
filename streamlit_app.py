import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(page_title="برنامه انتخاب رشته دکتر حسین جای", layout="wide")

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv('output_1.csv')
    return df

df = load_data()

# Custom CSS for better UI
st.markdown("""
<style>
            
    .stApp {
        background-color: #17a2b8;
        direction: RTL;
        unicode-bidi: bidi-override;
        text-align: right;
    }
    .stSelectbox, .stTextInput, .stSlider, .stNumberInput {
        background-color: transparent;
        direction: RTL;
        unicode-bidi: bidi-override;
        text-align: right;
    }
    .stDataFrame {
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("برنامه انتخاب رشته دکتر حسین جایروند")

# Sidebar for filters
st.sidebar.header("Filters")

# University filter
universities = ['همه'] + sorted(df['دانشگاه'].unique().tolist())
selected_university = st.sidebar.selectbox("انتخاب دانشگاه", universities)

# Major filter
majors = ['همه'] + sorted(df['رشته'].unique().tolist())
selected_major = st.sidebar.selectbox("انتخاب رشته تحصیلی", majors)

# Quota filter
quotas = ['همه'] + sorted(df['سهمیه'].unique().tolist())
selected_quota = st.sidebar.selectbox("انتخاب سهمیه", quotas)

# Rank filter
rank_filter_type = st.sidebar.radio("نوع فیلتر رتبه", ["Range", "Exact"])

if rank_filter_type == "Range":
    min_rank = int(df['رتبه در سهمیه'].min())
    max_rank = int(df['رتبه در سهمیه'].max())
    rank_range = st.sidebar.slider("محدوده رتبه", min_rank, max_rank, (min_rank, max_rank))
else:
    # Use the minimum rank from the dataset as the min_value
    exact_rank = st.sidebar.number_input(
        "رتبه دقیق",
        min_value=int(df['رتبه در سهمیه'].min()), 
        max_value=int(df['رتبه در سهمیه'].max()), 
        value=int(df['رتبه در سهمیه'].min())  # Set default to min rank
    )

# Apply filters
filtered_df = df.copy()

if selected_university != 'همه':
    filtered_df = filtered_df[filtered_df['دانشگاه'].str.contains(selected_university)]

if selected_major != 'همه':
    filtered_df = filtered_df[filtered_df['رشته'] == selected_major]

if selected_quota != 'همه':
    filtered_df = filtered_df[filtered_df['سهمیه'] == selected_quota]

if rank_filter_type == "Range":
    filtered_df = filtered_df[(filtered_df['رتبه در سهمیه'] >= rank_range[0]) & 
                              (filtered_df['رتبه در سهمیه'] <= rank_range[1])]
else:
    # Only filter if an exact rank is provided
    filtered_df = filtered_df[filtered_df['رتبه در سهمیه'] == exact_rank]

# Display results
st.header("نتایج فیلتر شده")
st.dataframe(filtered_df, use_container_width=True)
