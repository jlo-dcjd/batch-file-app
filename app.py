import streamlit as st
import pandas as pd
import numpy as np
import csv
import os
import time

st.header('Create DPS Batch File')

st.markdown('#### Instructions:')
st.markdown('''
1. Upload the Excel subfile. Make sure it has the following columns in the same order:

          
| PID | FirstName | MiddleName | LastName | BirthDate | Gender | Race |
|-----|-----------|------------|----------|-----------|--------|------|
''')

st.markdown('#')
st.markdown('#')
st.markdown('#')

uploaded_file = st.file_uploader("Upload your Excel subfile")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # make name columns all caps
    df.iloc[:, 1] = df.iloc[:, 1].str.upper()
    df.iloc[:, 2] = df.iloc[:, 2].str.upper()
    df.iloc[:, 3] = df.iloc[:, 3].str.upper()

    # sort by last name: important: set ignore_index=True
    df = df.sort_values(by=df.columns[3], ignore_index=True)

    df.iloc[:, 3] = df.iloc[:, 3].str.replace(' ', '')  # last name: remove spaces
    df.iloc[:, 3] = df.iloc[:, 3].str.replace('\'', '')  # last name: remove apostrophe
    df.iloc[:, 3] = df.iloc[:, 3].str.replace('-', '')  # last name: remove dashes
    df.iloc[:, 3] = df.iloc[:, 3].str.replace('.', '')  # last name: remove periods

    df.iloc[:, 1] = df.iloc[:, 1].str.replace(' ', '')  # first name: remove spaces
    df.iloc[:, 1] = df.iloc[:, 1].str.replace('\'', '')  # first name: remove apostrophe
    df.iloc[:, 1] = df.iloc[:, 1].str.replace('-', '')  # first name: remove dashes
    df.iloc[:, 1] = df.iloc[:, 1].str.replace('.', '')  # first name: remove periods

    # make batch file columns
    df['b_name'] = np.where(df.iloc[:, 2].isnull(), df.iloc[:, 3] + ',' + df.iloc[:, 1],
                            df.iloc[:, 3] + ',' + df.iloc[:, 1] + ' ' + (df.iloc[:, 2].str[0]))

    df['b_gender'] = np.where(df.iloc[:, 5] == 'Male', 'M', 'F')
    df['b_race'] = np.where(df.iloc[:, 6] == 'White', 'W',
                            np.where(df.iloc[:, 6] == 'Hispanic', 'W', np.where(df.iloc[:, 6] == 'Black', 'B', 'U')))

    df['b_bday'] = pd.to_datetime(df.iloc[:, 4], format='%Y-%m-%d').dt.strftime('%Y%m%d')

    batch = pd.DataFrame()
    batch['records'] = df["b_name"].str.pad(30, side='right', fillchar=' ') + df['b_gender'] + df['b_race'] + df['b_bday']

    batch.to_csv('output.txt', index=False, header=None)

    with open('output.txt', 'r') as f, open('batch_file.txt', 'w') as fo:
        for line in f:
            fo.write(line.replace('"', '').replace("'", ""))

    time.sleep(1)
    try:
        os.remove('output.txt')
    except:
        pass

    st.markdown('#')
    st.success('#### Batch file Is Ready To Download')
    st.download_button(
        label="Download Batch File",
        data=open('batch_file.txt', 'rb'),
        file_name='batch_file.txt',
        mime='text/csv',
    )
