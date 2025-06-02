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

def get_video(url, output, file_type="Video"):
	user_agent = UserAgent(
	    browsers=["Edge", "Chrome", "Firefox", "Safari", "Opera"]
	)
	try:
		max_try=3
		current_loop=1


		user_agent.random

		headers = {
		    'User-Agent': UserAgent().random,
		    "Referer": "https://www.facebook.com/",
		    "DNT": "1",

		}
		if not ((os.path.exists(output)) and (os.stat(output).st_size>0)):
			while current_loop<=max_try:
				try:
					video_response=requests.get(url, headers=headers)
					with open(output, "wb") as file:
						file.write(video_response.content)
					current_loop=max_try+1
					print(f"{file_type} saved at {output}")
				except Exception as e:
					print(e)
					current_loop+=1
		else:
			print(f"{file_type} already present and non empty at {output}")
			with open(output, "rb") as file:
				content=file.read()
	except Exception as e:
		raise e

def get_reel_video(url):
	if re.match("^https://www.facebook.com/reel/[0-9]+$", url):
		url=url
	elif re.match("^[0-9]+$", url):
		url=f"https://www.facebook.com/reel/{url}"
	else:
		filename=os.path.basename(__file__)
		print(f"invalid input {url}")
		print(f"please, use valid reel url or video id in first argument: \n\t- python {filename} 1234567788\n\t- python {filename} \"https://www.facebook.com/reel/1234567788\"")
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
			else:
				current_loop+=1	
		except Exception as e:
			print(e)
			print(f"new attempt ...")
			current_loop+=1
	if len(content)==0:
		print("An error has occured, please try later")
		sys.exit()

	main_parser = BeautifulSoup(content, 'html.parser')
	if main_parser.find("meta", {"property" : "og:video"}):
		video_link=main_parser.find("meta", {"property" : "og:video"})["content"]
		print(video_link)
		max_try=3
		current_loop=1
		output=video_id+".mp4"

		get_video(video_link, output)



def get_standart_video(url):
	if re.match(r"^https://www.facebook.com/watch\?v=[0-9]+$", url):
		url=url
	elif re.match("^[0-9]+$", url):
		url=f"https://www.facebook.com/watch?v={url}"
	else:
		filename=os.path.basename(__file__)
		print(f"invalid input {url}")
		print(f"please, use valid video url or video id in first argument: \n\t- python {filename} 1234567788\n\t- python {filename} \"https://www.facebook.com/watch?v=1234567788\"")
		sys.exit()

	# reels
	video_id=re.split("[/?]", url)[-1]
	if video_id=="":
		video_id=re.split("[/?]", url)[-2]
		
	video_id=re.sub("^.*=", "", video_id)
	print(video_id)
	current_loop=1
	max_try=3
	print(f"download page from  {url}")
	while current_loop<=max_try:
		try:			
			user_agent = UserAgent(
			    browsers=["Edge", "Chrome", "Firefox", "Safari", "Opera"]
			)
			user_agent.random

			headers = {
			    'User-Agent': f"{user_agent.random}",
			    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
			    "dnt": "1",
			    "dpr": "1",
			    "upgrade-insecure-requests": "1",
			}
			response=requests.get(url, headers=headers )
			content=response.content
			test_url = str(content).split('"browser_native_sd_url":"')
			if(len(test_url)>1):
				current_loop=max_try+1
			else:
				current_loop+=1			
		except Exception as e:
			print(e)
			print(f"new attempt ...")
			current_loop+=1
	if len(content)==0:
		print("An error has occured, please try later")
		sys.exit()

	main_parser = BeautifulSoup(content, 'html.parser')
	test_url_sd = str(content).split('"browser_native_sd_url":"')
	test_url_hd = str(content).split('"browser_native_hd_url":"')
	if len(test_url_sd)>1:
		video_link_sd=test_url_sd[1].split('"')[0]	
		video_link_sd=re.sub("\\u0025","%", video_link_sd)
		video_link_sd=re.sub(r"[\\]", "", video_link_sd)
		print(f"sd video link: {video_link_sd}")
		output=f"{video_id}_sd.mp4"
		get_video(video_link_sd, output)

	if len(test_url_hd)>1:
		video_link_hd=test_url_hd[1].split('"')[0]	
		video_link_hd=re.sub("\\u0025","%", video_link_hd)
		video_link_hd=re.sub(r"[\\]", "", video_link_hd)
		print(f"hd video link: {video_link_hd}")
		output=f"{video_id}_hd.mp4"
		get_video(video_link_hd, output)

	
