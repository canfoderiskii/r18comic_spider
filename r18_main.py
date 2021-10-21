# -*- coding: utf-8 -*-
"""
Used to download comic automatically from r18 comic site

@author: Geminii
"""
import os
import sys
import re
import datetime
import json
import time
import http.client
import urllib.request
import ssl
import urllib3
import certifi
import requests

# local imports
import r18_comics as comics
import r18_sites as sites
import r18_core as core

# 默认下载路径
CONFIG_OUTDIR = "download"

# 默认代理设置
PROXY = {"http": "127.0.0.1:7890", "https": "127.0.0.1:7890"}

# URL 访问使用的 User Agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"

TOPLOOP_RETRY_CNT = 5
URL_RETRY_LIMIT = 20  # Retry Max Count
IMGREQ_TIMEOUT = 15

# Basic page request header
# obtained from Chrome Dev Tools
REQHDR_PAGE_BASE = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6",
    "Cache-Control": "max-age=0",
    "Cookie": "skipserver=38143-18924; nw=1; tagaccept=1",
    # "Cookie": "__cfduid=d0700503b82f0b4aeba97f313d0fb0fc41619918416; nw=1",
    # "Cookie": "skipserver=36477-18910_31269-18907_30703-18907; nw=1; tagaccept=1",
    "Connection": "keep-alive",
    "DNT": "1",
    "upgrade-insecure-requests": "1",
    "Referer": "",  # ADD RUNTIME
    "User-Agent": USER_AGENT,
}

# Basic image request header
# obtained from Chrome Dev Tools
REQHDR_IMG_BASE = {
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "DNT": "1",
    "upgrade-insecure-requests": "1",
    "Pragma": "no-cache",
    "Referer": "",  # ADD RUNTIME
    # "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Dest": "image",
    # "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "cross-site",
    # "Sec-Fetch-User": "?1",
    "User-Agent": USER_AGENT,
}
REQHDR_IMG_BASE = {
    "User-Agent": USER_AGENT,
}


