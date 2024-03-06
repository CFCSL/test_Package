#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 12 13:53:20 2023

@author: namnguyen
"""
import pandas as pd
import streamlit as st
import Response_Spectrum as RS
import helper_functions as hf
import numpy as np
import matplotlib.pyplot  as plt
import zipfile
from io import BytesIO
import base64
from logo_header import *
logo()
header()

st.header("Eurocode 8")


st.write('**Direction:**')
Dir=st.radio("Select Direction:", ("Horizontal", "Vertical"))


st.write("**Response Spectrum:**")
RS_Type = st.radio("Response Spectrum Type", ["Type 1", "Type 2"], index=0)
RS_Type_value = 1 if RS_Type == "Type 1" else 2


st.write("G**round Type**: ")
options=["A","B","C","D","E"]
default_options = options  # Set all options as default
GroundType=st.multiselect("Select options:", options, default=default_options)

g=9.81 # acceleration

xi=st.number_input("$\\xi$ is the viscous damping ratio of the structure, expressed as a percentage.", value=5.0, min_value=0.0, step=1.0,format="%.1f")

alpha=st.number_input("$a_g/g\quad$ ($a_g$ is the design ground acceleration on type $A$ ground ($a_g = \gamma_I.a_{{gR}}$))", value= 0.2, min_value=0.0, step=0.1, format="%.1f")

ag=alpha*g

st.write("**Period T[s]**")


T_max=st.number_input("Select T_max[s]", value= 5., min_value=1., step=1., format="%.1f")
T = np.linspace(0.01,T_max , 200)

bi=st.radio("Is Base Isolation applied?", options=[False, True], key="radio1")


TD_bi= st.number_input("$T_D$ only if the base isolation is applied", value= 2.0, min_value=1.0, step=0.1,format="%.1f")

#st.write(RS.EC8(T=0.3,ag=1,GroundType='A',xi=100,Dir='Horizontal',RS_Type=1, bi=bi,TD_bi=TD_bi))

# Create the plot
fig, (ax1, ax2) = plt.subplots(2, 1,figsize=(5, 8))


for k in GroundType:
	ax1.plot(T, 1/ag*RS.EC8(T,ag=ag, GroundType=k,xi=xi, Dir=Dir, RS_Type=RS_Type_value, bi=bi,TD_bi=TD_bi), label=k)
	ax2.plot(T,1/g* RS.EC8(T,ag=ag, GroundType=k,xi=xi, Dir=Dir, RS_Type=RS_Type_value, bi=bi,TD_bi=TD_bi), label=k)

ax1.legend()
ax1.set_title(f"{Dir}-elastic response spectra")
ax1.set_xlabel('T[s]')
ax1.set_ylabel('$S_e/a_g$')

ax2.legend()
ax2.set_title(f"{Dir}-elastic response spectra of amplitude acceleration vs period")
ax2.set_xlabel('T[s]')
ax2.set_ylabel('$S_e \quad[g]$')

# Adjust spacing between subplots
plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(fig)


# Create the plot
fig, ax = plt.subplots()

for k in GroundType:
	ax.plot(T, (T/(2*np.pi))**2*RS.EC8(T,ag=ag, GroundType=k,xi=xi, Dir=Dir, RS_Type=RS_Type_value, bi=bi,TD_bi=TD_bi), label=k)

ax.legend()
ax.set_title(f"{Dir}-Displacement vs period")
ax.set_xlabel('T[s]')
ax.set_ylabel('$S_{{de}}=S_e(\\frac{{T}}{{2\pi}})^2$ [m]')

# Adjust spacing between subplots
plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(fig)


#st.write((T/(2*np.pi))**2*RS.EC8(T=4,ag=ag, GroundType=GroundType,xi=xi, Dir=Dir, RS_Type=RS_Type_value, bi=bi,TD_bi=TD_bi))



# Create an empty dataframe
df = pd.DataFrame({'Period[s]': T})
list_df=[]
list_df1=[]
# create interations
for k in GroundType:
	df_k=pd.DataFrame({'Period[s]':T,'Se/g'+"-"+str(k):1/g*RS.EC8(T,ag=ag,GroundType=k,xi=xi,Dir=Dir,RS_Type=RS_Type_value, bi=bi,TD_bi=TD_bi)})
	df1_k=pd.DataFrame({'Frequency[1/s]':(1/T),'Se/g'+" "+str(k):1/g*RS.EC8(T,ag=ag,GroundType=k,xi=xi,Dir=Dir,RS_Type=RS_Type_value, bi=bi,TD_bi=TD_bi)})
	# sort column 'Frequency[1/s]' in ascending order
	df1_k=df1_k.sort_values('Frequency[1/s]').round(4)
	
	# Merge df and df_k on the "Frequency[1/s]" column
	df = pd.merge(df, df_k, on="Period[s]")

	# Append the df_k into the list
	
	list_df.append(df_k)
	list_df1.append(df1_k)
	
df=df.round(4)

st.write(df)

# Download CSV
hf.download_csv(df,file_name="EC8")
hf.download_sofistik(list_df,file_name="EC8")
hf.download_abaqus(list_df1,file_name="EC8")









