import pandas as pd
from pandasql import sqldf
import billionaire.queries as queries
import billionaire.problems as problems
import streamlit as st

df = pd.read_csv("billionaire/billionaire.csv")
st.set_page_config(layout="wide")

# Initialize session state properly
if "place" not in st.session_state:
    st.session_state["place"] = queries.DROPDOWN_QUERY[0]

def update_selection():
    """Update session state when selectbox value changes."""
    st.session_state["place"] = st.session_state["query_select"]

def get_place():

    st.title(":orange[SQL PROJECTS COMPILATION]")
    
    st.write("")
    st.selectbox(
        ":orange[Select a query from the dropdown list]", 
        options=queries.DROPDOWN_QUERY,  # Add some options
        index=queries.DROPDOWN_QUERY.index(st.session_state["place"]),
        key="query_select",
        on_change=update_selection # This will trigger get_place() when the selection changes
    )
    

    selected_query = st.session_state["place"]+ "_QUERY"
    selected_problem = st.session_state["place"]+ "_PROBLEM"
    try:
        query = getattr(queries, selected_query)
        sql_problem = getattr(problems, selected_problem)
    except AttributeError:
        st.error(f"Query {selected_query} does not exist in queries.")
    
    result = sqldf(query)

    st.write("")
    st.write("")
    st.subheader("SQL PROBLEM", divider="green")
    st.code(sql_problem, language="sql")

    st.subheader("SQL CODE", divider="orange")
    st.code(query, language="sql", line_numbers=True, wrap_lines=True)

    st.subheader("RESULT", divider="rainbow")
    st.table(result)
    return


get_place()



