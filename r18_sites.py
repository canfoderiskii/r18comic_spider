"""R18 comic spider supportted sites information module.
"""
# Imports: builtin, 3rd-party, local
import re
import time
from typing import Union
import requests
from bs4 import BeautifulSoup

# local imports
import r18_core as core

# Module authorshipt information
__author__ = "Geminii"
__copyright__ = "None"
__license__ = "check repo's standalone license file"


class Site:
    """Base class for r18 comic sites.
    
    This class is designed as an abstract class, for define a common interface for different sites.
    """

    url_req_retrycount = 5
    """URL requset retry count on error."""

    reqhdr_page = dict()
    """Request header for page.

    NOTE: some site subclass needs this to be initialized.

    Format Example: {
        "Accept": str,
        "Accept-Encoding": str,
        "Accept-Language": str,
        "Referer": str,
        "User-Agent": str,
    }
    """

    reqhdr_image = dict()
    """Request header for image."""

    s: requests.Session = None
    """Request session for requests module."""

    prepreq: requests.PreparedRequest = None
    """NOT USED"""

    def __init__(self) -> None:
        pass

    @classmethod
    def _img_url2info(cls, img_url: str, page_index: int) -> dict:
        fileext = img_url.split(".")[-1]
        filename = str(page_index + 1) + "." + fileext  # use 1-base page number
        return {"url": img_url, "ext": fileext, "name": filename}

    @classmethod
    def comic_page_open(cls, url: str) -> BeautifulSoup:
        """Open comic home page.

        Args:
            url: Comic HomePage URL.

        Returns: processed homepage data.
        """

        # NOTE: if `PAGE_REQ_HEADER` is used as a whole in `request_parse_url()`,
        # e-hentai page cannot be accessed & decoded normally.
        page_bs = core.request_parse_url(
            cls.s, cls.reqhdr_page, url, cls.url_req_retrycount,
        )
        return page_bs

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

    HOMEPAGE = "https://nhentai.net"
    """All available and supportted homepage URLs"""

    def __init__(self):
        super.__init__()

    @classmethod
    def comic_names(cls, homepage_data: BeautifulSoup) -> list:
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
    def comic_page_url(
        cls, comic_url: str, page_index: int, homepage_data: BeautifulSoup
    ) -> str:
        # arguments invalidation
        if page_index < 0:
            page_index = 0

        # Page URL is HomePage URL + "/page/"
        # e.g. nhentai.net/g/123456 -> nhentai.net/g/123456/1/
        return comic_url + str(page_index + 1) + "/"  # page num 0-based to 1-based

    @classmethod
    def comic_img_info(cls, page_index: int, page_bs: BeautifulSoup) -> dict:
        url = page_bs.find("section", id="image-container").a.img.get("src")
        return cls._img_url2info(url, page_index)


