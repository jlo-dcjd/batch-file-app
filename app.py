import streamlit as st
import pandas as pd
import numpy as np
import csv

st.header('Create Batch File')

st.markdown('### Instructions:')
st.markdown('''
          1. Upload an excel file. 

          2. Make sure it has the following columns:
          
| PID | FirstName | MiddleName | LastName | BirthDate | Gender | Race |
|-----|-----------|------------|----------|-----------|--------|------|
|     |           |            |          |           |        |      |
''')

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
     df = pd.read_excel(uploaded_file)

     batch = pd.DataFrame()

     df.LastName = df.LastName.replace(' ', '-', regex=True)  # last name: replace spaces with dashes
     df.LastName = df.LastName.replace('\'', '', regex=True)  # last name: remove apostrophe

     df.FirstName = df.FirstName.replace('\'', '', regex=True)  # first name: remove apostrophe
     df.FirstName = df.FirstName.replace(' ', '', regex=True)  # first name: remove spaces
     df.FirstName = df.FirstName.replace('-', '', regex=True)  # first name: remove dashes

     batch['Name'] = np.where(df['MiddleName'].isnull(), df['LastName'] + ',' + df['FirstName'],
                              df['LastName'] + ',' + df['FirstName'] + ' ' + (df['MiddleName'].str[0]))

     batch['Gender'] = np.where(df['Gender'] == 'Male', 'M', 'F')
     batch['Race'] = np.where(df['Race'] == 'White', 'W', np.where(df['Race'] == 'Hispanic', 'W', np.where(df['Race'] == 'Black', 'B', 'U')))

     for i in df['BirthDate'].items():
               batch['BirthDate'] = pd.to_datetime(df['BirthDate'], format='%Y-%m-%d').dt.strftime('%Y%m%d')

     batch_all = pd.DataFrame()
     batch_all['1'] = batch["Name"].str.pad(30, side='right', fillchar=' ') + batch['Gender'] + batch['Race'] + batch['BirthDate']

     def convert_df(df):
         return df.to_csv(sep=' ', index=False, header=None).encode('utf-8')

     csv = convert_df(batch_all)

     batch_all.to_csv('batch_file.txt', index=False, header=None)

     with open('batch_file.txt','r') as f, open('output.txt','w') as fo:
         for line in f:
             fo.write(line.replace('"', '').replace("'", ""))

     f.close()
     fo.close()

     st.download_button(
         label="Download Batch File",
         data=open('output.txt', 'rb'),
         file_name='Batch File.txt',
         mime='text/csv',
     )







