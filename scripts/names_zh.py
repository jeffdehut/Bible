"""The names of people and places in Traditional Chinese, as the Chinese Union Version spells them.

    python3 scripts/names_zh.py        (after connections.py and maps.py)

Reads   the Chinese Union Version (Traditional, new punctuation, public domain), as USFM from
        eBible.org (downloaded once into .cache/cuv/), which marks every proper noun (\\pn);
        data/bible/people.json and data/bible/places.json: each person and place, and the verses
        that name them (Hebrew numbering in the Old Testament, turned into the English numbering
        the Union Version follows, through TVTMS); Theographic's people and places (in
        .cache/theographic/, from connections.py), which give every verse that names each one,
        where the site's own lists name a place only where a map shows it; data/graph.json for
        the names as the
        Connections page and the 3D web show them ("Abdi (1 Chronicles 6.29)")
Writes  i18n/zh-Hant.names.js   I18N.add({English name: Chinese name, ...})

How a name is found: among the proper nouns of the verses that name a person or place, the one
that is found in most of them (recall) and seldom elsewhere (precision) is its Chinese. People
and places of the same name are taken together, as the Union Version spells them alike. A name
whose verses don't settle it (one verse in a list of names) is matched by order: in such a verse,
once the names found already are set aside, the remaining English names and Chinese proper nouns
are paired in the order they come. A name still unsettled is left out, and shows in English.
Corrections go in OVERRIDES below, never in the written file.
"""

import ast
import collections
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from books import BOOKS                                   # noqa: E402
import connections                                        # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CUV_ZIP = "https://ebible.org/Scriptures/cmn-cu89t_usfm.zip"
OUT = os.path.join(ROOT, "i18n", "zh-Hant.names.js")
# The Union Version's book codes, in our book order.
CODES = ["GEN", "EXO", "LEV", "NUM", "DEU", "JOS", "JDG", "RUT", "1SA", "2SA", "1KI", "2KI", "1CH", "2CH",
         "EZR", "NEH", "EST", "JOB", "PSA", "PRO", "ECC", "SNG", "ISA", "JER", "LAM", "EZK", "DAN", "HOS",
         "JOL", "AMO", "OBA", "JON", "MIC", "NAM", "HAB", "ZEP", "HAG", "ZEC", "MAL",
         "MAT", "MRK", "LUK", "JHN", "ACT", "ROM", "1CO", "2CO", "GAL", "EPH", "PHP", "COL", "1TH", "2TH",
         "1TI", "2TI", "TIT", "PHM", "HEB", "JAS", "1PE", "2PE", "1JN", "2JN", "3JN", "JUD", "REV"]
