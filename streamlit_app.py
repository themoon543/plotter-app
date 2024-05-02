
import json
import requests
import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
from streamlit_option_menu import option_menu
import time
import seaborn as sns
#from PIL import Image
from streamlit_extras.app_logo import add_logo
from streamlit_lottie import st_lottie
from io import BytesIO

# Loading Image using PIL
#im = Image.open('app_icon.png')
im = "https://phd.pp.ua/wp-content/uploads/2019/07/x3-730x410.png"

st.set_page_config(page_title="Plotter",page_icon = im,layout="wide")


def get_eligible_columns(df, plot_type):
    eligible_columns_x = []
    eligible_columns_y = []

    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
    time_series_columns = df.select_dtypes(include=['datetime64[ns]']).columns.tolist()

    if plot_type in ['Bar Chart', 'Line Chart']:
        eligible_columns_x = categorical_columns + time_series_columns
        eligible_columns_y = numeric_columns
    elif plot_type == 'Pie Chart':
        eligible_columns_x = categorical_columns
        eligible_columns_y = []  # Pie charts do not use a Y-axis
    elif plot_type == 'Histogram':
        eligible_columns_x = numeric_columns
        eligible_columns_y = []  # Histograms do not use a Y-axis
    return eligible_columns_x, eligible_columns_y

def create_bar_chart(df, x_column, y_column, y_agg_func, aggregate_y):
    fig, ax = plt.subplots()
    if aggregate_y and y_agg_func:
        grouped_df = df.groupby(x_column)[y_column].agg(y_agg_func)
    else:
        grouped_df = df.groupby(x_column)[y_column].sum()  # Default to sum if no specific aggregation function is chosen
    grouped_df.plot(kind='bar', ax=ax)
    ax.set_xlabel(x_column)
    ylabel = f"{y_agg_func.capitalize()} of {y_column}" if aggregate_y else f"Sum of {y_column}"
    ax.set_ylabel(ylabel)
    title = f'Bar Chart: {ylabel} by {x_column}'
    ax.set_title(title)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

def create_line_chart(df, x_column, y_column, y_agg_func, aggregate_y):
    fig, ax = plt.subplots()
    if aggregate_y and y_agg_func:
        grouped_df = df.groupby(x_column)[y_column].agg(y_agg_func)
    else:
        grouped_df = df.groupby(x_column)[y_column].mean()  # Default to mean if no specific aggregation function is chosen
    ax.plot(grouped_df.index, grouped_df.values)
    ax.set_xlabel(x_column)
    ylabel = f"{y_agg_func.capitalize()} of {y_column}" if aggregate_y else f"Average of {y_column}"
    ax.set_ylabel(ylabel)
    title = f'Line Chart: {ylabel} by {x_column}'
    ax.set_title(title)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

def create_pie_chart(df, x_column):
    fig, ax = plt.subplots()
    df[x_column].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
    ax.set_title(f'Pie Chart: Distribution of {x_column}')
    st.pyplot(fig)

def create_histogram(df, x_column):
    fig, ax = plt.subplots()
    sns.histplot(df[x_column], kde=True, bins='auto', ax=ax)
    ax.set_xlabel(x_column)
    ax.set_title(f'Histogram: Distribution of {x_column}')
    st.pyplot(fig)


def show_about_us_page():
    st.markdown("""
<div class="centered">
    <h1></i>Who created the Plotter App?</h1>
</div>""", unsafe_allow_html=True)
    st.write("The  Plotter Web Application was created in May 2024")
    st.write("as a Final Project for Human Computer Interaction course")
    st.write(" at KIMEP University instructed by Hamid Reza Shahbazkia, PhD.")
    st.write("Developped by Assem, Aizhan, Khadisha, Alua, Dina.")

def show_help_page():
    st.markdown("""
<div class="centered">
    <h1></i>What type of graphs to use?</h1>
</div>""", unsafe_allow_html=True)

    if 'show_info' not in st.session_state:
        st.session_state.show_info = None


# Define a function to display information based on the chart type
    def show_chart_info(chart_type):
        st.session_state.show_info = chart_type


