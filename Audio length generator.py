from mutagen.mp3 import MP3
import os
import glob
import re
from tinytag import TinyTag 
from openpyxl import load_workbook
import requests
from bs4 import BeautifulSoup

spreadsheet= "audio time spreadsheet.xlsx"
mypath = ("C:/Users/adama/Downloads/Big Finish - Doctor Who - 2022/*")
# function to convert the information into 
# some readable format 
def file_name(file_path):
	
	file_name = os.path.basename(file_path)
	file = os.path.splitext(file_name)
	name = file [0]# returns the name of the file
	name = re.sub(r'^.*? -' , '', name).lstrip()

	return name

def fetch_data(url):
    # URL of the website to fetch data from
    url = "https://tardis.wiki/wiki/Rosa_(TV_story)"

    try:
        # Send a GET request to the website
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes

        # Access the content of the response
        soup = BeautifulSoup(response.text, 'html.parser')

        for item in soup.select('div.pi-item'): # a for loop that runs through at elements in the table
            label = item.select_one('h3.pi-data-label')

            #Parts Data retrival
            if label and 'Number of parts:' in label.text:
                value = item.select_one('div.pi-data-value')
                if value:
                    parts = value.text.strip()
            
            #Doctor Data retrival
            if label and 'Doctor:' in label.text:
                values = item.select('div.pi-data-value a')
                doctor = [d.text for d in values]

            
            #companion retrival    
            if label and 'Companion(s):' in label.text:
                values = item.select('div.pi-data-value a')
                companions = [c.text for c in values]
            
            #Featuring retrival    
            if label and 'Featuring' in label.text:
                values = item.select('div.pi-data-value a')
                featuring = [f.text for f in values]

            #Enemy retrival
            if label and 'Main enemy' in label.text:
                values = item.select('div.pi-data-value a')
                enemy = [e.text for e in values]

            #Writer Retrival
            if label and 'Writers' in label.text:
                values = item.select('div.pi-data-value a')
                writer = [w.text for w in values]

            #Director Retrival
            if label and 'Director' in label.text:
                values = item.select('div.pi-data-value a')
                director = [d.text for d in values]
        
        return parts,doctor,companions,featuring,enemy,writer,director

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def doctor_text_converter(text):
	doctor =''
	if text == 'Thirteenth Doctor':
		doctor = "13th Dr"

	return doctor

def audio_data(file_path): 
	
	name = file_name(file_path)

	parts,doctor,companions,featuring,enemy,writer,director = fetch_data("a")
	
	doctor_text_converter(doctor)

	tinytag_audio = TinyTag.get(file_path)
	audio = MP3(file_path)
	audio_info = audio.info 
	length = int(audio_info.length) 
	mins = length // 60 # calculate in minutes 
	if length > 0:
		mins += 1
	
	year = tinytag_audio.year
	track = (tinytag_audio.track)
	
	data = [name,'','','','',track,parts, mins,doctor,companions,featuring,enemy,writer,director,year]
	audio_data = [", ".join(item) if isinstance(item, list) else item for item in data]
	
	return audio_data # returns the data cleaned up 

def addtospreadsheet(new_data):
	work_book = load_workbook(spreadsheet)
	work_sheet = work_book.active
	
	for row in new_data:
		work_sheet.append(row)
	
	work_book.save(spreadsheet)

everyitem = (glob.glob(mypath))


while True:
	everyitem = (glob.glob(mypath))

	if "mp3" not in everyitem[0]:
		mypath+=("/*")
		everyitem = glob.glob(mypath)
	else:
		for item in everyitem:
			if ".mp3" in item:
				print(audio_data(item))
				addtospreadsheet([audio_data(item)])#get name and time of mp3 files and add to sheet	
			else:
				try: 
					data_to_add = (file_name(item))
					if data_to_add.isnumeric() == False:
						new_data = [[data_to_add,"N/A"]]
						addtospreadsheet(new_data)
				except:	
					break
		mypath+=("/*")
		everyitem = glob.glob(mypath)