# Hand corrections: English name -> Chinese, or None to leave a name out.
OVERRIDES = {
    "God": None, "LORD": None, "Lord": None,
    "Jesus": "耶穌", "Christ": "基督", "Pharaoh": "法老", "Nebaioth": "尼拜約", "Perez": "法勒斯", "Bel": "彼勒", "Perazim": "毗拉心", "Luhith": "魯希坡", "Dimon": "底們", "Sargon": "撒珥根", "Shear-jashub": "施亞雅述", "Immanuel": "以馬內利", "Barachel": "巴拉迦別", "Keziah": "基洗亞", "Keren-happuch": "基連‧哈樸", "Leviathan": "利維坦", "Behemoth": "比希摩", "Abaddon": "亞巴頓", "Biztha": "比斯他", "Bigtha": "比革他", "Carkas": "甲迦", "Carshena": "甲示拿", "Admatha": "押瑪他", "Meres": "米力", "Marsena": "瑪西拿", "Bigthan": "辟探", "Hadassah": "哈大沙", "Parmashta": "帕瑪斯他", "Arisai": "亞利賽", "Aridai": "亞利代", "Vaizatha": "瓦耶撒他", "Nisan": "尼散", "Sivan": "西彎", "Tebeth": "提別", "Purim": "普珥", "Hacaliah": "哈迦利亞", "Sheshbazzar": "設巴薩", "Shethar-bozenai": "示他‧波斯乃", "Osnappar": "亞斯那巴", "Hassophereth": "瑣斐列", "Addan": "押但", "Hobaiah": "哈巴雅", "Kelaiah": "基拉雅", "Isshijah": "伊示雅", "Cheluhu": "基祿", "Jaasai": "雅掃", "Chelal": "基拉", "Izziah": "耶西雅", "Ramiah": "拉米", "Sotai": "瑣太", "Gibbar": "吉罷珥", "Reaiah": "利亞雅", "Asnah": "押拿", "Mispar": "米斯拔", "Achmetha": "亞馬他", "Kiriath-arim": "基列‧亞琳", "Siaha": "西亞哈", "Pethahiah": "毘他希雅", "Asaiah (2 Kings 22.12)": "亞撒雅（列王紀下 22.12）", "Tokhath": "托哈", "Cyrus": "古列", "Gimzo": "瑾鎖", "Gur-baal": "姑珥‧巴力", "Hasrah": "哈斯拉", "Hozai": "何賽", "Ismachiah": "伊斯瑪基雅", "Beracah": "比拉迦", "Shimrith": "示米利", "Ephrain": "以法拉音", "Zephathah": "洗法", "Ben-hail": "便‧亥伊勒", "Tob-adonijah": "駝‧巴多尼雅", "Dodavahu": "多大瓦", "Jehoshabeath": "約示巴", "Imla": "音拉", "Kenaanah": "基拿拿", "Huram-abi": "戶蘭‧亞比", "Jakin": "雅斤", "Jehieli": "耶希伊利", "Asarelah": "亞薩利拉", "Jesarelah": "耶薩利拉", "Shubael": "書巴業", "Shebuel": "細布業", "Shelomoth": "示羅摩", "Dodai": "朵代", "Shamhuth": "珊合", "Obil": "阿比勒", "Jaziz": "雅悉", "Zina": "細拿", "Jeriah": "耶利雅", "Peullethai": "毗烏利太", "Eliehoenai": "以利約乃", "Shallecheth": "沙利基", "Jehezkel": "以西結", "Shitrai": "施提賚", "Shirtai": "施爾太", "Joshaphat": "約沙法", "Jehiel": "耶歇", "Ben": "便", "Huram": "戶蘭", "Tou": "陀烏", "Shophach": "朔法", "Beeliada": "比利雅大", "Amasai": "亞瑪賽", "Heled": "希立", "Ithai": "以太", "Hezro": "希斯羅", "Ezbai": "伊斯拜", "Mibhar": "彌伯哈", "Shama": "沙瑪", "Jeribai": "耶利拜", "Joshaviah": "約沙未雅", "Ithmah": "伊特瑪", "Elnaam": "伊利拿安", "Eluzai": "伊利烏賽", "Joezer": "約以謝", "Machbannai": "末巴奈", "Kushaiah": "古沙雅", "Jehiah": "耶希亞", "Shammoth": "沙瑪", "Hodiah": "荷第雅", "Hanniel": "漢聶", "Zillethai": "洗勒太", "Mattaniah": "瑪探雅", "Abram": "亞伯蘭", "Arpachshad": "亞法撒", "Diphath": "低法", "Hamran": "哈默蘭", "Homam": "荷幔", "Kenan": "該南", "Matred": "瑪特列", "Me-zahab": "米‧薩合", "Mehetabel": "米希她別", "Sabta": "撒弗他", "Sabteca": "撒弗提迦", "Shephi": "示非", "Zaavan": "撒番", "Ashhur": "亞施戶", "Atroth-beth-joab": "亞他綠‧伯‧約押", "Beth-gader": "伯迦得", "Caleb-ephrathah": "迦勒‧以法他", "Chelubai": "基路拜", "Jorkeam": "約干", "Machbenah": "抹比拿", "Menuhoth": "米努‧哈", "Raddai": "拉代", "Raham": "拉含", "Tirhanah": "特哈拿", "Anani": "阿拿尼", "Hasadiah": "哈撒底", "Hashubah": "哈舒巴", "Hoshama": "何沙瑪", "Jeconiah": "耶哥尼雅", "Jushab-hesed": "于沙‧希悉", "Ohel": "阿黑", "Aharhel": "亞哈黑", "Ahuzzam": "亞戶撒", "Anub": "亞諾", "Beth-biri": "伯‧比利", "Cozeba": "哥西巴", "Ethnan": "伊提南", "Ge-harashim": "革‧夏納欣", "Hammuel": "哈母利", "Hushah": "戶沙", "Idbash": "伊得巴", "Ir-nahash": "珥拿轄", "Ishma": "伊施瑪", "Jalon": "雅倫", "Jashubi-lehem": "雅叔比利恆", "Jekuthiel": "耶古鐵", "Jokim": "約敬", "Joshibiah": "約示比", "Koz": "哥斯", "Lahad": "拉哈", "Meonothai": "憫挪太", "Recah": "利迦", "Saraph": "薩拉", "Zereth": "洗列", "Zobebah": "瑣比巴", "Abdiel": "押比疊", "Beerah": "備拉", "Hara": "哈拉", "Jacan": "雅干", "Jorai": "約賴", "Nodab": "挪答", "Shapham": "沙番", "Zia": "細亞", "Tilgath-pilneser": "提革拉‧毘列色", "Ethni": "伊特尼", "Kishi": "基示", "Rimmono": "臨摩挪", "Toah": "陀亞", "Zophai": "瑣菲", "Birzaith": "比撒威", "Elead": "以列", "Hammolecheth": "哈摩利吉", "Ibsam": "易伯散", "Imna": "音那", "Ishhod": "伊施荷", "Jahmai": "雅買", "Jeriel": "耶勒", "Pispa": "毗斯巴", "Rephah": "利法", "Resheph": "利悉", "Rohgah": "羅迦", "Sheerah": "舍伊拉", "Zemirah": "細米拉", "Zethan": "細坦", "Aharah": "亞哈拉", "Anthothijah": "安陀提雅", "Bocheru": "波基路", "Eshek": "以設", "Hizki": "希西基", "Iphdeiah": "伊弗底雅", "Ishmerai": "伊施米萊", "Izliah": "伊斯利亞", "Jaareshiah": "雅利西", "Nohah": "挪哈", "Sachia": "沙迦", "Shamsherai": "珊示萊", "Shemed": "沙麥", "Shephuphan": "示孚汛", "Shimrath": "申拉", "Zecher": "撒迦", "Ibneiah": "伊比尼雅", "Ibnijah": "伊比尼雅", "Jahzerah": "雅希細拉", "Meshillemith": "米實利密", "Shimeam": "示米暗", "Tahrea": "他利亞", "Rabshakeh": "拉伯沙基", "Azaliah": "亞薩利", "Harhas": "哈珥哈斯", "Hephzibah": "協西巴", "Nisroch": "尼斯洛", "Nehushtan": "尼忽士但", "Tanhumeth": "單戶蔑", "Berodach-baladan": "比羅達‧巴拉但", "Tartan": "他珥探", "Rab-saris": "拉伯撒利", "Jehonadab": "約拿達", "Jehoash": "約阿施", "Silla": "悉拉", "Shimeath": "示米押", "Beth-eked": "伯‧艾克", "Joahaz": "約哈斯", "Carites": "迦利人", "Valley of Salt": "鹽谷", "Jerusha": "耶路沙", "Pul": "普勒", "Tiglath-pileser": "提革拉‧毘列色", "Medes": "米底亞人", "Cuth": "古他", "Succoth-benoth": "疏割‧比訥", "Nergal": "匿甲", "Ashima": "亞示瑪", "Nibhaz": "匿哈", "Tartak": "他珥他", "Anammelech": "亞拿米勒", "Joram": "約蘭", "Bidkar": "畢甲", "Gur": "姑珥", "Beth-haggan": "伯‧哈干", "Ramoth-gilead": "基列的拉末", "Ethbaal": "謁巴力", "Kerith": "基立溪", "Tishbite": "提斯比人", "Jezreelite": "耶斯列人", "Zeruah": "洗魯阿", "Abijam": "亞比央", "Tabrimmon": "他伯利們", "Tadmor": "達莫", "Abishalom": "押沙龍", "Chinnereth": "基尼烈", "Kue": "古耶", "Baana": "巴拿", "Shisha": "示沙", "Ahishar": "亞希煞", "Abda": "亞比大", "Adoniram": "亞多尼蘭", "Ben-hur": "便‧戶珥", "Ben-deker": "便‧底甲", "Elon-beth-hanan": "以倫‧伯‧哈南", "Ben-hesed": "便‧希悉", "Naphath-dor": "多珥山岡", "Ben-abinadab": "便‧亞比拿達", "Taphath": "她法", "Ben-geber": "便‧基別", "Basemath": "巴實抹", "Aloth": "亞祿", "Ezrahite": "以斯拉人", "Zoheleth": "瑣希列", "Gebalites": "迦巴勒人", "Ziv": "西弗", "Bul": "布勒", "Ethanim": "以他念", "Shobi": "朔比", "Ithra": "以特拉", "Adoram": "亞多蘭", "Araunah": "亞勞拿", "Hashem": "哈深", "Paarai": "帕萊", "Shagee": "沙基", "Sharar": "沙拉", "Sibbecai": "西比該", "Mebunnai": "米本乃", "Josheb-basshebeth": "約設‧巴設", "Netophathite": "尼陀法", "Hararite": "哈拉", "Ahohite": "亞合", "Tahchemonite": "他革捫", "Abi-albon": "亞比亞本", "Jaare-oregim": "雅雷俄珥金", "Hezrai": "希斯萊", "Tahtim-hodshi": "他停‧合示", "Dan-jaan": "但‧雅安", "Hushathite": "戶沙", "Hadadezer": "哈大底謝", "Jedidiah": "耶底底亞", "Talmai": "達買", "Tyrians": "推羅人", "Tyre": "推羅", "Damascus": "大馬色", "Bithron": "畢倫", "Ashurites": "亞書利", "Elishua": "以利書亞", "Toi": "陀以", "Cherethites": "基利提", "Pelethites": "比利提", "Merib-baal": "米力‧巴力", "Eshbaal": "伊施‧巴力", "Chidon": "基頓", "Beerothite": "比錄", "Paltiel": "帕鐵", "Hakilah": "哈基拉", "Racal": "拉哈勒", "Ezel": "以色", "Meholathite": "米何拉人", "Horesh": "何烈沙", "Jeshimon": "耶示門", "Zeror": "洗羅", "Aphiah": "亞斐亞", "Shalishah": "沙利沙", "Shaalim": "沙琳", "Shen": "善", "Bozez": "播薛", "Valley of Zeboim": "洗波音谷", "Ahijah (1 Samuel 14.3)": "亞希亞（撒母耳記上 14.3）", "Mara": "瑪拉", "Ephrathah": "以法他", "Abdon": "押頓", "Sorek Valley": "梭烈谷", "Sorek": "梭烈", "Rimmon": "臨門", "Har-heres": "希烈山", "Timnath-heres": "亭拿‧希烈", "Harosheth-ha-goiim": "夏羅設", "Jerubbaal": "耶路‧巴力", "Harod": "哈律", "Moreh": "摩利", "Karkor": "加各", "Baal-berith": "巴力‧比利土", "El-berith": "伊勒‧比利土", "Shihor": "西曷河", "Eltolad": "伊勒多臘", "Chitlish": "基提利", "Cabbon": "迦本", "Nibshan": "匿珊", "En-gedi": "隱‧基底", "Ir-hamelah": "鹽城", "Shikkeron": "施基崙", "Gederah": "基底拉", "Maralah": "瑪拉拉", "Gath-hepher": "迦特‧希弗", "Ebron": "義伯崙", "Rakkath": "拉甲", "Zer": "側耳", "Horem": "和璉", "Migdal-el": "密大‧伊勒", "Kartah": "加珥他", "Dimnah": "丁拿", "Emek-keziz": "伊麥‧基悉", "Haeleph": "以利弗", "Shahazimah": "沙哈洗瑪", "Mount Gaash": "迦實山", "Mount Ephron": "以弗崙山", "Mount Jearim": "耶琳山", "Mount Baalah": "巴拉山", "Valley of Iphtah-el": "伊弗他‧伊勒谷", "Valley of Jezreel": "耶斯列平原", "Brook of Egypt": "埃及小河", "Valley of the Son of Hinnom": "欣嫩子谷", "Kanah Valley": "加拿河", "Ascent of Akrabbim": "亞克拉濱坡", "Ascent of Adummim": "亞都冥坡", "En-tappuah": "隱‧他普亞", "Rumah": "魯瑪", "Mount Seir": "西珥山", "Zelah": "洗拉", "Hazar-gaddah": "哈薩‧迦大", "Mount Halak": "哈拉山", "Valley of Mizpeh": "米斯巴平原", "Arnon Valley": "亞嫩谷", "Sea of Kinnereth": "基尼烈海", "Valley of Achor": "亞割谷", "Mount Ebal": "以巴路山", "Mount Gerizim": "基利心山", "Mount Hermon": "黑門山", "Naphoth-dor": "多珥山岡", "Gibeath-haaraloth": "除皮山", "Kephirah": "基非拉", "Jashar": "雅煞珥", "Book of Jashar": "雅煞珥書", "waters of Merom": "米倫水", "Greater Sidon": "大西頓", "Anakim": "亞衲人", "Abel of Beth-maacah": "亞伯‧伯‧瑪迦", "Appii forum": "亞比烏市", "Canaanitish woman": "迦南婦人", "Diviners' Oak": "米惡尼尼橡樹", "Dung Gate": "糞廠門", "Fish Gate": "魚門", "Jordan Valley": "約旦河平原", "King's Valley": "王谷", "Mary Magdalene": "抹大拉的馬利亞", "Red Sea": "紅海", "Rock of Escape": "西拉哈瑪希羅結", "Ur of the Chaldees": "迦勒底的吾珥", "gate of the foundation": "根基門", "valley of Lebanon": "黎巴嫩平原", "valley of Shaveh": "沙微谷", "sons of Jashen": "雅善的眾子", "Caesarea Philippi": "該撒利亞‧腓立比", "Valley of Aijalon": "亞雅崙谷", "Valley of Aven": "亞文平原", "Valley of Elah": "以拉谷", "Valley of Lebanon": "黎巴嫩平原", "Valley of Rephaim": "利乏音谷", "Valley of Shaveh": "沙微谷", "Mount Carmel": "迦密山", "Mount Gilboa": "基利波山", "Mount Zion": "錫安山", "Ebal": "以巴路", "Gerizim": "基利心", "Jeshurun": "耶書崙", "Di-zahab": "底撒哈", "Tophel": "陀弗", "Sion": "西雲", "Emim": "以米", "Zamzummim": "散送冥", "Nimrah": "寧拉", "Sebam": "示班", "Shepher": "沙斐", "Hahiroth": "哈希錄", "Parnach": "帕納", "Arod": "亞律", "Zephon": "洗分", "Puvah": "普瓦", "Iezer": "伊以謝", "Hoglah": "曷拉", "Shephupham": "書反", "Hupham": "戶反", "Shuham": "書含", "Waheb": "哇哈伯", "Suphah": "蘇法", "Zophim": "瑣腓", "Bamoth-baal": "巴末‧巴力", "Gaddiel": "迦疊", "Sodi": "梭底", "Susi": "穌西", "Mount Hor": "何珥山", "Ahiezer": "亞希以謝", "Ammishaddai": "亞米沙代", "Ochran": "俄蘭", "Pagiel": "帕結", "Zuriel": "蘇列", "Nazirite": "拿細耳人", "Oholiab": "亞何利亞伯", "Abib": "亞筆", "Asherah": "亞舍拉", "Pi-hahiroth": "比‧哈希錄", "Baal-zephon": "巴力‧洗分", "Meribah": "米利巴", "Mishael": "米沙利", "Sithri": "西提利", "Pithom": "比東", "Shiphrah": "施弗拉", "Elzaphan": "以利撒反", "Abiasaph": "亞比亞撒", "Putiel": "普鐵", "Areli": "亞列利", "Huppim": "戶平", "Ziphion": "洗非芸", "Ishvah": "亦施瓦", "Ishvi": "亦施韋", "Muppim": "母平",
    # Found with others in every verse, so the verses can't tell them apart:
    "Simon": "西門", "Philip": "腓力", "Pilate": "彼拉多", "Galilee": "加利利", "Jordan": "約旦河",
    "Sinai": "西奈", "Huldah": "戶勒大", "Darda": "達大", "Telah": "他拉", "Heldai": "黑玳",
    "Ibhar": "益轄", "Gaddi": "迦底", "Suah": "書亞", "Shua": "書亞", "Mica": "米迦",
    "Ezrah": "以斯拉", "Elpalet": "以利法列",
}


