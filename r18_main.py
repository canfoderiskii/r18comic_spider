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
import http.client
from bs4 import BeautifulSoup

# local imports
import r18_comics as comics
import r18_sites as sites
import r18_core as core

CONFIG_OUTDIR = "download1"  # Downloader output directory

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"

URL_RETRY_LIMIT = 20  # Retry Max Count

# obtained from Chrome Dev Tools
# "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
IMG_REQ_HEADER = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6",
    "Cache-Control": "max-age=0",
    # "Cookie": "__cfduid=d5502268083fd2569821ec4c403893df91572661861",
    "DNT": "1",
    "upgrade-insecure-requests": "1",
    # "Pragma": "no-cache",
    "Referer": "TO BE ADDED RUNTIME",
    "User-Agent": USER_AGENT,
}

Error_count = 0

# Local Proxy Settings
proxy_support = urllib.request.ProxyHandler(
    {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
)
opener = urllib.request.build_opener(proxy_support)
urllib.request.install_opener(opener)

# check the basic downloading directory
if os.path.exists(CONFIG_OUTDIR):
    if not os.path.isdir(CONFIG_OUTDIR):
        print("[ERR]download location is not dir")
        sys.exit(1)
else:
    print("creating downloading folder for the 1st time.")
    os.mkdir(CONFIG_OUTDIR)


for c in comics.COMIC_INFOS:
    # Check if current comic is skipped.
    if c["SKIP"] is True:
        continue

    # Get Home Page URL infomation
    comic_url = c["URL"]
    print("Crawling {}..".format(comic_url))

    # Get correct comic site process class.
    site = sites.get_class(comic_url)
    if site is None:
        print("[ERR]site class not found, abort")
        break

    # construct Home Page request
    homepage_req = urllib.request.Request(
        comic_url, headers={"Referer": comic_url, "User-Agent": USER_AGENT,}
    )

    # Fetch the homepage
    retry = URL_RETRY_LIMIT
    while retry:
        try:
            homepage_resp = urllib.request.urlopen(homepage_req)
            if homepage_resp.status == 200:
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
    homepage_soup = BeautifulSoup(homepage_html_raw, "html.parser")
    homepage_soup.prettify()  # translate unicode string

    # Find Comic Nmae
    comic_names = site.comic_names(homepage_soup)
    if len(comic_names) < 1:
        print("[ERR]No name is found, abort.")
        break

    # Find comic total page count
    comic_page_count = site.comic_page_count(homepage_soup)

    # Comic downloading dir: use 1st comic name as default dir name
    comic_dirname = comic_names[0]["name"]
    # Get rid of invalid OS path characters
    # NOTE: successive dots(.) shall be deleted, or path is erroneous on Windows.
    regex_pattern = r'([\\/:|*?<>,"])|(\.+)'
    if re.search(regex_pattern, comic_dirname) is not None:
        comic_dirname = re.sub(regex_pattern, "", comic_dirname)
        print("[WARN]replaced invalid chars, new dirname: {}..".format(comic_dirname))
    comic_dirpath = CONFIG_OUTDIR + "/" + comic_dirname
    if not os.path.exists(comic_dirpath):
        print("creating dir..")
        os.mkdir(comic_dirpath)

    # Count downloaded images.
    downloaded_imgcount = core.count_downloaded_img(comic_dirpath)
    if downloaded_imgcount >= comic_page_count:
        print("[SKIP], all image downloaded already..")
        continue

    # Save Comic infomation into a dedicated file
    comic_localinfo = {
        "Name1": comic_names[0]["name"],
        "Pages": str(comic_page_count),
        "Src": comic_url,
        "UpdateTime": str(datetime.datetime.now()),
    }
    if len(comic_names) > 1:
        comic_localinfo["Name2"] = comic_names[1]["name"]
    comic_localinfo_filepath = comic_dirpath + "/info.json"
    with open(comic_localinfo_filepath, "w", encoding="utf-8") as f:
        f.write(json.dumps(comic_localinfo, sort_keys=True, indent=2))

    # Fetch all pages' URLs
    page_urls = site.comic_page_urls(comic_url, homepage_soup)

    print("")  # new line

    # Select start page
    page_start_index = core.get_page_start_index(c)

    # Keep working until we find the last page.
    for page_index in range(page_start_index, comic_page_count):
        page_num = page_index + 1  # page number, 1-based
        print("({}/{})Fetching Page...".format(page_num, comic_page_count), end="")

        # Get current comic page URL
        page_url = page_urls[page_index]

        retry = URL_RETRY_LIMIT
        while retry:
            try:
                page_req = urllib.request.Request(
                    page_url, headers={"Referer": page_url, "User-Agent": USER_AGENT,},
                )

                # Get the page content
                page_resp = urllib.request.urlopen(page_req)
                if page_resp.status == 200:
                    break
            except (
                urllib.error.HTTPError,
                urllib.error.URLError,
                ConnectionResetError,
            ):
                retry -= 1
                if retry:
                    print("Retry..")
                    continue
                else:
                    raise
            else:
                break

        # Get the HTML Content & Necessary Info
        page_html_raw = page_resp.read()  # get the home page html
        page_soup = BeautifulSoup(page_html_raw, "html.parser")

        img_info = site.comic_img_info(page_index, page_soup)
        img_url = img_info["url"]
        img_filepath = comic_dirpath + "/" + img_info["name"]

        # Check if the file already exists
        if os.path.exists(img_filepath):
            print("[SKIP], file exists..")
            continue
        print("")

        # Request Image Content
        print("Fetching Image from {}..".format(img_url), end="")
        IMG_REQ_HEADER["Referer"] = page_url
        img_data = bytearray()

        retry = URL_RETRY_LIMIT
        while retry:
            try:
                img_req = urllib.request.Request(
                    img_url, headers=IMG_REQ_HEADER, method="GET"
                )
                img_resp = urllib.request.urlopen(img_req)
                if img_resp.status != 200:
                    print("Img Respond != 200, Retry...")
                    continue
            except (
                urllib.error.HTTPError,
                urllib.error.URLError,
                ConnectionResetError,
            ):
                retry -= 1
                if retry:
                    print("Retry..")
                    continue
                else:
                    raise

            # request action is completed here.
            print("")

            # read & write image content into file
            print("Read HTTP respond..")

            try:
                img_data = img_resp.read()
            except http.client.IncompleteRead:
                retry -= 1
                if retry:
                    print("Request Again..")
                    continue
                else:
                    raise
            else:
                break

        print("Saving Img into {}..".format(img_filepath))
        with open(img_filepath, "wb") as img_file:
            img_file.write(img_data)

    # All images are downloaded or skipped without exception raised

if Error_count:
    print("[NOTICE]Total Error Count = {}".format(Error_count))
