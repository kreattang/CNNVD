
import re
import requests
import os
def boolstr(string:str):
	if 'y' in string or "1" in string: return 1
	else: return 0
url = 'https://free-proxy-list.net/'
headers = {'User-Agent': 'Python Scraper'}
source = str(requests.get(url, headers=headers, timeout=10).text)
data = [list(filter(None, i))[0] for i in re.findall('<td class="hm">(.*?)</td>|<td>(.*?)</td>', source)]
groupings = [dict(zip(['ip', 'port', 'code', 'using_anonymous'], data[i:i+4])) for i in range(0, len(data), 4)]
for group in groupings[:-5]: print(group['ip']+":"+group['port']+" "+group['code']+"\tType: "+group['using_anonymous'])
if boolstr(input("Save? ")):
	try:
		try: os.remove("proxy.txt"); print("Old file removed")
		except: print("Failed to remove the old file")
		file=open("proxy.txt",'w')
		for group in groupings[:-5]: file.write(group['ip']+":"+group['port']+"\n")
		print("Kinda saved")
		file.close()
		print("Checking if the file saved")
		file=open("proxy.txt",'r')
		if len(file.read())>30:
			print("File saved successfully")
		else:
			print("Error creating the file. Please retry.")
	except: print("Error!")
else: print("Not saved")