def cuv_text():
    """{(osis, chapter, verse): [proper nouns, in order]} and {osis: book name}, from the USFM."""
    folder = os.path.join(connections.CACHE, "cuv", "usfm")
    if not os.path.isdir(folder):
        import zipfile
        z = connections.fetch(CUV_ZIP, os.path.join(connections.CACHE, "cuv", "cuv.zip"))
        zipfile.ZipFile(z).extractall(folder)
    osis_of = {code: BOOKS[i][1] for i, code in enumerate(CODES)}
    nouns, names = {}, {}
    for fn in sorted(os.listdir(folder)):
        if not fn.endswith(".usfm"):
            continue
        code = fn.split("-")[1][:3]
        if code not in osis_of:
            continue
        osis, c, vs = osis_of[code], 0, []
        for line in open(os.path.join(folder, fn), encoding="utf-8-sig"):
            line = re.sub(r"\\f .*?\\f\*", "", line)      # footnotes
            if (m := re.match(r"\\toc1 (.+)", line)):
                names[osis] = m[1].strip()
            if (m := re.match(r"\\c (\d+)", line)):
                c = int(m[1])
                continue
            if (m := re.match(r"\\v (\d+)(?:-(\d+))?", line)):
                vs = list(range(int(m[1]), int(m[2] or m[1]) + 1))
            if not vs or line.startswith(("\\s", "\\r", "\\ms", "\\mt", "\\d ")):
                continue
            for n in re.findall(r"\\pn (.+?)\\pn\*", line):
                n = n.strip()
                for v in vs:
                    nouns.setdefault((osis, c, v), []).append(n)
    return nouns, names


