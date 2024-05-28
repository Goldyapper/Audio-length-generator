from mutagen.mp3 import MP3
# function to convert the information into 
# some readable format 
def audio_duration(file_name): 
	audio = MP3(file_name)
	audio_info = audio.info 
	length = int(audio_info.length) 
	mins = length // 60 # calculate in minutes 
	if length > 0:
		mins += 1
	return mins # returns the duration 

print(audio_duration("E16 - Chase the Night.mp3"))