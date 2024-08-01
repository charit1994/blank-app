import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data as vega_data

# Sample data creation
def create_sample_data():
    df = pd.DataFrame({
        'candidate_no': range(1, 101),
        'prediction': [0, 1] * 50,
        'categorical_var_1': ['Category A', 'Category B', 'Category C', 'Category D', 'Category E'] * 20,
        'categorical_var_2': ['Type X', 'Type Y', 'Type Z', 'Type W', 'Type V'] * 20,
        'us_state': ['CA', 'TX', 'NY', 'FL', 'IL'] * 20
    })
    return df

df = create_sample_data()

# Sidebar with navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a page:", ["Home", "Reasons For Churn", "FAQ"])

# Title of the dashboard
st.title("My First Dashboard")

if page == "Home":
    st.header("Home Page")
    
    # Top 5 categories by frequency for categorical_var_1
    top_5_cat_var1 = df[df['prediction'] == 1]['categorical_var_1'].value_counts().nlargest(5).index
    df_top_5_cat_var1 = df[df['categorical_var_1'].isin(top_5_cat_var1)]

    # Top 5 categories by frequency for categorical_var_2
    top_5_cat_var2 = df[df['prediction'] == 1].value_counts().nlargest(5).index
    df_top_5_cat_var2 = df[df['categorical_var_2'].isin(top_5_cat_var2)]

    # Bar chart for categorical_var_1
    chart_var1 = alt.Chart(df_top_5_cat_var1).mark_bar().encode(
        x=alt.X('categorical_var_1:N', title='Categorical Var 1'),
        y=alt.Y('count():Q', title='Count'),
        color=alt.Color('categorical_var_1:N', legend=None),
        tooltip=['categorical_var_1', 'count()']
    ).properties(
        title='Top 5 Categories of Categorical Var 1'
    )

    # Bar chart for categorical_var_2
    chart_var2 = alt.Chart(df_top_5_cat_var2).mark_bar().encode(
        x=alt.X('categorical_var_2:N', title='Categorical Var 2'),
        y=alt.Y('count():Q', title='Count'),
        color=alt.Color('categorical_var_2:N', legend=None),
        tooltip=['categorical_var_2', 'count()']
    ).properties(
        title='Top 5 Categories of Categorical Var 2'
    )

    # Display the bar charts side by side
    st.altair_chart(alt.hconcat(chart_var1, chart_var2), use_container_width=True)

    # US States data for map
    states = alt.topo_feature(vega_data.us_10m.url, 'states')
    state_abbr = pd.read_csv('https://raw.githubusercontent.com/jasonong/List-of-US-States/master/states.csv')

    # Aggregate data by state for predictions
    state_data = df[df['prediction'] == 1].groupby('us_state').size().reset_index(name='count')
    state_data = state_data.merge(state_abbr, left_on='us_state', right_on='Abbreviation')

    # Color coded map for prediction counts
    map_chart = alt.Chart(states).mark_geoshape().encode(
        color=alt.Color('count:Q', scale=alt.Scale(scheme='reds'), legend=alt.Legend(title="Prediction Count")),
        tooltip=['State:N', 'count:Q']
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(state_data, 'ID', ['State', 'count'])
    ).properties(
        width=800,
        height=400,
        title='Prediction Counts by State'
    ).project(
        type='albersUsa'
    )

    # Display the map
    st.altair_chart(map_chart, use_container_width=True)

elif page == "Reasons For Churn":
    st.header("Reasons For Churn")
    st.write("This page will display reasons for customer churn.")
    
elif page == "FAQ":
    st.header("FAQ")
    st.write("This page will contain frequently asked questions.")