def hebrew_numbering():
    """{(osis, English chapter, verse): (osis, Hebrew chapter, verse)} where they differ."""
    vers = connections.Versification(connections.fetch_stepbible("tvtms"), connections.load_texts())
    return dict(vers.to_hebrew)


def site_names():
    """{English name: set of (osis, chapter, verse)}, in our (Hebrew) numbering."""
    where = collections.defaultdict(set)

    def add(name, osis, cv):
        if name:
            c, v = map(int, cv.split(":"))
            where[name].add((osis, c, v))

    people = json.load(open(os.path.join(ROOT, "data", "bible", "people.json"), encoding="utf-8"))
    for osis, vs in people["verses"].items():
        for cv, ks in vs.items():
            for k in ks:
                add(people["n"][k], osis, cv)
    places = json.load(open(os.path.join(ROOT, "data", "bible", "places.json"), encoding="utf-8"))
    for osis, vs in places["verses"].items():
        for cv, entries in vs.items():
            for e in entries:
                add(e[2] if len(e) > 2 else places["places"][e[0]][1], osis, cv)
    for n in [p[1] for p in places["places"]] + people["n"]:
        if n:
            where.setdefault(n, set())
    return where


def theographic_names(heb):
    """{name: set of verses} from Theographic's people and places, which list every verse that
    names them (the site's own lists name a place only where a map shows it). Its references are
    in English numbering, turned into ours."""
    folder = os.path.join(connections.CACHE, "theographic", "json")
    load = lambda f: json.load(open(os.path.join(folder, f), encoding="utf-8"))
    ref = {}
    for r in load("verses.json"):
        b, c, v = r["fields"]["osisRef"].split(".")
        ref[r["id"]] = heb.get((b, int(c), int(v)), (b, int(c), int(v)))
    ids = lambda x: ast.literal_eval(x) if isinstance(x, str) else (x or [])
    where = collections.defaultdict(set)
    for f, keys in (("people.json", ("name",)), ("places.json", ("displayTitle", "kjvName", "esvName"))):
        for r in load(f):
            vs = {ref[i] for i in ids(r["fields"].get("verses")) if i in ref}
            for k in keys:
                if r["fields"].get(k):
                    where[r["fields"][k]] |= vs
    return where


