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

# Dark mode & UI Styling
st.markdown(
    """
    <style>
        body {
            background-color: #0e1117;
            color: white;
        }
        div[data-testid="stAppViewContainer"] {
            background-color: #0e1117;
            padding: 20px;
        }
        div[data-testid="stSidebar"] {
            background-color: #161a23;
        }
        .stSelectbox label {
            color: #FFA500 !important;
            font-size: 16px;
            font-weight: bold;
        }
        .stCodeBlock {
            border-radius: 8px;
        }
        .sql-container {
            background: #161a23;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3);
        }
        .stDataFrame {
            border-radius: 8px;
        }
    </style>
    <script>
        function closeSidebar() {
            var sidebar = window.parent.document.querySelector('section[data-testid="stSidebar"]');
            if (sidebar) {
                sidebar.style.display = 'none';
            }
        }
    </script>
    """,
    unsafe_allow_html=True
)

# Load data
df = pd.read_csv("billionaire/billionaire.csv")

# Initialize session state
if "place" not in st.session_state:
    st.session_state["place"] = queries.DROPDOWN_QUERY[0]

def update_selection():
    """Update session state when selectbox value changes & close sidebar."""
    st.session_state["place"] = st.session_state["query_select"]
    st.markdown('<script>closeSidebar();</script>', unsafe_allow_html=True)  # Auto-hide sidebar

# Sidebar Navigation
with st.sidebar:
    st.header(":orange[SQL Queries]")
    st.write("Choose a SQL query to execute and analyze its results.")
    
    st.selectbox(
        "Select a query", 
        options=queries.DROPDOWN_QUERY,  
        index=queries.DROPDOWN_QUERY.index(st.session_state["place"]),
        key="query_select",
        on_change=update_selection
    )

def display_sql_project():
    st.title(":orange[SQL Projects Compilation] :bar_chart:")

    selected_query = st.session_state["place"] + "_QUERY"
    selected_problem = st.session_state["place"] + "_PROBLEM"

    try:
        query = getattr(queries, selected_query)
        sql_problem = getattr(problems, selected_problem)
    except AttributeError:
        st.error(f"Query {selected_query} does not exist in queries.")
        return

    result = sqldf(query)

    # Display SQL Problem
    with st.container():
        st.markdown('<div class="sql-container">', unsafe_allow_html=True)
        st.subheader(":green[SQL Problem]")
        st.code(sql_problem, language="sql")
        st.markdown('</div>', unsafe_allow_html=True)

    # Display SQL Code
    with st.container():
        st.markdown('<div class="sql-container">', unsafe_allow_html=True)
        st.subheader(":orange[SQL Code]")
        st.code(query, language="sql", line_numbers=True, wrap_lines=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Display Query Results
    with st.container():
        st.markdown('<div class="sql-container">', unsafe_allow_html=True)
        st.subheader(":blue[Query Results]")
        st.dataframe(result, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

display_sql_project()
