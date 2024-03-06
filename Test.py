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

import CFC
#importlib.reload(CFC)
CFC.logo()

CFC.header()



r1=CFC.EC8(T=0.3, ag=2)

print(r1)
st.write(f"The value of $S_e$ is:  {round(r1[0],3)}" )



