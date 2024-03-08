# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 15:49:41 2024

@author: cfcpc2
"""
import numpy as np
import pandas as pd
import os
import io
import zipfile
import json
from collections import defaultdict
from tempfile import NamedTemporaryFile




def read_excel(input_file):
	"""
	

	Parameters
	----------
	input_file : file.xlsx
		DESCRIPTION.

	Returns
	-------
	DICTIONARY
		Return one database of dictionary

	"""
	
	def singularize(word):
		if word.endswith('s') or word.endswith('S') :
			return word[:-1]
		else:
			return word
		
	DB=defaultdict(lambda: defaultdict(dict))
	df_dict=pd.read_excel(input_file,sheet_name=None)
	for object_type in df_dict:
		obj=df_dict[object_type]
		
		# Data processing
		# Remove white space, then Delete "#" in case 
		obj = obj.applymap(lambda x: x.lstrip() if isinstance(x, str) else x).applymap(lambda x: x.lstrip('#') if isinstance(x, str) and x.startswith('#') else x)
		obj=obj.applymap(lambda x: x.replace("'", "") if isinstance(x, str) else x)
		
		obj.columns=[x.upper() for x in obj.columns] #change all columns name to upercase
		obj.columns =  [singularize(x.lower()) if  x in ['VALUE', 'UNITS', 'NOTES'] else x for x in obj.columns] #change some columns to slower singular
		obj=obj.dropna(subset=['value'])
		
		unexpected_unit=['ud', '#',"", " ", np.nan]
		obj['unit']=obj['unit'].apply(lambda x: "-" if x in unexpected_unit else x)
		subset=obj.columns.drop('note')
		obj[subset]=obj[subset].applymap(lambda x: x.replace(' ', "")if isinstance(x, str) else x)

		#Separating data to two DataFrame
		df_revit=obj.drop(columns=["SOFISTIK"],errors='ignore').dropna(subset=['REVIT'])
		df_sofistik=obj.drop(columns=["REVIT"],errors='ignore').dropna(subset=['SOFISTIK'])
		unique_IDs=obj["ID"].dropna().unique()
		for _id in unique_IDs:
			DB[object_type]["REVIT"][str(_id)]=df_revit[df_revit['ID']==_id].set_index('REVIT').drop(columns=['ID']).to_dict('index')
			
			DB[object_type]["SOFISTIK"][str(_id)]=df_sofistik[df_sofistik['ID'] == _id].set_index('SOFISTIK').drop(columns=['ID']).to_dict('index')

	return DB

def to_json(DB, json_file):
	"""
	

	Parameters
	----------
	DB : Dictionary
		DESCRIPTION.
	json_file : json
		The desired file name.

	Returns
	-------
	json_file : json
		output json file

	"""
	
	with open(json_file, "w") as outfile: 
		json.dump(DB, outfile,indent=4)
	return json_file

def read_json(uploaded_file): # uploaded_file is an UploadedFile object
	# Read the contents of the UploadedFile object as bytes
	content_bytes = uploaded_file.read()
	
	# Create a file-like object from the bytes content
	content_file = io.BytesIO(content_bytes)
	
	# Parse the JSON content from the file-like object into a dictionary
	return json.load(content_file)

def DB_to_SOFISTIK(DB):

	# Define the zip file name
	zip_file_name = 'SOFISTIK_files.zip'
	
	# Check if the zip file exists and remove it if it does
	if os.path.exists(zip_file_name):
		os.remove(zip_file_name)
	DB_SOFISTIK=defaultdict(lambda: defaultdict(dict))
	for object_type in DB:
		DB_SOFISTIK.update({object_type:DB[object_type]['SOFISTIK']})
		file=DB_SOFISTIK[object_type]
		for _id in file:
			local_text =f"$Generation Sofistik_{object_type}_{_id}\n\n$Lets have in mind that units may be defined correctly by users\n\n" 
			for var in file[_id]:
				#local_text += f"LET#{var}\t\t{file[_id][var]['value']} {file[_id][var]['unit'].strip("'")}\t\t${file[_id][var]['note']}\n"
				if file[_id][var]['unit']=='-':
					local_text+= f"LET#{var}\t\t{file[_id][var]['value']}   \t\t${file[_id][var]['note']}\n"
				else:
					local_text+= f"LET#{var}\t\t{file[_id][var]['value']}[{file[_id][var]['unit']}]\t\t${file[_id][var]['note']}\n"
			
			# Save local text as a .dat file within the zip file
			file_name = f"Sofistik_{object_type}_{_id}.dat"
			with zipfile.ZipFile(zip_file_name, 'a') as zf:
				zf.writestr(file_name, local_text)
	
	return zip_file_name

def DB_to_REVIT(DB):
	DB_REVIT=defaultdict(lambda: defaultdict(dict))
	for object_type in DB:
		DB_REVIT.update({object_type:DB[object_type]['REVIT']})
	json_file="DB_REVIT.json"
	to_json(DB_REVIT, json_file)
	
	return json_file

