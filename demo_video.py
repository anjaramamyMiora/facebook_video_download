import sys
from  facebook_scraping import get_reel_video, get_standart_video

if len(sys.argv)>1:
	input_value = sys.argv[1]
else:
	input_value=""

get_standart_video(input_value)
