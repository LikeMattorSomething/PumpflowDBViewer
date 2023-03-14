import datetime
import os
import pyodbc

import streamlit as st

st. set_page_config(layout="wide")

import pandas as pd

#Server connection info
server   = 'pumpflow.database.windows.net'
database = 'Performance_Database '
username = 'PumpflowAdmin'
password = '{Pumpflow2022}'   
driver   = '{ODBC Driver 17 for SQL Server}'

st.title('Pumpflow SQL Database Searcher')

TableNum = 0

with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:

        def SQLSearch_JobAndTest(TableNum):

            LowerTableLimit = (TableNum*100)
            UpperTableLimit = ((TableNum*100)+100)

            #SelectTable = st.selectbox("Select a table to display",["MainTable","JobInfo","AddTemperatures","AddAuxPressure","AddAuxFlow","Value_Description"])
            JobNumber = st.number_input('Job Number',value=0)
            TestNumber = st.number_input('Test Number',value=0)
            TempList = cursor.execute("SELECT * FROM MainTable WHERE Job_Number = ? AND Test_Number = ?",JobNumber,TestNumber).fetchall()
            st.table(pd.DataFrame.from_records(TempList,columns=["Time","Job_Number","Test_Number","Take_Point","NGH","Efficiency","Absorbed_Power","Flow_Rate","Suction_Pressure","Discharge_Pressure","V1_DEX","V1_DEY","V1_DEZ","V2_NDEX","V2_NDEY","V2_NDEZ","TT1","Out_Torque","RPM_Used","Current","Voltage","Power","Current_P1","Current_P2","Current_P3","Frequency","LT1","PT_Atm"]).iloc[LowerTableLimit:UpperTableLimit])



        def SQLSearch_Date(TableNum):

            LowerTableLimit = (TableNum*100)
            UpperTableLimit = ((TableNum*100)+100)

            #SelectTable = st.selectbox("Select a table to display",["MainTable","AddTemperatures","AddAuxPressure","AddAuxFlow"])
            Date = st.date_input("Choose a date")
            TempList = cursor.execute("SELECT * FROM MainTable WHERE CONVERT(DATETIME, FLOOR(CONVERT(FLOAT, Time))) = ?", Date).fetchall()
            st.table(pd.DataFrame.from_records(TempList,columns=["Time","Job_Number","Test_Number","Take_Point","NGH","Efficiency","Absorbed_Power","Flow_Rate","Suction_Pressure","Discharge_Pressure","V1_DEX","V1_DEY","V1_DEZ","V2_NDEX","V2_NDEY","V2_NDEZ","TT1","Out_Torque","RPM_Used","Current","Voltage","Power","Current_P1","Current_P2","Current_P3","Frequency","LT1","PT_Atm"]).iloc[LowerTableLimit:UpperTableLimit])


        
        SortMethod = st.radio('Sort by', ['Date','Job and Test Number'], horizontal=True)
        TableNum = st.number_input('Table Page',value=0)

        if SortMethod == 'Job and Test Number':
            SQLSearch_JobAndTest(TableNum)
        elif SortMethod == "Date":
            SQLSearch_Date(TableNum)