from mutagen.mp3 import MP3
import os
import glob
from openpyxl import load_workbook

spreadsheet= "audio time spreadsheet.xlsx"
mypath = ("C:/Users/adama/Downloads/Big Finish Productions/*")

# function to convert the information into 
# some readable format 
def file_name(file_path):
	file_name = os.path.basename(file_path)
	file = os.path.splitext(file_name)
	name = file [0]# returns the name of the file
	
	return name

def audio_duration(file_path): 
	
	name = file_name(file_path)

	audio = MP3(file_path)
	audio_info = audio.info 
	length = int(audio_info.length) 
	mins = length // 60 # calculate in minutes 
	if length > 0:
		mins += 1
	return [name, mins] # returns the duration 

def addtospreadsheet(new_data):
	work_book = load_workbook(spreadsheet)
	work_sheet = work_book.active
	
	for row in new_data:
		work_sheet.append(row)
	
	work_book.save(spreadsheet)

everyitem = (glob.glob(mypath))


while True:
	for item in everyitem:
		if ".mp3" in item :
			addtospreadsheet([audio_duration(item)])#get name and time of mp3 files and add to sheet	
		else:
			mypath+=("/*")
			everyitem = glob.glob(mypath)
			
			if ".mp3" not in item:
				try: 
					data_to_add = (file_name(item))
					if data_to_add.isnumeric() == False:
						new_data = [[data_to_add,"N/A"]]
						addtospreadsheet(new_data)
				except:	
					break