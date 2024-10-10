import streamlit as st
import pandas as pd
import ast

page_title= "One Stop Shop for Small Business Compliance Act 2023"

st.set_page_config(
    page_title=page_title,
    page_icon="https://www.sba.gov/brand/assets/sba/img/pages/logo/logo.svg",
    layout="wide",
    initial_sidebar_state="expanded")

hide_streamlit_style = """
             <style>
             footer {visibility: hidden;}
             </style>
             """

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

#df= pd.read_csv(r'C:\Users\cpsolerkanchumarthy\U.S. Small Business Administration\Analysis and Evaluation Division (AED) - Documents\2. Analytics\Ombudsman\Code\ombudsman_streamlit_demo\src\ombudsman_demo_dataset.csv').rename(columns={'title':'Title', 'html_url':'Link to Rule and Regulation','effective_date':'Effective Date'})
df= pd.read_csv('src/ombudsman_demo_dataset.csv').rename(columns={'title':'Title', 'html_url':'Link to Rule and Regulation','effective_date':'Effective Date'})


#Converting NAICS and topics to list in oprder to explode
df['topics']= df['topics'].apply(lambda x: ast.literal_eval(x) if isinstance(x,str)else x)
df['NAICS']= df['NAICS'].apply(lambda x: ast.literal_eval(x) if isinstance(x,str)else x)

# Unpack the topics and naics lists
df_exploded = df.explode('topics').explode('NAICS')

# Filter columns for display
columns_to_display = ['Title', 'Link to Rule and Regulation', 'Effective Date'] 

filtered_df = df_exploded[columns_to_display]


# Remove NaN/None from the filter options but not from the dataset 
agency_options = sorted(df_exploded['Agency'].dropna().unique())
topics_options = sorted(df_exploded['topics'].dropna().unique())
naics_options = sorted(df_exploded['NAICS'].dropna().unique())
department_options = sorted(df_exploded['Department'].dropna().unique())
state_options = sorted(df_exploded['state_final'].dropna().unique())


# Sidebar filters sorted alphabetically without NaN/None 
selected_topics = st.sidebar.multiselect('Filter by Topics', options=topics_options) 
selected_naics = st.sidebar.multiselect('Filter by NAICS', options=naics_options) 
selected_department = st.sidebar.multiselect('Filter by Department', options=department_options) 
selected_agency = st.sidebar.multiselect('Filter by Agency', options=agency_options) 
selected_state = st.sidebar.multiselect('Filter by State', options=state_options)


# Filter the dataframe based on the sidebar selections 
if selected_topics:
    filtered_df = filtered_df[df_exploded['topics'].isin(selected_topics)]
if selected_naics:
    filtered_df = filtered_df[df_exploded['NAICS'].isin(selected_naics)]
if selected_department:
    filtered_df = filtered_df[df_exploded['Department'].isin(selected_department)]
if selected_agency:
    filtered_df = filtered_df[df_exploded['Agency'].isin(selected_agency)]
if selected_state:
    filtered_df = filtered_df[df_exploded['state_final'].isin(selected_state)]

# Display the filtered dataframe
if __name__ == "__main__":
    st.header(page_title)
    #t.write(filtered_df.reset_index(drop=True))
    st.dataframe(df_exploded[['Title', 'Link to Rule and Regulation', 'Effective Date']].drop_duplicates(subset=['Title', 'Link to Rule and Regulation', 'Effective Date']).reset_index(drop=True))

