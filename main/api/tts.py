import gtts
import io
from django.core import files
from time import sleep

import string

def to_voice(text : str, title : str = "") -> files.File:
	if title == "":
		title = "".join([ch for ch in text[:20] if ch in string.ascii_letters])
	try:
		sleep(1)	#	To delay API requests, otherwise some API requests err.
		file = io.BytesIO()
		voice = gtts.gTTS(text, lang = "tr")
		voice.write_to_fp(file)
		file.flush()
		file.seek(0)
		django_file = files.File(file, title + ".mp3")
		return django_file
	except:
		print("TTS crashed on ", title, ".")
		return None