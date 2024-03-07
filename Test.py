# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 15:31:33 2024

@author: cfcpc2
"""

import sys
import numpy as np

#sys.path.append(r'C:\Users\cfcpc2\Documents\Nam_Local_Works')
#print(sys.path)
import importlib
import streamlit as st
import os
import CFC
#current_path= os.getcwd()

current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)

sys.path.append(current_directory)



#importlib.reload(CFC)
CFC.logo()

CFC.header()

st.write("Hello")

df=CFC.read_excel("Parameters.xlsx")

print(df)







