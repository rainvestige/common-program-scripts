# coding=utf-8
"""
Voice of American Web Crawler
"""

import os
import requests
import re
import time
import datetime

from bs4 import BeautifulSoup
from urllib.request import urlopen,urljoin


def crawl(url):
    """Obtain the html text

    Args:
        url: The web link we want to scrape.

    Returns:
        A raw html text.
    """

    response = urlopen(url)
    time.sleep(0.1)  # slightly delay for downloading
    return response.read().decode('utf-8')  #return raw html page


def parse(html, date): 
    """Find the urls which meet the date requirement in html object.

    Args:
        html: The html object we obtained in `crawl(url)` function
        date: Download the audio according to the given date.

    Returns:
        the set of urls obtained from the html 
    """

    soup = BeautifulSoup(html, features='html.parser')  # use bs4 to parse html object
    urls = soup.find_all(
        'a',
        {'href':re.compile('^/VOA_Special_English/.+?\d.html$')},
        text=re.compile(date)  # the text content should contain the date
    )    
    # '^/'('/$') means start(stop) with '/' 
    # '+?' match none or one regular expression as small as possible

    #for i, url in enumerate(urls):
    #    print('{}-- {}'.format(i, url))
    
    return urls


def parse_audio_url(html):
    """The second parse to find the audio download urls.

    Args:
        html: All html links that may contain the audio file we want.

    Returns:
        The download links of audio source
    """

    soup = BeautifulSoup(html, features='html.parser')
    try:
        audio_url_tag = soup.find_all(
            'a', 
            {'id': 'mp3', 'href': re.compile('.mp3$')}
        )
        audio_url = audio_url_tag[0]['href']
        title = soup.find('title').get_text().strip()
    except:
        print('Unfortunately, an unknown error has happened\n')
    else:
        return audio_url, title


def download_src(url, date, save_dir):
    """Download the audio .mp3 file from the url

    Args:
        url: The url of the source audio .mp3 file
        date: Used to save the name.
    """

    try:
        r = requests.get(url, stream=True)
    except:
        print("Unfortunately an unknown error has happened,please wait 3 seconds\n")
        time.sleep(3)
    else:
        name = url.split('/')[-1]
        src_name = ' '.join(name.split('-'))
        #src_name = src_name[0].upper() + src_name[1:]
        src_name = src_name.capitalize()
        with open(save_dir+r'/%s' % (date+'--'+src_name), 'wb') as f:
            for chunk in r.iter_content(chunk_size=10240):
                f.write(chunk)         
            print("%s saved %s\n" %(date,src_name))
    return None


def main():
    # make dirs for saving VOA sources
    save_dir = r'/media/windows/Projects/python_tutorials/Download_VOA'
    os.makedirs(save_dir, exist_ok=True)
    
    count = 0  # count the downloaded files

    date_prefix = input('Date prefix(2020/4/):')
    date_start = int(input('Date start from: '))
    date_end = int(input('Date end at: '))
    
    base_url = "http://www.51voa.com/"
    html = crawl(base_url)
    for d in range(date_start, date_end+1, 1):
        day = '%s' % d
        date = date_prefix + day
        urls = parse(html, date)
        page_urls = set([urljoin(base_url, url['href']) for url in urls])
        print(page_urls)

        for page_url in page_urls:
            html_mp3 = crawl(page_url)
            src_url, _ = parse_audio_url(html_mp3)
            print(src_url)
            date = '-'.join(date.split('/'))
            download_src(src_url, date, save_dir)
            count += 1


if __name__ == "__main__":
    main()
