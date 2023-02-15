import os
import pyodbc

import streamlit as st
import pandas as pd
import numpy as np

from streamlit_extras.function_explorer import function_explorer

#Server connection info
server   = 'pumpflow.database.windows.net'
database = 'Performance_Database '
username = 'PumpflowAdmin'
password = '{Pumpflow2022}'   
driver   = '{ODBC Driver 17 for SQL Server}'

st.title('Pumpflow SQL Database Searcher')



def SQLSearch(JobNumber: int = 1669,TestNumber: int = 1):

    ##Makes a connection to the database. Args defined earlier
    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            TempList = cursor.execute("SELECT TOP 100 * FROM MainTable WHERE Job_Number = ? AND Test_Number = ?",JobNumber,TestNumber).fetchall()
            st.table(pd.DataFrame.from_records(TempList,columns=["Time","Job_Number","Test_Number","Take_Point","NGH","Efficiency","Absorbed_Power","Flow_Rate","Suction_Pressure","Discharge_Pressure","V1_DEX","V1_DEY","V1_DEZ","V2_NDEX","V2_NDEY","V2_NDEZ","TT1","Out_Torque","RPM_Used","Current","Voltage","Power","Current_P1","Current_P2","Current_P3","Frequency","LT1","PT_Atm"]))


function_explorer(SQLSearch)