def english_text():
    """{(osis, chapter, verse): our English text}, for the order names come in."""
    text = {}
    folder = os.path.join(ROOT, "data", "bible", "text")
    for fn in sorted(os.listdir(folder)):
        d = json.load(open(os.path.join(folder, fn), encoding="utf-8"))
        for ch in d["chapters"]:
            for row in ch["v"]:
                text[(d["osis"], int(ch["c"]), row[0])] = re.sub(r"\[\^\w+\]", "", row[1] or "")
    return text


def onset(name):
    """How an English name begins, for its sound: its first consonants ("sh", "t"), or its first
    vowel."""
    m = re.match(r"[^aeiouy]+|[aeiouy]", name.lower().replace("-", ""))
    return m[0][:2] if m else ""


def match(where, nouns):
    """The names their verses settle: {English: Chinese}, and the rest. Each proper noun is
    scored for a name by recall (the share of the name's verses that have it), squared, times a
    little of its precision (the share of its verses that are the name's: a little, as the Union
    Version gives many people one name, 雅各 for Jacob and James), times how well its first character fits the
    sound the English begins with (learned from the pairs the verses settle clearly: "H" is
    usually 哈 or 希, rarely 特), which tells apart names always found together (Huldah,
    daughter-in-law of Tikvah). A name takes its best proper noun when that is clearly ahead of
    the next; one already given to a name found in the same verses is not given again (Pedahzur,
    father of Gamaliel). The names are gone over until nothing changes."""
    df = collections.Counter(n for ns in nouns.values() for n in set(ns))
    base = {}
    for name, vs in where.items():
        cands = collections.Counter(n for key in vs for n in set(nouns.get(key, [])))
        hits = sum(1 for key in vs if nouns.get(key))
        base[name] = {n: (cnt / hits) ** 2 * (cnt / df[n]) ** 0.3 for n, cnt in cands.items() if cnt / hits >= 0.2 or len(vs) < 5}
    # The sound: first characters of the clearly settled pairs, by how the English begins.
    sound = collections.defaultdict(collections.Counter)
    for name, sc in base.items():
        top = sorted(sc.items(), key=lambda x: -x[1])
        if top and top[0][1] >= 0.5 and (len(top) == 1 or top[0][1] >= 3 * top[1][1]) and len(where[name]) >= 3:
            sound[onset(name)][top[0][0][0]] += 1
    def fit(name, n):
        c = sound.get(onset(name))
        if not c:
            return 1.0
        return 0.25 + 0.75 * (c[n[0]] + 0.5) / (max(c.values()) + 0.5)
    scores = {name: {n: sc * fit(name, n) for n, sc in cs.items()} for name, cs in base.items()}
    found, given = {}, collections.defaultdict(list)
    blocked = lambda n, name: any(where[o] & where[name] for o in given[n])
    pairs = sorted(((sc, name, n) for name, cs in scores.items() for n, sc in cs.items()), reverse=True)
    changed = True
    while changed:
        changed = False
        for sc, name, n in pairs:
            if name in found or sc < 0.1 or blocked(n, name):
                continue
            second = max((x for m, x in scores[name].items() if m != n and not blocked(m, name)), default=0)
            if sc < 1.5 * second:
                continue
            # One verse is little to go on: then the sound must fit well, and the next be far behind.
            if len(where[name]) < 2 and (fit(name, n) < 0.6 or sc < 2.5 * second):
                continue
            # A people named after a place ("Gittites") is written with 人, which the
            # Union Version doesn't mark: left to the dictionary.
            if re.search(r"(ite|ites|ians)$", name) and not n.endswith("人"):
                continue
            found[name] = n
            given[n].append(name)
            changed = True
    unsure = [name for name in where if name not in found]
    return found, unsure


