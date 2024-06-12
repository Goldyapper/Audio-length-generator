from mutagen.mp3 import MP3
import os
import glob
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
	return name, mins # returns the duration 

#print(audio_duration("C:/Users/adama/Downloads/Big Finish Productions/1. Doctor Who/5. Bernice Summerfield/2. Bernice Summerfield Audiobooks (BSAB)/BSAB 1.0X - Treasury.mp3"))

mypath = ("C:/Users/adama/Downloads/Big Finish Productions/*")

everyitem = (glob.glob(mypath))
while True:
	for item in everyitem:
		#print(item)
		if ".mp3" in item :
			print (audio_duration(item))
			
		
		else:
			#print ('false ' + item)
			mypath+=("/*")
			everyitem = glob.glob(mypath)
			
			if ".mp3" not in item:
				try: 
					print (audio_duration(item))
				except:	
					print(item)
			#print (everyitem)

