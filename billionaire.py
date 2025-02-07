import pandas as pd
from pandasql import sqldf
import billionaire.queries as queries
import billionaire.problems as problems
import streamlit as st

# Set up the page
st.set_page_config(
    layout="wide",
    page_title="SQL Projects Compilation",
    page_icon=":bar_chart:"
)

# Dark mode & UI Styling with Pink Accents
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

        body {
            background-color: #121212;
            color: #EDEDED;
            font-family: 'Roboto', sans-serif;
        }

        /* App Container Styling */
        div[data-testid="stAppViewContainer"] {
            background-color: #121212;
            padding: 20px;
        }

        /* Dropdown Styling */
        .stSelectbox label {
            color: #FF1493 !important; /* Pink color */
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 15px;
        }

        .stSelectbox {
            background-color: #333;
            padding: 10px;
            border-radius: 10px;
            margin-top: 20px;
        }

        .stSelectbox:hover {
            background-color: #555;
        }

        /* SQL Container Styling */
        .sql-container {
            background: #1C1C1C;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.3);
            margin-top: 20px;
        }

        .sql-container:hover {
            box-shadow: 0px 12px 30px rgba(255, 20, 147, 0.5); /* Lighter pink on hover */
        }

        .stDataFrame {
            border-radius: 10px;
            background-color: #232323;
        }

        /* Title Styling */
        .stTitle {
            color: #FF1493;
            font-weight: 700;
            font-size: 36px;
            text-align: center;
            margin-bottom: 20px;
        }

        /* Subtitle Styling */
        .stSubheader {
            color: #FF1493 !important;
            font-size: 24px;
            padding-bottom: 10px;
        }

    </style>
    """,
    unsafe_allow_html=True
)

# Load data
df = pd.read_csv("billionaire/billionaire.csv")

# Initialize session state
if "place" not in st.session_state:
    st.session_state["place"] = queries.DROPDOWN_QUERY[0]

def update_selection():
    """Update session state when selectbox value changes."""
    st.session_state["place"] = st.session_state["query_select"]

def display_sql_project():
    st.markdown('<h1 class="stTitle">SQL Projects Compilation</h1>', unsafe_allow_html=True)

    # Centered Dropdown
    st.markdown("### 🔍 **Select a SQL Query**")
    selected_query = st.selectbox(
        "Choose a query to execute:",
        options=queries.DROPDOWN_QUERY,
        index=queries.DROPDOWN_QUERY.index(st.session_state["place"]),
        key="query_select",
        on_change=update_selection
    )

    # Retrieve Query & Problem
    selected_query_key = st.session_state["place"] + "_QUERY"
    selected_problem_key = st.session_state["place"] + "_PROBLEM"

    try:
        query = getattr(queries, selected_query_key)
        sql_problem = getattr(problems, selected_problem_key)
    except AttributeError:
        st.error(f"Query {selected_query_key} does not exist in queries.")
        st.stop()

    result = sqldf(query)

    # Display SQL Problem
    st.markdown('<div class="sql-container">', unsafe_allow_html=True)
    st.subheader(":green[SQL Problem]")
    st.code(sql_problem, language="sql")
    st.markdown('</div>', unsafe_allow_html=True)

    # Display SQL Code
    st.markdown('<div class="sql-container">', unsafe_allow_html=True)
    st.subheader(":orange[SQL Code]")
    st.code(query, language="sql", line_numbers=True, wrap_lines=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Display Query Results
    st.markdown('<div class="sql-container">', unsafe_allow_html=True)
    st.subheader(":blue[Query Results]")
    st.dataframe(result, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

display_sql_project()
