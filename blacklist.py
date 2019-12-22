from os import unlink, walk
from os.path import join
from re import compile

base = "D:\\"
blacklist_file = "rappers.txt"
extensions = [".mp3", ".mcg", ".mp4"] #karaoke files
artist_separator = " - "
name_separator = ", "

blacklist = []
with open(blacklist_file, "r") as listfile:
	for artist in listfile:
		artist = artist.strip().upper()
		if not artist in blacklist:
			blacklist.append(artist)

class InvalidFile(Exception):
	pass
invalidfile = InvalidFile()

track_number_filter = compile("^[0-9]* ")

delete_count = 0
for root, dirs, files in walk(base, topdown=True):
	for fn in files:
		try:
			goodfile = False
			for x in extensions:
				if fn.endswith(x):
					goodfile = True
					break
			if not goodfile:
				raise invalidfile
		except InvalidFile:
			continue
			
		t = track_number_filter.sub("", fn)
		
		split_point = t.find(artist_separator)
		artist = t[:split_point]
		
		if name_separator in artist:
			if artist.count(name_separator) == 1:
				last, first = artist.split(name_separator)
				artist = first + " " + last
				
		if artist in blacklist:
			unlink(join(root, fn))
			delete_count += 1

print("Deleted", delete_count, "songs.")	