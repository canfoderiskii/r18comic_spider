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
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/2483",
        'NAME': '[星野竜一] 潜入妻サトミ 洗脳凌辱の記録/潛行人妻 洗腦凌辱記錄',
        'DIR': '[星野竜一] 潛行人妻 洗腦凌辱記錄',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/2940",
        'NAME': '[YU-RI] 成長しました。/現已成長。 (海賊王)',
        'DIR': '[YU-RI]現已成長(海賊王)',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/784",
        'NAME': '[クリムゾン] JK強制操作 -スマホで長期間弄ばれた風紀委員長',
        'DIR': '[クリムゾン] JK強制操作 -スマホで長期間弄ばれた風紀委員長',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/2870",
        'NAME': '[戦闘的越中] 淫蜜学園',
        'DIR': '[戦闘的越中] 淫蜜学園',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/936",
        'NAME': '[御堂つかさ] パンスト刑事「獄」(シティーハンター/城市獵人)',
        'DIR': '[御堂つかさ] パンスト刑事「獄」(城市獵人)',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/758",
        'NAME': '[中田モデム] 包茎ナマ弄り + とらのあな特典リーフレット',
        'DIR': '[中田モデム] 包茎ナマ弄り + とらのあな特典リーフレット',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/394",
        'NAME': '[十六夜清心] M女專科',
        'DIR': '[十六夜清心] M女專科',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/1563",
        'NAME': '[風船クラブ] 母姦獄-惨',
        'DIR': '[風船クラブ] 母姦獄-惨',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/3012",
        'NAME': '[さいこ] 半分玩具/半身玩具',
        'DIR': '[さいこ] 半身玩具',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/3071",
        'NAME': '[かわもりみさき] 孕ませ！人妻調教師/受孕吧!人妻調教師',
        'DIR': '[かわもりみさき] 受孕吧!人妻調教師',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/1735",
        'NAME': '[クラック] NIGHTFLY 夜間飛行 3 (貓眼三姊妹)',
        'DIR': '[クラック] NIGHTFLY 夜間飛行 3 (貓眼三姊妹)',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/1729",
        'NAME': '[クラック] 夜間飛行 1 DAY DREAMIN’ (貓眼三姊妹)',
        'DIR': '[クラック] 夜間飛行 1 DAY DREAMIN’ (貓眼三姊妹)',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/951",
        'NAME': '[クラック] 夜間飛行 vol.4 CHAIN of FOOLS (Cat’s Eye/貓眼三姊妹)',
        'DIR': '[クラック] 夜間飛行 vol.4 CHAIN of FOOLS (Cat’s Eye 貓眼三姊妹)',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/1823",
        'NAME': '[風船クラブ] 母姦獄∞ INFINITY',
        'DIR': '[風船クラブ] 母姦獄 INFINITY',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/1877",
        'NAME': '[墓場] 公開便所',
        'DIR': '[墓場] 公開便所',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/3284",
        'NAME': '[もっちー] 陵辱学園/凌辱學園 (監獄學園)',
        'DIR': '[もっちー] 凌辱學園(監獄學園)',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/2971",
        'NAME': '[あちゅむち] 人妻不信～淫欲に堕ちる爆乳/妻不信～淫欲裡墮落的爆乳們～',
        'DIR': '[あちゅむち] 妻不信～淫欲裡墮落的爆乳們～',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/1529",
        'NAME': '[唄 飛鳥] 僕の母さんは友人の牝犬/朋友的母親是母犬 ',
        'DIR': '[唄 飛鳥] 朋友的母親是母犬',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/1510",
        'NAME': '[沢田大介] 絶対隷母 ',
        'DIR': '[沢田大介] 絶対隷母',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/2998",
        'NAME': '[sugarBt] 愛が無くてもエッチは出来る!/即使沒有愛，你也可以做! ',
        'DIR': '[sugarBt] 即使沒有愛，你也可以做!',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/3119",
        'NAME': '[ミサキ闘] 妊婦性活',
        'DIR': '[ミサキ闘] 妊婦性活',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/133",
        'NAME': '[成沢空] 男子便所の古手川さん (ToLOVEる-とらぶる-/出包王女)',
        'DIR': '[成沢空] 男子便所の古手川さん (ToLOVE 出包王女)',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/2391",
        'NAME': '[ピンク太郎] 遭毒蟲褻瀆的白百合 白百合に毒蟲',
        'DIR': '[ピンク太郎] 遭毒蟲褻瀆的白百合 白百合に毒蟲',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/2393",
        'NAME': '[溝口 ぜらちん] ガクセイ～娼学性奴～/淫蕩學生～娼學性奴',
        'DIR': '[溝口 ぜらちん] 淫蕩學生～娼學性奴',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/2436",
        'NAME': '[NABURU] 母娘姦刑',
        'DIR': '[NABURU] 母娘姦刑',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/1725",
        'NAME': '[墓場] けだものの家 上/畜牲禽獸之家 上',
        'DIR': '[墓場] 畜牲禽獸之家 上',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/1535",
        'NAME': '[萬蔵] 盗撮コレクター/盜拍材料精題集',
        'DIR': '[萬蔵] 盜拍材料精題集',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/1565",
        'NAME': '[秋神サトル] 調教→屈服→肉奴隷',
        'DIR': '[秋神サトル] 調教→屈服→肉奴隷',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/608",
        'NAME': '[舞六まいむ] デリママ～淫らな俺の義母さん～/外約媽媽 淫蕩的我的繼母媽媽',
        'DIR': '[舞六まいむ] 外約媽媽 淫蕩的我的繼母媽媽',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/1121",
        'NAME': '[室永叉焼] ハイブリッド通信vol.15 (監獄學園)',
        'DIR': '[室永叉焼] ハイブリッド通信vol.15 (監獄學園)',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/1051",
        'NAME': '[骨太男爵] 女地獄、肉の壺~変態類淫乱科メス豚一代記~/女地獄,地獄肉之壺~',
        'DIR': '[骨太男爵] 女地獄,地獄肉之壺~',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/2266",
        'NAME': '[野原ひろみ] 性玩具拘束人形',
        'DIR': '[野原ひろみ] 性玩具拘束人形',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/313",
        'NAME': '[まぐろ帝國] 奴隷妻',
        'DIR': '[まぐろ帝國] 奴隷妻',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/2343",
        'NAME': '[舞六まいむ] 国立人妻学園/國立人妻學園',
        'DIR': '[舞六まいむ] 國立人妻學園',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/449",
        'NAME': '[舞六まいむ] お姉様がイかせてあげる',
        'DIR': '[舞六まいむ] お姉様がイかせてあげる',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/1043",
        'NAME': '[弥美津ヒロ]飼い主様になってよネッ!',
        'DIR': '[弥美津ヒロ]飼い主様になってよネッ!',
        'ENABLE': False,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/1503",
        'NAME': '[鈴木あどれす] Love Love Hurricane II (One Piece/海賊王)',
        'DIR': '[鈴木あどれす] Love Love Hurricane II (One Piece 海賊王)',
        'ENABLE': True,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/1507",
        'NAME': '[YU-RI] 蛇姫様ご乱心ですッ!2 (One Piece/海賊王)',
        'DIR': '[YU-RI] 蛇姫様ご乱心ですッ!2 (One Piece 海賊王)',
        'ENABLE': True,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/1501",
        'NAME': '[カーマイン] 海賊王蛇姬被海軍輪著幹 (One Piece/海賊王)',
        'DIR': '[カーマイン] 海賊王蛇姬被海軍輪著幹 (One Piece 海賊王)',
        'ENABLE': True,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/1531",
        'NAME': '[此花] 女殺蛇地獄 (ワンピース/海賊王)',
        'DIR': '[此花] 女殺蛇地獄 (海賊王)',
        'ENABLE': True,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/1533",
        'NAME': '[此花] 続・女殺蛇地獄 (ワンピース/海賊王)',
        'DIR': '[此花] 続・女殺蛇地獄 (海賊王)',
        'ENABLE': True,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/1601",
        'NAME': '[電気将軍] MEROMERO GIRLS 3 (海賊王)',
        'DIR': '[電気将軍] MEROMERO GIRLS 3 (海賊王)',
        'ENABLE': True,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/1596",
        'NAME': '[YU-RI] ナミちゃんとあ・そ・ぼ☆ (海賊王)',
        'DIR': '[YU-RI] ナミちゃんとあ・そ・ぼ☆ (海賊王)',
        'ENABLE': True,
    },
    {
        'HOMEPAGE_URL': "http://18h.animezilla.com/manga/2968",
        'NAME': 'MEROMEROGIRLS2 MUSIWARA GIRLS SIDE/淫魔之子 (海賊王)',
        'DIR': 'MEROMEROGIRLS2 MUSIWARA GIRLS SIDE 淫魔之子(海賊王)',
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

Error_count = 0

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

        # Get the page content with retry
        retry = 5
        while retry:
            try:
                page_resp = urllib.request.urlopen(current_page_url)
                if (page_resp.status == 200):
                    break
            except urllib.error.HTTPError:
                retry -= 1
                if retry:
                    print("Retry..")
                    continue
                else:
                    raise
        if (page_resp.status != 200):
            print("[ERROR]:Request comic page {}, respcode={}, abort..".format(
                page_number, page_resp.status))
            Error_count += 1
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

        retry = 5
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
        if (img_resp.status != 200):
            print("[ERROR]:Request image, page {}, respcode={}, abort..".format(
                page_number, page_resp.status))
            Error_count += 1
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
            Error_count += 1

if Error_count:
    print("[NOTICE]Total Error Count = {}".format(Error_count))
