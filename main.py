from dotenv import load_dotenv
import sqlalchemy as sql
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from report_builder import ReportFormatBuilder
from query import MobilisationQueries
import pandas as pd
import streamlit as st
import os

report_map =   {

        'Select Phase': {},    
        'Mobilsation Phase': {
                'Select Activity': [],
                'PC Activity' : ['Select Report', 'PC Selection Summary Report','Village Selection Summary Report'],
                'Pragati Sabha Activity': ['Select Report', 'Report 1', 'Report 2'],
                'Prerak Activity': ['Select Report', 'Report 1', 'Report 2']
                },

        'Neev Phase': {
                'Select Activity': [],
                'Neev Activity 1': ['Select Report', 'Report 1', 'Report 2'], 
                'Neev Activity 2': ['Select Report', 'Report 1', 'Report 2']
                },

        'Prayaas Phase' : {
                'Select Activity': [],
                'Prayaas Activity 1': ['Select Report', 'Report 1', 'Report 2'], 
                'Prayaas Activity 2': ['Select Report', 'Report 1', 'Report 2']}
        }



# logging in impact database
load_dotenv('db_cred.env')
username = os.getenv("DB_USERNAME")
raw_password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")
password = quote_plus(raw_password.strip())
connection_string = f"postgresql://{username}:{password}@{host}:{port}/{database}"
engine = create_engine(connection_string, pool_pre_ping=True)


# st.set_page_config(layout = "wide")
st.header(":red[Cohort-26 Report Generator]", divider="gray")

    

# phase selection
selected_phase = st.selectbox("Select Phase of Pragati", list(report_map.keys()))

# activity selection
if selected_phase:
    selected_activity = st.selectbox("Select Activity", list(report_map[selected_phase].keys()))

    # report selection
    if selected_activity:
        report_options = report_map[selected_phase][selected_activity]
        selected_report = st.selectbox("Select Report", report_options)

        if selected_report:
            if st.button("Generate Report/Sheet"):
                with engine.connect() as connection:
                    sql_query = MobilisationQueries(selected_report).give_query()
                    if len(sql_query) > 0:
                        try:
                            result = connection.execute(sql.text(sql_query))
                            data = pd.DataFrame(result.fetchall(), columns=result.keys())             
                            if not data.empty:                
                                html = ReportFormatBuilder(selected_report, data).build()
                                st.markdown(html, unsafe_allow_html=True)
                            else:
                                st.warning("Oops !! Data didn't Fetched")
                        except Exception as e:
                            st.error(f"We Facing Some Issue --> '{e}'")
                    
                    
                        









