import sys
import requests
import os
import re
from typing import List
from tqdm import tqdm
import html
CV_URL = "https://proceedings.neurips.cc/paper"


def download_file(url, dir, filename):
    filename = re.sub('[:\?/+"<>]', " ", filename).replace('Abstract.html', '')
    filename = filename.replace('\\','')
    # print(filename)
    url = (url+'Paper.pdf').replace('hash', 'file')
    r= requests.get(url, stream=False, allow_redirects=True)
    open(f"{dir}/{filename}.pdf", 'wb').write(r.content)


class PaperHelper:
    def __init__(self, year):
        self.year = str(year)
        webpage = requests.get(f"{CV_URL}/{year}").text
        open('temp.html','w',encoding='utf8').write(webpage)
        webpage = open('temp.html', encoding='utf8').read()
        webpage=html.unescape(webpage)

        self.urls = re.findall("(?<=href=\").+(?=Abstract.html\")", webpage)
        self.titles = re.findall("(?=Abstract.html\").+(?=</a>)", webpage)

    def search_keyword(self,kw):
        result = []
        for idx, title in enumerate(self.titles):
            if kw.lower() in title.lower():
                result.append(idx)
        print(f"found {len(result)} papers")
        return result        

    def download_paper(self, idx, save_to):
        self.urls[idx] = "https://proceedings.neurips.cc" + self.urls[idx]
        download_file(url=self.urls[idx], dir=save_to, filename=self.titles[idx])

    def download_keyword(self, kw):
        paper_idx_list = self.search_keyword(kw)
        try :
            assert len(paper_idx_list) >0
            download_dir = f"./NeurIPS{self.year}-{kw}/"
            os.makedirs(download_dir, exist_ok=True)
            bar = tqdm(paper_idx_list)
            for paper_idx in bar:
                self.download_paper(paper_idx, download_dir)
                bar.set_description(
                    f"Downloading \"{self.titles[paper_idx][15:30]}...\"")
        except:
            print(f"{kw} paper does not found")
           
    
if __name__ == '__main__':
    kw = "survival"
    # kw=sys.argv[1]
    helper = PaperHelper(2021)
    print(f"Searching for \"{kw}\"...")
    helper.download_keyword(kw)