# Using columns for layout
    col1, col2, col3, col4 = st.columns(4)  # Four columns for four buttons

    with col1:
        if st.button('📉 Line chart'):
            show_chart_info('Line')

    with col2:
        if st.button('📊 Histogram'):
            show_chart_info('Histogram')

    with col3:
        if st.button('🥧 Pie chart'):
            show_chart_info('Pie')

    with col4:
        if st.button('📊 Bar chart'):
            show_chart_info('Bar')


# Display the information based on what's stored in session_state
    if st.session_state.show_info:
        if st.session_state.show_info == 'Line':
            st.subheader('Line Chart')
            st.write("A line chart displays information as a series of data points connected by straight line segments.")
        elif st.session_state.show_info == 'Histogram':
            st.subheader('Histogram')
            st.write("A histogram is a type of bar chart that represents the distribution of data by forming bins along the range of the data and drawing bars to show the number of observations in each bin.")
        elif st.session_state.show_info == 'Pie':
            st.subheader('Pie Chart')
            st.write("A pie chart is a circular statistical graphic, which is divided into slices to illustrate numerical proportion.")
        elif st.session_state.show_info == 'Bar':
            st.subheader('Bar Chart')
            st.write("A bar chart presents categorical data with rectangular bars with heights or lengths proportional to the values they represent.")




def load_lottieurl(url:str):
    r = requests.get(url)
    if r.status_code!=200:
        return None
    return r.json()


