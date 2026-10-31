# 淺白中文譯本 · The Plain Chinese Translation

A new translation of the Bible into plain, modern Traditional Chinese for native readers, made
directly from the Hebrew, Aramaic and Greek texts in this repository. It is written for readers
in Hong Kong, in the standard written Chinese they read every day, not in Cantonese.

**Status:** Mark drafted; the rest of the Bible in progress from Genesis (see translation-zh/STATUS.md). Every chapter is an AI draft until native readers have reviewed it.

## What carries over from the English translation

The English translation's goals, principles and checklist ([TRANSLATION.md](TRANSLATION.md))
apply here unchanged wherever they are not about English itself:

- **The same sources:** the Leningrad Codex (UXLC 2.6) and the SBL Greek New Testament (v1.2),
  with the same rules for the ketiv/qere, the SBLGNT apparatus and the Textus Receptus.
- **The same verse numbering:** Hebrew numbering in the Old Testament, one line per verse,
  and a verse left out of the SBLGNT is skipped with a note.
- **The same limits:** translate every verse and only what is there; keep the imagery, the
  repetition and the deliberate ambiguity; no harmonizing and no interpretation in the text.
- **The same notes:** where a choice was made, where an idiom is restated, where manuscripts
  differ in meaning, where an Old Testament passage is quoted.
- **The same status steps:** draft → checked → reviewed → approved.

**Translate from the Hebrew and Greek, never from the English.** The English text is not a
source. Its notes are a useful list of the places that need a note (variants, idioms, unclear
words), but each note is written afresh, in Chinese, for Chinese readers. A sentence shaped
like an English sentence is a mistake even if every word is right.

Tools: `python3 scripts/source.py mark 1` prints a chapter's source with its apparatus;
`python3 scripts/translation.py --lang zh` checks every chapter and compiles the books into
`text/chinese/`.

## Goals

1. **Accurate meaning.** As in English: nothing added, left out, softened or sharpened.
2. **Plain Chinese.** Natural modern written Chinese (白話文) that a Hong Kong secondary-school
   student can follow. Short sentences, everyday words, and idioms rendered by their meaning.
   Not the Union Version's early-twentieth-century style, and not Cantonese (冇、佢、嘅).
3. **Familiar where it helps.** Names, and the long-established words of Chinese churches,
   follow the 1919 Chinese Union Version (和合本, public domain), so readers recognize them.
   Its sentences are not copied: the translation is new.

## Decisions (glossary)

Decided by the project owner:

| Source | Rendering | Notes |
|---|---|---|
| θεός, אֱלֹהִים, אֵל, אֱלוֹהַּ | **神** | Never 上帝 (the checker enforces this). Other gods: 神明, 別的神. |
| יהוה (YHWH) | **耶和華** | As in the Union Version. A note at its first occurrence in each chapter: `耶和華：神的名字，希伯來文作 YHWH。` |
| Names of people and places | **as in the Union Version** | 摩西、耶路撒冷、保羅、迦百農、撒但. A name the Union Version lacks is transliterated in its style. |
| Readers | **Hong Kong** | Hong Kong character forms and usage (below). |

Proposed in the pilot, open for review:

| Source | Rendering | Notes |
|---|---|---|
| אֲדֹנָי יְהוִה / יְהוָה אֲדֹנָי | 主耶和華 / 耶和華主 | As in the Union Version. |
| יהוה צְבָאוֹת | 萬軍之耶和華 | Noted at its first occurrence in each chapter: *tseva'ot* means armies. |
| κύριος | 主 | Where a quotation has the divine name: `在希伯來文中，「主」是神的名字 YHWH（耶和華）。` |
| χριστός | 基督 | Also where it is a title (「你是基督」, Mark 8:29): a century of the Union Version has made it one in Chinese. At its first occurrence in each book: `希臘文 *christos*，意思是「受膏者」，就是希伯來文的「彌賽亞」。` 彌賽亞 only where the Greek spells out *Messias* (John 1:41, 4:25), as in the Union Version. |
| מָשִׁיחַ | 受膏者 | A note where later readers heard the Messiah, as in English. |
| πνεῦμα ἅγιον; πνεῦμα ἀκάθαρτον | 聖靈；污靈 | |
| δαιμόνιον | 鬼 | 趕鬼, 被鬼附的人. |
| ὁ υἱὸς τοῦ ἀνθρώπου | 人子 | Noted at its first occurrence in each book. |
| ἡ βασιλεία τοῦ θεοῦ | 神的國 | |
| γραμματεύς | 經學家 | Experts in the Law of Moses. Not 文士, which in modern Chinese means a man of letters (文人雅士); not 律法教師, kept for νομοδιδάσκαλος (Luke 5:17). Noted at its first occurrence in each book: `傳統譯作「文士」`. |
| λεπρός, צָרַעַת | 患嚴重皮膚病的人；嚴重的皮膚病 | Not 痲瘋, which now means Hansen's disease only, and carries a stigma; plain 皮膚病 sounds minor, and loses that it made a person unclean. Noted: `傳統譯作「長大痲瘋」`. On clothing and walls (Leviticus 13–14): 霉斑, noted. |
| חֶסֶד | 慈愛 | Noted where it matters: `希伯來文 *chesed*，指信實不變、守約的愛。` |
| נֶפֶשׁ | 生命、自己、人、心, by context | Not automatically 靈魂. |
| שְׁאוֹל | 陰間 | Noted at its first occurrence in each chapter: the realm of the dead. |
| ἀδελφοί (to a mixed group) | 弟兄姊妹 | 弟兄 for a group of men, as in English. |
| Pronouns for God and Jesus | 他 | Not 祂, though it is common in Hong Kong hymns and devotional writing: the Hebrew and Greek have no such distinction, and 祂 would make the text decide what it leaves open (what Jesus' opponents think of him; whether the angel of the LORD is God, Genesis 16, Judges 6; whether a psalm's king is the Messiah). The Union Version and the Chinese New Version (新譯本) also use 他. |
| ἀμὴν λέγω ὑμῖν | 我實在告訴你們 | |
| οἱ ἄρτοι τῆς προθέσεως, לֶחֶם הַפָּנִים | 供奉在神面前的餅 | Noted: `傳統譯作「陳設餅」`. Never 聖餅, the Catholic word for the communion wafer. |
| Σατανᾶς, הַשָּׂטָן | 撒但 | The Union Version's form, by the decision on names, though most writing outside the Bible has 撒旦. |

Settled while drafting Mark (open for review like the rest):

| Source | Rendering | Notes |
|---|---|---|
| Ῥαββί; Ραββουνι | 拉比；拉波尼 | Noted: 「我的老師」. Διδάσκαλε is 老師 (not the dated 夫子). |
| Καῖσαρ | 該撒 | The Union Version's form, by the decision on names; noted: today usually 凱撒. |
| γέεννα | 地獄 | Noted: *geenna*, from the Valley of Hinnom (欣嫩子谷). |
| ζωὴ αἰώνιος; ἡ ζωή | 永生；生命 | "Enter life" (Mark 9:43, 45) is 進入生命: 永 is not added. |
| σκανδαλίζω | 跌倒；使……絆倒 | By context; noted where the other is possible. |
| συνέδριον; βουλευτής | 議會；議員 | Noted: the Union Version's 公會. |
| λῃστής | 叛亂分子 | Noted: 或譯「強盜」. As the English "rebel". |
| ἀρχιερεῖς; πρεσβύτεροι | 祭司長；長老 | |
| τὰ ἔθνη | 外邦人 | |
| δηνάριον; λεπτόν, κοδράντης | 銀幣；小銅錢 | Values in notes: a day's wage; ¹⁄₆₄ of a denarius. |
| Ὡσαννά | 和散那 | Noted: from Psalm 118:25. |
| ἀδελφοί, ἀδελφαί (of Jesus) | 兄弟；姊妹 | Not 哥哥／弟弟, which would add birth order. |
| Hours | 上午九時左右, 中午十二時, 下午三時 | The original hour in a note. |
| The days of the week | 七日的第一日 | |
| Animals | 牠 | |

