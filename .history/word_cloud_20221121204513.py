import sys
import requests
import html
from wordcloud import WordCloud
from matplotlib import pyplot as plt
import re


class PaperHelper:
    def __init__(self, year):
        self.year = str(year)
        if self.year=='2022':
        	webpage = requests.get(f"https://conferences.miccai.org/{year}/papers").text
        elif self.year=='2021':
        	webpage = requests.get(f"https://miccai2021.org/openaccess/paperlinks//index.html").text
        else:
        	print(f'Please adding the source for {self.year}')
        	raise ValueError
        webpage = html.unescape(webpage)
        self.titles= re.findall(f"(?=html\">).+(?=</a>)", webpage)
        self.titles = [title[6:] for title in self.titles]


def fancy_word_cloud(name,year):
    helper = PaperHelper(year)
    text = ' '.join(helper.titles)
    wc = WordCloud(background_color='white',font_path="times.ttf",height=1500,width=2000)
    wc.generate(text)
    plt.axis("off")
    plt.imshow(wc, interpolation="bilinear")
    plt.savefig(f'worldcloud/{name+str(year)}.png',dpi=1200)
    plt.show()
    
    
    
if __name__ == '__main__':
	print('Choose the conference name: ')  
	name=sys.stdin.readline().strip()
	print('Choose the year: ')
	year=int(sys.stdin.readline().strip()) 
	print(f'name={name},year={year}')

	if name=='CVPR':
		from paperhelp_CVPR import PaperHelper
	elif name=='ICCV':
		from paperhelp_ICCV import PaperHelper
	elif name=='NIPS':
		from paperhelp_NIPS import PaperHelper
	else:
		assert name=='MICCAI'
		print(f'using the current settings')

	fancy_word_cloud(name,year)
