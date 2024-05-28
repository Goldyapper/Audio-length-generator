from mutagen.mp3 import MP3
import os
# function to convert the information into 
# some readable format 
def audio_duration(file_path): 
	
	file_name = os.path.basename(file_path)
	file = os.path.splitext(file_name)
	name = file [0]# returns the name of the file

	audio = MP3(file_path)
	audio_info = audio.info 
	length = int(audio_info.length) 
	mins = length // 60 # calculate in minutes 
	if length > 0:
		mins += 1
	return name, mins # returns the duration 

print(audio_duration("E16 - Chase the Night.mp3"))