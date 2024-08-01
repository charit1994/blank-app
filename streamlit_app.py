import streamlit as st
import pandas as pd
import altair as alt

# Sample data
data = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D', 'E'],
    'Values': [5, 3, 6, 7, 2]
})

# Sidebar with navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a page:", ["Home", "Reasons For Churn", "FAQ"])

# Title of the dashboard
st.title("My First Dashboard")

if page == "Home":
    st.header("Home Page")
    
    # Create an Altair bar chart
    chart = alt.Chart(data).mark_bar().encode(
        x='Category',
        y='Values',
        tooltip=['Category', 'Values']
    ).properties(
        title='Sample Bar Chart'
    )
    
    st.altair_chart(chart, use_container_width=True)
    
elif page == "Reasons For Churn":
    st.header("Reasons For Churn")
    st.write("This page will display reasons for customer churn.")
    
elif page == "FAQ":
    st.header("FAQ")
    st.write("This page will contain frequently asked questions.")
