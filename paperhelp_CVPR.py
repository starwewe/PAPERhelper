import sys
import requests
import os
import re
import html
from typing import List
from tqdm import tqdm

CVF_URL = "https://openaccess.thecvf.com/"


def download_file(url, dir, filename):
    r = requests.get(url, stream=False,allow_redirects=True)
    filename=re.sub('[:\?/+"<>]'," ",filename)
    filename = re.sub("[\u4e00-\u9fa5]", "", filename)
    open(f"{dir}/{filename}.pdf", 'wb').write(r.content)

class PaperHelper:
    def __init__(self, year):
        self.year = str(year)
        webpage = requests.get(f"{CVF_URL}/CVPR{year}?day=all").text
        open('temp.html','w',encoding='utf-8').write(webpage)
        webpage = open('temp.html').read()
        webpage = html.unescape(webpage)
            
        self.urls = re.findall("(?<=href=\").+?pdf(?=\">pdf)|(?<=href=\').+?pdf(?=\">pdf)", webpage)
        self.titles= re.findall(f"(?<={year}_paper.html\">).+(?=</a>)", webpage)
    
    def search_keyword(self,kw):
        result = []
        for idx, title in enumerate(self.titles):
            if kw.lower() in title.lower():
                result.append(idx)
        print(f"found {len(result)} papers")
        return result        

    def download_paper(self, idx, save_to):
        self.urls[idx]=CVF_URL +self.urls[idx]
        download_file(url=self.urls[idx], dir=save_to, filename=self.titles[idx])
            
    def download_keyword(self, kw):
        paper_idx_list = self.search_keyword(kw)
        try:
            assert len(paper_idx_list) > 0
            download_dir = f"./CVPR{self.year}/CVPR{self.year}-{kw}/"
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
    kw = "prognosis"
    # kw='graph'
    # kw=sys.argv[1]
    helper = PaperHelper(2022)
    print(f"Searching for \"{kw}\"...")
    helper.download_keyword(kw)
