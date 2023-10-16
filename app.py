import streamlit as st
import pandas as pd
import numpy as np
import csv

st.header('Create DPS Batch File')

st.markdown('#### Instructions:')
st.markdown('''
1. Upload an Excel file. Make sure it has the following columns in the same order:

          
| PID | FirstName | MiddleName | LastName | BirthDate | Gender | Race |
|-----|-----------|------------|----------|-----------|--------|------|
''')

st.markdown('#')
st.markdown('#')
st.markdown('#')

uploaded_file = st.file_uploader("Upload your Excel file")
if uploaded_file is not None:
     df = pd.read_excel(uploaded_file)
     df = df.sort_values(by=df.columns[3])

     batch = pd.DataFrame()

     df.iloc[:, 3] = df.iloc[:, 3].replace(' ', '')  # last name: remove spaces
     df.iloc[:, 3] = df.iloc[:, 3].replace('\'', '')  # last name: remove apostrophe
     df.iloc[:, 3] = df.iloc[:, 3].replace('\'', '')  # last name: remove apostrophe

     df.iloc[:, 1] = df.iloc[:, 1].replace('\'', '')  # first name: remove apostrophe
     df.iloc[:, 1] = df.iloc[:, 1].replace(' ', '')  # first name: remove spaces
     df.iloc[:, 1] = df.iloc[:, 1].replace('-', '')  # first name: remove dashes

     batch['Name'] = np.where(df['MiddleName'].isnull(), df['LastName'] + ',' + df['FirstName'],
                              df['LastName'] + ',' + df['FirstName'] + ' ' + (df['MiddleName'].str[0]))

     batch['Gender'] = np.where(df['Gender'] == 'Male', 'M', 'F')
     batch['Race'] = np.where(df['Race'] == 'White', 'W', np.where(df['Race'] == 'Hispanic', 'W', np.where(df['Race'] == 'Black', 'B', 'U')))

     for i in df.iloc[:, 4].items():
               batch['BirthDate'] = pd.to_datetime(df.iloc[:, 4], format='%Y-%m-%d').dt.strftime('%Y%m%d')

     batch_all = pd.DataFrame()
     batch_all['1'] = batch["Name"].str.pad(30, side='right', fillchar=' ') + batch['Gender'] + batch['Race'] + batch['BirthDate']

     def convert_df(df):
         return df.to_csv(sep=' ', index=False, header=None).encode('utf-8')

     csv = convert_df(batch_all)

     batch_all.to_csv('batch_file.txt', index=False, header=None)

     with open('batch_file.txt','r') as f, open('output.txt','w') as fo:
         for line in f:
             fo.write(line.replace('"', '').replace("'", ""))

     st.markdown('#')     
     st.markdown('#### Batch file is ready to download')
     st.download_button(
         label="Download Batch File",
         data=open('output.txt', 'rb'),
         file_name='batch_file.txt',
         mime='text/csv',
     )







