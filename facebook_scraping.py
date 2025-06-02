import requests
import re
from json import dumps, loads
import os
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import sys

dir="medias/content"
os.makedirs(dir, exist_ok=True)
video_dir="medias/reels"
os.makedirs(video_dir, exist_ok=True)

def get_reel_video(url):
	if re.match("^https://www.facebook.com/reel/[0-9]+$", url):
		url=url
	elif re.match("^[0-9]+$", url):
		url=f"https://www.facebook.com/reel/{url}"
	else:
		filename=os.path.basename(__file__)
		print(f"invalid input {url}")
		print(f"please, use valid url or video id in first argument: \n\t- python {filename} 1234567788\n\t- python {filename} \"https://www.facebook.com/reel/1234567788\"")
		sys.exit()

	# reels
	video_id=re.split("[/?]", url)[-1]
	if video_id=="":
		video_id=re.split("[/?]", url)[-2]
		
	video_id=re.sub("^.*=", "", video_id)
	print(video_id)
	headers = {
	    'User-Agent': UserAgent().random,
	    "Referer": "https://www.facebook.com/",
	    "DNT": "1",

	}
	output=f"{dir}/{video_id}.html"
	if not ((os.path.exists(output)) and (os.stat(output).st_size>0)):
		current_loop=1
		max_try=3
		while current_loop<=max_try:
			try:			
				user_agent = UserAgent(
				    browsers=["Edge", "Chrome", "Firefox", "Safari", "Opera"]
				)
				user_agent.random

				headers = {
				    'User-Agent': UserAgent().random,
				    "Referer": "https://www.facebook.com/",
				    "DNT": "1",

				}
				print(f"download page from  {url}")
				response=requests.get(url, headers=headers )
				content=response.content
				
				main_parser = BeautifulSoup(content, 'html.parser')
				if main_parser.find("meta", {"property" : "og:video"}):
					current_loop=max_try+1
					with open(output, "wb") as file:
						file.write(content)
				else:
					current_loop+=1

				
				
				
			except Exception as e:
				print(e)
				print(f"new attempt ...")
				current_loop+=1
	try:
		with open(output, "r") as file:
			content=file.read()
	except Exception as e:
		raise e
		sys.exit()
	

	main_parser = BeautifulSoup(content, 'html.parser')
	if main_parser.find("meta", {"property" : "og:video"}):
		video_link=main_parser.find("meta", {"property" : "og:video"})["content"]
		print(video_link)
		max_try=3
		current_loop=1
		output=video_dir+"/"+video_id+".mp4"
		if not ((os.path.exists(output)) and (os.stat(output).st_size>0)):
			while current_loop<=max_try:
				try:
					video_response=requests.get(video_link, headers=headers)
					with open(output, "wb") as file:
						file.write(video_response.content)
					current_loop=max_try+1
					print(f"video {video_id} saved at {output}")
				except Exception as e:
					print(e)
					current_loop+=1
		else:
			print(f"video already present and non empty at {output}")
		