Settled while drafting Genesis:

| Source | Rendering | Notes |
|---|---|---|
| יְהוָה אֱלֹהִים | 耶和華神 | Noted in Genesis 2. |
| רָקִיעַ | 穹蒼 | Noted: pictured as a solid dome; not the Union Version's 空氣. |
| תֹּהוּ וָבֹהוּ | 荒涼空虛 | |
| נֶפֶשׁ חַיָּה | 有生命的活物 (animals); 有生命的活人 (Genesis 2:7) | Notes link them. |
| נְפִלִים | 拿非利人 | Noted: traditionally 偉人. |
| בְּנֵי הָאֱלֹהִים | 神的兒子們 | |
| תֵּבָה; כְּרֻבִים | 方舟；基路伯 | |
| תּוֹלְדֹת | 來歷 (a section's heading); 後代、後代的記錄 (a genealogy) | |
| הָאָדָם (Genesis 2–3) | 那人 | Notes where the vowel points read the name 亞當. |
| מוֹעֲדִים | 節期 | |
| Rivers | 希底結 (Tigris), 伯拉河 (Euphrates) | Union Version names; modern names in a note. |
| מִצְרַיִם | 埃及 | Also where the Union Version has 麥西 (Genesis 10). |
| צֹר; דַּמֶּשֶׂק | 推羅；大馬色 | The classic Union Version forms, as in its New Testament; not the 1989 edition's 泰爾, 大馬士革. |
| אֵל עֶלְיוֹן; אֵל שַׁדַּי | 至高的神；全能的神 | Noted at first occurrence in each chapter (*El Elyon*; *El Shaddai*, meaning uncertain). |
| בְּרִית; כָּרַת בְּרִית | 約；立約 | |
| מַלְאַךְ יְהוָה | 耶和華的使者 | |
| שִׁפְחָה | 使女 | |
| הַנֶּגֶב; יָם הַמֶּלַח | 南地；鹽海 | The Dead Sea, noted. |
| Name changes and meanings | 亞伯蘭→亞伯拉罕, 撒萊→撒拉 | The meaning in a note. |
| עֹלָה | 燔祭 | Noted: an offering burned whole. |
| פִּילֶגֶשׁ; אָמָה | 妾；女奴 or 婢女 | A wife's maid (Genesis 29–30): 婢女. |
| שֶׁקֶל | 舍客勒 | About 11.5 g, noted. |
| בְּכֹרָה; מַצֵּבָה | 長子的名分；石柱 | |
| יְהוָה יִרְאֶה; אֵל עוֹלָם | 耶和華以勒；永生神 | |

Settled while drafting Exodus:

| Source | Rendering | Notes |
|---|---|---|
| אֶהְיֶה אֲשֶׁר אֶהְיֶה (3:14) | 我就是我 | Noted: *ehyeh asher ehyeh*; 「我是那我是的」, 「我必是我所是的」, and the Union Version's 「我是自有永有的」. 3:15 notes YHWH, *Yahweh*, and how 耶和華 arose. |
| Pharaoh's heart: חָזַק; כָּבֵד; קָשָׁה | 剛硬；頑固；頑梗 | Three verbs kept apart. |
| נֹגְשִׂים; שֹׁטְרִים | 監工；工頭 | |
| מַטֶּה; תַּנִּין | 杖；大蛇 | נָחָשׁ stays 蛇. |
| חַרְטֻמִּים; מְכַשְּׁפִים; לְהָטִים | 術士；行邪術的；秘術 | |
| זָבַת חָלָב וּדְבָשׁ | 流奶與蜜之地 | |
| יַם־סוּף | 紅海 | Noted: 「蘆葦海」. |
| צִבְאוֹת (Israel's divisions) | 隊伍 | |
| פֶּסַח; מַצּוֹת | 逾越節；無酵餅、無酵節 | The wordplay with *pasach* noted. |
| מִקְרָא קֹדֶשׁ | 聖會 | |
| מָן | 嗎哪 | *man hu* noted (16:15). |
| עֵדֻת; סְגֻלָּה | 法版；珍寶 | |
| שְׁלָמִים; עֹלָה | 平安祭；燔祭 | |
| קִדֵּשׁ | 分別為聖 | |
| אֵל קַנָּא | 忌邪的神 | |
| The Ten Commandments | 不可謀殺 (20:13, noted: traditionally 不可殺人), 不可妄用耶和華你神的名 | How the traditions count them, noted at 20:1. |
| מִשְׁפָּטִים; חֻקִּים | 典章；律例 | |
| מִשְׁכָּן; אֹהֶל מוֹעֵד | 帳幕；會幕 | |
| אֲרוֹן הָעֵדֻת; כַּפֹּרֶת | 法櫃；施恩座 | *kipper* noted. |
| פָּרֹכֶת; מָסָךְ; קְלָעִים | 幔子；門簾；帷子 | |
| קֹדֶשׁ הַקֳּדָשִׁים; מְנוֹרָה | 至聖所；燈臺 | |
| אֵפוֹד; חֹשֶׁן; אוּרִים וְתֻמִּים | 以弗得；胸牌；烏陵和土明 | |
| מִלֵּא יָד | 授予聖職 | Noted: 「充滿手」. |
| חַטָּאת; תְּנוּפָה; אִשֶּׁה | 贖罪祭；搖祭；火祭 | |
| רֵיחַ נִיחֹחַ | 馨香的氣味 | |
| Festivals | 無酵節、收割節、收藏節 | |
| Precious stones, dyes, spices | Modern identifications, as in the English | Traditional names in notes. |
| The law code (Exodus 21–23) | Without quotation marks | A note at 21:1 says who speaks. |
| רַחוּם וְחַנּוּן … רַב־חֶסֶד וֶאֱמֶת (34:6) | 有憐憫、有恩典……充滿慈愛和信實 | Notes on *rachum*, *chesed*, *emet*. |
| נִחַם | 改變心意 | |
| שַׁבַּת שַׁבָּתוֹן | 完全休息的安息日 | |
| אֲשֵׁרִים | 亞舍拉木柱 | |
| חֹדֶשׁ הָאָבִיב; חַג שָׁבֻעֹת | 亞筆月；七七節 | |
| מִנְחָה; אָשָׁם; תּוֹדָה | 素祭；贖愆祭 (noted: 賠償祭)；感恩祭 | |
| קָרְבָּן; תָּמִים | 供物；沒有殘疾的 | |
| טָמֵא; טָהוֹר | 不潔淨；潔淨 | |
| כִּפֶּר | 贖罪 | *kipper* noted: to wipe clean, cleanse, pay a ransom. |
| הִקְטִיר; שָׂרַף | 燒……化為煙；燒掉 | |
| נֶדֶר; נְדָבָה | 還願祭；自願祭 | |
| שֶׁרֶץ; שֶׁקֶץ; נְבֵלָה | 爬物；可憎的動物；自死的牲畜 | |
| מַעַל; בִּשְׁגָגָה | 不忠；無意中 | |
| נָשִׂיא; עַם הָאָרֶץ | 領袖；普通百姓 | |
| אֵשׁ זָרָה | 別樣的火 | Noted: 「凡火」. |
| שֵׁכָר | 啤酒 | Noted: 「濃酒」, brewed from grain (as the English "beer"). |
| צָרַעַת | 嚴重的皮膚病 (people)；霉斑 (cloth, leather, houses) | |
| נֶגַע; זוֹב; נִדָּה | 患處；漏症；經期不潔 | |
| מַיִם חַיִּים | 活水 | |
| עֲזָאזֵל | 阿撒瀉勒 | Noted, with 替罪羊. |
| יוֹם הַכִּפֻּרִים; עִנָּה נֶפֶשׁ | 贖罪日；刻苦己心 | Fasting, noted. |
| גִּלָּה עֶרְוָה | 發生性關係 | Noted: 「露出下體」. |
| תּוֹעֵבָה; זִמָּה | 可憎的事；邪惡的事 | |
| Animals in Leviticus 11, Deuteronomy 14 | Modern identifications, as in the English | Uncertainty and traditional names in notes. |
| Festivals (Leviticus 23) | 逾越節、無酵節、七七節、吹角紀念的日子、贖罪日、住棚節 | Notes link 七七節 with 收割節 and 五旬節, 住棚節 with 收藏節. |
| יוֹבֵל; דְּרוֹר | 禧年；自由 | |
| גְּאֻלָּה; גֹּאֵל | 贖回；至近的親屬 | Noted: 救贖者. |
| גֵּר; תּוֹשָׁב | 寄居的外人；寄居者 | |
| חֵרֶם | 永獻；永獻當滅的 | Noted. |
| אֹבוֹת וְיִדְּעֹנִים | 招魂的和交鬼的 | |
| בָּמוֹת; גִּלּוּלִים; אֱלִילִים | 丘壇；可憎的偶像；虛無的偶像 | |
| מַעֲשֵׂר | 十分之一 | |

Settled while drafting Numbers:

| Source | Rendering | Notes |
|---|---|---|
| מִשְׁפָּחָה; בֵּית אָבוֹת | 宗族；家族 | 家族 noted: 「父家」. As in Exodus 6. |
| פָּקַד; פְּקֻדִים | 數點；被數點的 | Census totals in Chinese numerals with 人: 四萬零五百人, 六十萬零三千五百五十人. |
| צָבָא; צִבְאוֹת | 軍隊；隊伍 | Of the Levites' work (Numbers 4, 8): 服役, noted. |
| דֶּגֶל; מַחֲנֶה | 旗；營 | |
| מִשְׁמֶרֶת; עֲבֹדָה; מַשָּׂא | 職守、職責；工作；抬的東西 | |
| זָר | 外人 | Noted: here anyone not a Levite (or not a priest). |
| אֶלֶף (a clan or unit) | 千萬人 | Noted: 「以色列的千」. |
| נָזִיר; נֵזֶר | 拿細耳人；分別出來、歸給神的頭髮 | |
| מֵי הַמָּרִים הַמְאָרְרִים | 帶來詛咒的苦水 | |
| חֲנֻכָּה | 奉獻禮 | |
| קְעָרָה; מִזְרָק; כַּף (Numbers 7) | 銀盤；銀碗；金碟 | |
| חֲצֹצְרָה; תְּרוּעָה | 號筒；警號 | |
| The priestly blessing (6:24–26) | 願耶和華賜福給你，保護你…… | Three plain lines, each opening 願耶和華. |
| תּוּר; דִּבָּה | 窺探；壞消息 | Of the spies (Numbers 13–14). |
| רוּחַ (given to Moses and the elders) | 靈 | Noted: *ruach*; the same word is 風 in 11:31. |
| מַחְתָּה | 火鼎 | As in Exodus–Leviticus; noted: 「香爐」. |
| מַטֶּה (Numbers 17) | 杖 | Noted: also means 支派. |
| מֵי נִדָּה; פָרָה אֲדֻמָּה | 除污穢的水；紅色的母牛 | |
| נֶאֱסַף אֶל־עַמָּיו | 歸到他的族人那裏 | Noted: died and joined his ancestors. |
| בְּרִית מֶלַח | 鹽約 | Noted: a covenant that cannot be broken. |
| נִכְרַת מֵעַמָּיו | 從族人中被剪除 | Notes refer to 9:13. |
| הֶחֱרִים | 完全毀滅 | Noted: 永獻當滅 (21:2–3). |
| נְחָשִׁים שְׂרָפִים; נְחַשׁ נְחֹשֶׁת | 火蛇；銅蛇 | |
| מָשָׁל (Balaam's oracles) | 詩歌 | 「巴蘭就說出他的詩歌」; noted at 23:7. Oracles kept as poetry in one quotation, parallel lines joined by ，；. |
| נְאֻם | 宣告 | 「比珥的兒子巴蘭的宣告」. |
| אָרַר; קָבַב; זָעַם | 詛咒；咒詛；怒斥 | Two verbs for cursing kept apart. |
| רְאֵם | 野牛 | Noted: traditionally 獨角獸. |
| כּוֹכָב; שֵׁבֶט (24:17) | 星；權杖 | Noted: *shevet* is also 支派; later read of the Messiah. |
| מַלְאַךְ יְהוָה (Numbers 22) | 耶和華的使者 | *le-satan* noted: 作敵對者. |
| קִנְאָה (Phinehas) | 忌恨 | Noted: also 熱心. |
| Clans in the census (Numbers 26) | 屬哈諾的，有哈諾族 | As in Numbers 3; names exactly as the Union Version, even where it spells one Hebrew name two ways (希斯倫 26:6, 希斯崙 26:21). |
| תָּמִיד (offerings) | 經常獻的燔祭 | Noted: *tamid*. |
| רָאשֵׁי חָדְשֵׁיכֶם | 每月的初一 | |
| מְלֶאכֶת עֲבֹדָה | 日常的工作 | As in Leviticus 23. |
| עֲצֶרֶת | 嚴肅的聚會 | As in Leviticus 23:36; noted. |
| נֶדֶר; אִסָּר; הֵפֵר | 許願；約束自己的話；廢除 | Numbers 30; *issar* noted. A vow 有效／無效 (קוּם). |
| מֶכֶס | 稅 | Noted. Spoil totals in Chinese numerals: 羊六十七萬五千隻. |
| מַסָּע; חָנָה (Numbers 33) | 他們從……起行，在……安營 | Kept as one repeated line; camp names exactly as the Union Version (伊坦 33:8 beside 以倘 33:6). |
| עִיר מִקְלָט | 逃城 | |
| רֹצֵחַ | 殺人的 (by accident)；殺人犯 (35:16–21, 30–31) | One Hebrew word, noted at 35:6. |
| גֹּאֵל הַדָּם | 報血仇的 | *go'el* noted (35:12). |
| מִגְרָשׁ | 草場 | Noted: open land around a town. |

Settled while drafting Deuteronomy:

| Source | Rendering | Notes |
|---|---|---|
| Moses' speeches | In quotation marks, as in English | 「 reopened at each chapter and new paragraph; the first speech 1:6–4:40, the second from 5:1 (noted). The LORD's words inside them 『』, a third level 「」. Asides in （）(2:10–12, 20–23; 3:9, 11, 13–14). |
| עֵבֶר הַיַּרְדֵּן | 約旦河東 | Noted: 「在約旦河那邊」. West of the river (3:20, 25): 約旦河那邊. |
| יָרַשׁ; הוֹרִישׁ | 佔領 (land)；趕走 (nations) | |
| שֹׁטְרִים | 官員 | As Numbers 11:16; noted. |
| הָעֲרָבָה; הַשְּׁפֵלָה; הַמִּישֹׁר | 亞拉巴；低地；高原 | Each noted. |
| עֵדֹת | 法度 | Noted. With 律例 (חֻקִּים) and 典章 (מִשְׁפָּטִים). |
| הַמִּצְוָה (singular) | 誡命 | Noted where it means the whole law. |
| The Ten Commandments (Deuteronomy 5) | Exodus 20's wording wherever the Hebrew is the same | 5:12 要謹守 (*shamor*, Exodus 要記念); 5:21 貪圖 (*chamad*) and 貪戀 (*hit'avvah*). Differences noted. |
| The Shema (6:4–5) | 以色列啊，你要聽：耶和華我們的神，耶和華是獨一的。你要全心、全人、全力愛耶和華你的神。 | Other readings of 6:4 noted: 耶和華我們的神是獨一的耶和華；耶和華是我們的神，唯獨耶和華. |
| טֹטָפֹת; מְזוּזֹת | 頭帶；門框 | *tefillin* and *mezuzah* noted. |
| קְשֵׁה־עֹרֶף | 頑梗的百姓 | As Exodus 32:9; noted: 「硬着頸項」. |
| אִמֵּץ לֵב | 使……心固執 | Kept apart from 剛硬, 頑梗 (2:30). |
| דָּגָן, תִּירוֹשׁ, יִצְהָר | 五穀、新酒和新油 | |
| צִרְעָה | 黃蜂 | Noted: uncertain. |
| The law code (Deuteronomy 12–26) | Without quotation marks | Note at 12:1: Moses still speaking, speech ends 26:19. Chapter 11 ends with the speech open. Quotations inside the laws 「」. |
| הַמָּקוֹם אֲשֶׁר יִבְחַר … לְשַׁכֵּן שְׁמוֹ שָׁם | 耶和華所選擇作他名居所的地方 | Noted: 「使他的名住在那裏」. |
| בִּשְׁעָרֶיךָ | 你城裏 | Noted: 「城門裏」. |
| יָתוֹם; אַלְמָנָה; גֵּר | 孤兒；寡婦；寄居的外人 | *yatom* noted. |
| נָכְרִי | 外族人 | Noted: a foreigner not settled in Israel. |
| בִּעַרְתָּ הָרָע | 把那惡從你們中間除掉 | Noted: 「焚除」. |
| הַכֹּהֲנִים הַלְוִיִּם | 利未人祭司 | Noted: 「祭司，就是利未人」. |
| שְׁמִטָּה | 豁免；豁免年 | Noted: *shemittah*, cancelling debts. |
| צְבִי; אַיָּל | 羚羊；鹿 | |
| Animals (Deuteronomy 14) | Leviticus 11's names for the same Hebrew words | Extra quadrupeds 狍子、野山羊、羱羊、劍羚、野綿羊; *ra'ah* 鳶 (as *da'ah*), *dayyah* 黑鳶; noted. |
| לֶחֶם עֹנִי | 困苦的餅 | Noted: 「困苦餅」. |
| קֹסֵם; מְעוֹנֵן; מְנַחֵשׁ; מְכַשֵּׁף; חֹבֵר חָבֶר | 占卜的；觀兆的；用法術的；行邪術的；念咒語的 | Deuteronomy 18:10–11. |
| נָבִיא כָּמֹנִי (18:15, 18) | 一位像我的先知 | Noted: Acts 3:22–23, 7:37. |
| עִיר מִקְלָט; רֹצֵחַ; גֹּאֵל הַדָּם (Deuteronomy 19) | 逃城；殺人的；報血仇的 | As Numbers 35; *rotseach* and *go'el ha-dam* noted. |
| לֹא תָחוֹס עֵינְךָ | 不可憐惜 | Noted: 「你的眼不可憐惜」. |
| נַעֲרָה written נַעַר | 少女 | One note per chapter: written *na'ar*, read *na'arah* (22:15). |
| קְדֵשָׁה; קָדֵשׁ | 廟妓 | Noted (23:18). |
| יִבֵּם; יְבָמָה | 盡夫兄弟的本分；兄弟的遺孀 | *yabbem* noted (25:5). |
| אֲרַם נַהֲרַיִם | 兩河之間的亞蘭 | As Genesis 24:10 (Union Version 美索不達米亞); noted. |
| אֲרַמִּי אֹבֵד אָבִי (26:5) | 我祖先是一個流浪的亞蘭人 | *oved* noted: 流浪的 or 將要滅亡的. |
| The curses of 27:15–26 | 『……的，必受咒詛！』眾民都要說：『阿們！』 | One formula throughout; 『』 because Moses' speech is open. 27:15 回答說 (*ve'anu*). |
| אָמֵן | 阿們 | Noted: 確實如此，願它成就. |
| בָּרוּךְ; אָרוּר (28:3–6, 16–19) | 必蒙福；必受咒詛 | The two lists kept word for word parallel. |
| פְּרִי בִטְנְךָ, פְּרִי אַדְמָתְךָ | 你身體所生的、你土地所出產的 | Also 28:53 and 30:9. |
| אָלָה | 誓言 (with 約)；咒詛 | Noted at 29:11. |
| The third speech (29:1–30:20) | In quotation marks | Noted at 29:1 and 30:20. |
| The Song of Moses (32:1–43); the Blessing (33:2–29) | Poetry without quotation marks | The LORD's words in the song unmarked (noted 32:20); 論……，他說： for each tribe. |
| צוּר (of God) | 磐石 | Noted at 32:4: *tsur*. |
| עֶלְיוֹן (alone); שֵׁדִים | 至高者；鬼魔 | |
| יְשֻׁרוּן | 耶書崙 | Noted: from *yashar*. |
| הוֹשֵׁעַ (32:44) | 何西阿 | Noted: Joshua's earlier name; the Union Version has 約書亞. |

Settled while drafting Joshua:

| Source | Rendering | Notes |
|---|---|---|
| אֲרוֹן הַבְּרִית; אֲרוֹן הָעֵדֻת | 約櫃；法櫃 | *aron* noted at 3:3; 法櫃 explained at 4:16. |
| חֵרֶם; הֶחֱרִים | 永獻當滅的（物）；完全毀滅 | *cherem*, *charam* noted at the first occurrence in each chapter. |
| שׁוֹפְרוֹת הַיּוֹבְלִים; הֵרִיעַ, תְּרוּעָה (of the people) | 羊角號；吶喊 | |
| שַׂר־צְבָא־יְהוָה | 耶和華軍隊的元帥 | *tsava* noted. |
| זוֹנָה (Rahab) | 妓女 | Noted: the Targum's 開旅店的. |
| כִּידוֹן | 短槍 | Noted: or a curved sword. |
| תֵּל | 廢墟堆 (8:28)；土丘 (11:13) | Noted. |
| נַחַל | 谷 (亞嫩谷) | *nachal* noted. |
| הָאֲשֵׁדוֹת; הָהָר הֶחָלָק | 山坡；哈拉山 | |
| עֲנָקִים; רְפָאִים | 亞衲人；利乏音人 | |
| סֵפֶר הַיָּשָׁר | 《雅煞珥書》 | Book titles in 《》. |
| The list of kings (12:9–24) | 一個是……王 | Uniform, names exactly as the Union Version. |
| Place names of two words ("Valley of X", "Mount X") | As in the Union Version's text | 亞割谷, 米斯巴平原, 黎巴嫩平原, 多珥山岡, 米倫水, 除皮山. |
| Boundaries (Joshua 15–19): יָצָא; עָבַר; עָלָה, יָרַד; נָסַב; תָּאַר; תֹּצְאֹת | 伸到；經過；上到，下到；轉向；延伸到；盡頭在 | One verb, one rendering, throughout. |
| Town lists: עָרִים … וְחַצְרֵיהֶן; בְּנוֹת (of a town) | 一共二十九座城，連同屬城的村莊；屬它的鎮 | Counts in Chinese numerals; *chatserim* and 「女兒們」 noted. |
| X וְאֶת־מִגְרָשֶׁהָ (Joshua 21) | X和屬它的草場 | Uniform through the list. |
| גּוֹרָל | 籤；抽籤所得的地 | 「第二籤抽出來是西緬」. |
| עִיר מִקְלַט הָרֹצֵחַ | 殺人者的逃城 | As Numbers 35; *rotseach* noted. |
| A name the Leningrad Codex spells unlike the Union Version | The Hebrew's form in the text, the Union Version's in a note | 魯瑪 (15:52, 和合本「度瑪」); 基法‧阿摩拿 (18:24, qere; ketiv as 和合本). |
| הַנָּהָר | 大河 | Noted: the Euphrates. |
| אֲנִי וּבֵיתִי נַעֲבֹד אֶת־יְהוָה (24:15) | 至於我和我一家，我們必事奉耶和華 | |

Settled while drafting Judges:

| Source | Rendering | Notes |
|---|---|---|
| שֹׁפֵט; שָׁפַט אֶת־יִשְׂרָאֵל | 士師；作以色列的士師 | Noted at 2:16 (*shofetim*): leaders and deliverers who also governed, not only judges in court. God as הַשֹּׁפֵט (11:27): 審判者, noted as the same word. |
| וַיַּעֲשׂוּ בְנֵי־יִשְׂרָאֵל אֶת־הָרַע בְּעֵינֵי יְהוָה | 以色列人（又）行耶和華眼中看為惡的事 | Word for word the same each time. |
| The cycle: וַיִּחַר־אַף יְהוָה בְּיִשְׂרָאֵל; מָכַר בְּיַד; נָתַן בְּיַד | 耶和華的怒氣向以色列發作；把他們賣給；交在……手中 | 賣給 noted: 「賣在……手中」. |
| זָעַק אֶל־יְהוָה; הֵקִים מוֹשִׁיעַ | 以色列人向耶和華呼求；耶和華為他們興起一位拯救者 | |
| וַתִּשְׁקֹט הָאָרֶץ; נִכְנַע | 那地太平了……年；被制伏 | 太平 noted: 「安靜了」. |
| רוּחַ יְהוָה (הָיְתָה) עַל; לָבְשָׁה | 耶和華的靈臨到；籠罩 (6:34) | *ruach* noted; 籠罩 noted: 「穿上」. |
| הַבְּעָלִים; הָעַשְׁתָּרוֹת; הָאֲשֵׁרוֹת | 眾巴力；亞斯她錄；眾亞舍拉 | Plurals explained at 2:11, 13; 3:7. A single אֲשֵׁרָה: 亞舍拉木柱. |
| בְּנֵי־קֶדֶם | 東方人 | Noted: 「東方的子孫」. |
| בַּעֲלֵי שְׁכֶם | 示劍的領袖 | Noted at 9:2: *ba'alei Shekhem*. |
| The Song of Deborah (5:2–31) | Poetry without quotation marks, as Deuteronomy 32 | 5:1 ends 說：; words quoted inside the song 「」; a note on each hard line. |
| Gaal (9:26–41) | 迦勒 | The Union Version's form; noted as not Caleb (*Ga'al*, not *Kalev*). |
| אֵל בְּרִית (9:46) | 伊勒‧比利土 | The Hebrew's form, as in Joshua; noted: 和合本作「巴力‧比利土」. |
| שִׁבֹּלֶת / סִבֹּלֶת (12:6) | 示播列／西播列 | The sound difference kept visible; noted: *sh* said as *s*. |
| צָלְחָה רוּחַ יְהוָה עַל | 耶和華的靈猛然臨到 | *tsalach* noted (14:6, 19; 15:14). Kept apart from 臨到 (הָיְתָה עַל). |
| נְזִיר אֱלֹהִים (Samson) | 歸給神的拿細耳人 | As Numbers 6; *nazir* noted (13:5; 16:17). |
| סַרְנֵי פְלִשְׁתִּים | 非利士人的首領 | *seranim* noted (3:3; 16:5). |
| אֶלֶף וּמֵאָה כֶסֶף (no unit) | 一千一百塊銀子 | Noted: probably shekels, with the weight. |
| פֶּסֶל וּמַסֵּכָה; תְּרָפִים | 雕刻的像和鑄造的像；家中的神像 | Judges 17–18; *teraphim* noted. |
| בַּיָּמִים הָהֵם אֵין מֶלֶךְ בְּיִשְׂרָאֵל; אִישׁ הַיָּשָׁר בְּעֵינָיו יַעֲשֶׂה | 那時以色列中沒有王，各人隨自己的意思行事 | Identical at 17:6, 21:25 (18:1, 19:1 the first clause only); noted 直譯：「各人做自己眼中看為正的事」, linked to 14:3 (她在我眼中看為正 → 我喜歡她). |
| The suspended nun (18:30) | 瑪拿西 in the text | 摩西 in a note, with the scribal mark. |
| בְּנֵי־בְלִיַּעַל | 無賴之徒 | As Deuteronomy 13:14; *beliyya'al* noted. |
| נְבָלָה; זִמָּה וּנְבָלָה | 醜惡的事；淫亂醜惡的事 | *nevalah* noted (19:23; 20:6). |

Settled while drafting Ruth:

| Source | Rendering | Notes |
|---|---|---|
| גֹּאֵל; גָּאַל | 至近的親屬；盡至近親屬的本分、贖 | As Leviticus 25; *go'el* noted at 2:20 with 「救贖者」. |
| חֶסֶד | 慈愛 | The glossary note at 1:8, 2:20, 3:10. |
| שַׁדַּי (alone) | 全能者 | Noted: *Shaddai*, meaning uncertain (1:20). |
| כֹּה יַעֲשֶׂה יְהוָה לִי וְכֹה יֹסִיף | 願耶和華（神）重重懲罰我（你） | Oath formula; literal wording in a note (Ruth 1:17; 1 Samuel 3:17). |
| גִּבּוֹר חַיִל; אֵשֶׁת חַיִל | 有地位的人；賢德的女子 | *chayil* noted and linked (2:1; 3:11; 4:11). |
| לִקֵּט | 拾麥穗 | Gleaning law noted (2:2). |
| כָּנָף (2:12; 3:9) | 翅膀；衣襟 | The one word noted. |
| נָעֳמִי; מָרָא | 拿俄米；瑪拉 | Meanings noted: 「甜美」, 「苦」 (1:20). |

Settled while drafting 1 Samuel:

| Source | Rendering | Notes |
|---|---|---|
| יְהוָה צְבָאוֹת | 萬軍之耶和華 | *tseva'ot* noted at the first occurrence in each chapter (1:3, the first in the Bible). |
| Hannah's song (2:1–10) | Poetry without quotation marks | 2:1 opens 哈拿禱告說：. |
| שָׁאַל; שָׁאוּל | 求；歸給 | The play on Samuel's and Saul's names noted (1:20, 28; 2:20). |
| מְשִׁיחוֹ (2:10, 35) | 他的受膏者 | *mashiach* noted: the king. |
| הֵיכַל יְהוָה | 耶和華的殿 | *heikhal* noted (1:9). |
| אֲרוֹן בְּרִית יְהוָה; אֲרוֹן הָאֱלֹהִים | 耶和華的約櫃；神的約櫃 | |
| יֹשֵׁב הַכְּרֻבִים | 坐在基路伯上的 | Noted: or 「坐在……之間」. |
| עֳפָלִים / טְחֹרִים | 腫瘤 | Ketiv and qere noted (5:6; 6:4); traditionally 痔瘡. |
| אָשָׁם (1 Samuel 6) | 贖愆祭 | Noted: 賠償祭. |
| אִי־כָבוֹד | 以迦博 | Noted: 「榮耀在哪裏？」 or 「沒有榮耀」 (4:21). |
| Text-critical notes | 七十士譯本；4QSam-a（一份撒母耳記的死海古卷） | As the English has them. |
| שָׁפַט (Samuel; the king, 8:5, 20) | 作以色列的士師；治理 | *shafat* noted. |
| מֶלֶךְ; מִשְׁפַּט הַמֶּלֶךְ; מִשְׁפַּט הַמְּלֻכָה | 王；王的權利；王位的規例 | *mishpat* noted (8:9; 10:25). |
| רֹאֶה; נָבִיא | 先見；先知 | 9:9 in （）, both noted. |
| נָגִיד | 領袖 | Noted: 和合本「君」 (9:16). |
| מָשַׁח; מְשִׁיחוֹ | 膏；他的受膏者 | Noted 10:1, 16:13; 12:3, 16:6. |
| נְצִיב; מַצָּב | 駐軍；防營、防軍 | *netsiv* noted (10:5). |
| יְחִי הַמֶּלֶךְ | 願王萬歲 | |
| נֹשֵׂא כֵלָיו | 替他拿兵器的人 | |
| רוּחַ רָעָה מֵאֵת יְהוָה | 從耶和華那裏來的惡靈 | Noted: 使人受害的靈 (16:14). |
| נִחַם (God, 1 Samuel 15) | 後悔；改變心意 (15:29) | One verb, noted. |
| אִישׁ הַבֵּנַיִם | 出陣挑戰的勇士 | *ish ha-benayim* noted (17:4). |
| חֵרֵף; מַעַרְכוֹת; מַעֲרָכָה | 辱罵；軍隊；戰陣 | 1 Samuel 17. |
| קֶלַע | 機弦 | As Judges 20:16. |
| The women's song (18:7; 21:12) | 「掃羅殺敵千千，大衛殺敵萬萬。」 | Literal wording and ketiv/qere noted. |
| מַשְׂכִּיל | 成功 | *maskil* noted (18:5). |
| הִתְנַבֵּא (Saul, 18:10) | 胡言亂語 | Noted: 「說預言」; 19:20–24 說預言, as 10:5. |
| מְצוּדָה, מְצָדוֹת | 要塞 | |
| שָׁאַל בַּיהוָה / בֵּאלֹהִים | 求問耶和華／神 | |
| לֶחֶם קֹדֶשׁ (21:5–7) | 分別為聖的餅 | Never 聖餅. With 供奉在神面前的餅 (21:7) and the note on Mark 2:26 (亞比亞他). |
| מְשִׁיחַ יְהוָה | 耶和華的受膏者 | Noted (24:7). |
| Names the Union Version translates (חֹרְשָׁה, הַיְשִׁימוֹן) | 何烈沙；耶示門 | Transliterated; its 樹林, 曠野 in notes. |
| נָבָל; נְבָלָה (25:25) | 拿八；愚頑 | The wordplay noted: *Naval*, 「愚頑人」. |
| אָמָה; שִׁפְחָה (a woman of herself) | 婢女 | Both noted as humble self-reference (25:24, 27; 28:21). |
| אֵשֶׁת בַּעֲלַת־אוֹב; קָסַם בָּאוֹב | 招魂的婦人；招魂占卜 | As Leviticus 19:31 (招魂的); *ov* noted (28:7–8). Not 「巫婆」. |
| אֱלֹהִים (28:13) | 神靈 | Noted: god(s) or a spirit being; the verb is plural. |
| שָׂרֵי פְלִשְׁתִּים; סַרְנֵי פְלִשְׁתִּים | 非利士人的將領；非利士人的首領 | Kept apart (1 Samuel 29). |
| גְּדוּד | （這幫）匪徒 | *gedud* noted (30:8). |
| שָׁלָל; אִישׁ חַיִל | 掠物；勇士 | |

Settled while drafting 2 Samuel:

| Source | Rendering | Notes |
|---|---|---|
| 1 Samuel's terms | 耶和華的受膏者；求問耶和華；萬軍之耶和華 | Unchanged, with the same notes (1:14; 2:1; 6:2). |
| David's lament (1:19–27) | Poetry without quotation marks | 1:18 ends with 《雅煞珥書》上：; the title 〈弓歌〉 in 〈〉, noted. |
| הַצְּבִי (1:19) | 你的榮耀 | Noted: also 「羚羊」. |
| אִישׁ־בֹּשֶׁת; מְפִיבֹשֶׁת | 伊施波設；米非波設 | *boshet* for *baal* noted (2:8; 4:4), with 伊施‧巴力, 米力‧巴力. |
| חֹמֶשׁ | 肚腹 | Noted: traditionally 第五根肋骨 (2:23). |
| מְצֻדַת צִיּוֹן; עִיר דָּוִד | 錫安的要塞；大衛城 | |
| The blind and the lame (5:6–8) | 連瞎子和瘸子也能把你趕走；水道 | The other reading of 5:6, *tsinnor*, the ketiv and 「那殿」 noted. |
| יְהוָה אֱלֹהֵי צְבָאוֹת | 耶和華萬軍之神 | *tseva'ot* noted (5:10). |
| אֲדֹנָי יְהוִה | 主耶和華 | Noted at its first occurrence in each chapter (7:18). |
| בַּיִת (2 Samuel 7) | 宮殿 (the king's)；殿宇 (for the LORD)；家室 (David's line) | The one word and the wordplay noted at 7:11. |
| זֶרַע (7:12) | 後裔 | Noted: 「種子」. |
| מַזְכִּיר; סוֹפֵר | 史官；書記 | Noted (8:16–17). |
| הַכְּרֵתִי וְהַפְּלֵתִי | 基利提人和比利提人 | Noted: David's foreign guard (8:18). |
| Chronicles parallels | 歷代志上…作「……」 | Wherever the English notes them. |
| הֲדַדְעֶזֶר | 哈大底謝 | As the Union Version in Samuel and Kings (歷代志 has 哈大利謝). |
| הַנָּהָר (10:16) | 大河 | As Joshua; noted: the Euphrates. |
| נִבְאַשׁ בְּ | 惹……憎恨；使……憎恨你 | Noted: 「發臭」 (10:6; 16:21). |
| בּוֹא אֶל (sexual) | 同房 | Noted: 「進到……那裏」 (3:7; 16:21). |
| עִנָּה (2 Samuel 13) | 玷辱 | *innah* noted (13:12). |
| נְבָלָה; נְבָלִים (13:12–13) | 醜惡的事；愚頑無恥的人 | As Judges 19:23; *nevalah* and the shared root noted. |
| גֹּאֵל הַדָּם (14:11) | 報血仇的 | As Numbers 35; *go'el ha-dam* noted. |
| מַלְאַךְ הָאֱלֹהִים (14:17, 20) | 神的使者 | Noted: 或譯「神的信差」. |
| כִּכָּר | 他連得 | About 34 kg, noted (12:30). |
| חֶסֶד (16:17, between friends) | 情義 | The glossary note on *chesed*. |
| 19:1 (Union Version 18:33) | 我兒押沙龍啊！我兒，我兒押沙龍啊！ | Numbering noted at 18:32 and 19:1 (19:2–44 = 和合本 19:1–43). |
| הַכּוּשִׁי (18:21–32) | 古實人 | Noted: 和合本 takes it as the name 古示. |
| David's song (2 Samuel 22) | Poetry without quotation marks, one verse per line | 22:2 opens 他說：. Differences from Psalm 18 noted as 詩篇18篇3節（和合本作18篇2節）; Psalm 18 to follow this wording where the Hebrew is the same. |
| סַלְעִי; מְצוּדָתִי; מִשְׂגַּבִּי; מָגִנִּי; קֶרֶן יִשְׁעִי (22:2–3) | 我的巖石；我的要塞；我的高臺；我的盾牌；我拯救的角 | צוּר stays 磐石. |
| נְאֻם (23:1) | 宣告 | As Numbers 24; *ne'um* noted. David's last words (23:1–7) poetry. |
| הַשְּׁלֹשָׁה; הַשְּׁלֹשִׁים (23:8–39) | 三個勇士；三十個勇士 | Ketiv/qere and *ha-shalishi* (軍官) noted. Names exactly as the Union Version; Chronicles differences noted. |
| הָרָפָה (21:16–22) | 拉法的後代 | *ha-rapha* noted with 利乏音人; 和合本「偉人」. |
| הוֹקִיעַ (21:6, 9, 13) | 處決 | Noted: uncertain (impale, hang, expose). |
| הַמַּלְאָךְ (24:16–17) | 天使 | *mal'akh* noted; מַלְאַךְ יְהוָה stays 耶和華的使者. |

Settled while drafting 1 Kings:

| Source | Rendering | Notes |
|---|---|---|
| Samuel's terms | 萬軍之耶和華；耶和華的受膏者；基利提人和比利提人；史官；書記；願王萬歲 | Unchanged, with the same notes. |
| וַיִּשְׁכַּב X עִם־אֲבֹתָיו וַיִּקָּבֵר בְּעִיר דָּוִד | X與他的祖先同睡，葬在大衛城 | Fixed regnal formula for all of Kings; noted at its first occurrence in each book (2:10): 「與他的祖先一同躺臥」, a way of speaking of death. In speech (1:21) the same words. |
| מָלַךְ X עַל־יִשְׂרָאֵל N שָׁנָה | X作以色列王N年 | 2:11. |
| נָגִיד | 領袖 | As 1 Samuel 9:16; noted 和合本「君」 (1:35). |
| שׁוֹפָר | 羊角號 | As Joshua (1:34). |
| נִצָּבִים (Solomon's districts) | 地方長官 | *nitsavim* noted (4:5). מַס: 服勞役的人 (4:6; 5:27). |
| Numbering of 1 Kings 5 | 5:1–14 = 和合本 4:21–34；5:15–32 = 和合本 5:1–18 | Noted at 4:20 and 5:1; other references give both, as 5章22節（和合本作5章8節）. |
| Temple: הֵיכָל; דְּבִיר; אוּלָם; יָצִיעַ; צְלָעוֹת | 大殿；內殿；前廊；旁屋；廂房 | Each noted (6:3–5); 大殿 corresponds to the tabernacle's 聖所, and 8:8, 10 (הַקֹּדֶשׁ) have 聖所. |
| קֹדֶשׁ הַקֳּדָשִׁים; כְּרוּבִים; כִּיּוֹר; לֶחֶם הַפָּנִים; מַחְתּוֹת | 至聖所；基路伯；洗濯盆；供奉在神面前的餅；火鼎 | The tabernacle's terms (Exodus); the other vessels too (盆、鏟子、盤子、碟子、燈剪). |
| Temple measurements (1 Kings 6–7) | Chinese numerals in the text (二十肘, 一肘半, 半肘) | Metric values in notes (一肘約 45 厘米; 一掌寬約 7.5 厘米; 一罷特約 22 公升). |
| הַיָּם (7:23–44) | 海 | Noted: 和合本「銅海」. |
| מְכֹנוֹת; כֹּתָרוֹת; שְׂבָכָה | 盆座；柱頂；網子 | 1 Kings 7. |
| חִירָם (the craftsman, 7:13) | 戶蘭 | As the Union Version, apart from King Hiram 希蘭; noted. |
| בְּרוֹשׁ | 松木 | As 2 Samuel 6:5; *berosh* noted. |
| כֹּר | 柯珥 | About 220 liters, noted (和合本「歌珥」). |
| Months: זִו; בּוּל; אֵתָנִים | 西弗月；布勒月；以他念月 | With 二月, 八月, 七月 as the Hebrew has them; the modern months noted. |
| Solomon's prayer (8:23–53) | In quotation marks, one paragraph per petition | The petitions keep one shape: 求你在天上（你居住的地方）垂聽……; עָשָׂה מִשְׁפָּט 伸張公義 (8:45, 49, 59). |
| וְיֶתֶר דִּבְרֵי X … הֲלֹא־הֵם כְּתוּבִים עַל־סֵפֶר דִּבְרֵי הַיָּמִים לְמַלְכֵי יִשְׂרָאֵל / יְהוּדָה | X其餘的事，……，都寫在《以色列諸王記》／《猶大諸王記》上 | Fixed formula, a statement also where the Hebrew asks (直譯「不是寫在……上嗎？」 noted at 11:41); the title noted at its first occurrence in each chapter: 「……諸王的日子的事的書」, lost. 《所羅門記》 (11:41). |
| וַיִּשְׁכַּב … וַיִּקָּבֵר עִם־אֲבֹתָיו | X與他的祖先同睡，與他的祖先一同葬在…… | Without burial (14:20): 就與他的祖先同睡. 接續他作王 for וַיִּמְלֹךְ … תַּחְתָּיו. |
| Synchronisms: בִּשְׁנַת N לְX מֶלֶךְ יְהוּדָה מָלַךְ Y עַל־יִשְׂרָאֵל | 猶大王X第N年，Y登基作以色列王 | The same for Judah's kings (15:1, 9); the length follows: 作以色列王N年 / 他在耶路撒冷作王N年. |
| בֶּן־N שָׁנָה X בְּמָלְכוֹ | X開始作王的時候是N歲 | As 2 Samuel 5:4 (14:21). |
| עָשָׂה הָרַע / הַיָּשָׁר בְּעֵינֵי יְהוָה | 行耶和華眼中看為惡的事；行耶和華眼中看為正的事 | Word for word as Judges, every time. |
| הָלַךְ בְּדֶרֶךְ … וּבְחַטָּאתוֹ אֲשֶׁר הֶחֱטִיא אֶת־יִשְׂרָאֵל | 行……所行的道，犯……使以色列人陷入的罪 | 15:26, 34. 耶羅波安所犯的罪，又使以色列人犯罪 (14:16; 15:30). |
| לֵבָב שָׁלֵם עִם־יְהוָה | 心……完全忠於耶和華 | As 8:61 (11:4; 15:3, 14). |
| אָב (of a remote ancestor) | 祖先 | 「他父親」 noted (15:3, 11, 24). |
| עֶגְלֵי זָהָב (Jeroboam) | 金牛犢 | 12:28 「以色列啊，看哪，這就是領你從埃及地上來的神！」 as Exodus 32:4, plural noted. |
| שָׂטָן (11:14, 23, 25) | 敵對者 | *satan* noted, as 5:18. |
| עַשְׁתֹּרֶת; מִלְכֹּם; כְּמוֹשׁ; מֹלֶךְ; שִׁקּוּץ | 亞斯她錄；米勒公；基抹；摩洛；可憎的神 | 1 Kings 11. |
| גְּבִירָה | 王后 (11:19)；太后 (15:13) | *gevirah* noted. |
| נִיר (11:36; 15:4) | 一盞燈 | *nir* noted. |
| אִישׁ הָאֱלֹהִים | 神人 | Noted: a title for a prophet. |
| בָּמוֹת; בֵּית בָּמוֹת; מַצֵּבוֹת; אֲשֵׁרִים; קָדֵשׁ; גִּלֻּלִים | 丘壇；丘壇的廟宇；石柱；亞舍拉木柱；廟妓；可憎的偶像 | As the Pentateuch's terms. |
| הָרָצִים | 護衞兵 | Noted: 「奔跑的人」 (14:27). |
| מַשְׁתִּין בְּקִיר | 男子 | Noted: 「靠牆小便的」 (14:10). |
| הֲבָלִים | 虛無的偶像 | *havalim* noted: 「氣、虛空」 (16:13, 26). |
| הַבַּעַל; הַבְּעָלִים; נְבִיאֵי הַבַּעַל / הָאֲשֵׁרָה | 巴力；眾巴力；巴力的先知／亞舍拉的先知 | Baal noted at 16:31; plural as Judges 2:11 (18:18). |
| חַי־יְהוָה … אֲשֶׁר עָמַדְתִּי לְפָנָיו | 我指着永活的耶和華……起誓，就是我所事奉的那位 | 「我站在他面前的」 noted (17:1; 18:15). |
| פֹּסְחִים עַל־שְׁתֵּי הַסְּעִפִּים (18:21) | 你們在兩者之間搖擺不定，要到幾時呢？ | Noted: 「在兩根樹枝上跛行」, *se'ippim*, 和合本「心持兩意」; 18:26 跳來跳去, the same verb noted. |
| קוֹל דְּמָמָה דַקָּה (19:12) | 輕微寂靜的聲音 | Noted: 「稀薄的寂靜的聲音」; 和合本「微小的聲音」. |
| יְהוָה אֱלֹהֵי צְבָאוֹת | 耶和華萬軍之神 | As 2 Samuel 5:10; noted (19:10). |
| כֹּה יַעֲשׂוּן אֱלֹהִים (plural verb) | 願眾神明重重懲罰我 | Noted (19:2; 20:10). |
| בְּנֵי הַנְּבִיאִים | 先知門徒 | Noted: 「先知的兒子們」 (20:35). |
| אִישׁ חֶרְמִי (20:42) | 我定為當滅的人 | *cherem* noted. |
| בְּנֵי־בְלִיַּעַל; בֵּרַךְ (for "cursed") | 無賴之徒；詛咒 | The euphemism 「祝福」 noted (21:10). |
| רוּחַ שֶׁקֶר (22:22–23) | 謊言的靈 | *ruach* noted. |
| Numbering of 1 Kings 22 | 22:44–54 = 和合本 22:43b–53 | Noted at 22:44. |

Settled while drafting 2 Kings:

| Source | Rendering | Notes |
|---|---|---|
| 1 Kings' terms and regnal formulas | 與他的祖先同睡，與他的祖先一同葬在大衛城；猶大王X第N年，Y登基作王；X開始作王的時候是N歲；都寫在《以色列諸王記》／《猶大諸王記》上 | Unchanged; the burial note at its first occurrence in the book (8:24), the title note at its first occurrence in each chapter. A king of Judah 登基作王 where the Hebrew does not repeat 猶大 (8:16, 25). |
| יְהוֹרָם; יוֹרָם | 約蘭 | Both forms of the name, for both kings, as the Union Version; noted (1:17; 8:16, 21; 9:15). |
| בַּעַל זְבוּב | 巴力‧西卜 | Noted: 「蒼蠅之主」, mocking *Baal-zebul*; 別西卜 (馬可福音3章22節). |
| דָּרַשׁ בְּ | 求問 | *darash be-* noted (1:2). |
| שַׂר־חֲמִשִּׁים | 五十夫長 | |
| חַי־יְהוָה וְחֵי־נַפְשְׁךָ | 我指着永活的耶和華，又指着你的性命起誓 | As 1 Samuel 25:26 (2:2; 4:30). |
| אֲדֹנֶיךָ (a prophet's master) | 你的師傅 | 2:3, 5, 16. |
| פִּי־שְׁנַיִם (2:9) | 加倍 | Noted: 「兩個口」, the firstborn's share. |
| רֶכֶב יִשְׂרָאֵל וּפָרָשָׁיו (2:12) | 以色列的戰車和騎兵 | For 13:14 too. |
| אַדֶּרֶת | 外衣 | |
| מְצֹרָע | 患了嚴重的皮膚病；患嚴重皮膚病的人 | The glossary note at 5:1; 7:3 refers to it. |
| אֲרָם | 亞蘭；亞蘭人 | Noted at 5:1: 傳統譯作「敘利亞」. |
| שָׁלִישׁ | 軍官 | *shalish* noted (7:2; 9:25). |
| סָרִיס | 官員 | Noted: also 太監 (8:6; 9:32). |
| Units: סְאָה; קַב; כִּכָּר | 細亞；卡布；他連得 | Values in notes (約 7 公升；約 1.2 公升, 和合本「升」；約 34 公斤). |
| חֲרֵי יוֹנִים / דִּבְיוֹנִים (6:25) | 鴿子糞 | Ketiv and the politer qere noted; perhaps a name for a cheap food. |
| כֹּה יַעֲשֶׂה־לִּי אֱלֹהִים וְכֹה יוֹסִף (singular verb) | 願神重重懲罰我 | As Ruth 1:17 (6:31). |
| נְאֻם־יְהוָה (in an oracle) | 這是耶和華的宣告 | *ne'um* noted (9:26). |
| חֲגֹר מָתְנֶיךָ | 你束上腰 | Noted: tucking the robe into the belt (4:29; 9:1). |
| הֲשָׁלוֹם (Jehu, 9:17–31) | 平安嗎？ | |
| Israel's synchronisms (10–17) | 猶大王X第N年，Y在撒馬利亞登基作以色列王，作王N年 | Judah's: 以色列王X第N年，Y登基作猶大王; where the length is placed after Samaria, 他在撒馬利亞作王N年 (15:13, 17). Months: 作王六個月, 一個月. |
| הִנָּם כְּתוּבִים | 都寫在……上 | As the question form; noted once (15:6). |
| יְהוֹאָשׁ; יוֹאָשׁ; יוֹאָחָז | 約阿施；約哈斯 | Both forms, both kings named Joash, one rendering; noted (11:2; 12:1; 13:10; 14:1). |
| Numbering of 2 Kings 12 | 12:1 = 和合本 11:21；12:2–22 = 和合本 12:1–21 | Noted at 11:20 and 12:1. |
| עֲזַרְיָה; עֻזִּיָּה | 亞撒利雅；烏西雅 | As the Hebrew has each; noted (14:21; 15:13). |
| פּוּל; תִּגְלַת פִּלְאֶסֶר | 普勒；提革拉‧毘列色 | The classic 毘, not the 1989 edition's 毗; noted as one king (15:19, 29). |
| רָצִים; כָּרִי; עַם הָאָרֶץ (2 Kings 11) | 護衞兵；迦利人；國中的百姓 | *am ha-arets* noted (11:14). |
| חֻקּוֹת; מִשְׁפַּט (2 Kings 17) | 律例；規矩 | One rendering each through 17:7–41, so the repetitions stand; *mishpat* noted (17:26). |
| יָרֵא (worship, 2 Kings 17) | 敬畏 | Noted: 「懼怕」 (17:7). |
| הֶעֱבִיר בָּאֵשׁ | 使……經火 | Noted: burned as a sacrifice (16:3; 17:17). |

## Style

**Characters and words.** Plain words over the Union Version's literary ones (吊下去, not 縋下來). Hong Kong standard forms: 裏 (not 裡), 着 for the particle (看着、
帶着; 著 only in 顯著、著作), 衞, 甚麼 (not 什麼), 只 (not 祇), 吃 (not 喫). Hong Kong usage where it differs
from Taiwan or the mainland. The checker rejects 裡.

**Punctuation.** Full-width: ，。、；：？！ Quotations take 「」, a quotation inside one 『』.
A speech that runs over several verses or paragraphs reopens 「 at each new paragraph and closes
only where it ends, as in English. Dashes ——, ellipses …… .

**Numbers.** Chinese numerals in the text, as Chinese Bibles have them: 四十天, 一百二十歲,
一千四百輛戰車, 四萬六千五百. Modern measurements and dates in notes use digits: 約 45 厘米.

**Units, money and time.** As in English: the original unit in the text, its value in a note at
its first occurrence in each chapter (`一肘約 45 厘米`). Coins: 銀幣 (denarius), with
`約為散工一天的工資`. Time of day in modern terms (下午四時左右), the original in a note.

**Narrative.** Chinese has no tenses; use 了、過、就 as natural Chinese needs, not to mirror Greek
aspect. Mark's εὐθύς is 立刻、一……就 or 正在那時, as the sentence requires.

**Notes.** Markdown footnotes, numbered within the chapter. The marker goes straight after the
word or phrase, before Chinese punctuation (`基督[^1]。`); a note on a whole quotation goes after
its closing 」. Standard forms:

- `直譯：「……」。` literally; `或譯：「……」。` or
- `希伯來文 *chesed*，……` `希臘文 *logos*，……` (transliterated simply, as in English)
- References: `以賽亞書40章3節`, ranges `24章5至9節`.
- Where the Hebrew numbering differs from the Union Version's (which follows the English), add
  it: `（和合本作89章52節）`.
- Manuscript notes follow the English rules, worded: `許多抄本作「……」` (many manuscripts read),
  `許多抄本加上「……」` (add), `有些抄本作「……」` (some), `SBL 希臘文新約在此依循韋斯科特和霍特（Westcott and Hort）的版本；其他版本……`.

## Format

As in English, one file per chapter, `translation-zh/NN-book/CCC.md`, with the book's English
name in the front matter so the tools can match it to its source:

```markdown
---
book: Mark
chapter: 1
source: SBLGNT v1.2
status: draft
translator: Claude (AI), draft
reviewers: []
---

**1** 這是耶穌基督[^1]的福音的開始。

[^1]: 希臘文 *christos*，……
```

## Review

Drafts are AI-generated (Claude). A chapter becomes **checked** when the checker passes and it
has been compared with the source; **reviewed** when a native Chinese reader who reads Greek or
Hebrew has confirmed every verse, and a native reader has read it aloud for natural Chinese;
**approved** when accepted for publication. Reviewers' names go in `reviewers`.

## License

CC BY 4.0, as for the English translation.
