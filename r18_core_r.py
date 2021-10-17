# -*- coding: utf-8 -*-
"""R18 comic spider core logic, utility, etc..
"""
# Imports: builtin, 3rd-party, local
import os
import re
import requests
from bs4 import BeautifulSoup

# Module authorshipt information
__author__ = "Geminii"
__copyright__ = "None"
__license__ = "check repo's standalone license file"


def count_downloaded_img(path: str):
    IMG_FILES = re.compile("|".join([r"(.*\.jpg)", r"(.*\.jpeg)", r"(.*\.png)",]))
    count = 0

    for i in os.listdir(path):
        if IMG_FILES.match(i) is not None:
            count += 1

    return count


def get_page_start_index(comics: list) -> int:
    page_index = 0
    if "PAGE_START" in comics:
        # argument checking
        page_num = comics["PAGE_START"]
        if page_num < 1:
            page_num = 1
            print("[WARN]Start page number invalid, corrected.")

        page_index = page_num - 1  # change to 0-based

    return page_index


def request_parse_url(
    s: requests.Session, reqhdr: dict, url: str, retry_count: int
) -> BeautifulSoup:
    """Send request to URL, get reponse, parse HTML using BS4.

    Args:
        s: Connection session with prepared request class.
        preqreq: Prepared request data.
        url: URL. (NOT USED)
        retry_count: retry count.

    Returns: parsed reponse HTML data.
    """

    # prepare request header. Do copy because we do some runtime tweaks here.
    reqhdr_r = reqhdr.copy()
    reqhdr_r["Referer"] = url

    # open target URL
    retry = retry_count
    while retry:
        try:
            # resp = s.send(prepreq, timeout=10)
            resp = s.get(url, headers=reqhdr_r, timeout=10)
            if resp.ok:
                break
        except:
            retry -= 1
            if retry:
                print("Retry..")
                continue

    # Parse the page
    page_soup = BeautifulSoup(resp.content, "html.parser")
    page_soup.prettify()  # translate unicode string
    # print(page_soup)

    return page_soup
