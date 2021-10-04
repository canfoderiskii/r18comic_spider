# -*- coding: utf-8 -*-
"""R18 comic spider core logic, utility, etc..
"""
# Imports: builtin, 3rd-party, local
import urllib.request
import os
import re
import http.client
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


def request_parse_url(url: str, reqhdr: dict, retry_count: int) -> BeautifulSoup:
    # prepare request header. Do copy because we do some runtime tweaks here.
    reqhdr_r = reqhdr.copy()
    reqhdr_r["Referer"] = url

    # construct page request
    page_req = urllib.request.Request(url, headers=reqhdr_r)
    # page_req = urllib.request.Request(
    #     url, headers={"Referer": url, "User-Agent": reqhdr_r["User-Agent"],}
    # )

    # open target URL
    retry = retry_count
    while retry:
        try:
            page_resp = urllib.request.urlopen(page_req)
            if page_resp.status == 200:
                break
        except (
            urllib.error.HTTPError,
            urllib.error.URLError,
            http.client.RemoteDisconnected
        ):
            retry -= 1
            if retry:
                print("Retry..")
                continue
            else:
                raise  # if error, raise directly to abort program.

    # Parse the page
    page_html_raw = page_resp.read()
    page_soup = BeautifulSoup(page_html_raw, "html.parser")
    page_soup.prettify()  # translate unicode string

    return page_soup
