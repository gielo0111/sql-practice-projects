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

# Custom CSS for Styling
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

        body {
            background-color: #0d1b2a;
            color: white;
            font-family: 'Poppins', sans-serif;
        }

        /* Container styling */
        .sql-container {
            background: rgba(20, 30, 48, 0.85);
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.5);
            margin-bottom: 20px;
            transition: all 0.3s ease-in-out;
            backdrop-filter: blur(8px);
        }

        /* Hover effect */
        .sql-container:hover {
            box-shadow: 0px 6px 16px rgba(255, 102, 0, 0.4);
            transform: translateY(-3px);
        }

        /* Dropdown label */
        .stSelectbox label {
            color: #FF6600 !important;
            font-size: 18px;
            font-weight: bold;
        }

        /* Code block styling */
        .stCodeBlock {
            border-radius: 8px;
            background-color: #112240 !important;
            font-size: 14px;
            padding: 10px;
        }

        /* Table styling */
        .stDataFrame {
            border-radius: 8px;
            overflow: hidden;
        }

        /* Title Styling */
        .stTitle {
            color: #FF6600;
            font-weight: bold;
            text-align: center;
            font-size: 32px;
        }

        /* Subtitle Styling */
        .stSubheader {
            color: #F4A261 !important;
            font-size: 22px;
        }

        /* Centering the dropdown */
        div[data-testid="stSelectbox"] {
            display: flex;
            justify-content: center;
            text-align: center;
        }

        /* Smooth animations */
        .fade-in {
            animation: fadeIn 0.5s ease-in-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
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

# Page Title
st.markdown('<h1 class="stTitle">🚀 SQL Projects Compilation</h1>', unsafe_allow_html=True)

# Centered Dropdown
st.markdown("### 🔍 Select a SQL Query")
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
st.markdown('<div class="sql-container fade-in">', unsafe_allow_html=True)
st.subheader("📝 SQL Problem")
st.code(sql_problem, language="sql")
st.markdown('</div>', unsafe_allow_html=True)

# Display SQL Code
st.markdown('<div class="sql-container fade-in">', unsafe_allow_html=True)
st.subheader("💻 SQL Code")
st.code(query, language="sql", line_numbers=True, wrap_lines=True)
st.markdown('</div>', unsafe_allow_html=True)

# Display Query Results
st.markdown('<div class="sql-container fade-in">', unsafe_allow_html=True)
st.subheader("📊 Query Results")
st.dataframe(result, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
