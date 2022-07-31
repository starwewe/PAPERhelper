import sys
from paperhelp import PaperHelper
from wordcloud import WordCloud
from matplotlib import pyplot as plt


def fancy_word_cloud():
    helper = PaperHelper(2022)
    text = ' '.join(helper.titles)
    wc = WordCloud(height=600, width=1000,background_color='white')
    wc.generate(text)
    plt.axis("off")
    plt.imshow(wc, interpolation="bilinear")
    plt.show()
    
    
if __name__ == '__main__':  
    fancy_word_cloud()
