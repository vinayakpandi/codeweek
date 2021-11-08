# Importing Packages
import json
import camelot
import requests
import numpy as np
import pandas as pd
import tabula as tb
import streamlit as st
from pdf2image import convert_from_path

st.set_page_config(
				   page_title="Borderless Table Parser",
				   page_icon="🧊",
				   layout="wide",
				   initial_sidebar_state="expanded",
				  )
st.title("Borderless Table Parser")

pdf_file = st.file_uploader("Upload PDF File")

# c1, c2 = st.columns((.1,1))
# show_f = c1.button(label="Show File")
process_f = st.button(label="Process File")

# df = st.empty()
notify = st.empty()
my_bar = st.progress(0)

if process_f:
	if pdf_file:
		# df.empty()
		my_bar.progress(0)
		notify.header("Process File")

		# print(pdf_file.name)
		fn = pdf_file.name
		# fn = files.file.read()
		images = convert_from_path(fn,poppler_path=r'C:\Program Files\poppler-0.68.0\bin')
		images[0].save('test.png', 'PNG')

		# with io.open(fn,mode = "rb") as f:
		#   input_pdf = PdfFileReader(f)
		#   media_box = input_pdf.getPage(0).mediaBox
		# min_pt = media_box.lowerLeft
		# max_pt = media_box.upperRight

		my_bar.progress(50)

		url = "http://localhost:5000/pred"
		result = requests.post(url)
		final_pdf_coordinates = result.json()
		print("FINAL_TABLE_COORDINATES: ",final_pdf_coordinates)

		# tables = tb.read_pdf(fn,area = [final_pdf_coordinates],stream = True,output_format = "dataframe",pandas_options = {'header':None})
		# if len(tables) > 0:
		# 	df = pd.DataFrame(np.concatenate(tables))
		# 	df.columns = df.iloc[0]
		# 	df = df.drop(0)
		# else:
		# 	# print("No table")
		# 	df = pd.DataFrame()
		
		bb = final_pdf_coordinates.split(",")
		bb = [int(i) for i in bb]
		bc = [str(i) for i in bb]
		joined_string = ",".join(bc)
		bd = []
		bd.append(joined_string)
		# print(bd)

		tables = camelot.read_pdf(fn,flavor='stream',table_regions = bd)
		if len(tables) > 0:
			df = tables[0].df
			dl = list(df.columns)
			cl = dl[1]
			df[cl].replace('', np.nan, inplace=True)
			df.dropna(subset=[cl], inplace=True)
		else:
			print("No table")
			df = pd.DataFrame()

		my_bar.progress(100)
		notify.dataframe(df)
		# notify.header("File executed")

	else:
		notify.header("Please upload the pdf file to process")
