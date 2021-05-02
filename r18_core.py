# -*- coding: utf-8 -*-
"""R18 comic spider core logic, utility, etc..
"""
# Imports: builtin, 3rd-party, local
import os
import re
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
        if (page_num < 1):
            page_num = 1
            print("[WARN]Start page number invalid, corrected.")

        page_index = page_num - 1  # change to 0-based

    return page_index
