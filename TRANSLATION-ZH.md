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

## Style

**Characters and words.** Plain words over the Union Version's literary ones (吊下去, not 縋下來). Hong Kong standard forms: 裏 (not 裡), 着 for the particle (看着、
帶着; 著 only in 顯著、著作), 衞, 甚麼 (not 什麼), 只 (not 祇). Hong Kong usage where it differs
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
