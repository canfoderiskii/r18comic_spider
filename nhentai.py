# -*- coding: utf-8 -*-
"""
Used to download comic automatically from nhentai.net

@author: Geminii
"""
import urllib.request
import os
import sys
import re
import datetime
import json
import fnmatch
from bs4 import BeautifulSoup

CONFIG_OUTDIR = 'download'

COMICSITE_HOMEPAGE = "https://nhentai.net"

COMIC_INFOS = [{
    'HOMEPAGE_URL': "https://nhentai.net/g/62579/",
    'ENABLE': True,
}
]

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"

URL_RETRY_LIMIT = 5

# obtained from Chrome Dev Tools
IMG_REQ_HEADER = {
    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6",
    "Cache-Control": "no-cache",
    # "Cookie": "__cfduid = de7cd5643e91352477018f4cfb6e70c5f1521986530",
    "DNT": "1",
    "Pragma": "no-cache",
    "Referer": "TO BE ADDED RUNTIME",
    "User-Agent": USER_AGENT,
}

Error_count = 0

# check the basic downloading directory
if os.path.exists(CONFIG_OUTDIR):
    if not os.path.isdir(CONFIG_OUTDIR):
        print("[ERR]download location is not dir")
        sys.exit(1)
else:
    print("creating downloading folder for the 1st time.")
    os.mkdir(CONFIG_OUTDIR)


for c in COMIC_INFOS:
    homepage_url = c['HOMEPAGE_URL']
    print('Crawling {}..'.format(homepage_url), end='')

    if c['ENABLE'] == False:
        print('[SKIP]')
        continue
    print('')

    # PAGE_REQ_HEADER['Referer'] = homepage_url
    homepage_req = urllib.request.Request(homepage_url, headers={
        "Referer": homepage_url,
        "User-Agent": USER_AGENT,
    })

    # Fetch the homepage
    retry = URL_RETRY_LIMIT
    while retry:
        try:
            homepage_resp = urllib.request.urlopen(homepage_req)
            if (homepage_resp.status == 200):
                break
        except urllib.error.HTTPError:
            retry -= 1
            if retry:
                print("Retry..")
                continue
            else:
                raise

    # Homepage is fetched & get the comic information
    homepage_html_raw = homepage_resp.read()
    homepage_soup = BeautifulSoup(homepage_html_raw, 'html.parser')

    info_tag = homepage_soup.find('div', id='info')
    c['NAME_EN'] = info_tag.h1.getText()
    c['NAME_JP'] = info_tag.h2.getText()
    c['PAGES'] = int(info_tag.find('div', text=re.compile(
        'pages')).getText().replace('pages', ''))

    # determine downloading directory
    c['DIRNAME'] = c['NAME_EN']  # use the english name only
    comic_dirpath = CONFIG_OUTDIR + '/' + c['DIRNAME']
    if not os.path.exists(comic_dirpath):
        print("creating dir..")
        os.mkdir(comic_dirpath)

    # check download count by comparing the file count with page count
    downloaded_imgcount = len(fnmatch.filter(
        os.listdir(comic_dirpath), '*.jpg'))
    if downloaded_imgcount >= c['PAGES']:
        print("[SKIP], all image downloaded already..")
        continue

    # Save Comic infomation into a dedicated file
    comic_localinfo = {
        "Name": c['NAME_EN'] + " " + c['NAME_JP'],
        "Pages": str(c['PAGES']),
        "Src": homepage_url,
        "UpdateTime": str(datetime.datetime.now()),
    }
    comic_localinfo_filepath = comic_dirpath + "/info.json"
    with open(comic_localinfo_filepath, 'w', encoding="utf-8") as f:
        f.write(json.dumps(comic_localinfo, sort_keys=True, indent=2))

    # get the 1st comic page as a start
    page = 0
    nextpage_rel_url = homepage_soup.find('div', id='cover').a.get('href')
    nextpage_url = COMICSITE_HOMEPAGE + nextpage_rel_url

    # Keep working until we find the last page.
    while (nextpage_url != "") and (nextpage_url is not None):
        page += 1
        current_page_url = nextpage_url
        print("({}/{})Fetching Page...".format(page, c['PAGES']), end='')

        page_req = urllib.request.Request(current_page_url, headers={
            "Referer": current_page_url,
            "User-Agent": USER_AGENT,
        })

        # Get the page content with retry
        retry = URL_RETRY_LIMIT
        while retry:
            try:
                page_resp = urllib.request.urlopen(page_req)
                if (page_resp.status == 200):
                    break
            except urllib.error.HTTPError:
                retry -= 1
                if retry:
                    print("Retry..")
                    continue
                else:
                    raise

        # Get the HTML Content & Necessary Info
        page_html_raw = page_resp.read()  # get the home page html
        page_soup = BeautifulSoup(page_html_raw, 'html.parser')

        img_url = page_soup.find(
            'section', id='image-container').a.img.get('src')
        img_file_ext = img_url.split('.')[-1]
        img_filename = str(page) + '.' + img_file_ext
        img_filepath = comic_dirpath + '/' + img_filename

        # last page's section class is 'next invisible', so the find() has
        # result as well, but it don't have any link.
        nextpage_tag = page_soup.find(
            'section', id='pagination-page-top').find('a', 'next')
        nextpage_rel_url = nextpage_tag.get('href')
        if nextpage_rel_url is not None:
            nextpage_url = COMICSITE_HOMEPAGE + nextpage_rel_url
        else:
            nextpage_url = ""

        # Check if the file already exists
        if os.path.exists(img_filepath):
            print('[SKIP], file exists..')
            continue
        print('')

        # Request Image Content
        print("Fetching Image from {}..".format(img_url), end='')
        IMG_REQ_HEADER['Referer'] = current_page_url
        img_req = urllib.request.Request(
            img_url, headers=IMG_REQ_HEADER, method='GET')

        retry = URL_RETRY_LIMIT
        while retry:
            try:
                img_resp = urllib.request.urlopen(img_req)
                if (img_resp.status == 200):
                    break
            except urllib.error.HTTPError:
                retry -= 1
                if retry:
                    print("Retry..")
                    continue
                else:
                    raise
        print('')

        # read & write image content into file
        print("Saving Img into {}..".format(img_filepath))
        img_data = img_resp.read()
        with open(img_filepath, 'wb') as img_file:
            img_file.write(img_data)

    # All images are downloaded or skipped without exception raised


if Error_count:
    print("[NOTICE]Total Error Count = {}".format(Error_count))
