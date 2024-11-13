
import requests
import sys

def getUrlContent(url):
	page = requests.get(url)
	pageLine = page.text.splitlines()
	links = []
	bodyArray = []
	bodycheck = False
	scriptlist = [False]
	inside_tag = False
	inside_script_tag = False

	for line in pageLine:
		line = line.strip()
		if line.find("<title>") != -1:
			print("Title :- ",line[line.find("<title>")+7: line.find("</title>")]+"\n")
		if line.find("https") != -1:
			idxOf_https = line.find("https")
			links.append(line[line.find('https') : line.find('"', line.find('"', idxOf_https))])

		if line.find("<body") != -1:
			bodycheck = True
		
		if bodycheck:
			text = ""
			for char in line:
				if char == '<':
					inside_tag = True
					if text.endswith('<script'):
						inside_script_tag = True
				elif char == '>':
					inside_tag = False
					if text.endswith('</script'):
						inside_script_tag = False
				elif not inside_tag and not inside_script_tag:
					text += char
			bodyArray.append(text.replace('^ "',""))

	print("\nlinks:- ")
	for link in links:
		print(link)
	print("\nLinks have ended.\n")

	print("\nBody of web\n")
	for subline in bodyArray:
		if subline == "" or subline == "\n" or subline.find("{")!= -1 or subline.count(";") >= 2 or subline.find("العربي") !=-1 or subline.find("한국어Հայերենहिन्द") != -1 or subline.find("https:")!=-1 or subline.find("MediaWiki") !=-1:
			continue
		for chare in subline:
			if chare == "^" or chare =='"':
				print("",end="")
			else:
				print(chare, end="")
		print()
	print("\nBody end")

url = sys.argv[1]
getUrlContent(url)