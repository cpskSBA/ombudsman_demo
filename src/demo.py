import streamlit as st
import pandas as pd
import ast

page_title= "One Stop Shop for Small Business Compliance Act 2024"

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

st.header(page_title)

st.caption("""
This page is designed to help small business owners navigate important compliance guidelines issued by federal and state agencies. Here, you can easily access the latest compliance guides tailored to various industries, ensuring that your business remains up-to-date with key regulations.

### How to Use This Page:

- **Search for Compliance Guides**: Filter guides by topics, industries (NAICS codes), agencies, or states to find the information most relevant to your business.
- **Quick Access to Important Information**: For each guide, you’ll find essential details such as the guide’s title, a direct link to the full document, the effective date, and more.
- **Explore Additional Insights**: Each guide includes summaries, applicable industries, compliance deadlines, and relevant contacts to assist you further.
- **Stay Informed**: Use the filters to quickly view guides by focus areas like labor, environmental regulations, taxes, and other business-critical topics.

Whether you’re starting a new business or ensuring ongoing compliance, this app is your resource to stay informed and compliant.
""")


#df= pd.read_csv(r'C:\Users\cpsolerkanchumarthy\U.S. Small Business Administration\Analysis and Evaluation Division (AED) - Documents\2. Analytics\Ombudsman\Code\ombudsman_streamlit_demo\src\ombudsman_demo_dataset.csv').rename(columns={'title':'Title', 'html_url':'Link to Rule and Regulation','effective_date':'Effective Date'})
df= pd.read_csv('src/ombudsman_demo_dataset.csv').rename(columns={'title':'Title', 'html_url':'Rule and Regulation Link','effective_date':'Effective Date'})


#Converting NAICS and topics to list in oprder to explode
df['topics']= df['topics'].apply(lambda x: ast.literal_eval(x) if isinstance(x,str)else x)
df['NAICS']= df['NAICS'].apply(lambda x: ast.literal_eval(x) if isinstance(x,str)else x)

# Unpack the topics and naics lists
df_exploded = df.explode('topics').explode('NAICS')

# Create a new 'Contact' column by appending '@sba.gov' to the department name 
df_exploded['General Point of Contact Information'] = df_exploded['Department'].apply(lambda x: f'{x.lower().replace(" ", ".")}@sba.gov' if pd.notna(x) else '')

# Create a new column with hyperlinks to the rules and regulations 

#df_exploded['Rule and Regulation Link'] = df_exploded['Link to Rule and Regulation'].apply(lambda x: f'<a href="{x}" target="_blank">Rule and Regulation</a>')

# Function to filter based on selections 
def apply_filters(df, selected_topics, selected_naics, selected_department, selected_agency, selected_state):
    filters = {
        'topics': selected_topics,
        'NAICS': selected_naics,
        'Department': selected_department,
        'Agency': selected_agency,
        'state_final': selected_state
    }

    for column, selection in filters.items():
        if selection:
            df = df[df[column].isin(selection)]

    return df

# Sidebar filters with dynamic options based on current selections 

selected_topics = st.sidebar.multiselect('Filter by Topics', options=sorted(df_exploded['topics'].dropna().unique()))
selected_naics = st.sidebar.multiselect('Filter by Industry (NAICS)', options=sorted(df_exploded['NAICS'].dropna().unique()))
selected_department = st.sidebar.multiselect('Filter by Department', options=sorted(df_exploded['Department'].dropna().unique()))
selected_agency = st.sidebar.multiselect('Filter by Agency', options=sorted(df_exploded['Agency'].dropna().unique()))
selected_state = st.sidebar.multiselect('Filter by State (Default All States)', options=sorted(df_exploded['state_final'].dropna().unique()))

# Apply filters based on selections
df_filtered = apply_filters(df_exploded, selected_topics, selected_naics, selected_department, selected_agency, selected_state)

# Check if the filtered dataframe is empty before displaying 
if df_filtered.empty:
    st.warning("No compliance guides match the selected filters. Please adjust the filters.")
else:
    # Display unique dataset based on title, link, and effective_date without index
    st.dataframe(df_filtered[['Department','Title','Rule and Regulation Link','General Point of Contact Information']].drop_duplicates(subset=['Department','Title','Rule and Regulation Link','General Point of Contact Information']).reset_index(drop=True),hide_index= True,column_config={
            "Rule and Regulation Link": st.column_config.LinkColumn(
                "Rule and Regulation Link",
                display_text="Rule and Regulation"
            ),
            "General Point of Contact Information": st.column_config.LinkColumn(
                "General Point of Contact Information",
                display_text="Contact Email"
            ),
        })



# Display the filtered dataframe
#if __name__ == "__main__":
    #st.header(page_title)
    #t.write(filtered_df.reset_index(drop=True))
    #st.dataframe(filtered_df[['Title','Link to Rule and Regulation', 'Department']].drop_duplicates(subset=['Department','Title','Link to Rule and Regulation']).reset_index(drop=True))