def download(ssl_ctx: ssl.SSLContext) -> None:
    """Comic download core."""

    with requests.Session() as session:  # initial session via context manager
        session.proxies.update(PROXY)  # configure proxy for entire session
        session.trust_env = False

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

            # init Headers
            pagehdr = REQHDR_PAGE_BASE
            pagehdr["Referer"] = comic_url

            # init site class
            site.url_req_retrycount = URL_RETRY_LIMIT
            site.reqhdr_page = pagehdr
            site.reqhdr_image = REQHDR_IMG_BASE
            site.s = session

            # open & parse Home page
            homepage_soup = site.comic_page_open(comic_url)
            time.sleep(0.5)

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
                print("[WARN]replaced invalid chars, new dirname:", comic_dirname)
            comic_dirpath = CONFIG_OUTDIR + "/" + comic_dirname
            if not os.path.exists(comic_dirpath):
                print("creating dir..")
                os.mkdir(comic_dirpath)

            # Count downloaded images.
            if core.count_downloaded_img(comic_dirpath) >= comic_page_count:
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

            # display comic name, after URL.
            print("Comic Name:", comic_names[0]["name"])

            # Fetch all pages' URLs
            page_urls = site.comic_page_urls(comic_url, homepage_soup)
            # Select start page
            page_start_index = core.get_page_start_index(c)

            # Keep working until we find the last page.
            for page_index in range(page_start_index, comic_page_count):
                page_num = page_index + 1  # page number, 1-based
                print(
                    "({}/{})Fetching Page...".format(page_num, comic_page_count), end=""
                )

                # Get current comic page URL
                page_url = page_urls[page_index]

                # open & parse image page
                page_soup = core.request_parse_url(
                    site.s, site.reqhdr_page, page_url, site.url_req_retrycount,
                )
                time.sleep(0.5)
                # print(page_soup)

                img_info = site.comic_img_info(page_index, page_soup)
                img_url = img_info["url"]
                img_filepath = comic_dirpath + "/" + img_info["name"]

                # Check if the file already exists & valid
                if os.path.exists(img_filepath):
                    if os.path.getsize(img_filepath) > 0:
                        print("[SKIP]file exists & valid..")
                        continue
                    else:  # file invalid
                        os.remove(img_filepath)
                        print("[WARN]del invalid file")
                print("")

                # Request Image Content
                print("Fetching Image from {} ..".format(img_url))
                img_url_s = img_url.split("://")

                reqhdr_r = site.reqhdr_image.copy()
                reqhdr_r["Referer"] = page_url
                reqhdr_r["Host"] = img_url_s[0] + "://" + img_url_s[1].split("/")[0]

                # Here, use urllib instead of requests, because I always get an error
                # message like this:
                # requests.exceptions.ConnectTimeout: HTTPSConnectionPool(host='xxx.xxx.xxx', port=443):
                # Max retries exceeded with url: /xxx/xxx/1.jpg (Caused by ConnectTimeoutError
                # (<urllib3.connection.HTTPSConnection object at 0x0000016699F1D610>,
                # 'Connection to xxx.xxx.xxx timed out. (connect timeout=5)'))
                retry = URL_RETRY_LIMIT
                timeout = IMGREQ_TIMEOUT
                while retry:
                    try:
                        img_req = urllib.request.Request(
                            img_url, headers=reqhdr_r, method="GET",
                        )

                        with urllib.request.urlopen(
                            img_req, context=ssl_ctx, timeout=timeout,
                        ) as img_resp:
                            img_data = img_resp.read()

                            print("Saving Img into {}..".format(img_filepath))
                            with open(img_filepath, "wb") as img_file:
                                img_file.write(img_data)
                                break  # image file is written, abort retry loop
                    except (
                        urllib.error.HTTPError,
                        urllib.error.URLError,
                        ConnectionResetError,
                        http.client.IncompleteRead,
                    ) as e:
                        print(e, "", end="")

                        retry -= 1
                        timeout += 0.5
                        if retry:
                            print("Request Again, next timeout {}sec..".format(timeout))
                            continue
                        else:
                            raise
                continue  # skip codes below

                # request image with try
                # retry = URL_RETRY_LIMIT
                # while retry:
                #     try:
                #         # resp = requests.get(img_url, headers=reqhdr_r, timeout=5, verify=False, proxies=PROXY)
                #         resp = site.s.get(img_url, headers=reqhdr_r, timeout=5)
                #         if (not resp.ok) and resp.status_code != 200:
                #             print("respond not ok, status code:", resp.status_code)

                #             # manually raise to make sure exception catch logic will
                #             # be executed, even if the requests's exception is not
                #             # triggerred.
                #             raise resp.raise_for_status()
                #     except (
                #         KeyboardInterrupt,
                #         requests.exceptions.ConnectionError,
                #         requests.exceptions.ProxyError,
                #         requests.exceptions.SSLError,
                #     ):
                #         # if trial count still remains, continue to retry, otherwise,
                #         # expetion is raised up again.
                #         retry -= 1
                #         if retry:
                #             print("Request Again..")
                #             continue  # next trial
                #         else:
                #             raise

                # # save image file into downloader dir.
                # print("Saving Img into {}..".format(img_filepath))
                # with open(img_filepath, "wb") as img_file:
                #     img_file.write(resp.content)

            # All images are downloaded or skipped without exception raised


if __name__ == "__main__":
    urllib3.disable_warnings()

    sslctx = ssl._create_unverified_context()
    # sslctx = ssl._create_default_https_context()
    # sslctx = ssl.create_default_context(cafile=certifi.where())

    # urllib: Local Proxy Settings
    urllib.request.install_opener(
        urllib.request.build_opener(urllib.request.ProxyHandler(PROXY))
    )

    # check the basic downloading directory
    if os.path.exists(CONFIG_OUTDIR):
        if not os.path.isdir(CONFIG_OUTDIR):
            print("[ERR]download location is not dir")
            sys.exit(1)
    else:
        print("creating downloading folder for the 1st time.")
        os.mkdir(CONFIG_OUTDIR)

    retry = TOPLOOP_RETRY_CNT
    while retry:
        try:
            download(sslctx)
        except:
            retry -= 1
            if retry:
                print("Try Download Again, {} remaining..".format(retry))

                if (retry & 1) == 0:
                    sslctx = ssl._create_default_https_context()
                else:
                    sslctx = ssl._create_unverified_context()

                continue  # next trial

            raise