def show_home_page():

    # Custom CSS to vertically align the column contents
    st.markdown("""
    <style>
    .stMarkdown, .stButton, .stLottie {
        margin-bottom: 50px;  /* Adjust space between Streamlit components */
    }
    .css-1d391kg {
        padding-top: 50px; /* Add padding to the top of the column if needed */
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
<div class="centered">
    <h1></i>Welcome to Plotter App!</h1>
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Struggle creating plots and charts? 🤔💭")
        st.subheader("We can help you!")
        st.subheader("Upload your data file and with one click 👆 create your chart.")

    with col2:
        lottie_graph = load_lottieurl("https://lottie.host/66722155-7642-4d7d-aa01-4834e7ec7ba8/0uhwqsYGce.json")
        if lottie_graph:
            st_lottie(lottie_graph, height=300, width=800)

# Embed FontAwesome and Custom Styles
    st.markdown("""
<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css');

.centered {
    text-align: center;
    font-family: 'Arial', sans-serif;
}

.icon {
    color: #4CAF50;  /* Example color */
}
</style>
""", unsafe_allow_html=True)

# Title with Icon, Centered
    st.markdown("""
<div class="centered">
    <h1></i>How it Works?</h1>
</div>
""", unsafe_allow_html=True)

# Section Headers with Icons, Centered
    st.markdown("""
<div class="centered">
    <h2><i class="fas fa-edit icon"></i>Enter The Data</h2>
    <p>Go to Projects section and upload your file(s).</p>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="centered">
    <h2><i class="fas fa-paint-brush icon"></i>Customize The Chart</h2>
    <p>Customize the plot and click the button.</p>
</div>
""", unsafe_allow_html=True)

    st.info('If you are still confused go to Help section', icon="ℹ️")


def show_projects_page():

    st.markdown("""
    <style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css');
    .centered {
        text-align: center;
        font-family: 'Arial', sans-serif;
    }
    .icon {
        color: #4CAF50;  /* Example color */
    }
    </style>
    <div class="centered">
        <h1><i class="fas fa-bar-chart-o icon"></i> Let's create a plot!🤓</h1>
        <p><em>Choose file(s) from your computer and select the data to plot. Click the button and enjoy.<em></p>
    </div>
    """, unsafe_allow_html=True)


    col_fileuploadertext, col_datapreviewtext = st.columns([1, 1])
    df = None

    with col_fileuploadertext:
        st.write('### File Uploader')
    with col_datapreviewtext:
        st.write("### Data Preview")



    col_uploader, col_preview = st.columns([1,1])
    with col_uploader:
        uploaded_files = st.file_uploader("Choose an your file (xlsx, xls or csv). You can upload multiple.", accept_multiple_files=True, type=['xlsx', 'xls', 'csv'])

        dfs = {}
        file_names = ['Not selected']
        selected_file = 'Not selected'

        #if uploaded_files:

        if uploaded_files:
            for uploaded_file in uploaded_files:
                file_name = uploaded_file.name
                try:
                    if file_name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    elif file_name.endswith(('.xls', '.xlsx')):
                        df = pd.read_excel(uploaded_file)
                    else:
                        st.error("Unsupported file format")
                        continue
                    dfs[file_name] = df
                    file_names.append(file_name)
                except Exception as e:
                    st.error(f"An error occurred while processing {file_name}: {e}")

        selected_file = st.selectbox('Choose a file to preview and plot.', options=file_names)

    with col_preview:
        if selected_file and selected_file != 'Not selected':
            with st.spinner('Wait a sec...'):
                time.sleep(2)  # Simulate a delay for processing
                # Display the DataFrame of the selected file
                st.dataframe(dfs[selected_file], height=300, width=700)
        else:
            # Placeholder text if no file is selected
            st.write("Preview of selected file will be displayed here. Choose a file👀.")


    if selected_file and selected_file != 'Not selected':
      col_custom, col_showplot = st.columns([1,1])
      with col_custom:
          st.write("### Chart Customization")
          plot_type = st.selectbox("Select Plot Type:", options=['Not selected', 'Bar Chart', 'Line Chart', 'Pie Chart', 'Histogram'])

          eligible_columns_x, eligible_columns_y = get_eligible_columns(df, plot_type)
          eligible_columns_x = ['Not selected'] + eligible_columns_x
          eligible_columns_y = ['Not selected'] + eligible_columns_y if eligible_columns_y else eligible_columns_y

          x_column = st.selectbox("Select column for X-axis:", options=eligible_columns_x)
          y_column = None
          y_agg_func = None
          aggregate_y = False

          if plot_type in ['Bar Chart', 'Line Chart']:
                y_column = st.selectbox("Select column for Y-axis:", options=eligible_columns_y)
                if y_column != 'Not selected':
                    aggregate_y = st.checkbox("Group Y-axis Values?")
                    if aggregate_y:
                        y_agg_func = st.selectbox("Select Aggregation Function:", options=['sum', 'mean', 'median', 'count'])

          button_clicked = st.button("Create Plot")

      with col_showplot:
        st.write("### Your Plot")
        chart_placeholder = st.empty()

        if not button_clicked:
          chart_placeholder.markdown("Your chart will appear here 🙂")
        else:
          with st.spinner('Processing data...'):
            time.sleep(2)
            chart_placeholder.empty()  # Clear previous contents

            if x_column != 'Not selected' and plot_type != 'Not selected':

              if plot_type == 'Bar Chart':
                fig, ax = plt.subplots()
                sns.barplot(data=df, x=x_column, y=y_column, ax=ax)
                st.pyplot(fig)

              elif plot_type == 'Line Chart':
                fig, ax = plt.subplots()
                sns.lineplot(data=df, x=x_column, y=y_column, ax=ax)
                st.pyplot(fig)
              elif plot_type == 'Pie Chart':
                fig, ax = plt.subplots()
                df[x_column].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
                st.pyplot(fig)
              elif plot_type == 'Histogram':
                fig, ax = plt.subplots()
                sns.histplot(data=df[x_column], kde=True, ax=ax)
                st.pyplot(fig)
            else:
              st.error("Please choose columns and a plot type to generate a plot.")


# option menu
selected = option_menu(menu_title=None, options=["Home", "Projects", 'Help', 'About Us'], icons=['house', 'bar-chart', 'info-circle', 'question'], default_index=0, orientation="horizontal")
if selected == "Home":
    show_home_page()
if selected == "Projects":
    show_projects_page()
if selected == "Help":
    show_help_page()
if selected == "About Us":
    show_about_us_page()

# Hide Streamlit Style
#hide_st_style = """
#<style>
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
#</style>
#"""
#st.markdown(hide_st_style, unsafe_allow_html=True)
