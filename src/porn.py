from downloader import Download
from util import Tools
from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse, os, jsonpickle
class PornHub:
	def __init__(self):
		self.helper = Tools()
		self.MAIN_FILE = "./MAIN_PH.list"
		self.TBD_FILE = "./TBD_PH.list"
		self.ARCHIVE_FILE = "./ARCHIVE_PH.list"

	def PH_extractor_(self,resp):
		try:
			parse_tree = BeautifulSoup(resp,"html.parser")
			tag_finder = parse_tree.findAll("li", {"class" : "videoblock"})
			del resp, parse_tree
			for each_tag in tag_finder:
				link = str(each_tag['_vkey'])
				if not self.helper.find_link(self.MAIN_FILE,link):
					self.helper.append_link(self.MAIN_FILE,link)
					self.helper.append_link(self.TBD_FILE,link)
			del tag_finder
		except:
			# Bad connection. Maybe. Or not...
			pass

	def _fetch_CDN_(self,resp):
		resp = str(resp)
		if str(resp).find("alt=\"Upgrade to Pornhub Premium to enjoy this video.\"") != -1:
			# There is nothing to fetch, then "Upgrade to Pornhub Premium" appears
			return True
		import re
		regex = r"(var flashvars_)(.*?)(=)(.*?)(};)"
		match = re.findall(regex, resp)[0][3]
		json = f"{match.strip()}{'}'}"
		json = re.sub('("embedCode":"<iframe src=)(.*?)(iframe>",)', '', json)
		json = re.sub('({"disable_sharebar")(.*?)("mediaDefinitions":)', '', json)
		json = re.sub('(,"video_unavailable_country")(.*)("})', '', json)
		json = jsonpickle.decode(json.replace("\\\\\"", "\"").replace("\\\\/", "//").replace("\/\"", "\"").replace("//", "/"))
		definition, link = "", ""
		l_1080, l_720, l_480, l_280 = None, None, None, None
		for d in json:
			q = int(d["quality"])
			if q == 1080:
				l_1080 = d["videoUrl"]
			if q == 720:
				l_720 = d["videoUrl"]
			if q == 480:
				l_480 = d["videoUrl"]
			if q == 280:
				l_280 = d["videoUrl"]
				
		config = {"download":{"1080":True, "720":True, "480":True, "280":True}}
		if not os.path.exists("./config.json"):
			with open("./config.json","w") as cfg:
				cfg.write('{"download":{"1080":true, "720":true, "480":true, "280":true}}')
		else:
			with open("./config.json","r+") as cfg:
				config = jsonpickle.decode(cfg.read())
		
		if l_1080 is not None and config["download"]["1080"]:
			link = l_1080
			definition = "_1080P"
			print("Found video in 1080P")
		elif l_720 is not None and config["download"]["720"]:
			link = l_720
			definition = "_720P"
			print("Found video in 720")
		elif l_480 is not None and config["download"]["480"]:
			link = l_480
			definition = "_480P"
			print("Found video in 480")
		elif l_280 is not None and config["download"]["280"]:
			link = l_280
			definition = "_280P"
			print("Found video in 280")
		else:
			print("No video found")
			return True
		file_name = BeautifulSoup(resp,"html.parser")
		file_name = str(file_name.title.string)
		for bc in "'*:\"\/?<>|":
			file_name = file_name.replace(bc, " ")
		file_name = file_name.replace(" - Pornhub.com", "")
		download = Download(link,f"{file_name}{definition}.mp4")
		download = download.now()
		if download:
			return True
		return False

	def __prepare__(self):
		# Here starts infinite loop TBD_PH.list is no empty
		while os.stat(self.TBD_FILE).st_size>0:
			link = self.helper.get_me_link(self.TBD_FILE)
			print(("\n[Downloading] : http://www.pornhub.com/view_video.php?viewkey=%s" %(link)))
			resp = urllib.request.Request("http://www.pornhub.com/view_video.php?viewkey=%s"%(link))
			resp.add_header('Cookie',"RNKEY=1043543*1527941:2834309375:3318880964:1;")
			try:
				resp = urllib.request.urlopen(resp).read()
				self.PH_extractor_(resp)
				rc=self._fetch_CDN_(resp)
				if rc==True:
					self.helper.remove_link(self.TBD_FILE,link)
					self.helper.append_link(self.ARCHIVE_FILE,link)
					print("\n[WIN] : File Download Complete!")
				else:
					print("\n[ERROR] : Something went wrong!")
			except Exception as e:
				print(e)
