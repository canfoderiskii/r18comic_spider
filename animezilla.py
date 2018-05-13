# -*- coding: utf-8 -*-
"""
Used to download comic automatically from animezilla

@author: Geminii
"""
import urllib.request
import os
import sys
from bs4 import BeautifulSoup

CONFIG_OUTDIR = 'download'

COMIC_INFOS = [
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/3286",
        'NAME': '[星野竜一] 牝妻/母豬人妻',
        'DIR': '[星野竜一]牝妻母豬人妻',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/2946",
        'NAME': '[山本同人] TWO PIECE ナミVSアーロン/TWO PIECE 娜美VS惡龍船長 (海賊王)',
        'DIR': '[山本同人]TWO PIECE 娜美VS惡龍船長 (海賊王)',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/1094",
        'NAME': '[星野竜一] 家庭教師が堕ちるまで/家庭教師她墮落了為止',
        'DIR': '[星野竜一] 家庭教師她墮落了為止',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/3218",
        'NAME': '[舞六まいむ] 女教師と僕の秘密/女教師與我的秘密',
        'DIR': '[舞六まいむ] 女教師與我的秘密',
        'ENABLE': True,
    },
]

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"

# obtained from Chrome Dev Tools
img_req_header = {
    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6",
    "Cache-Control": "no-cache",
    "DNT": "1",
    "Host": "m.iprox.xyz",
    "Pragma": "no-cache",
    "Proxy-Connection": "keep-alive",
    "Referer": "TO BE ADDED RUNTIME",
    "User-Agent": USER_AGENT,
}

# check the basic downloading directory
if os.path.exists(CONFIG_OUTDIR):
    if not os.path.isdir(CONFIG_OUTDIR):
        print("[ERR]download location is not dir")
        sys.exit(1)
else:
    print("creating downloading folder for the 1st time.")
    os.mkdir(CONFIG_OUTDIR)


for comic in COMIC_INFOS:
    print('Crawling for Comic {}..'.format(comic['NAME']), end='')

    if comic['ENABLE'] == False:
        print('[SKIP]')
        continue
    print('')

    # check the comic's downloading directory
    comic_dirpath = CONFIG_OUTDIR + '/' + comic['DIR']
    if not os.path.exists(comic_dirpath):
        print("creating dir for comic..")
        os.mkdir(comic_dirpath)

    total_page_number = 0
    page_number = 0
    nextpage_url = comic['HOMEPAGE_URL']  # use 1st page as a start

    # Keep working until we find the last page.
    while (nextpage_url != "") and (nextpage_url is not None):
        page_number += 1
        current_page_url = nextpage_url

        if total_page_number == 0:
            print("Fetching Home Page...")
        else:
            print("({}/{})Fetching Page...".format(
                page_number, total_page_number), end='')

        page_resp = urllib.request.urlopen(current_page_url)
        if (page_resp.status != 200):
            print("[ERROR]:Request comic page {}, respcode={}, abort..".format(
                page_number, page_resp.status))
            break  # break for continuing on next comic

        # Get the HTML Content
        page_html_raw = page_resp.read()  # get the home page html
        page_soup = BeautifulSoup(page_html_raw, 'html.parser')

        # Get the total page number
        if total_page_number == 0:
            pagenavi_tag = page_soup.find(
                'div', 'wp-pagenavi').find('a', 'last')
            total_page_number = int(pagenavi_tag.get('href').split('/')[-1])

        # Is this a last page?
        nextpage_tag = page_soup.find('a', 'nextpostslink')
        nextpage_url = ""
        if nextpage_tag is not None:
            nextpage_url = nextpage_tag.get('href')

        # Get Image address & Image file name
        img_url = page_soup.find('img', id='comic').get('src')
        img_filename_remote = img_url.split('/')[-1]
        img_file_ext = img_filename_remote.split('.')[-1]
        img_filename = str(page_number) + '.' + img_file_ext
        img_filepath = comic_dirpath + '/' + img_filename

        # Check if the file already exists
        if os.path.exists(img_filepath):
            print('[SKIP], file exists..')
            continue
        print('')

        # Request Image Content
        print("Fetching Image from {}..".format(img_url), end='')
        img_req_header['Referer'] = current_page_url
        img_req = urllib.request.Request(
            img_url, headers=img_req_header, method='GET')
        img_resp = urllib.request.urlopen(img_req)
        if (img_resp.status != 200):
            print("[ERROR]:Request image, page {}, respcode={}, abort..".format(
                page_number, page_resp.status))
            continue
        print('')

        # read & write image content into file
        print("Saving Img into {}..".format(img_filepath))
        img_data = img_resp.read()
        try:
            with open(img_filepath, 'wb') as img_file:
                img_file.write(img_data)
        except Exception as e:
            print("[ERROR]write file exception:{}".format(e))
