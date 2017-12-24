from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse, os
class Tools:
	def __init__(self):
		if not os.path.exists("./MAIN_PH.list"):
			print("[WELCOME] First Run! ")
			open("./MAIN_PH.list","w")
		if not os.path.exists("./TBD_PH.list"):
			print("[PREPARING] Files")
			open("./TBD_PH.list","w")
		if not os.path.exists("./ARCHIVE_PH.list"):
			print("[DONE] okay we are done!")
			open("./ARCHIVE_PH.list","w")
		
	def find_link(self,file_path,link):
		# this will check if the given link is there in the provided file link
		file_object = open(file_path,'r')
		data = file_object.read()
		data = data.split()
		file_object.close()
		del file_object
		if str(link) in data:
			return True
		return False

	def append_link(self,file_path,link):
		#this will add a new link to the provided file at the end of the file 
		try:
			with open(file_path,'r') as file_object:
				data = file_object.read()
				data += f"\n{str(link)}"
			with open(file_path,'w') as file_object:
				file_object.write(data)
			del file_object, data
			return True
		except Exception as e:
			print("utils.py; 26;", ", ".join(e.args))
			return False

	def remove_link(self,file_path,link):
		try:
			data = None
			with open(file_path,'r') as file_object:
				data = file_object.read()
				data = data.split()
				data.remove(link)
				with open(file_path,'w') as file_object:
					data = '\n'.join(data)
					file_object.write(data)
			return True
		except Exception as e:
			print("utils.py; 40;", ", ".join(e.args))
			return False
				
	def get_me_link(self,file_path):
		with open(file_path,'r') as file_object:
			data = file_object.read()
			return '0' if not data else data.split()[0]
