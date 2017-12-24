import sys, requests, argparse, os, jsonpickle
from porn import PornHub
parser = argparse.ArgumentParser()
parser.add_argument('-u/-url', action='store', dest='url', help='Porn-Hub URL')
parser.add_argument('--version', action='version', version='version 1.0.1 an open book project (C) 2016')
results = parser.parse_args()

config = '{"download":{"1080":true, "720":true, "480":true, "280":true}}'
if not os.path.exists("./config.json"):
	print("Config file not found. Generating new one...")
	with open("./config.json","w") as cfg:
		cfg.write(config)
	print(config)
else:
	print("Config file found.")
	with open("./config.json","r+") as cfg:
		doc = cfg.read()
		if len(doc) <= 62:
			exit("Config file corupted. Remove it.")
		else:
			config = jsonpickle.decode(doc)
		print(config)

if not results.url:
    if not os.path.exists("./TBD_PH.list"):    
        #must pass something to fetch first
        print("please Provide an URL to Fetch !!! ")
    else:
        #simple download porn from saved file list
        newPorn = PornHub()
        newPorn.__prepare__()
else:
    #simple download porn from link provided
    newPorn = PornHub()
    resp=requests.get(str(results.url)).content
    newPorn._fetch_CDN_(resp)
    newPorn.PH_extractor_(resp)
    del resp
    newPorn.__prepare__()