import sys
import requests
import os
import re
import html
from typing import List
from tqdm import tqdm

CVF_URL = "https://conferences.miccai.org/"


def download_file(url, dir, filename):
    r = requests.get(url, stream=False,allow_redirects=True)
    filename=re.sub('[:\?/+\'"<>]'," ",filename)
    filename = re.sub("[\u4e00-\u9fa5]", "", filename)
    open(f"{dir}/{filename}.pdf", 'wb').write(r.content)


class PaperHelper:
    def __init__(self, year):
        self.year = str(year)
        webpage = requests.get(f"{CVF_URL}/{year}/papers").text
        open('temp.html','w',encoding='utf-8').write(webpage)
        webpage = open('temp.html').read()
        webpage = html.unescape(webpage)
                
        self.titles= re.findall(f"(?=html\">).+(?=</a>)", webpage)
        self.titles = [title[6:] for title in self.titles]
        
        if not os.path.exists(f'MICCAI{self.year}/MICCAI{self.year}_list.txt'):
            self.url = re.findall(f"(?={self.year}/).+(?=.html)", webpage)
            self.urls = [os.path.join(f'{CVF_URL}', url+'.html') for url in self.url]
            self.dois=[]
            for i,url in enumerate(tqdm(self.urls)):
                webpage = requests.get(f"{CVF_URL}/{url}").text
                open('doi.html','w',encoding='utf-8').write(webpage)
                webpage = open('doi.html').read()
                webpage = html.unescape(webpage)
                doi=re.findall("(?=DOI: <a href=\").+(?=\">https)", webpage)
                doi=doi[0][14:]
                doi=doi.replace('https://link.springer.com/chapter/','https://link.springer.com/content/pdf/')
                self.dois.append(doi+'.pdf')  
            self.urls=self.dois
            with open(f'MICCAI{self.year}/MICCAI{self.year}_list.txt','w') as fp:
                [fp.write(str(item)+'\n') for  item in self.urls]
                fp.close()
                
        self.urls=open(f'MICCAI{self.year}/MICCAI{self.year}_list.txt').readlines()
                 
          
    def search_keyword(self,kw):
        result = []
        for idx, title in enumerate(self.titles):
            if kw.lower() in title.lower():
                result.append(idx)
        print(f"found {len(result)} papers")
        return result        

    def download_paper(self, idx, save_to):
        url = self.urls[idx].strip('\n')
        download_file(url=url, dir=save_to, filename=self.titles[idx])
            
    def download_keyword(self, kw):
        paper_idx_list = self.search_keyword(kw)
        try:
            assert len(paper_idx_list) > 0
            download_dir = f"./MICCAI{self.year}/MICCAI{self.year}-{kw}/"
            print (f"Downloading in {download_dir}...")
            os.makedirs(download_dir, exist_ok=True)
            bar = tqdm(paper_idx_list)
            for paper_idx in bar:
                self.download_paper(paper_idx, download_dir)
                bar.set_description(
                    f"Downloading \"{self.titles[paper_idx][:15]}...\"")
        except:
            print(f"{kw} paper does not found")
            
    
if __name__ == '__main__':
    kw = "transformer"
    # kw='graph'
    # kw=sys.argv[1]
    helper = PaperHelper(2022)
    print(f"Searching for \"{kw}\"...")
    helper.download_keyword(kw)
