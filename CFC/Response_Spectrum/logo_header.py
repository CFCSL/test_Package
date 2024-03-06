# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 11:13:55 2023

@author: cfcpc2
"""

import streamlit as st



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
