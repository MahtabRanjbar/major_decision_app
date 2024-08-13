import streamlit as st
import pandas as pd
from PIL import Image
import base64
from st_social_media_links import SocialMediaIcons
import gdown
# Function to convert image to Base64
def get_image_as_base64(image_file):
    with open(image_file, "rb") as file:
        return base64.b64encode(file.read()).decode()

# Set the page configuration
st.set_page_config(page_title="My Streamlit App", layout="wide")

# Path to your local image (update this path)
image_path = "bg4.jpg"  # Replace with your image filename

# Convert image to Base64
image_base64 = get_image_as_base64(image_path)
# Load your image
image = Image.open("bg23.png")  # Replace with your image path



# Add custom CSS for background image
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/jpeg;base64,{image_base64});
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        height: 200vh;

        direction: RTL;
        unicode-bidi: bidi-override;
        text-align: right;
    }}
    .stApp h1 {{
        color: #000000!important;
        padding: 10px 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        font-size: 40px;
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0,5,0,0.1);

    }}
    [data-testid="stDataFrameColumnHeadersRow"] button {{
        display: none;
    }}
    
    /* Ensure horizontal scrolling is available if needed */
    [data-testid="stDataFrame"] {{
        overflow-x: auto !important;
    }}
    
    .sidebar .sidebar-content {{

        align-items: center;
        width: 500px;
    }}
    .sidebar .element-container:first-child {{
        width: 80%;
        margin-top: 20px;
        margin-bottom: 20px;
    }}

    .sidebar img {{
        width: 100%;
        height: 0;
        padding-bottom: 100%; /* This makes it square */
        object-fit: cover;
        border-radius: 50%; /* Optional: rounds the corners */
    }}
        .black-text {{
        color: black !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


@st.cache_data
def load_data():
    # Replace 'your_file_id' with the actual file ID from your Google Drive shareable link
    url = 'https://drive.google.com/uc?id=1ltG10sbaogW6Z5-7CaLPWg0JYF-WaWCJ'
    with st.spinner('Loading data...'):
        gdown.download(url, 'output.csv', quiet=False)
    df = pd.read_csv('output.csv')
    return df

# Create a placeholder for the loading message
placeholder = st.empty()

# Load data
with placeholder.container():
    df = load_data()

# Clear the placeholder after loading
placeholder.empty()

# Custom CSS for better UI
st.markdown("""
<style>
    .stSelectbox, .stTextInput, .stNumberInput {
        background-color: transparent;
        direction: RTL;
        unicode-bidi: bidi-override;
        text-align: right;
    }
    .stDataFrame {
        border: none;
    }
    .body {
            
            }        
</style>
""", unsafe_allow_html=True)

# Title
#st.title("🎓 انتخاب رشته دکتر حسین جایروند")

with st.sidebar:
    # Sidebar for filters
    # Display the image at the top of the sidebar
    st.image(image, use_column_width=True)


    social_media_links = [

        "https://www.instagram.com/",
        "https://www.t.me.com/dr_hoseinjayervand",
    ]

    social_media_icons = SocialMediaIcons(social_media_links)

    social_media_icons.render()

    # Initialize select box states
    universities = ['همه'] + sorted(df['دانشگاه'].unique().tolist())
    majors = ['همه'] + sorted(df['رشته'].unique().tolist())

    # First, let the user choose either university or major
    filter_choice = st.sidebar.radio("انتخاب بر اساس", ["دانشگاه", "رشته تحصیلی"])

    if filter_choice == "دانشگاه":
        selected_university = st.sidebar.selectbox("انتخاب دانشگاه", universities, key='university_select')
        if selected_university != 'همه':
            majors = ['همه'] + sorted(df[df['دانشگاه'] == selected_university]['رشته'].unique().tolist())
        selected_major = st.sidebar.selectbox("انتخاب رشته تحصیلی", majors, key='major_select')
    else:  # filter_choice == "رشته تحصیلی"
        selected_major = st.sidebar.selectbox("انتخاب رشته تحصیلی", majors, key='major_select')
        if selected_major != 'همه':
            universities = ['همه'] + sorted(df[df['رشته'] == selected_major]['دانشگاه'].unique().tolist())
            selected_university = st.sidebar.selectbox("انتخاب دانشگاه (بر اساس رشته انتخاب شده)", universities, key='university_select_2')
        else:
            selected_university = 'همه'

    # Quota filter
    quotas = ['همه'] + sorted(df['سهمیه'].unique().tolist())
    selected_quota = st.sidebar.selectbox("انتخاب سهمیه", quotas)

    # Rank filter
    rank_filter_type = st.sidebar.radio("نوع فیلتر رتبه", ["بازه رتبه", "رتبه دقیق"])

    if rank_filter_type == "بازه رتبه":
        min_rank = int(df['رتبه در سهمیه'].min())
        max_rank = int(df['رتبه در سهمیه'].max())
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            min_rank_input = st.number_input("حداقل رتبه", min_value=min_rank, max_value=max_rank, value=min_rank)
        with col2:
            max_rank_input = st.number_input("حداکثر رتبه", min_value=min_rank, max_value=max_rank, value=max_rank)
    else:
        exact_rank = st.sidebar.number_input(
            "رتبه دقیق",
            min_value=int(df['رتبه در سهمیه'].min()),
            max_value=int(df['رتبه در سهمیه'].max()),
            value=int(df['رتبه در سهمیه'].min())
        )

# Apply filters
filtered_df = df.copy()

if selected_university != 'همه':
    filtered_df = filtered_df[filtered_df['دانشگاه'].str.contains(selected_university)]

if selected_major != 'همه':
    filtered_df = filtered_df[filtered_df['رشته'] == selected_major]

if selected_quota != 'همه':
    filtered_df = filtered_df[filtered_df['سهمیه'] == selected_quota]

if rank_filter_type == "بازه رتبه":
    filtered_df = filtered_df[(filtered_df['رتبه در سهمیه'] >= min_rank_input) &
                              (filtered_df['رتبه در سهمیه'] <= max_rank_input)]
else:
    filtered_df = filtered_df[filtered_df['رتبه در سهمیه'] == exact_rank]

# Display results

original_title = '<p style="font-family:Courier; color:Black; font-size: 30;">🎓انتخاب رشته دکتر حسین جایروند</p>'


st.title("🎓انتخاب رشته دکتر حسین جایروند")
st.write("") # Add 3 more newlines for additional spacing




st.markdown(
    """
    <style>
    .no-copy {
        -webkit-user-select: none; /* Safari */
        -moz-user-select: none; /* Firefox */
        -ms-user-select: none; /* Internet Explorer/Edge */
        user-select: none; /* Non-prefixed version, currently
                            supported by Chrome and Opera */
    }
    </style>
    <script>
    document.addEventListener("DOMContentLoaded", function() {
        const elements = document.querySelectorAll("div[data-testid='stTable']");
        elements.forEach(el => {
            el.classList.add('no-copy');
        });
    });
    </script>
    """,
    unsafe_allow_html=True
)

st.write("")
# Display the dataframe
st.dataframe(filtered_df, use_container_width=True)
# Display the table
