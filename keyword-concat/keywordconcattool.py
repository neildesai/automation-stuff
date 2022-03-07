import streamlit as st 
import pandas as pd
import re
import base64
import io
import time
import requests
import json



def main():


	st.title("Concatutatool")

	best = st.multiselect('Select variation', ['',' best ', ' nearest '])
	list_1 = st.text_input("List 1")
	set_1 = list_1.split(",")
	texted = st.multiselect('Select variation', ['',' ',' in ',' for ',' with ', ' below ', '  above ', ' near '])
	list_2 = st.text_input("List 2")
	set_2 = list_2.split(",")
	combination_1 = [(bes + a + text + b) for a in set_1 for b in set_2 for bes in best for text in texted]
	all = combination_1
	df =  pd.DataFrame(all, columns=['Keyword'])


	st.write(df)







	#combination_2 = [(b + " " + c) for b in set_2 for c in set_3]
	#combination_3 = [(a + " for " + c) for a in set_1 for c in set_3]
	#combination_4 = [(a + " " + b + " for " + d) for a in set_1 for b in set_2 for d in set_4]

	#all = combination_1 + combination_2 + combination_3 + combination_4



	
	

	
	api_key_input = st.text_input("API Key")
	api_key = 'Bearer ' + api_key_input
	country = st.selectbox('Select country', ('', 'us', 'uk', 'ca', 'au', 'in', 'nz'))
	dataSource = st.selectbox('Select data source', ('gkp','cli'))

	my_data = {
	    'country': country,
	    'currency': 'USD',
	    'dataSource': dataSource,
	    'kw[]': ['']
		}
	my_headers = {
		'Accept': 'application/json',
		'Authorization': api_key
		}


	kw = df['Keyword']
	phrase = kw[0]
	def kw_volume(keyword):
		
		my_data['kw[]'] = keyword
		r = requests.post('https://api.keywordseverywhere.com/v1/get_keyword_data', data=my_data, headers=my_headers)
		data = r.json()
		df_temp = pd.DataFrame.from_dict(data['data'])
		searchVolume = df_temp['vol']
		return searchVolume
		
	run_api = st.button('Fetch me the search volumes')
	if run_api:	
		df['Volume'] = df['Keyword'].apply(kw_volume)
		st.write(df)



	timestr = time.strftime("%Y%m%d-%H%M%S")

	def csv_downloader(data):

		csvfile = data.to_csv()
		b64 = base64.b64encode(csvfile.encode()).decode()
		new_filename = "keyword_concat_output_{}_.csv".format(timestr)
		href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Download the data</a>'
		st.markdown(href,unsafe_allow_html=True)

	csv_downloader(df)











if __name__ == '__main__':
	main()