class ehentai(Site):
    """Class of Site e-hentai
    
    e-hentai is more complicated than nhentai, because we cannot simply add sequence
    string to the end of comic home page URL to get the image page URL. And it has
    thumb page turning function via mouse clicking.

    For example:
    - Home page(Thumb Page 1) URL: https://e-hentai.org/g/1901092/90d1410d1b/
    - Thumb page 2 URL: https://e-hentai.org/g/1901092/90d1410d1b/?p=1
    - Image Page URL: https://e-hentai.org/s/SomeKindHash/1901092-{IMG}
    - Image URL: get from Image Page.

    Some comic page has a warning page before into comic homepage, so a mouse click
    simulation is needed.
    """

    HOMEPAGES = "https://e-hentai.org"
    """All available and supportted homepage URLs"""

    def __init__(self):
        super.__init__()

    @classmethod
    def _warnpage_is_provided(cls, homepage_data: BeautifulSoup) -> bool:
        s = str(homepage_data)
        if "Warning" in s:  # Full title: Content Warning
            return True
        return False

    @classmethod
    def _thumb_page_count(cls, homepage_data: BeautifulSoup) -> int:
        """Get thumb images page count.

        NOTE: Image page URLs are not sequenced. I need to collect the info from
        the thumb image page, which is also the front page if the thumb page is
        the first one.

        Args:
            homepage_data: The homepage data processed by `BeautifulSoup()`

        Returns: Thumb page count.
        """
        count = 0

        # use page control table in HTML to calculate.
        t = homepage_data.find("table", {"class": "ptt"})
        td = t.find_all("td", {"onclick": "document.location=this.firstChild.href"})
        elem_count = len(td)

        if elem_count < 1:  # single thumb page
            count = 1
        else:  # multiple thumb pages
            # The button left of '>' is the last thumb page. And the element's
            # text content is the last page number (1-based), which is also the
            # thumb page count.
            count = int(td[-2].get_text())
        return count

    @classmethod
    def _thumb_page_1st_img_index(cls, thumbpage_data: BeautifulSoup) -> int:
        """Get first image index from current specified thumb page.

        Args:
            homepage_data: The homepage data processed by `BeautifulSoup()`

        Returns: 1st image 0-based index of current thumb page.
        """
        imgpage_1st_url = (
            thumbpage_data.find("div", {"class": "gdtm"}).find("a").get("href")
        )
        img_index = len(imgpage_1st_url.split(" ")[-1]) - 1  # 1-based to 0-based
        return img_index

    @classmethod
    def _thumb_page_img_count(cls, thumbpage_data: BeautifulSoup) -> int:
        """Get the count of thumb images from current thumb page.
        
        Returns: (thumb) image count contained by current thumb page.
        """
        return len(
            thumbpage_data.find("div", id="gdt").find_all("div", {"class": "gdtm"})
        )

    @classmethod
    def _thumb_page_url(cls, comic_url: str, page_index: int) -> str:
        """Get thumb page URL, simply according to index and homepage.
        
        Returns: Thumb page URL.
        """
        if page_index < 1:
            return comic_url
        return comic_url + "?p=" + str(page_index)

    @classmethod
    def _thumb_page_imgpage_urls(cls, thumbpage_data: BeautifulSoup) -> list:
        """Get all image pages' URLs from current thumb page .

        Args:
            thumbpage_data: page data processed by `BeautifulSoup()`

        Returns:
            list: collection of image URLs.
        """

        # all elements with link
        elems = thumbpage_data.find("div", id="gdt").find_all("a")
        urls_list = []

        for e in elems:
            link = e.get("href")
            urls_list.append(link)

        return urls_list

    @classmethod
    def _img_page_infos(cls, comic_url: str, homepage_data: BeautifulSoup) -> tuple:
        """Get image pages' information

        Args:
            comic_url (str): Comic home page URL.
            homepage_data (BeautifulSoup): processed HomePage.

        Returns:
            tuple: image page infomation. 
                [0]: list, each element is image count per thumb page.
                [1]: list, all images' URLs of comic.
        """
        thumb_pages = cls._thumb_page_count(homepage_data)
        imgcount_per_thumbpage = []
        thumbpage_imgurls = []

        for i in range(thumb_pages):
            thumbpage_url = cls._thumb_page_url(comic_url, i)
            page_bs = core.request_parse_url(
                cls.s, cls.reqhdr_image, thumbpage_url, cls.url_req_retrycount,
            )
            time.sleep(0.1)

            imgcount_per_thumbpage.append(cls._thumb_page_img_count(page_bs))
            thumbpage_imgurls += cls._thumb_page_imgpage_urls(page_bs)

        return (imgcount_per_thumbpage, thumbpage_imgurls)

    @classmethod
    def comic_page_open(cls, url: str) -> BeautifulSoup:
        # replemented version

        page_bs = super().comic_page_open(url)  # open homepage
        if cls._warnpage_is_provided(page_bs):  # not homepage, but a warning page
            page_bs = super().comic_page_open(url + "?nw=always")  # open real homepage

        return page_bs

    @classmethod
    def comic_names(cls, homepage_data: BeautifulSoup) -> list:
        ret = []
        info_tag = homepage_data.find("div", id="gd2")

        # 1st title, can be any language
        ret.append({"name": info_tag.find("h1", id="gn").getText(), "lang": "UND"})

        # 2nd title, may not exist.
        try:
            ret.append({"name": info_tag.find("h1", id="gj").getText(), "lang": "UND"})
        except AttributeError:
            pass

        return ret

    @classmethod
    def comic_page_count(cls, homepage_data: BeautifulSoup) -> int:
        # Target format: XX Pages
        # find_all() will get us all td elements whose class=gdt2
        td_list = homepage_data.find_all("td", {"class": "gdt2"})
        page_count = 0

        for td in td_list:
            if "page" in td.getText():
                page_count = int(td.getText().split(" ")[0])

        return page_count

    # reimplement the version from base class
    @classmethod
    def comic_page_urls(cls, comic_url: str, homepage_data: BeautifulSoup) -> list:
        dummy, urls_list = cls._img_page_infos(comic_url, homepage_data)
        return urls_list

    @classmethod
    def comic_page_url(
        cls, comic_url: str, page_index: int, homepage_data: BeautifulSoup
    ) -> str:
        raise NotImplementedError("Not implemented.")

    @classmethod
    def comic_img_info(cls, page_index: int, page_bs: BeautifulSoup) -> dict:
        url = page_bs.find("div", id="i3").a.img.get("src")

        # 检查是否达到了每日阅览限制
        # NOTE: 此时加载图片会是一个固定 gif 图。
        if url == "https://ehgt.org/g/509.gif":
            raise Exception("Daily limits has reached!")

        return cls._img_url2info(url, page_index)


def get_class(url: str) -> Union[Site, None]:
    """Get site class according to download URL."""
    pattern = re.compile(r"nhentai.")
    if pattern.search(url) is not None:
        return nhentai

    if re.search(r"e\-hentai\.", url) is not None:
        return ehentai

    return None
