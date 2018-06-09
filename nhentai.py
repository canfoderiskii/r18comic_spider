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

COMIC_INFOS = [
    {'HOMEPAGE_URL': "https://nhentai.net/g/62579/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/223546/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/224010/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/232943/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/158063/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/141782/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/61781/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/233784/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/230955/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/227442/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/227108/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/232325/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/232324/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/232319/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/232326/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/227288/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/231727/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/217194/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/216547/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/216545/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/215205/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/211378/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/206449/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/206448/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/206441/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/204617/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/202806/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/193819/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/190922/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/193155/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/192764/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/186944/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/168460/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/188310/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/163050/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/163051/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/163143/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/163047/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/163041/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/157883/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/157239/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/151214/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/151215/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/150989/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/148538/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/143751/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/144365/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/129120/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/126805/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/119714/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/114601/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/113509/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/126523/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/129411/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/107480/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/106597/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/105550/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/105090/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/105085/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/102886/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/92809/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/86861/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/89934/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/84328/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/97175/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/228997/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/224796/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/215671/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/229256/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/230586/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/191719/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/181318/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/181710/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/189432/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/191834/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/234712/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/234427/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/233986/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/233166/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/233164/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/233162/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/233160/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/233156/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/233155/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/233154/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/233153/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/232161/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/233152/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/231987/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/231861/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/231606/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/229135/", 'ENABLE': False,
        'DIRNAME': "[Nightmare Express -Akumu no Takuhaibin-]Yokubou Kaiki Dai 531 Shou 欲望回帰第531章-誘拐相姦-被強迫性交攝影的母子[Chinese]"},
    {'HOMEPAGE_URL': "https://nhentai.net/g/226165/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/226163/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/225231/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/225765/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/225550/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/224259/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/165008/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/165007/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/165006/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/165004/", 'ENABLE': False,
        'DIRNAME': "[Nightmare Express -Akumu no Takuhaibin-] Yokubou Kaiki dai 432 shou -Kyuura Mitsuin Goku Oyakodon GP Kasshoku Haramase Shikomi- (Tenchi Muyo) [Chinese]"},
    {'HOMEPAGE_URL': "https://nhentai.net/g/165003/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/165000/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164998/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164995/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164997/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164994/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164993/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164992/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164991/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164989/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164990/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164988/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164987/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164986/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164985/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164983/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164982/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164913/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164912/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164907/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164906/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164905/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164904/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164903/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164902/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164901/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164900/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164898/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164896/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164895/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164894/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164887/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164889/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164885/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164883/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164884/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164881/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164853/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164852/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164848/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164831/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164830/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164829/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164827/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164826/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164824/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164818/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164817/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164816/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164815/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164811/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/172130/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/179749/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/180103/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/172043/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/180191/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/180471/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/180507/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/180513/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/180510/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/180826/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164673/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164672/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164552/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/158403/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/149365/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/149351/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/149049/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/149048/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/148859/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/148853/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/108997/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/103563/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/100436/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/90566/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/85457/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/83993/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/82460/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/81531/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/77996/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/77885/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/75632/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/73532/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/73001/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/71039/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/69402/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/67560/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/67056/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/64590/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/63195/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/58077/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/59602/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/55542/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/54767/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/54556/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/49520/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/49491/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/47213/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/47581/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/47965/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/47215/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/45588/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/46330/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/42632/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/44856/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/43502/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/41412/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/41411/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/37641/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/35304/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/32155/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/31117/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/24314/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/24313/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/24315/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/24310/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/24311/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/24312/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/24304/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/24308/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/24306/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/24300/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/24297/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/24285/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/24283/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/24265/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/24252/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/24244/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/24243/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/24241/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/24233/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/24225/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/24218/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/20656/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/22330/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/235410/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/235380/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/234777/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/235260/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/208767/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/211508/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/203733/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/203421/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/224845/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/218902/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/181619/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/212436/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/210888/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/210171/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/52974/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/84262/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/88840/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/110642/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/133799/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/110225/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/109958/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/128315/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/135103/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/235264/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/229181/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/223607/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/208759/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/161693/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/207834/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/229206/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/228719/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/159188/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/161684/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/118613/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/105228/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/84531/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/69055/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/61019/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/54978/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/49865/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/46411/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/48703/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/232696/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/221497/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/203736/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/190267/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/166344/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/165087/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/166333/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/165084/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/165078/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/165066/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/165062/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/165060/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/165058/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/165057/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/165056/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/165054/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/165053/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/165049/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/165045/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/165044/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/165041/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/165037/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/165033/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/164620/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/150761/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/130668/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/130430/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/120619/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/18424/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/34647/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/27445/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/35707/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/67195/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/53561/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/91742/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/92731/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/94272/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/99097/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/219945/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/190580/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/119778/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/219953/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/194310/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/159835/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/138593/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/210376/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/209592/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/203377/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/203475/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/203760/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/189995/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/168376/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/125834/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/105279/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/212453/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/212519/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/207811/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/207006/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/204364/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/155902/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/211452/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/206902/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/173510/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/143709/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/200103/", 'ENABLE': False, },
    {'HOMEPAGE_URL': "https://nhentai.net/g/200281/", 'ENABLE': False, },
]

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, \
              like Gecko) Chrome/64.0.3282.140 Safari/537.36"

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

    if c['ENABLE'] is False:
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
    homepage_soup.prettify()  # translate unicode string

    info_tag = homepage_soup.find('div', id='info')
    c['NAME_EN'] = info_tag.h1.getText()
    try:
        c['NAME_JP'] = info_tag.h2.getText()
    except AttributeError:
        print("no jp name")
        c['NAME_JP'] = ""
    c['PAGES'] = int(info_tag.find('div', text=re.compile(
        'pages')).getText().replace('pages', ''))

    # determine downloading directory
    if 'DIRNAME' not in c:
        c['DIRNAME'] = c['NAME_EN']  # use the english name only
    # check & remove invalid character
    regex_pattern = r'[\\/:|*?<>"]'
    if re.search(regex_pattern, c['DIRNAME']) is not None:
        c['DIRNAME'] = re.sub(regex_pattern, '', c['DIRNAME'])
        print("[WARN]replaced some invalid chars for dirname {}..".format(
            c['DIRNAME']))
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
