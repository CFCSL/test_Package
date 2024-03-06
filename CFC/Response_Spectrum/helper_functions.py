#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 12:58:48 2023

@author: namnguyen
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import os,re
import base64
from io import BytesIO

def logo():
	logo_css = """
	<style>
		[data-testid="stSidebarNav"] {
			background-image: url(https://raw.githubusercontent.com/CFCSL/Images-in-Public/main/figures/CFC_LOGO_20220510_Negro_jpeg.jpg);
			background-repeat: no-repeat;
			padding-top: 100px;
			background-position: 20px 20px;
			background-size: 300px;
		}
		[data-testid="stSidebarNav"]::before {
			content: "Carlos Fernandez Casado, S.L.";
			margin-left: 40px;
			margin-top: 20px;
			font-size: 20px;
			position: relative;
			top: 50px;
		}
	</style>
	"""
	
	st.markdown(logo_css, unsafe_allow_html=True)
	
def header():
	t1, t2,t3 = st.columns((0.7,1, 1))


	logo_path = "https://raw.githubusercontent.com/CFCSL/Images-in-Public/main/figures/CFC_LOGO_20220510_Negro_jpeg.jpg"
	# Display the image from the URL with a specified width
	
	t2.image(logo_path, width=350)
	
 # Use HTML to center-align the text vertically and add the link
	centered_text_html = """
	<div style="display: flex; align-items: center; height: 100%;">
		<div style="flex:0.8;"></div>  <!-- Create space on the left -->
		<div style="flex: 4; text-align: center;">
			<a href="https://www.cfcsl.com/" target="_blank">https://www.cfcsl.com/</a>
		</div>  <!-- Centered text -->
		<div style="flex: 1;"></div>  <!-- Create space on the right -->
	</div>
	"""
	st.markdown(centered_text_html, unsafe_allow_html=True)

#%% Download CSV

def download_csv(df,file_name):

    data_csv = df.to_csv(index=False, float_format='%.4f')
    
    # Encode and create the download link
    b64 = base64.b64encode(data_csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{file_name}.csv">Download CSV</a>'
    st.markdown(href, unsafe_allow_html=True)



def download_sofistik(list_df, file_name):
    text = '\n'.join([
        "+PROG SOFILOAD",
        "HEAD 'Definition of response spectrum'",
        "UNIT 5 $ units: sections in mm, geometry+loads in m"
    ])
    local_text = ""
    for i, df in enumerate(list_df, 1):
        # Round the DataFrame columns to four decimal places
        df_rounded = df.round(4)
        
        # Create a string representation of the rounded DataFrame with columns separated by three spaces
        data_csv = df_rounded.to_string(index=False, header=False, col_space=3)
        
        local_text += '\n'.join([
            "lc no " + "10" + str(i) + " type none titl 'Sa(T)-SOIL " + str(df.columns[1]) +"'",
            "resp type user mod 5[%] ag 9.81",
            "ACCE DIR AX 1",
            "FUNC   T   F",
            data_csv,
            '\n\n'
        ])
    
    # Concatenate the existing text and the DataFrame
    combined_text = text + '\n' + local_text + '\n' + "END"
    
    # Create a BytesIO object and write the combined text to it
    text_bytes = combined_text.encode('utf-8')
    buffer = BytesIO()
    buffer.write(text_bytes)
    buffer.seek(0)
    
     # Create the download link
    b64 = base64.b64encode(buffer.read()).decode()
    href = f'<a href="data:text/plain;base64,{b64}" download="{file_name}_RS_SOFISTIK.dat">Download Sofistik dat</a>'
    st.markdown(href, unsafe_allow_html=True)



def download_abaqus(list_df, file_name):

    text = ""
    for i, df in enumerate(list_df, 1):
        # Round the DataFrame columns to four decimal places
        df_rounded = df.round(4)
        
        # Create a string representation of the rounded DataFrame with columns separated by commas
        data_csv = df_rounded.to_csv(index=False, header=False, sep=',')
		
         # Add multiple spaces between columns in the data_csv string
        data_csv = data_csv.replace(',', ',  ')
		
        pattern = r'[A-Z]'
        result = re.findall(pattern, df.columns[1])
        text += '\n'.join([
            "*Spectrum, " + " name=" +str(file_name)+"_"+str(result[1]) +", type=ACCELERATION",
            data_csv,
            "**---------------------------------------------------",
            '\n\n'
        ])

    # Create a BytesIO object and write the combined text to it
    text_bytes = text.encode('utf-8')
    buffer = BytesIO()
    buffer.write(text_bytes)
    buffer.seek(0)
    
     # Create the download link
    b64 = base64.b64encode(buffer.read()).decode()
    href = f'<a href="data:text/plain;base64,{b64}" download="{file_name}_RS_ABAQUS.inp">Download Abaqus inp</a>'
    st.markdown(href, unsafe_allow_html=True)





