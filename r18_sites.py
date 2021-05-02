"""R18 comic spider supportted sites information module.
"""
# Imports: builtin, 3rd-party, local
import enum
import typing
import re
from typing import Union
from bs4 import BeautifulSoup

# Module authorshipt information
__author__ = "Geminii"
__copyright__ = "None"
__license__ = "check repo's standalone license file"


class Site:
    """Base class for r18 comic sites.
    
    This class is designed as an abstract class, for define a common interface for different sites.
    """

    def __init__(self) -> None:
        pass

    @classmethod
    def homepage(cls) -> tuple:
        """Get all available and supported homepage URLs of current site.
        
        Returns: collection of homepage URLs.
        """
        raise NotImplementedError("Subclass must implement this")

    @classmethod
    def comic_names(cls, homepage_data: BeautifulSoup) -> list:
        """Get All available comic's name from its front page.
        
        Args:
            homepage_data: The homepage data processed by `BeautifulSoup()`

        Returns: Comic's name and languange. 
            Format: {'name': 'str', 'lang': 'en/ch/jp/und'}, {...}
                lang: en -> english, ch -> chinese, jp -> japanese, und -> undefined
            Sequence: main title has higher priority.
        """
        raise NotImplementedError("Subclass must implement this")

    @classmethod
    def comic_page_count(cls, homepage_data: BeautifulSoup) -> int:
        """Get comic total page count.

        Args:
            homepage_data: The homepage data processed by `BeautifulSoup()`

        Returns: comic total page count.
        """
        raise NotImplementedError("Subclass must implement this")

    @classmethod
    def comic_page_urls(cls, comic_url: str, homepage_data: BeautifulSoup) -> list:
        """Get comic all pages' URLs.
        
        Args:
            comic_url: The homepage URL of comic.`
            homepage_data: The homepage data processed by `BeautifulSoup()`

        Returns: comic all pages' URLs.
        """
        raise NotImplementedError("Subclass must implement this")

    @classmethod
    def comic_page_url(
        cls, comic_url: str, page_index: int, homepage_data: BeautifulSoup
    ) -> str:
        """Get comic page's URL.
        
        Args:
            comic_url: The homepage URL of comic.`
            page_index: The 0-based comic page index.
            homepage_data: The homepage data processed by `BeautifulSoup()`

        Returns: The specified comic page's URL.
        """
        raise NotImplementedError("Subclass must implement this")

    @classmethod
    def comic_img_info(cls, page_index: int, page_bs: BeautifulSoup) -> dict:
        """Get image information in specified comic page.
        
        Args:
            page_index: The 0-based comic page index.
            page_bs: The image page data processed by `BeautifulSoup()`

        Returns: Comic image's information. 
            Format: {"url": url, "ext": fileext, "name": filename}
                url: Image's URL.
                ext: Image file extension.
                filename: Image filename(with extension)
        """
        raise NotImplementedError("Subclass must implement this")


class nhentai(Site):
    """Class of Site nhentai"""

    HOMEPAGES = "https://nhentai.net"
    """All available and supportted homepage URLs"""

    def __init__(self):
        super.__init__()

    @classmethod
    def homepage(cls) -> tuple:
        return tuple(cls.HOMEPAGES)

    @classmethod
    def comic_names(cls, homepage_data: BeautifulSoup):
        ret = []
        info_tag = homepage_data.find("div", id="info")

        # 1st title, can be any language
        ret.append({"name": info_tag.h1.getText(), "lang": "UND"})

        # 2nd title, may not exist.
        try:
            ret.append({"name": info_tag.h2.getText(), "lang": "UND"})
        except AttributeError:
            pass

        return ret

    @classmethod
    def comic_page_count(cls, homepage_data: BeautifulSoup) -> int:
        return len(homepage_data.find("div", {"class": "thumbs"}).contents)

    @classmethod
    def comic_page_urls(cls, comic_url: str, homepage_data: BeautifulSoup) -> list:
        page_count = cls.comic_page_count(homepage_data)
        urls_list = []
        page_index = 0

        while page_index < page_count:
            urls_list.append(cls.comic_page_url(comic_url, page_index, homepage_data))
            page_index += 1

        return urls_list

    @classmethod
    def comic_page_url(
        cls, comic_url: str, page_index: int, homepage_data: BeautifulSoup
    ) -> str:
        # arguments invalidation
        if page_index < 0:
            page_index = 0

        # # Get 1st page relative URL: something like /g/123456/1/
        # url = homepage_data.find("div", id="cover").a.get("href")
        # if page > 0:
        #     url = url[:-2] + str(page + 1) + "/"  # page num 0-based to 1-based

        # Page URL is HomePage URL + "/page/"
        # e.g. nhentai.net/g/123456 -> nhentai.net/g/123456/1/
        return comic_url + str(page_index + 1) + "/"  # page num 0-based to 1-based

    @classmethod
    def comic_img_info(cls, page_index: int, page_bs: BeautifulSoup) -> dict:
        url = page_bs.find("section", id="image-container").a.img.get("src")
        fileext = url.split(".")[-1]
        filename = str(page_index + 1) + "." + fileext  # use 1-base page number
        return {"url": url, "ext": fileext, "name": filename}


def get_class(url: str) -> Union[Site, None]:
    pattern = re.compile(r"nhentai.")
    if pattern.search(url) is not None:
        return nhentai
    return None