def by_order(unsure, found, where, nouns, text):
    """Pair the rest verse by verse: once the names already found are set aside on both sides,
    if a verse has as many English names left as Chinese proper nouns, they pair in order. A name
    is taken when every verse that pairs it agrees."""
    at = collections.defaultdict(list)
    for name, vs in where.items():
        for key in vs:
            at[key].append(name)
    added = {}
    changed = True
    while changed:
        changed = False
        known = {**found, **added}
        votes = collections.defaultdict(collections.Counter)
        for key, names in at.items():
            left = [x for x in names if x not in known]
            if not left or key not in text:
                continue
            en = text[key]
            pos = {x: en.find(x) for x in left}
            if any(p < 0 for p in pos.values()):
                continue                       # a name not written out (a pronoun): no pairing
            done = {known[x] for x in names if x in known}
            zh = [n for n in dict.fromkeys(nouns.get(key, [])) if n not in done]
            if len(zh) != len(left):
                continue
            for x, n in zip(sorted(left, key=pos.get), zh):
                votes[x][n] += 1
        for x, v in votes.items():
            if len(v) == 1 and x in unsure:
                added[x] = next(iter(v))
                unsure.remove(x)
                changed = True
    return added


def main():
    cuv, book_names = cuv_text()
    heb = hebrew_numbering()
    nouns = {}
    for (osis, c, v), ns in cuv.items():
        nouns.setdefault(heb.get((osis, c, v), (osis, c, v)), []).extend(ns)
    where = site_names()
    for name, vs in theographic_names(heb).items():
        where[name] |= vs          # its names the site lacks too: a map or the timeline may show them
    found, unsure = match(where, nouns)
    found.update(by_order(unsure, found, where, nouns, english_text()))
    for k, v in OVERRIDES.items():
        if v is None:
            found.pop(k, None)
        else:
            found[k] = v

    # The Connections page and the 3D web tell people of one name apart by a verse:
    # "Abdi (1 Chronicles 6.29)" -> "亞伯底（歷代志上 6.29）".
    zh_book = {name: book_names[osis] for num, osis, name, t in BOOKS if osis in book_names}
    graph = json.load(open(os.path.join(ROOT, "data", "graph.json"), encoding="utf-8"))
    words = dict(found)
    for n in graph["n"]:
        m = re.fullmatch(r"(.+) \((\d? ?[A-Z][a-z]+(?: [A-Z][a-z]+)*) (\d+\.\d+)\)", n)
        if m and m[1] in found and m[2] in zh_book:
            words[n] = f"{found[m[1]]}（{zh_book[m[2]]} {m[3]}）"

    names = sorted(where)
    print(f"Names: {len(names):,}; in Chinese {sum(1 for n in names if n in found):,}; "
          f"left in English {sum(1 for n in names if n not in found):,}; with the graph's forms, {len(words):,} entries")
    import random
    random.seed(7)
    sample = random.sample(sorted(found), min(40, len(found)))
    print("  ".join(f"{k}={found[k]}" for k in sample))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("// The names of people and places in Traditional Chinese, as the Chinese Union Version\n"
                "// (public domain) spells them. Written by scripts/names_zh.py: don't edit by hand;\n"
                "// corrections go in OVERRIDES there.\n"
                "I18N.add({\n")
        for k in sorted(words):
            f.write(f"{json.dumps(k, ensure_ascii=False)}:{json.dumps(words[k], ensure_ascii=False)},\n")
        f.write("});\n")


if __name__ == "__main__":
    main()
