# 淺白中文譯本 · The Plain Chinese Translation

A new translation of the Bible into plain, modern Traditional Chinese for native readers, made
directly from the Hebrew, Aramaic and Greek texts in this repository. It is written for readers
in Hong Kong, in the standard written Chinese they read every day, not in Cantonese.

**Status:** the four Gospels, Acts, Romans, 1 and 2 Corinthians, Galatians, Ephesians, Philippians, Colossians, 1 and 2 Thessalonians, 1 and 2 Timothy, Titus, Philemon, Hebrews, James, 1 and 2 Peter, 1 and 2 John, Jude drafted; the rest of the Bible in progress from Genesis (see translation-zh/STATUS.md). Every chapter is an AI draft until native readers have reviewed it.

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
| נְאֻם־יְהוָה (in an oracle) | 這是耶和華說的 | *ne'um* noted (9:26); aligned with the prophets (Isaiah table). |
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
| 2 Kings 18:13–20:19 (Isaiah 36–39) | Isaiah to follow this wording where the Hebrew is the same | Differences noted as 以賽亞書36章5節作「……」; the parallel noted at 18:13, 19:1, 20:1. Rabshakeh's speech 「」, Hezekiah's message 『』, the king of Assyria's words unmarked (18:29–35). 19:21–28 poetry inside Isaiah's speech, Sennacherib's boast 『』. |
| תַּרְתָּן; רַב־סָרִיס; רַב־שָׁקֵה | 他珥探；拉伯撒利；拉伯沙基 | Titles, transliterated as the Union Version; each noted (18:17), 拉伯沙基 「酒政長」. |
| אֲשֶׁר עַל־הַבַּיִת | 王宮總管 | As 10:5 (1 Kings 16:9; 18:3 have 王宮總管). |
| אֲרָמִית; יְהוּדִית (18:26, 28) | 亞蘭語；猶大話 | 猶大話 noted: Hebrew. |
| נְחֻשְׁתָּן; בְּרֹאדַךְ בַּלְאֲדָן | 尼忽士但；比羅達‧巴拉但 | Transliterated (和合本「銅塊」); the Hebrew's Berodach, with Isaiah's 米羅達 noted (20:12). |
| בְּתוּלַת בַּת־צִיּוֹן; בַּת יְרוּשָׁלַםִ | 錫安的處女；耶路撒冷的女兒 | Noted (19:21). |
| סֵפֶר הַתּוֹרָה; סֵפֶר הַבְּרִית | 律法書；約書 | 22:8; 23:2. |
| כְּמָרִים; קְדֵשִׁים; מַזָּלוֹת | 拜偶像的祭司；廟妓；星座 | Josiah's reform (23:5, 7). |
| הַר הַמַּשְׁחִית | 毀滅山 | Noted with *har ha-mishchah* and 和合本「邪僻山」 (23:13). |
| כַּשְׂדִּים | 迦勒底人 | Noted at its first occurrence in each chapter. |
| רַב־טַבָּחִים | 護衞長 | Noted: 「屠夫長」或「廚師長」 (25:8). |
| Dates (2 Kings 25) | 十月十日；第三十七年十二月二十七日 | Chinese numerals; modern dates and Jeremiah 52's differences in notes. |

Settled while drafting 1 Chronicles:

| Source | Rendering | Notes |
|---|---|---|
| Genealogies: בְּנֵי X; X הוֹלִיד אֶת־Y; Y בְנוֹ | X的兒子是……；X生了Y；Y的兒子Z | Chains of בֶּן (6:18–32) as 「A是B的兒子，B是C的兒子」; short ones 「C的孫子、B的兒子A」 (5:15). 「直譯：兒子們」 where one son is named. |
| Names | The Union Version of Chronicles, passage by passage | Even where it spells one Hebrew name two ways (希斯崙 2:5, 希斯倫 5:3; 抹利 6:4, 末力 6:32). Where it harmonizes against the Hebrew (Genesis' form, a name added from the parallel), the Hebrew's form in the text and 和合本作「……」 in a note (羅單人 1:7, 洗非 1:36, 亞連 1:40, 亞迦 2:7, 薩瑪 2:11, 沙麥 7:34; 8:29, 31; 9:41). |
| אֲבִי (of a town or clan) | X的父親 | Noted at 2:21: founder or leading man. |
| בְּנוֹתֶיהָ (of a town) | 屬它的鎮 | As Joshua; 「女兒們」 noted. |
| בֵּית אָבוֹת; רָאשֵׁי (בֵית) אָבוֹת | 家族；族長 | 「父家」 noted. |
| אַלּוּף (Edom) | 族長 | As Genesis 36. |
| X וְאֶת־מִגְרָשֶׁהָ (1 Chronicles 6) | X和屬它的草場 | As Joshua 21; Joshua's differing names noted. |
| הִתְיַחֵשׂ | 按家譜登記 | |
| Numbering of 1 Chronicles 5–6 | 5:27–41 = 和合本 6:1–15；6:1–66 = 和合本 6:16–81 | Noted at 5:27 and 6:1. |
| נְתִינִים | 殿役 | Noted: *netinim*, 和合本「尼提寧」 (9:2). |
| לֶחֶם הַמַּעֲרֶכֶת | 陳列的餅 | Noted as 供奉在神面前的餅, traditionally 陳設餅 (9:32). |
| Parallels with Genesis, Joshua, Samuel | 創世記36章11節作「……」 | Wherever the English notes them. |
| Parallels with Samuel (1 Chronicles 11–20) | 2 Samuel's wording wherever the Hebrew is the same | Differences noted as 撒母耳記下23章11節作「……」; the parallel noted at the start of each section. Names by the Union Version of Chronicles (哈大利謝, beside Samuel's 哈大底謝, noted at 18:3). |
| הַגִּבּוֹרִים; הַשְּׁלֹשָׁה; הַשְּׁלוֹשִׁים; הַשָּׁלִישִׁים (qere) | 勇士；三個勇士；三十個勇士 (三十個首領 11:15)；軍官 | As 2 Samuel 23; ketiv/qere noted (11:11; 12:19). |
| חוּרָם (qere, the king of Tyre, 14:1) | 戶蘭 | The Hebrew's form; 和合本「希蘭」 and the ketiv noted. |
| Musical terms: נְבָלִים; כִּנֹּרוֹת; מְצִלְתַּיִם; חֲצֹצְרוֹת; שׁוֹפָר; תְּרוּעָה | 瑟；琴；鈸；號筒；羊角號；吶喊 | 鼓瑟彈琴, 敲鈸, 吹號筒. |
| עַל־עֲלָמוֹת; עַל־הַשְּׁמִינִית (15:20–21) | 按着女高音的調子；按着第八調 | Both noted as uncertain, with the psalm titles. |
| מַשָּׂא (15:22, 27) | 歌唱 | *massa* noted: lifting the voice, or carrying the ark. |
| The psalm of 16:8–36 | Poetry without quotation marks, one verse per line | 16:7 ends with ：; differences from Psalms 105, 96, 106 noted as 詩篇105篇6節作「……」; those psalms to follow this wording where the Hebrew is the same. |
| יְהוָה אֱלֹהִים (17:16–17) | 耶和華神 | 2 Samuel 7's 主耶和華 noted. |
| שָׂטָן (21:1, no article) | 撒但 | 或譯「一個敵對者」 noted, with *ha-satan* and 2 Samuel 24:1. Chapter 21 follows 2 Samuel 24's wording where the Hebrew is the same; מַלְאָךְ alone 天使, מַלְאַךְ יְהוָה 耶和華的使者. |
| מַחְלְקוֹת; מִשְׁמָרוֹת | 班次、班；職守 | Priests, Levites, singers, gatekeepers, army (1 Chronicles 23–28). |
| Lots (24:7–18; 25:9–31) | 頭一籤抽出來是X，第二籤是Y | 25:10–31 one line: 第N籤是X，他的兒子和兄弟共十二人. |
| הָרֹאשׁ; הַשֵּׁנִי; הַבְּכוֹר (lists) | 為首的；第二；長子 | |
| אֹצְרוֹת; בֵּית הָאֲסֻפִּים; פַּרְבָּר | 府庫；庫房；廊院 | *asuppim*, *parbar* noted (26:15, 18), 廊院 as 2 Kings 23:11. |
| הַקֳּדָשִׁים (gifts) | 奉獻物 | |
| גִּבּוֹרֵי חַיִל; בְּנֵי־חַיִל (Levites) | 能幹的人 | As 9:13. |
| Months in the army list (27:2–15) | 一月班、二月班；第四位，四月的 | Not 正月. |
| תַּבְנִית | 式樣 | As Exodus 25:9 (28:11–19). |
| בִּירָה (the temple) | 宮殿 | *birah* noted (29:1). |
| אֲדַרְכֹנִים | 達利克 | Persian gold coin, noted (29:7). |

Settled while drafting 2 Chronicles:

| Source | Rendering | Notes |
|---|---|---|
| Parallels with Kings (2 Chronicles 1–12) | 1 Kings' wording wherever the Hebrew is the same | Temple terms (大殿, 內殿, 前廊, 海, 盆座, 洗濯盆, 柱頂, 網子), the dedication prayer, the regnal formulas. Differences noted as 列王紀上8章25節作「……」; the parallel noted at the start of each section. |
| Numbering of 2 Chronicles 1–2 | 1:18 = 和合本 2:1；2:1–17 = 和合本 2:2–18 | Noted at 1:18 and 2:1; other references give both. |
| חוּרָם (king of Tyre) | 戶蘭 | As 1 Chronicles 14:1; noted 和合本「希蘭」 (2:2; 8:2; 9:10). |
| חוּרָם אָבִי / אָבִיו (the craftsman) | 戶蘭‧亞比 | *Huram avi* noted (2:12; 4:16); 和合本 reads 2:12 as 「我父親希蘭所用的」, 4:16 「巧匠戶蘭」. |
| הַבַּיִת הַגָּדוֹל; הֵיכָל | 大殿 | As 1 Kings 6 (3:5, 17). |
| סִירוֹת; יָעִים; מִזְרָקוֹת; מִזְלָגוֹת | 盆；鏟子；盤子；肉叉 | 4:11, 16; *sirot* noted against 1 Kings 7:40. |
| אַלְגּוּמִּים | 檀香木 | As 1 Kings 10:11 (*almuggim*); noted (2:7; 9:10). |
| כִּיּוֹר (6:13) | 銅臺 | Noted: the word for 洗濯盆. |
| מַעַל | 不忠 | *ma'al* noted (12:2): a key word in Chronicles. |
| Records of prophets (9:29; 12:15) | 先知拿單的記錄；示羅人亞希雅的預言；先見易多的默示 | Statement form, as the Kings formula; 直譯「不是都寫在……上嗎？」 noted. |
| כִּי טוֹב כִּי לְעוֹלָם חַסְדּוֹ | 因為他是美善的，他的慈愛永遠長存 | As 1 Chronicles 16:34 (5:13; 7:3). |
| Parallels with Kings (2 Chronicles 13–24) | The wording of 1 Kings 15, 22 and 2 Kings 8, 11–12 wherever the Hebrew is the same | Regnal formulas as Kings (登基作猶大王；開始作王的時候是N歲；與他的祖先同睡，葬在大衛城); differences noted as 列王紀下11章6節作「……」. |
| Numbering of 2 Chronicles 13–14 | 13:23 = 和合本 14:1；14:1–14 = 和合本 14:2–15 | Noted at 13:23 and 14:1. |
| סֵפֶר הַמְּלָכִים לִיהוּדָה וְיִשְׂרָאֵל; סֵפֶר מַלְכֵי יִשְׂרָאֵל | 《猶大和以色列諸王記》；《以色列諸王記》 | 16:11; 20:34. 「諸王的書」 noted. הִנָּם כְּתוּבִים 都寫在……上, 「看哪」 noted. |
| מִדְרַשׁ | 註釋 | 先知易多的註釋 (13:22)；《諸王記》的註釋 (24:27); *midrash* noted. |
| שְׂרֵפָה (at a king's burial) | 為他燒起極大的火 | Noted: a ceremonial fire of spices (16:14; 21:19). |
| Names the Union Version harmonizes (2 Chronicles 13–24) | The Hebrew in the text | 俄德的預言 (15:8, 和合本 adds 亞撒利雅)；米迦 (18:14, 和合本「米該雅」)；亞捫人 (20:1, 和合本「米烏尼人」)；以色列王 (21:2, 和合本「猶大王」)；拉瑪 (22:6, 和合本「拉末」). |
| הִזְנָה | 使……行邪淫 | 「賣淫」 noted as the image of unfaithfulness (21:11, 13). |
| Parallels with Kings (2 Chronicles 25–36) | The wording of 2 Kings 14–25 wherever the Hebrew is the same | Regnal formulas unchanged; differences noted as 列王紀下14章20節作「……」; the parallel noted at the start of each section. |
| הֲלֹא הִנָּם כְּתוּבִים עַל־סֵפֶר מַלְכֵי יְהוּדָה וְיִשְׂרָאֵל | 都寫在《猶大和以色列諸王記》上 | 《以色列和猶大諸王記》 where the Hebrew has that order (27:7; 35:27; 36:8); 「看哪」, 「諸王的書」 noted. 33:18 《以色列諸王記》 (「諸王的話」). |
| צָרַעַת; בֵּית הַחָפְשִׁית (26:19–23) | 嚴重的皮膚病；隔離的房子 | As 2 Kings 15:5; the glossary note. |
| חַטָּאת (29:21–24) | 贖罪祭 | 或譯「潔淨祭」 noted. |
| הָרָצִים (30:6, 10) | 傳信的人 | 「奔跑的人」 noted (護衞兵 in Kings). |
| בְּנֵי הָעָם (35:5–13) | 平民 | 「民眾的子孫」 noted. |
| Names the Union Version harmonizes (2 Chronicles 25–36) | The Hebrew in the text | 托哈 (34:22, 和合本「特瓦」 from 2 Kings 22:14). |
| כּוֹרֶשׁ; פְּרָת | 古列；伯拉河 | The classic Union Version forms, not the 1989 edition's 塞魯士, 幼發拉底河 (35:20; 36:22); 居魯士 noted. |
| 2 Chronicles 36:22–23 (Ezra 1:1–3) | Ezra to follow this wording where the Hebrew is the same | Differences to be noted in Ezra. |

Settled while drafting Ezra:

| Source | Rendering | Notes |
|---|---|---|
| Ezra 1:1–3 (2 Chronicles 36:22–23) | 2 Chronicles 36's wording wherever the Hebrew is the same | 1:3 讓他上猶大的耶路撒冷去，建造耶和華以色列神的殿; the differences noted. |
| Lists (Ezra 2; Nehemiah 7): בְּנֵי X N; אַנְשֵׁי X N | X的子孫，二千一百七十二人；X的人，五十六人 | A town's 「子孫」 are its people (noted 2:21). Nehemiah 7's names and numbers noted. |
| Names (Ezra 2, 8, 10) | The Union Version of Ezra, list by list | Where it harmonizes, the Hebrew in the text: 基列‧亞琳 (2:25, 和合本「基列‧耶琳」), 西亞哈 (2:44, 和合本「西亞」); where it follows the ketiv, the qere: 撒刻 (8:14, 和合本「撒布」), 拉末 (10:29, 和合本「耶利末」). |
| נְתִינִים; עַבְדֵי שְׁלֹמֹה | 殿役；所羅門僕人的子孫 | As 1 Chronicles 9:2; 和合本「尼提寧」 noted. |
| בְּנֵי הַגּוֹלָה; בְּנֵי גָלוּתָא | 被擄歸回的人 | 「被擄的子孫」 noted. |
| רָאשֵׁי הָאָבוֹת | 族長 | 「父親們的首領」 noted (1:5). |
| סֹפֵר (Ezra) | 經學家 | Noted: 傳統譯作「文士」 (7:6). An official's scribe (Shimshai) 書記. |
| פֶּחָה; תִּרְשָׁתָא; אֲחַשְׁדַּרְפְּנִים | 省長；省長；總督 | *pechah* (和合本 calls Tattenai 「總督」) and *tirshata* noted; satraps 總督 (8:36). |
| עֲבַר נַהֲרָה (Aramaic); עֵבֶר הַנָּהָר | 河西省 | Noted at its first occurrence in each chapter: west of the Euphrates. |
| Aramaic letters: בְּעֵל טְעֵם; טְעֵם; פַּרְשֶׁגֶן; וּכְעֶנֶת | 指揮官；命令；副本；如此如此 | *be'el te'em* (和合本「省長」), *ukhe'enet* (和合本「云云」) noted. |
| The Aramaic of 4:8–6:18 and 7:12–26 | Noted where it starts and ends | 4:8, 6:18; 7:12, 7:27; and in the first note of 5:1, 6:1. |
| מַעַל; תּוֹעֵבוֹת | 不忠；可憎的事 | *ma'al* noted (9:2). |
| סְגָנִים; חֹרִים | 地方官；貴族 | *seganim* noted (Ezra 9:2; Nehemiah 2:16). |
| הוֹשִׁיב נָשִׁים נָכְרִיּוֹת | 娶外族女子為妻 | 「使……住下」 noted (10:2). |

Settled while drafting Nehemiah:

| Source | Rendering | Notes |
|---|---|---|
| Gates, towers and pools (Nehemiah 2–3) | As in the Union Version's text | 羊門、魚門、古門、谷門、糞廠門、泉門、水門、馬門、東門、哈米弗甲門；哈米亞樓、哈楠業樓、爐樓、寬牆；王池、西羅亞池. Ein ha-tannin 大蛇泉 (2:13), 和合本「野狗井」 noted. |
| הֶחֱזִיק; עַל־יָדוֹ; אַחֲרָיו (Nehemiah 3) | 修造；在他旁邊；他之後 | One rendering each through the chapter. |
| שַׂר (חֲצִי) פֶּלֶךְ X | 管理X（半個）區的官長 | *pelekh* noted (3:9). |
| Numbering of Nehemiah 3–4 | 3:33–38 = 和合本 4:1–6；4:1–17 = 和合本 4:7–23 | Noted at 3:33. |
| הָעֶבֶד הָעַמֹּנִי (Tobiah) | 亞捫人官員 | 和合本「為奴的」 noted (2:10). |
| מַשְׁקֶה | 酒政 | *mashqeh* noted (1:11). |
| Nehemiah 7:6–72 (Ezra 2) | Ezra 2's wording and name forms wherever the Hebrew agrees | Differences noted as 以斯拉記2章5節作「……」; 第來雅 (7:62) kept as in Ezra, 和合本 here 第萊雅 noted. |
| Numbering of Nehemiah 7 and 9–10 | 7:68–72 = 和合本 7:69–73；10:1 = 和合本 9:38；10:2–40 = 和合本 10:1–39 | The horses-and-mules line is not in the Leningrad Codex (noted 7:68); noted at 9:37 and 10:1. |
| סֹפֵר (Ezra); כֹּהֵן סֹפֵר | 經學家；祭司兼經學家 | Noted at its first occurrence in the book (8:1). A storehouse official (13:13) 書記. |
| סֻכּוֹת; עֲצֶרֶת (Nehemiah 8) | 棚；嚴肅的聚會 | 住棚節 noted (8:14). |
| אֲמָנָה; הַחֲתוּם | 堅定的約；蓋了印的文件 | 10:1–2; 11:23 定規, noted as the same word. |
| נְעָרַי (Nehemiah's men) | 我的僕人 | 4:10, 16; 5:10, 16; 13:19. |
| הַגּוֹיִם (around Judah) | 外族 | 5:8–9, 17; 6:6, 16. |
| תְּרוּמָה; לִשְׁכָּה; אוֹצָרוֹת | 舉祭；房間；庫房 | *terumah* noted (10:38; 12:44; 13:5). |
| Chains of בֶּן (Nehemiah 11; 12:35) | A是B的兒子，B是C的兒子 | As 1 Chronicles 6. |
| Names (Nehemiah 8–13) | The Union Version of Nehemiah, passage by passage | Even where it differs from Ezra or itself: 約撒達 (12:26, Ezra 約薩達), 哈疊 (11:34, 7:37 哈第), 撒迦利雅／撒迦利亞 (11:4, 12). 毘 for its 毗. |
| תּוֹדֹת (12:31, 38, 40) | 稱謝的人（兩大隊） | Literal wording noted. |

Settled while drafting Esther:

| Source | Rendering | Notes |
|---|---|---|
| God in Esther | Not added | 4:14 「別處」 noted: the Hebrew book never names God; the Septuagint's additions. |
| שׁוּשַׁן הַבִּירָה; הָעִיר שׁוּשָׁן | 書珊城堡；書珊城 | As Nehemiah 1:1. |
| מְדִינָה; אֲחַשְׁדַּרְפְּנִים; פַּחוֹת; שָׂרֵי הַמְּדִינוֹת | 省；總督；省長；各省的首領 | As Ezra and Nehemiah; satraps noted at 3:12. |
| שָׂרִים; פַּרְתְּמִים | 大臣；顯貴 | *partemim* noted (1:3; 6:9). |
| סָרִיס | 太監 | *saris* noted at 1:10 (官員 in Kings). |
| דָּת | 法令 (律例 for Haman's "their laws", 3:8) | *dat* noted (1:8). |
| בֵּית הַנָּשִׁים; פִּילַגְשִׁים | 後宮；妃嬪 | 「婦女的房屋」 and *pilagshim* (elsewhere 妾) noted (2:3, 14). |
| שַׁעַר הַמֶּלֶךְ | 王宮的大門（口） | Noted: where officials did business (2:19). |
| עֵץ; תָּלָה | 木柱；掛在……上 | *ets* noted at 2:23: a pole or stake, traditionally 「木頭」, 「絞架」. |
| הָרָצִים | 傳信的人 | As 2 Chronicles 30:6; 「奔跑的人」 noted (3:13). |
| פַּתְשֶׁגֶן; פִּתְגָם | 副本；詔令 | Persian loanwords noted. |
| שַׁרְבִיט הַזָּהָב | 金杖 | |
| פּוּר; פּוּרִים | 普珥；普珥日 | *pur* 「籤」 noted (3:7; 9:26). |
| הַיְּהוּדִים | 猶太人 | As Nehemiah 13:23 (和合本 猶大人). |
| Months | 正月，就是尼散月；三月，就是西彎月；十月，就是提別月；十二月，就是亞達月 | Modern months noted. |
| סֵפֶר דִּבְרֵי הַיָּמִים | 年鑒；《米底亞和波斯諸王記》 (10:2) | 「日子的事的書」 noted (2:23). |
| Names where the Union Version harmonizes | The Hebrew in the text | 辟探拿 (6:2, 和合本「辟探」 as 2:21). |

Settled while drafting Job:

| Source | Rendering | Notes |
|---|---|---|
| Poetry (Job 3 onward) | One verse per line, its cola joined by ，；, speeches in 「」 | 「 reopened at each chapter of a speech that continues (5:1; 7:1); a voice quoted inside a speech 『』 (4:17–21). Prose frame (1–2; 42:7–17) as narrative. |
| וַיַּעַן X וַיֹּאמַר | X回答說： | 3:2 約伯說：, 「回答說」 noted. |
| הַשָּׂטָן (Job 1–2) | 撒但 | *ha-satan* noted at the first occurrence in each chapter: 「那敵對者、那控告者」, a title with the article; 或譯「那敵對者」; 1 Chronicles 21:1. |
| בְּנֵי הָאֱלֹהִים | 神的兒子們 | As Genesis 6; noted (1:6; 2:1). |
| בֵּרֵךְ for "curse" (1:5, 11; 2:5, 9) | 咒詛 | 直譯「祝福」 noted. |
| תָּם וְיָשָׁר; תֻּמָּה | 完全正直；純全 | *tam* noted (1:1). |
| אֱלוֹהַּ; אֵל; שַׁדַּי | 神；神；全能者 | *Eloah* and *Shaddai* noted at the first occurrence in each chapter. |
| צַלְמָוֶת | 死蔭 | *tsalmavet* noted (3:5). |
| לִוְיָתָן; תַּנִּין (7:12) | 利維坦；海怪 | 和合本「鱷魚」 noted (3:8). |
| שְׁאוֹל | 陰間 | Glossary note (7:9). |
| חֶסֶד (6:14) | 慈愛 | Glossary note. |
| Speakers' openings | 書亞人比勒達回答說；拿瑪人瑣法回答說；提幔人以利法回答說 | A speech running on (9→10, 12→14, 16→17) leaves 」 off at the chapter's end. |
| Job speaking to God inside a speech | No inner quotation marks | Noted where it starts (10:2; 13:20; 17:3), as in English. |
| רַהַב (9:13) | 拉哈伯 | The sea monster, noted as not 喇合 (Joshua 2). |
| עָשׁ, כְּסִיל, כִּימָה (9:9) | 北斗、參星、昴星 | Uncertain identifications noted; also for 38:31–32. |
| מוֹכִיחַ (9:33) | 仲裁人 | *mokhiach* and the Septuagint's 「但願」 noted. |
| תּוּשִׁיָּה | 真智慧 | As 5:12, noted (6:13; 11:6; 12:16). |
| צַלְמָוֶת | 死蔭 | Noted at the first occurrence in each chapter (10:21; 12:22; 16:16). |
| שַׁחַת (17:14) | 墳坑 | Noted: 或譯「朽壞」. |
| גֹּאֲלִי (19:25) | 我的救贖者 | Long note: *go'el* (至近的親屬, as Ruth), 維護者／伸冤者, who is meant left open, 和合本「救贖主」. |
| נָשָׂא פָנִים (13:8, 10) | 偏袒 | 「抬起他的臉」 noted. |
| The speakers of 24–27 | As the Hebrew stands: Job speaks 23–24 and 26–31 | The debate noted at 24:18, 25:1, 26:5, 27:1, 27:13; 28 continues Job's speech (noted 28:1). |
| נָשָׂא מְשָׁלוֹ (27:1; 29:1) | 繼續發表他的講論 | *mashal* noted. Job's speech 29–31 one quotation; 31:40 closes 」 before 約伯的話說完了. |
| אֲבַדּוֹן | 亞巴頓 | As 啟示錄9章11節; noted 「毀滅」, 和合本「滅亡」 (26:6). |
| רְפָאִים (the dead) | 陰魂 | Noted (26:5); the ancient people stay 利乏音人. |
| סַפִּיר; שֹׁהַם; פִּטְדָה (Job 28) | 青金石；紅瑪瑙；貴橄欖石 | As Exodus 28; traditional names noted. |
| יִרְאַת אֲדֹנָי … וְסוּר מֵרָע (28:28) | 敬畏主就是智慧，遠離惡事就是聰明 | Echoes 1:1 (敬畏神，遠離惡事); *Adonai* noted. |
| Job's oath (Job 31) | 我若……，就願…… | Conditions left unfinished where the Hebrew leaves them (31:29–34), with ——. |
| Elihu's speeches (32:6–37:24) | 以利戶回答說 (32:6; 34:1; 35:1)；以利戶接着說 (36:1) | Each section a quotation closed at its end; 36 runs on into 37. 巴拉迦別 (32:2), the classic form; the 1989 text has 巴拉迦. |
| שַׁחַת (Job 33) | 墳坑 | As 17:14, noted 或譯「朽壞」. *shelach* 死亡之河 (33:18; 36:12), 「刀」 noted. |
| מַלְאָךְ מֵלִיץ (33:23) | 天使作中間人 | *melits* noted, with 16:20. |
| סְעָרָה (38:1; 40:6) | 旋風 | 「暴風」 noted. The LORD's speeches: 38:2–39:30 (closed), 40:2, 40:7–41:26 (40 left open). |
| אֱזָר־נָא כְגֶבֶר חֲלָצֶיךָ (38:3; 40:7) | 你要像勇士一樣束腰；我要問你，你要指教我 | Identical in 38:3, 40:7 and 42:4. |
| Animals (Job 38–39) | 野山羊、野驢、野牛 (*re'em*)、鴕鳥、鸛、鷂鷹 (*nets*)、鷹 (*nesher*) | As Leviticus 11; *re'em* noted 「獨角獸」. *shofar* 羊角號. |
| בְּהֵמוֹת (40:15) | 比希摩 | Transliterated as 利維坦; *behemot*, hippopotamus or elephant, and 和合本「河馬」 noted. |
| Numbering of Job 40–41 | 40:25–32 = 和合本 41:1–8；41:1–26 = 和合本 41:9–34 | Noted at 40:25 and 41:1. |
| אֶמְאַס וְנִחַמְתִּי (42:6) | 我收回我的話，在塵土和爐灰中懊悔 | The other readings (我厭惡自己；不再在塵土和爐灰中哀哭；得了安慰) in a long note. |
| שָׁב אֶת־שְׁבוּת (42:10) | 扭轉……的命運 | As Deuteronomy 30:3, noted. |

Settled while drafting Psalms:

| Source | Rendering | Notes |
|---|---|---|
| Psalm titles | Part of verse 1 (or 1–2), in the Hebrew order, each element ending 。: 交給詩班長。用絲弦的樂器。大衛的詩。 | Noted once per psalm at the title: 希伯來文以標題為第1節，所以第2至9節和合本作3篇1至8節. A title sharing its verse with the first line (11; 14; 15) noted as keeping the Union Version's numbers. Psalm references in notes: 19篇15節. |
| לַמְנַצֵּחַ | 交給詩班長 | *lamenatseach* noted at its first occurrence in each psalm, with 和合本「交與伶長」. |
| מִזְמוֹר לְדָוִד; לְדָוִד (alone) | 大衛的詩；屬大衛的 | 「或譯『為大衛作的』、『關於大衛的』」 noted in each psalm; *mizmor* noted (3:1). |
| שִׁיר; תְּהִלָּה; תְּפִלָּה; שִׁיר הַמַּעֲלוֹת | 歌；讚美詩；禱告；上行之詩 | For later psalms. |
| שִׁגָּיוֹן; הִגָּיוֹן; מַשְׂכִּיל; מִכְתָּם | 示迦庸；希迦庸；瑪斯基勒；米克坦 | Meaning uncertain, so transliterated; the Hebrew and the Union Version's 流離歌, 訓誨詩, 金詩 in a note. |
| בִּנְגִינוֹת | 用絲弦的樂器 | Meaning known, translated. |
| Terms of uncertain meaning: עַל־הַשְּׁמִינִית; אֶל־הַנְּחִילוֹת; עַל־הַגִּתִּית; עַלְמוּת לַבֵּן | 按照舍米尼；用尼希錄；按照基提；按照慕拉便 | 按照 for עַל, 用 for אֶל and בְּ; the Union Version's 調用第八, 用吹的樂器, 用迦特樂器 in the note. |
| Tune names whose meaning is known (22:1, 56:1) | 調用「……」 | The name translated inside 「」. |
| סֶלָה | 細拉 | Its own word after the line's 。 (「……。細拉。」), wherever the Hebrew has it; *selah* noted at its first occurrence in each psalm. |
| אַשְׁרֵי | 多麼有福；有福 | *ashrei* noted at its first occurrence in each psalm, kept apart from בָּרוּךְ 蒙福. |
| חֶסֶד; חָסִיד | 慈愛；忠誠的人、忠於他的人 | The glossary note on *chesed* at its first occurrence in each psalm; *chasid* noted with it. |
| Divine names | 耶和華 (YHWH, noted in each psalm)；神 (Elohim, El, Eloah)；主 (Adonai)；至高者 (Elyon, noted)；萬軍之耶和華 | יְהוָה אֲדֹנֵינוּ 耶和華我們的主 (8:2). *Yah* alone 耶和華, noted; הַלְלוּ־יָהּ 你們要讚美耶和華, noted 「哈利路亞」. |
| מְשִׁיחוֹ (2:2) | 他的受膏者 | Noted: the king; *mashiach* and 彌賽亞; Acts 4:25–27. |
| New Testament quotations | The Hebrew in the text | A note only where the Septuagint or the New Testament reads differently (2:9; 4:5; 8:3, 6). |
| Acrostics | Noted at the first verse | Psalms 9–10 (9:2; 10:1). |
| עָנִי; עָנָו | 困苦人；謙卑人 | Kept apart, so a ketiv/qere between them is noted (9:13, 19; 10:12). Ketiv/qere differing only in form (5:9; 6:4; 10:5; 11:1) not noted. |
| שָׁב שְׁבוּת (14:7) | 扭轉……的命運 | As Job 42:10; 「帶回被擄的」 noted. |
| Psalm 18 (2 Samuel 22) | 2 Samuel 22's wording wherever the Hebrew is the same | Differences noted as 撒母耳記下22章5節作「……」; poetry without quotation marks, 18:2 opens 他說：. |
| מִזְמוֹר (alone, after לְדָוִד); שִׁיר חֲנֻכַּת הַבַּיִת | 一首詩；為殿行奉獻禮時唱的歌 | 24:1; 30:1, *chanukkah* noted. |
| Psalm 19:8–10 | 律法；法度；訓詞；誡命；敬畏；典章 | One rendering each for *torah*, *edut*, *piqqudim*, *mitsvah*, *yir'ah*, *mishpatim*; noted. |
| גֹּאֵל (of God, 19:15) | 救贖者 | As Job 19:25; *go'el* noted with Ruth. |
| כָּאֲרִי (22:17) | 他們像獅子一樣，撲咬我的手和我的腳 | The verb supplied and noted; 「扎」 (Septuagint, some manuscripts, 和合本) in the note. |
| בּוֹר; שַׁחַת | 坑 (下坑的人)；墳坑 | Each noted (28:1; 30:4, 10; 16:10). |
| כְּלָיוֹת | 心腸 | 「腎」 noted (16:7; 26:2). |
| צַלְמָוֶת (23:4) | 死蔭的幽谷 | As Job 3:5 (死蔭); 「最黑暗的山谷」 noted. |
| בְּנֵי אֵלִים (29:1) | 天上的眾生 | 「眾神的兒子們」 noted. |
| Acrostics (Psalm 25) | Noted at verse 1 | The gaps and the closing *pe* verse described. |
| Acrostics (Psalms 34, 37) | Noted at the first verse of the alphabet | 34:2 (no *vav*; closing *pe* verse 23, as 25); 37:1 (two-verse sections, *ayin* mid-verse 28). |
| לְהַזְכִּיר; שִׁיר יְדִידֹת; עַל־שֹׁשַׁנִּים | 為了記念；愛的歌；調用「百合花」 | 38:1; 45:1; 和合本「紀念詩」「愛慕歌」 noted. |
| עַל־עֲלָמוֹת (46:1) | 按照亞拉莫 | Coined; 「女高音」 and 和合本「調用女音」 noted, with 1 Chronicles 15:20. |
| לִבְנֵי־קֹרַח | 可拉後裔的 | 「或譯『為可拉後裔作的』」 and the Levite singers noted in each psalm. |
| Book divisions | Noted: 41:14 closes 第一卷; 42:1 opens 第二卷 (42–72) and the Korah psalms (42–49) | 42:2 notes the 「以羅欣詩集」 (42–83): 神 for *Elohim*, 耶和華 for YHWH, as each stands. |
| Refrains (42:6, 12; 43:5; 46:8, 12; 49:13, 21) | Identical wording wherever the Hebrew is identical | Where it differs (42:6 *yeshu'ot panav*; 49:13 *bal yalin*), the Chinese differs and a note says how. |
| הֶבֶל (39:6, 7, 12) | 一口氣；枉然 | *hevel* noted with 傳道書1章2節. |
| כִּסְאֲךָ אֱלֹהִים (45:7) | 神啊，你的寶座 | Long note: the king addressed as *elohim*, other readings, Septuagint and 希伯來書1章8至9節. |
| Hebrews quoting the Septuagint (40:7–9) | The Hebrew (你開通了我的耳朵) in the text | The Septuagint 「你卻為我預備了身體」 and Hebrews' other changes in the note. |
| צָפוֹן (48:3) | 北方的高處 | *Tsaphon*, the mountain of Canaanite myth, noted. |
| Historical titles taking two verses (51; 52; 54; 60) | 1 交給詩班長。大衛的詩。 2 那時…… | Noted: 希伯來文以標題為第1至2節，所以第3至21節和合本作51篇1至19節，相差兩節. |
| מַשְׂכִּיל לְדָוִד; לְדָוִד מִכְתָּם | 大衛的瑪斯基勒；屬大衛的。米克坦。 | The Hebrew order, as 16:1 and 32:1. |
| עַל־מָחֲלַת; עַל־יְדוּתוּן; עַל־נְגִינַת | 按照麻哈拉；按照耶杜頓；用絲弦的樂器 | 麻哈拉 as the Union Version (also 88:1); 和合本「照耶杜頓的作法」 noted. |
| Tune names: אַל־תַּשְׁחֵת; יוֹנַת אֵלֶם רְחֹקִים; שׁוּשַׁן עֵדוּת | 調用「不要毀壞」；調用「遠方無聲的鴿子」；調用「見證的百合花」 | 57–59, 75; 56; 60, 80. Union Version forms noted. |
| Psalm 53 (Psalm 14) | Psalm 14's wording wherever the Hebrew agrees, 神 for *Elohim* | Differences noted (53:2 *avel*; 53:4 *sag*; 53:6). |
| Psalm 108 (= 57:8–12; 60:7–14) | The wording of 57 and 60 | Psalm 108 to follow it where the Hebrew agrees; 60:10–11 note 108's differences. |
| יְהוָה אֱלֹהִים צְבָאוֹת (59:6) | 耶和華萬軍之神 | As 2 Samuel 5:10; the Hebrew and 「萬軍之神耶和華」 noted. |
| רוּחַ קָדְשְׁךָ (51:13) | 你聖潔的靈 | 傳統「你的聖靈」 noted. |
| Psalm 68 | One reading in the text, others in notes | 68:19 受了禮物; Ephesians 4:8 「賜給」 (*edōken*) noted. Its hapax words noted as only here. |
| Book divisions (72–73; 89) | 72:18–19 and 89:53 noted as closing 第二卷, 第三卷; 72:20 耶西的兒子大衛的禱告完畢了 | 73:1 notes 第三卷 (73–89) and the Asaph psalms (73–83); 83:1 the last of them. |
| לְאָסָף | 亞薩的詩 (מִזְמוֹר לְאָסָף)；屬亞薩的 (alone or before מִזְמוֹר: 屬亞薩的。一首詩。) | 「或譯『為亞薩作的』」 and the Levite singer (50:1) noted in each psalm. 以斯拉人以探, 希幔 (88; 89). |
| Psalm 70 (= 40:14–18) | Psalm 40's wording wherever the Hebrew agrees, 神 for *Elohim* | Each difference noted (70:2, 3, 4, 5, 6). |
| NT quotations where the Greek differs | The Hebrew in the text | 69:10 (John 2:17 future 「將要吞噬」); 69:26 (Acts 1:20 singular); 78:2 (Matthew 13:35 「從創立以來所隱藏的事」); 78:24 (John 6:31 *artos*). 82:6 noted as agreeing. |
| אֱלֹהִים (82:1, 6) | 神聖的議會；眾神；你們是神 | The divine council in the text; human judges (Exodus 21:6; 22:7–8) and 和合本「有權力者的會」「諸神」 in the notes. |
| עֵדוּת (78:5, 56; 81:6) | 法度 | As 19:8; noted. |
| Psalm 89 (2 Samuel 7) | 2 Samuel 7's words: 後裔、王位、堅立、兇惡的人、苦待、杖、鞭打、慈愛不收回 | בְּנֵי אֵלִים 天上的眾生 (89:7); *emunah* 信實. |
| רַהַב (87:4; 89:11); אֲבַדּוֹן; רְפָאִים | 拉哈伯 (not 喇合)；亞巴頓；陰魂 | As Job 26. |
| עַל־מָחֲלַת לְעַנּוֹת (88:1) | 按照麻哈拉利暗俄 | The Union Version's form; *le'annot* noted. |
| Psalm 78 (Exodus, Numbers) | The Pentateuch's words: 嗎哪、成群的蒼蠅、使水直立像牆壁 (Exodus 15:8) | 瑣安 as the Union Version's Psalms (鎖安 in Numbers 13:22, noted). |
| אִישׁ הָאֱלֹהִים (90:1) | 神人摩西的禱告 | As Deuteronomy 33:1. 90:1 notes 第四卷 (90–106); 106:48 noted as closing it. |
| יְהוָה מָלָךְ (93:1; 96:10; 97:1; 99:1) | 耶和華作王了 | As 1 Chronicles 16:31; 「耶和華已經作王了」「耶和華是王」 and the 「耶和華作王」詩篇 (93, 95–99) noted at 93:1. הַמֶּלֶךְ יְהוָה (98:6) 君王耶和華. |
| Psalms 96; 105:1–15; 106:1, 47–48 (1 Chronicles 16:8–36) | 1 Chronicles 16's wording wherever the Hebrew agrees | Differences noted as 歷代志上16章27節作「……」. |
| מִזְמוֹר לְתוֹדָה (100:1) | 感恩的詩 | 「為感恩祭作的詩」 noted. |
| כִּי טוֹב כִּי לְעוֹלָם חַסְדּוֹ | 因為他是美善的，他的慈愛永遠長存 | As 1 Chronicles 16:34 (100:5; 106:1); for 107, 118, 136. |
| בָּרֲכִי נַפְשִׁי אֶת־יְהוָה (103–104) | 我的心哪，你要稱頌耶和華 | *nephesh* noted. |
| NT quotations (91:11–12; 95:7–11; 102:26–28; 104:4) | The Hebrew in the text | Notes give Matthew 4:6 and Luke 4:10–11's omissions, Hebrews 3's translated place names and 「四十年」, Hebrews 1:10–12's 「主啊」「捲起來」, Hebrews 1:7's 「以他的使者為風」. |
| Psalms 105–106 (Genesis–Numbers) | The Pentateuch's words: 成群的蒼蠅、蚊子 (*kinnim*)、蝗蟲、蝻子 (*yeleq*)、鵪鶉、天上的糧食、米利巴水、巴力‧毗珥 | 含地 for Egypt, noted. |
| לִוְיָתָן (104:26) | 利維坦 | As 74:14 and Job; 和合本「鱷魚」 noted. |
| Book division (107) | 107:1 notes 第五卷 (107–150) | |
| הַלֵּל (113–118) | 「哈利爾」 | Noted at 113:1 (Passover, Mark 14:26); 114–118 refer back. |
| נְאֻם יְהוָה לַאדֹנִי (110:1) | 耶和華對我主說 | *ne'um*, *adoni* against *Adonai*, the Greek 主對我主說 and Mark's 「放在你的腳下」 noted. |
| עַל־דִּבְרָתִי מַלְכִּי־צֶדֶק (110:4) | 按照麥基洗德的方式 | Septuagint *taxis*, Hebrews and 和合本「等次」 noted. |
| Acrostics (111; 112; 119) | Noted at verse 1 | 119: each stanza's letter at its first verse: `*Bet*（ב）：這一段（第9至16節）每節的希伯來文都以這個字母開頭。` |
| Psalm 119's eight terms | 律法 (*torah*)；法度 (*edot*, *edut*)；訓詞 (*piqqudim*)；誡命 (*mitsvot*)；典章 (*mishpatim*)；律例 (*chuqqim*)；言語 (*imrah*)；話 (*davar*) | One rendering each, matching 19:8–10 and 78:5; listed at 119:1. *Mishpat* singular by context (審判 84; 公正 121, 149), noted. *Imrei El* 神的言語 (107:11). |
| חַיֵּנִי (Psalm 119) | 使我存活 | 「使我甦醒」「保全我的性命」 noted (119:25). |
| עֹמֶדֶת לָעַד (111:3, 10; 112:3, 9) | 存到永遠 | |
| Psalm 118:14, 22–23, 26 | Exodus 15:2's and Mark 12:10–11's wording: 房角的基石；這是耶和華所做的，在我們眼中看為奇妙 | 118:26 בָּרוּךְ 是蒙福的 (Mark 11:9 「是應當稱頌的」 noted); 118:25 *hoshi'ah na* and 和散那 noted. |
| שִׁיר הַמַּעֲלוֹת (120–134) | 上行之詩 | *shir ha-ma'alot* and the pilgrims noted at 120:1, later psalms refer back; 121:1 *shir lamma'alot* noted. 羅騰木 (120:4), 米設, 基達. |
| כִּי לְעוֹלָם חַסְדּוֹ (136) | 他的慈愛永遠長存！ | Identical at the end of all 26 verses; 136:1 as 107:1 and 118:1; verses 4–25 (Hebrew participles) as short clauses 他……; noted at 136:1, 4. |
| Psalm 135 (115:4–8; 136:17–22); Psalm 144 (Psalm 18) | The earlier psalm's wording wherever the Hebrew agrees | Differences noted. 雅珥 (132:6) coined, 和合本「基列‧耶琳」 noted. |
| Acrostic (145) | Noted at 145:1 | The missing *nun* verse at 145:13, with 11QPs-a and the Septuagint's line. 145:8 חַנּוּן וְרַחוּם 有恩典、有憐憫……大有慈愛, the reversed order of Exodus 34:6 noted. |
| Instruments: כִּנּוֹר; נֵבֶל; תֹּף; שׁוֹפָר; צֶלְצְלִים; עוּגָב | 琴；瑟；鼓；角、羊角號 (*shofar* noted)；鈸；簫 | 144:9 十弦的瑟 as 33:2. |
| הַלְלוּ־יָהּ (146–150) | 你們要讚美耶和華 | 「哈利路亞」 noted at 146:1; 150:6 notes the close of 第五卷 and of the whole Psalter, and the Septuagint's Psalm 151. |

Settled while drafting Proverbs:

| Source | Rendering | Notes |
|---|---|---|
| Layout | One verse per line, cola joined by ，；; 10:1–22:16 each saying one line of two halves | 10:1 notes the new collection. |
| חָכְמָה; חָכָם | 智慧；智慧人 | *chokhmah* noted (1:2). |
| בִּינָה; תְּבוּנָה; נָבוֹן | 聰明；悟性；聰明人 (有悟性的人 for אִישׁ תְּבוּנָה) | Same root, kept apart; noted 1:2, 2:2. |
| דַּעַת | 知識 | 認識神 (2:5), 認識至聖者 (9:10). |
| מוּסָר; תּוֹכַחַת; לֶקַח; תּוֹרָה | 管教；責備；學問；教導 | *musar* noted (1:2): 傳統譯作「訓誨」. A mother's *torah* 教導 (和合本「法則」). |
| עָרְמָה; עָרוּם | 精明；精明人 | *ormah* noted (1:4), 和合本「靈明」. |
| מְזִמָּה | 謀略 (good)；詭計 (bad: אִישׁ מְזִמּוֹת 設詭計的人) | 1:4; 12:2; 14:17. |
| תּוּשִׁיָּה; תַּחְבֻּלוֹת; שֵׂכֶל; מַשְׂכִּיל | 真智慧；指引；見識；明智的 | *tushiyyah* as Job. |
| Fools: כְּסִיל; אֱוִיל; פֶּתִי | 愚昧人；愚妄人；愚蒙人 | As the Union Version broadly; the three described at 1:7, the Hebrew noted at its first occurrence in each chapter. Abstracts כְּסִילוּת 愚昧, אִוֶּלֶת 愚妄, פְּתָיוּת 愚蒙. |
| לֵץ; חֲסַר־לֵב; בַּעַר; עָצֵל | 愛嘲笑人的 (as Psalm 1)；無知的人 (「缺少心的」 noted)；像畜類一樣愚蠢；懶惰人 | |
| צַדִּיק; רָשָׁע; יָשָׁר; תָּם | 義人；惡人；正直人；完全人 | *tsaddiq*, *rasha* noted (2:20, 22). |
| יִרְאַת יְהוָה | 敬畏耶和華 | 1:7 and 9:10 kept parallel (……是知識／智慧的開端); *reshit*, *techillah* noted. 15:33 refers to both. |
| בְּנִי | 我兒 | Noted 1:8. |
| אִשָּׁה זָרָה; נָכְרִיָּה | 陌生女子；外族女子 | 和合本「淫婦」「外女」 noted (2:16). |
| Lady Wisdom; Folly | 智慧 (她)；愚昧的婦人 | Her speeches in 「」, opened afresh in each chapter (1:22–33; 8:4–36; 9:4–6); 8:22 *qanani* 造了我, long note. |
| תּוֹעֲבַת יְהוָה | 耶和華所憎惡的 | *to'evah* noted (3:32). |
| עֵץ חַיִּים; רְפָאִים; אֲבַדּוֹן | 生命樹；陰魂；亞巴頓 | As Job and Psalms. |
| NT quotations (3:11–12; 3:34; 10:12; 11:31) | The Hebrew in the text | Hebrews 12:5–6 (「不要灰心」, 「鞭打」), James 4:6 / 1 Peter 5:5 (「神抵擋驕傲的人」), 1 Peter 4:8 (「許多的罪」), 1 Peter 4:18 in notes. |
| Collection headings (22:17; 24:23; 25:1; 30:1; 31:1) | 智慧人的言語；以下也是智慧人的言語；以下也是所羅門的箴言，是猶大王希西家的人抄錄的 | A note at each says where the collection runs; 22:17 notes Amenemope and that sayings now run over several verses (one verse per line). |
| מַשָּׂא (30:1; 31:1) | 默示 | 和合本「真言」; the tribe 瑪撒 (Genesis 25:14) in a note. As the prophets' *massa*. |
| נָבָל | 愚頑人 | Noted at 17:7 (Nabal, 1 Samuel 25:25); 30:32 the verb 行事愚頑. |
| נִרְגָּן | 說閒話的 | 16:28; 18:8; 26:20, 22. |
| תּוֹרָה (28:4–9; 29:18) | 律法 | Noted: 「教導」, here probably God's law. |
| אֵשֶׁת חַיִל (31:10; 12:4) | 賢德的婦人；賢德的妻子 | As Ruth 3:11 (賢德的女子); 和合本「才德的婦人」 noted; 31:10–31 noted as an acrostic. |
| NT quotations (25:21–22; 26:11) | The Hebrew in the text (恨你的人, 炭火) | Romans 12:20 (LXX: 「你的仇敵」, no bread and water, no 「耶和華也必賞賜你」) and 2 Peter 2:22 (first line only, with the sow proverb) in notes. |
| Repeated sayings (e.g. 18:8 = 26:22; 22:3 = 27:12; 6:10–11 = 24:33–34) | Word for word the same | Noted where the English notes them. |

Settled while drafting Ecclesiastes:

| Source | Rendering | Notes |
|---|---|---|
| קֹהֶלֶת | 傳道者 | As the Union Version; *Qohelet* (from *qahal*), the Greek *Ekklesiastes* and the feminine form noted at 1:1; 7:27 (feminine verb) and 12:8 (*ha-qohelet*) noted. |
| הֶבֶל | 虛空 | As the Union Version, every time, so the pattern shows (as the English keeps "vapor"); 1:2 notes *hevel* 「氣息、水氣」, Abel, 「一口氣」 (Psalm 39), and later chapters refer back. 6:12, 7:15, 9:9 「虛空的日子」, noted as 「短暫」. |
| הֲבֵל הֲבָלִים (1:2; 12:8) | 「虛空的虛空，」傳道者說，「虛空的虛空！一切都是虛空。」 | 12:8 the same words with the phrase once (「虛空的虛空，」傳道者說，「一切都是虛空。」), noted. |
| תַּחַת הַשֶּׁמֶשׁ; תַּחַת הַשָּׁמַיִם | 日光之下；天下 | Noted at 1:3, 13. |
| רְעוּת רוּחַ; רַעְיוֹן רוּחַ | 捕風 | Both; *re'ut ruach* noted at 1:14 (「追逐風」「牧放風」), *ra'yon* at 1:17. |
| יִתְרוֹן; עָמָל; חֵלֶק | 益處 (勝過 in comparisons)；勞碌；份 | *yitron* noted 1:3, *cheleq* 2:10. |
| עִנְיָן (רָע); מִקְרֶה | （苦）差事；遭遇 | 1:13; 2:14. |
| כְּסִיל; סָכָל, סִכְלוּת, סֶכֶל; הוֹלֵלוֹת | 愚昧人；愚蠢人、愚蠢；狂妄 | 愚昧人 as Proverbs; the *sakhal* family kept apart as 愚蠢. |
| אֵין טוֹב … מִ־/כִּי אִם | 人沒有甚麼比……更好的 | 2:24; 3:12, 22; 5:17; 8:15. |
| Numbering of 4:17–5:19 | 4:17 = 和合本 5:1；5:1–19 = 和合本 5:2–20 | Noted at 4:17 and 5:1. |
| Poetry (3:1–8; 12:1–7) | One verse per line, cola joined by ，； | 3:2–8 「……有時，……有時」. |

Settled while drafting Song of Songs:

| Source | Rendering | Notes |
|---|---|---|
| Speakers | In notes, as the English (「女子說話（「你」是陽性）」, 男子, 耶路撒冷的眾女子) | No headings in the text, though the 1989 Union Version prints them; the general note at 1:2. |
| דּוֹדִי; רַעְיָתִי; דֹּדִים | 我的良人；我的佳偶；愛情 | The Union Version's names, noted 1:9, 13; *dodim* 1:2. *re'i* (5:16) 我的愛友. |
| אֲחֹתִי כַלָּה | 我的妹子，我的新婦 | Noted 4:9. |
| בְּנוֹת יְרוּשָׁלַםִ | 耶路撒冷的眾女子 | |
| The refrain (2:7; 3:5; 8:4) | 耶路撒冷的眾女子啊，我指着羚羊或田野的母鹿，要你們起誓：不要驚動，不要喚醒愛情，等它自己情願。 | Identical; 8:4 without the oath by the animals, noted. |
| צְבִי; עֹפֶר הָאַיָּלִים; אַיָּלוֹת | 羚羊；小鹿；母鹿 | |
| Plants | 哪噠 (nard)、鳳仙花 (henna)、百合花、蘋果樹、番紅花、菖蒲、肉桂、沉香、風茄、核桃園 | Union Version names with the identification noted; חֲבַצֶּלֶת 水仙花 (2:1), not its 玫瑰花, noted. |
| Stones (5:14–15) | 水蒼玉 (*tarshish*)；青金石 (*sappir*)；白玉石 (*shesh*) | As Exodus 28; notes. |
| שׁוּלַמִּית | 書拉密女 | 7:1 noted. |
| שַׁלְהֶבֶתְיָה (8:6) | 耶和華的烈焰 | *-yah* and the superlative reading in a long note. |
| Numbering of 7:1–14 | 7:1 = 和合本 6:13；7:2–14 = 和合本 7:1–13 | Noted at 7:1. |

Settled while drafting Isaiah (for all the prophets):

| Source | Rendering | Notes |
|---|---|---|
| Layout | One verse per line; poetry and prose as the English lays them out | The LORD's words in the poems unmarked (noted 1:2, as Deuteronomy 32); narrative with speeches (6–8) in 「」, a message inside 『』. |
| חָזוֹן | 異象 | *chazon* noted (1:1). |
| כֹּה אָמַר יְהוָה; כֹּה אָמַר אֲדֹנָי יְהוִה | 耶和華這樣說；主耶和華這樣說 | As 2 Kings 19:6, 20 (Isaiah 37:6, 21). |
| נְאֻם יְהוָה | 耶和華說 (opening a saying, 1:24)；這是耶和華說的 (closing it, 3:15) | *ne'um*, 「……的宣告」, noted at the first occurrence in each chapter; Kings' 這是耶和華的宣告 mentioned (see REVIEW.md). |
| מַשָּׂא | 默示 | 「X的默示」, as Proverbs 30:1; *massa* noted (from 13:1). |
| קְדוֹשׁ יִשְׂרָאֵל | 以色列的聖者 | As 2 Kings 19:22; noted at 1:4. |
| יְהוָה צְבָאוֹת; הָאָדוֹן יְהוָה צְבָאוֹת; אֲדֹנָי יְהוִה צְבָאוֹת | 萬軍之耶和華；主萬軍之耶和華 | *tseva'ot* noted at the first occurrence in each chapter; *ha-adon* and *Adonai* noted. |
| בַּיּוֹם הַהוּא | 到那日 | |
| הוֹי; אוֹי | 禍哉；……有禍了 | *hoy* noted at 1:4 (a cry of mourning), later chapters refer back; 1:24 (resolve) 啊. *oy* 他們有禍了, 我有禍了 (3:9, 11; 6:5). |
| בַּת־צִיּוֹן; בְּנוֹת צִיּוֹן | 錫安的女兒；錫安的女子 | Noted (1:8). |
| אֱלִילִים | 虛無的偶像 | *elilim* noted (2:8). |
| בְּכָל־זֹאת לֹא־שָׁב אַפּוֹ וְעוֹד יָדוֹ נְטוּיָה | 雖然這樣，他的怒氣還沒有轉消，他的手仍然伸出 | Identical at 5:25; 9:11, 16, 20; 10:4. |
| עַלְמָה (7:14) | 少女 | 「童女」 (和合本) and the Septuagint's *parthenos* quoted in Matthew 1:23 in the note; *betulah* mentioned. |
| שְׁאָר יָשׁוּב; מַהֵר שָׁלָל חָשׁ בַּז; עִמָּנוּ אֵל | 施亞雅述；瑪黑珥‧沙拉勒‧哈施‧罷斯；以馬內利 | Meanings noted; 8:10 神與我們同在 (*immanu el*). |
| פֶּלֶא יוֹעֵץ אֵל גִּבּוֹר אֲבִיעַד שַׂר־שָׁלוֹם (9:5) | 奇妙的策士、大能的神、永恆的父、和平的君 | *el gibbor* 大能的神 also 10:21 (全能 is kept for *Shaddai*); 和合本, Targum, Septuagint noted. |
| Numbering of 8:23–9:20 | 8:23 = 和合本 9:1；9:1–20 = 和合本 9:2–21 | Noted at 8:23 and 9:1; other references give both. |
| NT quotations | The Hebrew in the text | A note where the Greek differs: 1:9; 6:9–10; 7:14; 8:12–14, 17–18; 8:23–9:1; 10:22–23; 11:10. |
| שְׂרָפִים; צֶמַח (4:2); חֹטֶר, נֵצֶר (11:1) | 撒拉弗；苗；嫩枝、枝子 | *tsemach* and *netser* noted. |
| מַשָּׂא X (13:1; 15:1; 17:1; 19:1; 21:1, 11, 13; 22:1; 23:1) | X的默示： | Heading as the first words of the verse; *massa* noted at 13:1 (「重擔」), later chapters refer back; 14:28 有這默示; 22:25 the same word 重擔 noted. |
| Nations and places (13–23) | 推羅、西頓、大馬色、米底亞、迦勒底、古實、瑣安、挪弗、西曷、基提、他施、度瑪、底但、提瑪、基達 | Union Version forms (classic 推羅, 大馬色); modern identifications (塞浦路斯, 孟斐斯, 努比亞) in notes. |
| הֵילֵל בֶּן־שָׁחַר (14:12) | 晨星，黎明之子 | Long note: *helel*, the Septuagint, the Vulgate's *lucifer*, 和合本「明亮之星，早晨之子」, the later reading of Satan. |
| יַרְכְּתֵי צָפוֹן (14:13) | 北方的極處 | Psalm 48:3 (北方的高處) cross-referred. |
| נְאֻם יְהוָה mid-verse (14:22; 22:25) | 這是……說的 after a clause; 萬軍之耶和華說： opening a verse | 22:14 *amar* (not *ne'um*) closing: ……，主萬軍之耶和華說. |
| לִוְיָתָן; תַּנִּין (27:1) | 利維坦；海怪 | As Job and Psalms; 和合本「鱷魚」 and Ugarit's Litan noted. |
| NT quotations (22:13; 25:8) | The Hebrew in the text | 22:13 1 Corinthians 15:32 agrees (LXX); 25:8 1 Corinthians 15:54 passive 「死亡被吞滅，得了勝利」 (*lanetsach* as victory) and the Septuagint's different line noted. |
| צַו לָצָו … קַו לָקָו (28:10, 13) | 「擦夫拉擦夫……卡夫拉卡夫，這裏一點，那裏一點」 | Transliterated as babble; 「命令上加命令……準繩上加準繩」 and 和合本 noted. |
| פִּנַּת יִקְרַת מוּסָד מוּסָּד (28:16) | 寶貴的房角石，是穩固的根基 | 房角石 as Job 38:6 and 1 Peter 2:6; Psalm 118:22 *rosh pinnah* stays 房角的基石. Romans 9:33; 10:11 and 1 Peter 2:6 (Septuagint 「不至於羞愧」, 「信靠他」) noted. |
| NT quotations (28:11–12; 28:16; 29:13–14; 35:3) | The Hebrew in the text | 29:13 shares Mark 7:6's 「用嘴唇尊敬我，心卻遠離我」; Paul's first person (1 Corinthians 14:21), Mark 7:7 (LXX), 1 Corinthians 1:19, Hebrews 12:12 in notes. |
| אֲרִיאֵל (29:1–7) | 亞利伊勒 | The name; 祭壇的爐臺 at 29:2 (Ezekiel 43:15) noted. |
| אוֹב (29:4) | 亡魂 | The spirit called up; 招魂的 stays for the medium. |
| אַשְׁרֵי (30:18; 32:20) | ……是有福的 | *ashrei* noted, as Psalms. |
| רַהַב (30:7) | 拉哈伯 | As Job 9:13, noted as not 喇合. |
| Animals of the ruins (34:11–15) | 13:21–22 and 14:23's names (曠野的走獸、鬣狗、野山羊、豺狼、鴕鳥、刺蝟); 鵜鶘、大鴞 as Leviticus 11; 黑鳶 (*dayyah*) | *lilit* 夜間的怪物, *qippoz* 貓頭鷹 (和合本「箭蛇」) noted. |
| Isaiah 36–39 (2 Kings 18:13–20:19) | 2 Kings' wording wherever the Hebrew agrees | Differences noted as 列王紀下18章20節作「……」; Isaiah's names (米羅達‧巴拉但, 39:1). 39:6 *amar YHWH* follows Kings' 這是耶和華說的, noted as not *ne'um*. |
| Hezekiah's psalm (38:9–20) | Poetry without quotation marks; 我曾說：「……」 for his quoted thoughts | *mikhtav* 所寫的 (*miktam* noted); *Yah* 耶和華; *bor* 下坑. |
| Isaiah 40:3–5 | 有聲音呼喊：「要在曠野為耶和華預備道路，在沙漠中為我們的神修直大路！」 | Mark 1:3's 有聲音……呼喊 kept; the Hebrew accents join 在曠野 to 預備, the Septuagint and the Gospels to the voice (noted, with 他的路徑). |
| עֶבֶד; עַבְדִּי; עֶבֶד יְהוָה | 僕人；我的僕人；耶和華的僕人 | Israel as 我的僕人 noted at 41:8; the four 「僕人之歌」 (42:1–9; 49:1–13; 50:4–11; 52:13–53:12), the readings of the servant, the Targum and Matthew 12:18–21 noted at 42:1; 49:1, 50:4, 52:13 refer back. |
| אִיִּים | 眾海島 | *iyyim* noted at the first occurrence in each chapter (40:15); 42:15 乾地, noted. |
| גֹּאֵל; גָּאַל; גְּאוּלִים; פָּדָה | 救贖者；救贖；被救贖的人；救贖 | As Job 19:25 and Psalm 19:15; *go'el* noted at 41:14, later chapters refer back. |
| אֲנִי הוּא; אָנֹכִי אָנֹכִי הוּא | 我就是那一位；我，惟有我是那一位 | *ani hu*, the Septuagint's *ego eimi* and John 8:24, 28 noted at 41:4; later chapters refer back. |
| רִאשׁוֹן … אַחֲרוֹן (41:4; 44:6; 48:12) | 我是首先的，我是末後的 | Revelation 1:17; 2:8; 22:13 noted (44:6). |
| הָרִאשֹׁנוֹת; חֲדָשׁוֹת | 先前的事；新的事 | |
| מְבַשֵּׂר, מְבַשֶּׂרֶת | 報好消息的 | *basar* and the New Testament's 福音 noted (40:9; 52:7). |
| מִשְׁפָּט (42:1–4; 49:4) | 公正；公理 (49:4, one's right) | 和合本「公理」 noted at 42:1. |
| כּוֹרֶשׁ; מְשִׁיחוֹ (45:1) | 古列；他的受膏者 | The classic Union form (the 1989 text has 塞魯士); *mashiach* noted. |
| בֵּל; נְבוֹ (46:1) | 彼勒；尼波 | Marduk and Nabu noted. |
| בְּתוּלַת בַּת־בָּבֶל; בַּת־כַּשְׂדִּים; גְּבֶרֶת | 處女巴比倫的女兒；迦勒底人的女兒；女主人 | Feminine *you* noted (47:1); Zion likewise (45:14; 49:15; 51:12). |
| יֹאמַר; אָמַר (closing) | 你們的神說 (40:1)；萬軍之耶和華說 (45:13)；耶和華說： (48:22) | Kept apart from *ne'um* 這是耶和華說的. חַי־אָנִי (49:18) 我指着我的永生起誓, as Numbers 14:21. |
| NT quotations (40:3–8, 13; 42:1–4; 45:23; 49:6, 8; 52:5, 7, 11, 15) | The Hebrew in the text | The Greek in notes: Luke 3:6 「神的救恩」; 1 Peter 1:25 「主的話」; Romans 11:34 「主的心」; Matthew 12:20–21 「使公正得勝」「寄望於他的名」; Romans 14:11 「向神承認」; Acts 13:47; 2 Corinthians 6:2; Romans 2:24 「因你們」; Romans 10:15 (plural, no 山嶺). |
| סִינִים (49:12) | 希尼地 | 和合本「秦國」 (its margin 希尼國) and 1QIsa-a's Syene noted; see REVIEW.md. |
| The fourth servant song (52:13–53:12) | Plain lines for reading aloud: 他被藐視，被人離棄……因他受的鞭傷，我們得了醫治 | Difficult lines (53:8, 10, 11) in the Masoretic text, the other readings noted; 53:11 1QIsa-a 「看見光」 noted. |
| אָשָׁם (53:10); וְאֶת־פֹּשְׁעִים נִמְנָה (53:12) | 贖愆祭；被列在罪犯之中 | 賠償祭 noted; 53:12 as Mark 15:28's note. |
| עַבְדֵי יְהוָה (54:17 to the end) | 耶和華眾僕人 | Plural servants, the faithful in Israel, noted at 54:17. |
| NT quotations (53; 54:1; 55:3; 56:7; 59:7–8, 20–21; 61:1–2; 64:3; 65:1–2; 66:1–2, 24) | The Hebrew in the text | The Greek in notes: John 12:38, Romans 10:16 「主啊」; Matthew 8:17 「軟弱」; Acts 8:32–33; 1 Peter 2:22 「罪」; Luke 22:37 「不法的人」; Luke 4:18–19 「貧窮的人」「瞎眼的得看見」, 58:6 added, 「包紮心靈破碎的人」 only in some manuscripts; 1 Corinthians 2:9 「愛他的人」; Romans 10:20–21 (clauses swapped); Romans 11:26–27 「從錫安出來」; Acts 7:49–50 (question). 56:7 keeps Mark 11:17's 我的殿要稱為萬民禱告的殿; 66:24 keeps Mark 9:48's 蟲不會死，火也不會熄滅. |
| עֲנָוִים (61:1) | 謙卑人 | As 11:4; 29:19. |
| רוּחַ קָדְשׁוֹ (63:10–11) | 他聖潔的靈 | As Psalm 51:13; 傳統「他的聖靈」 and 和合本「主的聖靈」 noted. |
| Numbering of 63:19b–64:11 | 63:19下 = 和合本 64:1；64:1–11 = 和合本 64:2–12 | Noted at 63:19 and 64:1. |
| נָזֹלּוּ (63:19; 64:2) | 崩流 | As Judges 5:5. |
| חֶפְצִי־בָהּ; בְּעוּלָה (62:4) | 「我喜悅她」；「有夫之婦」 | Translated, as the other names in the verse; 協西巴, 比烏拉 noted. |
| גַּד; מְנִי (65:11) | 時運之神；命運之神 | *Gad*, *Meni* noted; the pun with *u-maniti* 我要命定 (65:12). |
| שָׁמַיִם חֲדָשִׁים וָאָרֶץ חֲדָשָׁה (65:17; 66:22) | 新天新地 | 2 Peter 3:13 and Revelation 21:1 noted. |

Settled while drafting Jeremiah:

| Source | Rendering | Notes |
|---|---|---|
| Layout | Isaiah's: one verse per line; oracles without quotation marks; dialogue (1:4–19) and words quoted inside an oracle in 「」 | Noted at 2:2. Prose sermons (7; 11) laid out like the poetry, as in English. |
| נְאֻם יְהוָה; אָמַר יְהוָה (closing) | 這是耶和華說的 (also after a clause, mid-verse)；……，耶和華說 | As Isaiah; *ne'um* noted at its first occurrence in each chapter (1:8). *amar* closing (6:15; 8:12) kept apart. 9:21 *dabber koh ne'um YHWH* 你要這樣說，耶和華說：. |
| שָׁקֵד; שֹׁקֵד (1:11–12) | 杏樹；看守 | The wordplay noted (lost in Chinese); 5:6 *shoqed* 窺伺 refers back. |
| שׁוּב; מְשׁוּבָה; מְשֻׁבָה יִשְׂרָאֵל; בָּנִים שׁוֹבָבִים | 回轉、回來；背道；背道的以色列；背道的兒女 | The *shuv* wordplay noted at 2:19; 3:12, 14; 8:4. |
| בֹּגֵדָה יְהוּדָה; בָּגַד | 奸詐的猶大；行詭詐 | Her *achot* 姊妹 (not 妹妹, as Mark's 兄弟). |
| בַּת־עַמִּי; בַּת־צִיּוֹן | 我的子民；錫安的女兒 | 「我子民的女兒」 noted at its first occurrence in each chapter. |
| יְהוָה אֱלֹהֵי צְבָאוֹת (5:14) | 耶和華萬軍之神 | As 2 Samuel 5:10. |
| קִטֵּר | 燒香 | 或譯「燒祭物」, *qatar* noted at its first occurrence in each chapter. |
| שְׁפָיִם | 光禿的高處 | |
| הַשְׁכֵּם וְדַבֵּר / שָׁלֹחַ / הָעֵד | 從早到晚（一再、不斷）…… | 「早起而說」 noted (7:13; 11:7). |
| הַבַּיִת אֲשֶׁר נִקְרָא־שְׁמִי עָלָיו | 這稱為我名下的殿 | 「我的名在其上被稱呼的」 noted (7:10). |
| מְעָרַת פָּרִצִים (7:11) | 賊窩 | As Mark 11:17, noted. |
| תֹּפֶת; גֵּיא בֶן־הִנֹּם; גֵּיא הַהֲרֵגָה; מְלֶכֶת הַשָּׁמַיִם | 陀斐特；欣嫩子谷；殺戮谷；天后 | 7:18, 31–32. |
| מָגוֹר מִסָּבִיב (6:25) | 四面都是驚嚇 | For 20:3, 10; 46:5; 49:29. |
| הַבֹּשֶׁת | 那可恥的 | Baal, noted (3:24; 11:13). |
| Numbering of 8:23–9:25 | 8:23 = 和合本 9:1；9:1–25 = 和合本 9:2–26 | Noted at 8:23 and 9:1; 9:22–23 (= 和合本 9:23–24) and 1 Corinthians 1:31 noted. |
| The Aramaic of 10:11 | Noted where it starts and ends | |
| Layout of narratives (13:1–11; 14:11–16; 18:1–12; 20:1–6; 21:1–7; 24) | Dialogue in 「」, a message inside 『』 | Sermons and oracles to the people (15–17; 19; 22–23; 25) unmarked, as 7 and 11. |
| יוֹצֵר; חֹמֶר (18:1–11) | 陶匠；泥 | As Isaiah 45:9; 64:7 (Isaiah 29:16 has 窯匠). 18:11 *yotser* 塑造 (noted, as Isaiah 45:9). |
| צֶמַח צַדִּיק; יְהוָה צִדְקֵנוּ (23:5–6) | 公義的苗；「耶和華我們的義」 | *tsemach* as Isaiah 4:2; *YHWH tsidqenu* and the play on 西底家 noted. For 33:15–16. |
| נְבוּכַדְרֶאצַּר; כַּשְׂדִּים | 尼布甲尼撒；迦勒底人 | *Nevukhadre'tsar* noted at 21:2, later chapters refer back; *Kasdim* noted in each chapter. |
| כָּנְיָהוּ; יְכָנְיָהוּ | 哥尼雅 (22:24, 28)；耶哥尼雅 (24:1) | Both noted as 約雅斤. |
| מַשָּׂא יְהוָה (23:33–40) | 耶和華的默示 | The pun with 重擔 noted (23:33, 36). |
| מָגוֹר מִסָּבִיב as a name (20:3) | 瑪歌珥‧米撒畢 | Union Version form; the meaning 四面都是驚嚇 noted. |
| שִׁבְעִים שָׁנָה (25:11–12) | 七十年 | 29:10, 2 Chronicles 36:21, Daniel 9:2 noted. |
| חַי־אָנִי (22:24); חַי־יְהוָה (16:14–15; 23:7–8) | 我指着我的永生起誓；我指着……永活的耶和華起誓 | As Isaiah 49:18 and 12:16. |
| Layout of 33–42 | Narrative speech in 「」, a message inside 『』, a third level 「」; oracles introduced by narrative unmarked where the English leaves them so (33; 34) | As 32. |
| 33:14–26; 33:15–16 | 23:5–6's words (公義的苗；施行公正和公義；猶大必得救……安然居住；「耶和華我們的義」) | Absence from the Septuagint noted at 33:14; *atsmiach* 使……長出來 against 23:5 興起, noted. |
| חֲצַר הַמַּטָּרָה | 護衞兵的院子 | As 32:2; 和合本「護衞兵的院」. |
| דְּרוֹר (34:8–17) | 自由；宣告自由 | *deror* and the Jubilee noted; 34:17 「自由」 in quotation marks for the irony. |
| בֶּן־הַמֶּלֶךְ (36:26; 38:6) | 王子 | 「王族的人」 and 和合本 「哈米勒的兒子」 noted. |
| סֹפֵר (Baruch; Elishama; Jonathan) | 書記 | As Kings. |
| רַב־טַבָּחִים; רַב־סָרִיס; רַב־מָג (39–41) | 護衞長；拉撒力；拉墨 | 拉撒力, 拉墨 as 和合本 Jeremiah (Kings 拉伯撒利 noted), joined to the name with ‧. |
| Jeremiah 39:1–10; 40:7–9; 41:1–3 (2 Kings 25) | 2 Kings 25's wording wherever the Hebrew agrees (眾軍長、部下、剜了……眼睛、用銅鏈鎖着) | Differences noted as 列王紀下25章23節作「……」; names by 和合本 Jeremiah (單戶篾 beside Kings' 單戶蔑). |
| נָפַל אֶל (to the Babylonians) | 投降 | 37:13–14; 38:19; 39:9. יָצָא אֶל (38:17–21) 出去投降, 「出去」 noted. |
| גּוּר (42:15–22) | 寄居 | *gur* noted. |
| מְלֶכֶת הַשָּׁמַיִם; כַּוָּנִים (44:17–25) | 天后；餅 | As 7:18, noted there; *kavvanim* noted (44:19). |
| Oracles against the nations (46–51) | Poetry, one verse per line, unmarked; the heading as the first words (論埃及。論摩押。) | 46:1 notes the Septuagint's place and order. Names by 和合本 Jeremiah: 伯拉河 (classic, not 幼發拉底河), 推羅, 大馬色, 挪弗, 密奪, 答比匿, 迦斐託, 雅雜 (48:21), 愛 (49:3), 瑪勒堪 (49:1, 3, *malkam*/Milcom noted), 挪的亞們 (46:25, the 1989 text 亞捫 noted), 立加米, 示沙克. |
| Jeremiah 48 (Isaiah 15–16; 24:17–18) | Isaiah's wording wherever the Hebrew agrees (魯希坡的山坡；我的心……哀鳴；肥美的田園；恐懼、陷坑和網羅) | Differences noted as 以賽亞書16章6節作「……」. 48:45–46 as Numbers 21:28–29 (有火從希實本發出……你有禍了！基抹的人民). |
| Jeremiah 49:7–22 (Obadiah 1–9) | Sets the wording for Obadiah | Obadiah to follow it where the Hebrew agrees and note differences. 49:18 = 50:40; 49:19–21 = 50:44–46; 49:22 = 48:40–41; 49:26 = 50:30; 50:41–43 = 6:22–24: identical wording, differences noted. |
| חֶרֶב … ; חֹרֶב (50:35–38) | 刀劍臨到……；乾旱臨到…… | The *cherev*/*chorev* play noted. |
| זָדוֹן (50:31–32) | 狂傲者 | As a name for Babylon, noted. |
| פַּחוֹת וּסְגָנִים (51:23, 28, 57) | 省長和地方官 | As Ezra. |
| Jeremiah 52 (2 Kings 24:18–25:30) | 2 Kings' wording wherever the Hebrew agrees | Differences noted as 列王紀下25章8節作「……」; the parallel noted at 52:1; dates 主前 as Jeremiah. |

Settled while drafting Lamentations:

| Source | Rendering | Notes |
|---|---|---|
| Layout | Poetry, one verse per line, cola joined by ，；; no quotation marks for Zion's or the poet's voice | Speakers noted (1:9, 18; 2:11, 20), as in English; words quoted inside the poems 「」 (2:12, 15, 16; 3:18, 24, 54, 57; 4:15, 20). 3:41–47 (the people's prayer) in 「」 after 3:41's colon. |
| Acrostics (1–4) | Noted at verse 1 of each chapter | `*alef*（א）`…`*tav*（ת）`; *pe* before *ayin* in 2–4 (2:16–17; 3:46–51; 4:16–17); chapter 3 three verses per letter (noted at 3:1); 5:1 notes that chapter 5 has 22 verses but no acrostic. |
| אֵיכָה (1:1; 2:1; 4:1, 2) | 怎麼……竟……！ | *eikhah* and the book's Hebrew name noted at 1:1; 2:1 and 4:1 refer back. |
| בַּת־צִיּוֹן; בְּתוּלַת בַּת־יְהוּדָה / צִיּוֹן; בַּת־אֱדוֹם | 錫安的女兒；處女猶大的女兒／處女錫安的女兒；以東的女兒 | As Isaiah 47:1; *bat-tsiyyon* noted at 1:6. |
| בַּת־עַמִּי | 我的子民 | As Jeremiah; 「我子民的女兒」 noted at 2:11, later chapters refer back. |
| נִדָּה (1:8, 17) | 人搖頭厭棄的；不潔之物 | *nidah*/*niddah* noted. |
| חַסְדֵי יְהוָה (3:22) | 我們沒有滅絕，是出於耶和華的慈愛 | The Masoretic reading in the text; the Syriac and Targum 「它沒有窮盡」 noted. |
| עֶלְיוֹן (3:35, 38) | 至高者 | As Psalms. |
| מְשִׁיחַ יְהוָה (4:20) | 耶和華的受膏者 | Zedekiah noted. |
| תַּנִּים (4:3, ketiv *tannin*) | 豺狼 | As Jeremiah 9:10; ketiv noted. |

Settled while drafting Ezekiel:

| Source | Rendering | Notes |
|---|---|---|
| Layout | Narrative with the LORD's speeches in 「」, a message inside 『』 (2–5); oracles opening 耶和華的話臨到我說： unmarked (6–7), as in English | A speech running over chapters (3:24–5:17) reopens 「 at each chapter and closes only at its end (noted 4:1). |
| בֶּן־אָדָם | 人子 | As the Union Version; noted at 2:1 (「人的兒子」, 會死的凡人, used more than ninety times), later chapters refer back (見2章1節). |
| אֲדֹנָי יְהוִה | 主耶和華 | *Adonai YHWH* noted at its first occurrence in each chapter, with the YHWH note where 耶和華 has not yet appeared; 2:4 says Ezekiel uses it more than two hundred times. אֲהָהּ אֲדֹנָי יְהוִה (4:14) 唉，主耶和華啊！ as Jeremiah 1:6. |
| כֹּה אָמַר אֲדֹנָי יְהוִה; נְאֻם אֲדֹנָי יְהוִה | 主耶和華這樣說；這是主耶和華說的 | As Isaiah; *ne'um* noted at its first occurrence in each chapter (5:11). חַי־אָנִי (5:11) 我指着我的永生起誓. |
| אֲנִי יְהוָה דִּבַּרְתִּי | 這是我耶和華說的 | 5:15, 17. |
| וִידַעְתֶּם / וְיָדְעוּ כִּי־אֲנִי יְהוָה | 你們就知道我是耶和華；他們就知道我是耶和華 | Identical every time (6:7, 10, 13, 14; 7:4, 27), noted at its first occurrence (6:7); expansions keep the opening (5:13 他們就知道是我耶和華……說了這話; 7:9 你們就知道擊打你們的是我耶和華). |
| וַתְּהִי עָלַי יַד־יְהוָה | 耶和華的手臨到我（他）身上 | 1:3 noted (3:14, 22; 8:1; 37:1; 40:1); 3:14 *chazaqah* 耶和華的手大有能力地臨到我身上. |
| וַיְהִי דְבַר־יְהוָה אֵלַי לֵאמֹר | 耶和華的話臨到我說： | |
| The chariot vision (1; 10): חַיּוֹת; אוֹפַן, אוֹפַנִּים; רָקִיעַ; כִּסֵּא; דְּמוּת כְּבוֹד־יְהוָה | 活物；輪；穹蒼；寶座；耶和華榮耀的形象 | For chapter 10 and 43. *chayyot* and the cherubim (10:15, 20), *ofan*, *raqia* (as Genesis 1) noted. דְּמוּת 形象, מַרְאֶה 樣貌, עֵין 光彩 kept apart throughout 1:4–28. |
| חַשְׁמַל (1:4, 27; 8:2) | 琥珀金 | Settled (REVIEW.md): one rendering in all three verses, the note at 1:4, 8:2 refers back. The Septuagint's *elektron* (amber, electrum) and 和合本「光耀的精金」 noted. *tarshish* 水蒼玉, *sappir* 青金石, *nesher* 鷹, *qerach* 水晶, as earlier books. |
| רוּחַ (1:12, 20; 2:2; 3:12, 14, 24) | 靈 | *ruach* (靈、風、氣息) noted. |
| בֵּית מְרִי; מֶרִי | 悖逆的家；悖逆的 | |
| תּוֹעֵבוֹת; גִּלּוּלִים; שִׁקּוּצִים | 可憎的事；可憎的偶像；可厭之物 | As the Exodus table; each noted at its first occurrence in each chapter. |
| חַמָּנִים; בָּמוֹת | 香壇；丘壇 | 6:4, 6. |
| צֹפֶה (3:17) | 守望的人 | For 33:7. |
| מִכְשׁוֹל עָוֹן | 絆腳石；使……陷入罪孽的絆腳石 | 3:20; 7:19; noted for 14:3–4; 18:30; 44:12. |
| נָשִׂיא (of the king) | 領袖 | As the Exodus table; noted at 7:27 (12:10; 34:24; 37:25; 44–48). |
| עַם הָאָרֶץ | 普通百姓 | As Leviticus; 7:27 這地普通百姓. |
| נִדָּה (7:19–20) | 不潔之物 | As Lamentations 1:17. |
| Chapter 10 (= chapter 1) | 活物／基路伯、輪、穹蒼、寶座、形象、樣貌、光彩、水蒼玉、青金石 | Chapter 1's wording wherever the Hebrew agrees (10:9–11, 17 as 1:16–17, 21). גַּלְגַּל 旋輪 (10:2, 6, 13), kept apart from 輪 (*ofan*), noted. |
| סֵמֶל הַקִּנְאָה (8:3, 5) | 忌恨的偶像 | *semel*, *qin'ah* noted with 忌邪的神 (Exodus 20:5). |
| וַתִּפֹּל עָלַי יַד (8:1); רוּחַ יְהוָה (11:5) | 耶和華的手臨到我身上；耶和華的靈降在我身上 | 「落在」 noted. |
| הוֹי; אוֹי אוֹי לָךְ | 禍哉；你有禍了！你有禍了！ | As Isaiah; *hoy* noted (13:3); 16:23 in （）. |
| מַעַל | 不忠 | *ma'al* noted at its first occurrence in each chapter (14:13; 15:8; 17:20; 18:24). |
| נֹחַ, דנאל, אִיּוֹב (14:14, 20) | 挪亞、但以理、約伯 | Ketiv *Dan'el*, qere *Daniyyel*, and Ugarit's Dan'el noted (for 28:3). |
| מָשָׁל; חִידָה | 俗語 (12:22; 16:44; 18:2)、比喻 (17:2)；謎語 | 18:2 as Jeremiah 31:29. |
| זָנָה; תַּזְנוּת; זוֹנָה; אֶתְנַן (16; for 23) | 行淫；淫行；妓女；酬金 | *zanah* noted at 16:15. The allegory plain, neither coarsened nor softened (16:25 張開雙腿; 16:26 下體粗大, *basar* noted). |
| The ketiv *-ti* for "you" (16) | The qere | One combined note (16:13), as in English. |
| גַּב; רָמָה (16:24–39) | 土臺；高臺 | Noted. |
| טָפֵל (13:10–15); כְּסָתוֹת; מִסְפָּחוֹת | 白灰；符帶；蒙頭的帕子 | 和合本「未泡透的灰」「靠枕」 noted. |
| אֲדֹנָי alone (18:25, 29) | 主 | Noted: not YHWH. |
| קִינָה (19:1, 14) | 哀歌 | *qinah* noted. Chapters 17 and 19 (parables, lament) one verse per line, cola joined by ，；. |
| Numbering | Ezekiel 8–19 = 和合本 | No shift in 8–19 (the next is 21:1–5 = 和合本 20:45–49). |
| Numbering of 20–21 | 21:1–5 = 和合本 20:45–49；21:6–37 = 和合本 21:1–32 | Noted at 20:44, 21:1 and 21:6; 22–32 = 和合本. |
| Dates | 第七年五月十日；第十一年，某月初一 | Chinese numerals; a month the Hebrew leaves out is 某月 (26:1; 32:17), noted; the year BC in a note. |
| עָגַב; Oholah and Oholibah (23) | 迷戀；阿荷拉、阿荷利巴 | Chapter 16's 行淫、淫行、愛人、淫蕩、酬金 kept; the imagery as plain as 16 (23:3, 8, 20–21). Names' meanings noted at 23:4. |
| פַּחוֹת וּסְגָנִים; שָׁלִשִׁים (23) | 省長和地方官；軍官 | As Jeremiah 51:23; *shalishim* noted. |
| הִנְנִי עָלַיִךְ / אֵלַיִךְ | 看哪，我要與你為敵 | 21:8; 26:3; 28:22; 29:3, 10; 30:22. |
| נְבוּכַדְרֶאצַּר | 尼布甲尼撒 | *Nevukhadre'tsar* noted at 26:7; 29:18 and 30:10 refer back. |
| Oracles against the nations (25–32) | Unmarked, as 6–7; names as the Union Version | 推羅 (classic), 西頓, 亞發, 迦巴勒, 大馬色, 雅完, 陀迦瑪, 基抹 (*Kilmad*, noted as not Chemosh), 迦瑪 (*Gammadim*, 和合本「勇士」), 挪弗, 挪, 訓, 瑣安, 巴忒羅, 古實, 古巴, 亞文, 比伯實, 答比匿; 密奪 as Jeremiah (和合本 Ezekiel「色弗尼塔」 noted, 29:10; 30:6). |
| The stones of 28:13; 27:16 | Exodus 28's names: 肉紅玉髓、貴橄欖石、月長石、水蒼玉、紅瑪瑙、碧玉、青金石、綠松石、綠寶石 | Traditional names noted. 27:16 *nofekh* 綠松石, *ra'mot* 珊瑚, *kadkod* 紅寶石 as Job 28:18 and Isaiah 54:12. |
| כְּרוּב מִמְשַׁח הַסּוֹכֵךְ (28:14, 16); עֵדֶן גַּן־אֱלֹהִים | 受膏、遮掩的基路伯；伊甸，就是神的園 | *at*/*et*, *mimshach* and the Septuagint's reading noted. 28:12–19 one verse per line, as 19. |
| אֵל; אֱלֹהִים (the king's claim, 28:2, 6, 9) | 神明 | 或譯「神」 noted. |
| יְאֹר; יְאֹרִים | 尼羅河；河道 | As Genesis 41 and Exodus 7; 29:3, 9 「尼羅河是我的」. |
| תַּנִּים (29:3; 32:2) | 大海怪 | Crocodile and 和合本「大魚」 noted. |
| הָמוֹן (of Egypt) | 群眾 (財富 where it is carried off: 29:19; 30:4, 10) | *hamon* noted at 29:19, later chapters refer back. |
| בּוֹר; יוֹרְדֵי בוֹר; אֶרֶץ תַּחְתִּיּוֹת; שַׁחַת; שְׁאוֹל | 坑；下坑的人；地底深處；墳坑；陰間 | As Psalms and Isaiah 38 (26:20; 28:8; 31:14–17; 32:18–32). |
| עֲרֵלִים; חַלְלֵי־חֶרֶב | 未受割禮的人；被刀殺的人 | A death in disgrace, noted at 28:10 (31:18; 32:19–32). |
| 33:1–20 (3:17–21; 18:21–32) | Chapters 3 and 18's wording wherever the Hebrew agrees (守望的人；我卻要你為他流血的罪負責；主的道不公平；我必按你們各人所行的審判你們) | Differences noted (33:7, 18). שְׁמָמָה וּמְשַׁמָּה 荒涼淒慘, as 6:14 (33:28–29; 35:3, 7). |
| Shepherds (34) | 牧人；羊群；草場；牧養；我的僕人大衛……作他們的牧人 | As Jeremiah 23:1–4; the king as shepherd noted at 34:2; בְּרִית שָׁלוֹם 平安的約, as Isaiah 54:10 (34:25; 37:26). |
| 36:25–27 | 清水；新心；新的靈；石心；肉心；我的靈 | As 11:19 and 18:31; *ruach* noted at 36:27. |
| רוּחַ (37:1–14) | 靈 (37:1, 14)；氣息 (37:5–10)；四方的風 (37:9) | One long note at 37:1 on the three senses and the wordplay; בִּקְעָה 平原 as 3:22, 「山谷」 noted. |
| עֵץ (37:15–28) | 木杖 | *ets* noted (37:16). |
| גּוֹג אֶרֶץ הַמָּגוֹג נְשִׂיא רֹאשׁ מֶשֶׁךְ וְתֻבָל (38:2–3; 39:1) | 瑪各地的歌革，就是羅施、米設、土巴的領袖 | Rosh as a name, as the Union Version and the Septuagint; 「米設、土巴的大領袖」 (*nesi rosh*) and 和合本「王」 noted (38:2). 哈們‧歌革谷, 哈摩那 (39:11, 16). |
| Temple vision (40–42): הֵיכָל; אוּלָם (of the house); קֹדֶשׁ הַקֳּדָשִׁים; צֵלָע | 大殿；前廊；至聖所；廂房 | As 1 Kings 6 and 2 Chronicles 3–4; עָב 簷篷 as 1 Kings 7:6. |
| Gates and courts: תָּא; אַיִל; אוּלָם / אֵלָם הַשַּׁעַר; סַף; רִצְפָה; לִשְׁכָּה; חָצֵר הַחִיצוֹנָה / הַפְּנִימִית | 衞房；牆柱；門廊；門檻；鋪石地；房間；外院／內院 | *ta*, *ayil*, *elammot* noted (40:7–16). The singular ketiv / plural qere of chapter 40 in one note (40:6). |
| גִּזְרָה; בִּנְיָן; מֻנָּח; אַתִּיק | 隔開的地方；建築物；空地；樓廊 | Each noted as uncertain (41:9–15; 42:1–5). |
| קְנֵה הַמִּדָּה; the long cubit (40:5; 43:13) | 量度竿，一竿；一肘另加一掌寬 | Chinese numerals in the text; metric in notes (長肘約 52.5 厘米，一竿約 3.2 米); a unit the Hebrew omits is not supplied (45:1; 48). |
| The altar (43:13–17): חֵיק; עֲזָרָה; גְּבוּל; הַרְאֵל / אֲרִיאֵל; זֶרֶת | 底座；臺層；邊沿；爐臺；虎口 | *azarah* (和合本「磴臺」) and *har'el*/*ari'el* noted, with Isaiah 29:1–2. חִטֵּא 潔淨……除去它的罪; מִלֵּא יָד (of the altar) 分別為聖, 「充滿它的手」 noted. |
| Speech of 44:5–46:18 | 「 opened at 44:5, the message 『 at 44:6, both reopened (「『) at 45:1 and 46:1, closed 』」 at 46:18 | 47:13–48:35 one speech, 「 reopened at 48:1, closed at 48:35 (『耶和華在那裏』). |
| תְּרוּמָה (land, 45; 48); תְּרוּמַת הַקֹּדֶשׁ; אֲחֻזָּה; נַחֲלָה; מִגְרָשׁ | 獻地；聖獻地；地業；產業；草場 | *terumah* noted at 45:1 as the word for 舉祭 (offerings: 舉祭, 45:13, 16). |
| Measures (45:10–14) | 伊法；罷特；賀梅珥；柯珥；欣；舍客勒；季拉；彌那 | Values in notes. דְּרוֹר (46:17) 自由之年, Jubilee noted. |
| Tribal portions (48) | 挨着X的地界，從東到西，是Y的一份 | One line throughout; tribe names as settled (呂便, as Genesis). City gates 呂便門、猶大門…… (48:31–34). יְהוָה שָׁמָּה 『耶和華在那裏』, 和合本「耶和華的所在」 noted. |
| Numbering of 33–48 | = 和合本 | No differences. |

Settled while drafting Daniel:

| Source | Rendering | Notes |
|---|---|---|
| Layout | Narrative with speeches in 「」 (1–6); visions told by Daniel in 「」 from 7:2, the angel's words inside 『』 | 10:20–12:4 one speech, 「 reopened at 11:1 and 12:1, closed at 12:4 (noted 11:1). Prayers and doxologies (2:20–23; 3:31–33; 4:31–32; 6:27–28; 7:9–14; 9:24–27) one verse per line. |
| The Aramaic of 2:4b–7:28 | Noted where it starts and ends | 2:4 (用亞蘭語), 7:28, 8:1; and in the first note of 3–7, as Ezra. |
| Numbering | 3:31–33 = 和合本 4:1–3；4:1–34 = 和合本 4:4–37；6:1 = 和合本 5:31；6:2–29 = 和合本 6:1–28 | Noted at 3:31, 4:1, 6:1; other references give both (4章5節（和合本作4章8節）). |
| חַרְטֻמִּים; אַשָּׁפִים; מְכַשְּׁפִים; כַּשְׂדִּים; גָּזְרִין | 術士；巫師；行邪術的；迦勒底人；占卜的 | *chartummim* as Exodus; *ashshafim* (1:20), *kasdim* as a class of scholars (2:2), *gazerin* (2:27) noted. |
| חַכִּימִין; רַב סָרִיסִים; מֶלְצַר | 智慧人；宮廷總管；看守 | *sarisim* (官員，也可指太監) and *meltsar* noted (1:3, 11). |
| Officials (3:2; 6:2–8): אֲחַשְׁדַּרְפְּנִין; סִגְנִין; פַּחֲוָן; סָרְכִין; הַדָּבְרִין | 總督；地方官；省長；總長；謀士 | As Ezra; 謀士、司庫、法官、執法官 for the rest of 3:2. |
| עִלָּאָה, עֶלְיוֹנִין; אֱלָהָא עִלָּאָה; אֱלָהּ שְׁמַיָּא | 至高者；至高的神；天上的神 | As Genesis 14. |
| עִיר וְקַדִּישׁ (4:10, 14, 20) | 守望者，就是聖者 | *ir* noted. |
| עִדָּן, עִדָּנִין; מוֹעֵד | 期 (七期, 4:13)；一期、兩期、半期 (7:25; 12:7) | Noted: probably years; three and a half years. |
| עַתִּיק יוֹמִין (7:9, 13, 22) | 亙古常在者 | As the Union Version; 「日子久遠的那位」 noted. |
| כְּבַר אֱנָשׁ (7:13) | 一位像人子的，駕着天上的雲而來 | Echoes Ezekiel's 人子 (*ben adam*) and Mark 13:26; 14:62 (人子駕着雲降臨); the readings of the figure noted. 8:17 בֶּן־אָדָם 人子, as Ezekiel. |
| קַדִּישֵׁי עֶלְיוֹנִין (7:18, 22, 25); עַם קַדִּישֵׁי עֶלְיוֹנִין (7:27); קַדִּישִׁין (7:21–22) | 至高者的聖民；至高者聖民的百姓；聖民 | 「至高者的聖者們」 (angels or the faithful) noted at 7:18. |
| שַׂר (of angels and God) | 君 | 波斯國的君 (和合本「魔君」, 10:13)；為首的君米迦勒；大君米迦勒 (12:1)；天軍之君 (8:11)；萬君之君 (8:25). |
| הַתָּמִיד | 經常獻的燔祭 | As Numbers 28; noted at 8:11. |
| שָׁבֻעִים שִׁבְעִים (9:24–27) | 七十個七；七個七；六十二個七；一七；一七之半 | Noted: *shavua* usually 「星期」, hence 「七十個星期」; taken as weeks of years. 9:25 follows the Masoretic accents (seven apart from sixty-two), 和合本 joins them (noted). |
| מָשִׁיחַ נָגִיד (9:25); מָשִׁיחַ (9:26) | 受膏的領袖；受膏者 | 和合本「受膏君」 and the readings (Cyrus, Onias, the Messiah) noted. |
| הַשִּׁקּוּץ מְשׁוֹמֵם (11:31); שִׁקּוּץ שֹׁמֵם (12:11); שִׁקּוּצִים מְשֹׁמֵם (9:27); הַפֶּשַׁע שֹׁמֵם (8:13) | 那帶來荒涼的可憎之物；帶來荒涼的罪過 | As Mark 13:14; *shiqquts* here 可憎之物, not Ezekiel's 可厭之物 (noted 9:27). |
| חַיֵּי עוֹלָם (12:2) | 永生 | As Mark's ζωὴ αἰώνιος; noted as its only occurrence in the Old Testament. |
| מַשְׂכִּילִים (11:33, 35; 12:3, 10) | 有智慧的人 | *maskilim* noted. |
| מֶלֶךְ הַנֶּגֶב; מֶלֶךְ הַצָּפוֹן; אֶרֶץ הַצְּבִי | 南方王；北方王；榮美之地 | The Ptolemies and Seleucids named only in notes. |
| Names | 伯提沙撒、沙得拉、米煞、亞伯尼歌、伯沙撒、亞施毘拿、亞略、米底亞人大流士、古列、加百列、米迦勒、希底結、烏萊河、書珊城、杜拉、烏法、路比人 | Darius 大流士 as Ezra (the classic text 大利烏); Cyrus 古列 and Tigris 希底結 (the 1989 text 塞魯士, 底格里斯); 毘 for 亞施毘拿 and 毘勒斯 (5:28). 彌尼，彌尼，提客勒，烏法珥新 (5:25). |

Settled while drafting Hosea:

| Source | Rendering | Notes |
|---|---|---|
| Layout | Narrative with the LORD's words in 「」 (1; 3); oracles unmarked (2; 4–14), words quoted inside them 「」 | As Isaiah and Jeremiah. |
| Numbering | 2:1–2 = 和合本 1:10–11；2:3–25 = 和合本 2:1–23；12:1 = 和合本 11:12；12:2–15 = 和合本 12:1–14；14:1 = 和合本 13:16；14:2–10 = 和合本 14:1–9 | Noted at 1:9, 2:1; 11:11, 12:1; 13:15, 14:1; other references give both. |
| יִזְרְעֶאל; לֹא רֻחָמָה; לֹא עַמִּי; עַמִּי; רֻחָמָה | 耶斯列；羅‧路哈瑪；羅‧阿米；阿米；路哈瑪 | Union Version forms; meanings in notes (「神撒種」「不蒙憐憫」「不是我的子民」), 2:25 links them. |
| זָנָה; זְנוּנִים; נָאַף; אֶתְנָה, אֶתְנַן; קְדֵשׁוֹת | 行淫；淫亂；通姦（姦淫）；酬金；廟妓 | *zenunim* noted at 1:2 as the image of Israel's unfaithfulness. |
| חֶסֶד | 慈愛 | Glossary note at 2:21; 4:1; 6:4; 10:12; 12:7. 6:6 notes Matthew 9:13; 12:7 (*eleos* 「憐憫」, LXX). |
| רִיב | 爭訟；控告 (2:4) | *riv* noted at 4:1; 12:3 refers back. |
| אֶפְרַיִם | 以法蓮 | Noted at 4:17 as the northern kingdom. |
| בֵּית אָוֶן; אָוֶן | 伯‧亞文；亞文 | 「罪惡之家」, Bethel mocked, noted at 4:15; 10:8. |
| הַבְּעָלִים; הַבֹּשֶׁת | 眾巴力；那可恥的 | As Judges and Jeremiah (2:15; 9:10). |
| עֲגָלוֹת; עֵגֶל שֹׁמְרוֹן | 牛犢；撒馬利亞的牛犢 | 8:5–6; 10:5 (feminine plural noted). |
| מֶלֶךְ יָרֵב (5:13; 10:6) | 大王 | *malki rav* read; 和合本「耶雷布王」 noted. |
| שָׁב שְׁבוּת (6:11) | 扭轉……的命運 | As Job and Psalms. |
| מִצְרַיִם … קָרָאתִי לִבְנִי (11:1) | 我從埃及召出我的兒子 | Matthew 2:15 follows the Hebrew, the Septuagint 「他的兒女」, noted. |
| אֱהִי … שְׁאוֹל (13:14) | 死亡啊，你的災害在哪裏？陰間啊，你的毀滅在哪裏？ | *ehi* 「我要作」, the Septuagint and 1 Corinthians 15:55 (「勝利」「毒鉤」) noted. |
| מֹף (9:6) | 摩弗 | As 和合本 Hosea; 挪弗 elsewhere, noted. |

Settled while drafting Joel:

| Source | Rendering | Notes |
|---|---|---|
| Numbering | 3:1–5 = 和合本 2:28–32；4:1–21 = 和合本 3:1–21 | Noted at 2:27, 3:1, 4:1. |
| יוֹם יְהוָה | 耶和華的日子 | Identical every time (1:15; 2:1, 11; 3:4; 4:14); 1:15 as Isaiah 13:6; 3:4 「在耶和華的日子，那大而可畏的日子來到以前」 keeps the phrase whole. |
| גָּזָם; אַרְבֶּה; יֶלֶק; חָסִיל | 剪蟲；蝗蟲；蝻子；螞蚱 | As Psalms and 1 Kings 8:37; noted at 1:4. |
| קַדְּשׁוּ־צוֹם; עֲצָרָה | 分別出禁食的日子；嚴肅的聚會 | 1:14; 2:15. |
| חַנּוּן וְרַחוּם אֶרֶךְ אַפַּיִם וְרַב־חֶסֶד (2:13) | 有恩典、有憐憫，不輕易發怒，大有慈愛 | As Psalm 145:8. |
| אֶשְׁפּוֹךְ אֶת־רוּחִי עַל־כָּל־בָּשָׂר (3:1–5) | 我要把我的靈傾倒在所有的人身上 | Acts 2:17–21's differences (LXX) noted at 3:1; 3:5 Romans 10:13 「主的名」. |
| עֵמֶק יְהוֹשָׁפָט; עֵמֶק הֶחָרוּץ; נַחַל הַשִּׁטִּים | 約沙法谷；斷定谷；什亭谷 | Union Version names; meanings noted. |
| בְּנֵי הַיְּוָנִים (4:6) | 希臘人 | As 和合本 Joel; *Yevanim* and Isaiah 66:19's 雅完 noted. |

Settled while drafting Amos:

| Source | Rendering | Notes |
|---|---|---|
| Layout | Oracles unmarked; the visions and Amaziah's story (7:1–17; 8:1–3) with dialogue in 「」, a message inside 『』 | 9:1 他說： then unmarked, as in English. |
| עַל־שְׁלֹשָׁה פִּשְׁעֵי X וְעַל־אַרְבָּעָה לֹא אֲשִׁיבֶנּוּ (1:3–2:6) | X有三項罪行，甚至有四項，我必不撤回 | Identical in all eight oracles; *pesha* and the number saying noted at 1:3, 「我必不使它回轉」 at 1:3. |
| וְשִׁלַּחְתִּי אֵשׁ בְּ… וְאָכְלָה אַרְמְנוֹת | 我要降火在……，燒毀……的堡壘 | As Hosea 8:14; *armenot* noted at 1:4. |
| אָמַר יְהוָה (closing); נְאֻם יְהוָה | ……，耶和華說；這是耶和華說的 | Kept apart, as Isaiah and Jeremiah; *ne'um* noted at its first occurrence in each chapter. |
| יְהוָה אֱלֹהֵי צְבָאוֹת; אֲדֹנָי יְהוִה אֱלֹהֵי הַצְּבָאוֹת | 耶和華萬軍之神；主耶和華萬軍之神 | As Jeremiah 5:14; 9:5 *Adonai YHWH ha-tseva'ot* 主萬軍之耶和華. |
| הוֹי | 禍哉 | *hoy* noted at 5:18 (and Micah 2:1); 6:1 refers back. |
| יוֹם יְהוָה (5:18–20) | 耶和華的日子 | As Joel. |
| אֲנָךְ (7:7–8) | 鉛垂線 | 和合本「準繩」 and the reading 「錫」 noted. |
| קַיִץ; קֵץ (8:1–2) | 夏天的果子；結局 | The wordplay noted. |
| סִכּוּת; כִּיּוּן (5:26) | 西固特；基雲 | Coined; the Septuagint, Acts 7:42–43 and 和合本 noted. |
| סֻכַּת דָּוִיד (9:11–12) | 大衛那倒塌的棚子 | Acts 15:16–17 (Septuagint: 「人」 for Edom, 「尋求」, 「主」) noted at 9:12. |
| Hymns (4:13; 5:8–9; 9:5–6) | …的，他的名是耶和華（萬軍之神） | Noted at 4:13 as the first of three. |

Settled while drafting Obadiah:

| Source | Rendering | Notes |
|---|---|---|
| Obadiah 1–9 (Jeremiah 49:7–22) | Jeremiah 49's wording wherever the Hebrew agrees (我們從耶和華那裏聽見了消息；住在巖石穴中；你心中的驕傲欺騙了你；我必從那裏把你拉下來) | Differences noted as 耶利米書49章14節作「……」 (1–7). |
| יוֹם (11–14) | ……的日子，你不該…… | The commands as reproach; 「你本不該」 noted at 12. |
| מוֹשִׁעִים; שָׁפַט (21) | 拯救者；治理 | As Judges; noted. |

Settled while drafting Jonah:

| Source | Rendering | Notes |
|---|---|---|
| Numbering | 2:1 = 和合本 1:17；2:2–11 = 和合本 2:1–10 | Noted at 1:16 and 2:1. |
| Jonah's psalm (2:3–10) | Poetry, one verse per line, no quotation marks; 2:3 opens 說： | Psalm echoes noted in Psalms' wording (42:8; 120:1; 31:7; 3:9). |
| מִנָּה (2:1; 4:6–8) | 安排 | One verb throughout, noted. |
| קִיקָיוֹן | 蓖麻 | 「葫蘆」 noted. |
| רָעָה (3:8–4:6) | 惡；災禍；不高興；苦楚 | The one word noted at 3:10; 4:1, 6. |
| 4:2; 3:9 | Joel 2:13–14's wording (有恩典、有憐憫……不降災禍；誰知道呢？也許……) | |

Settled while drafting Micah:

| Source | Rendering | Notes |
|---|---|---|
| Numbering | 4:14 = 和合本 5:1；5:1–14 = 和合本 5:2–15 | Noted at 4:14 and 5:1. |
| Micah 4:1–3 (Isaiah 2:2–4) | Isaiah 2's wording wherever the Hebrew agrees | Differences noted (列民／萬國；許多國家／許多民族；遠方強盛的國家). |
| Micah 3:12 (Jeremiah 26:18) | 錫安必被犁成田地，耶路撒冷必變成廢墟堆，這殿所在的山必成為長滿樹木的高崗 | Identical with Jeremiah 26:18. |
| בֵּית־לֶחֶם אֶפְרָתָה (5:1) | 伯利恆‧以法他 | Matthew 2:6's Greek (「在猶大的首領中絕不是最小的」, with 2 Samuel 5:2) and *alfei*/*allufei* noted. |
| Wordplays on towns (1:10–15) | Union Version names in the text | Each pun explained in a note. |
| עֲשׂוֹת מִשְׁפָּט וְאַהֲבַת חֶסֶד וְהַצְנֵעַ לֶכֶת (6:8) | 行公正，愛慈愛，謙卑地與你的神同行 | *chesed* and *hatsnea* noted; 和合本「好憐憫」 mentioned. |
| רִיב (6:1–2) | 案件；控訴；爭訟 | *riv* noted, as Hosea 4:1. |
| מִי־אֵל כָּמוֹךָ (7:18) | 有哪一位神像你呢？ | The echo of 彌迦 noted. |

Settled while drafting Nahum:

| Source | Rendering | Notes |
|---|---|---|
| Numbering | 2:1 = 和合本 1:15；2:2–14 = 和合本 2:1–13 | Noted at 1:14 and 2:1. |
| מַשָּׂא נִינְוֵה (1:1) | 尼尼微的默示 | *massa* noted, as Isaiah 13:1. |
| 2:1 (Isaiah 52:7) | 看哪，那報好消息的人，他的腳登上山嶺，他傳揚平安！ | Isaiah 52:7's words; *mevasser* and Romans 10:15 noted. |
| הִנְנִי אֵלַיִךְ (2:14; 3:5) | 看哪，我要與你為敵 | As Ezekiel. |
| בְּלִיַּעַל (1:11; 2:1) | 邪惡的；那邪惡的 | *beliyya'al* noted. |
| נֹא אָמוֹן (3:8) | 挪亞們 | As 和合本 Nahum; Thebes noted (挪 in Jeremiah and Ezekiel). |
| יֶלֶק; אַרְבֶּה (3:15–17) | 蝻子；蝗蟲 | As Joel 1:4. |

Settled while drafting Habakkuk:

| Source | Rendering | Notes |
|---|---|---|
| Layout | The LORD's replies (1:5–11; 2:2–20) in 「」, the taunt song (2:6–19) inside 『』 | As in English; noted at 1:1. |
| וְצַדִּיק בֶּאֱמוּנָתוֹ יִחְיֶה (2:4) | 義人必因他的信實而活 | *emunah* noted, with 「因他的信心」, the Septuagint's 「我的信實」, Romans 1:17 and Galatians 3:11 (「義人必因信而活」) and Hebrews 10:37–38 (Septuagint, lines reversed). |
| Habakkuk 3 (a psalm) | 先知哈巴谷的禱告。按照示迦庸。…細拉。…交給詩班長。用我絲弦的樂器。 | Psalms' rules: *shigyonot* as the plural of 示迦庸 (Psalm 7:1), 和合本「調用流離歌」; 細拉 after the line's 。; *lamenatseach* closing the psalm noted. No numbering difference. |
| יְהוִה אֲדֹנָי (3:19) | 耶和華主 | As settled; 3:19 noted against Psalm 18:34. |
| דֶּבֶר; רֶשֶׁף (3:5) | 瘟疫；熱病 | Resheph the god noted. |
| tiqqune sopherim (1:12) | 文士的修正 | Also Zechariah 2:12; Malachi 1:13. |

Settled while drafting Zephaniah:

| Source | Rendering | Notes |
|---|---|---|
| מַלְכָּם (1:5) | 瑪勒堪 | As 和合本 and Jeremiah 49:1; *malkam*/Milcom noted. |
| מִשְׁנֶה; מַכְתֵּשׁ (1:10–11) | 第二區；瑪革提施 | 2 Kings 22:14's 第二區; *makhtesh* as 和合本's name, its meaning noted. |
| יוֹם יְהוָה (1:7, 14–18; 2:2–3) | 耶和華的日子；耶和華發怒的日子 | 1:15 shares Joel 2:2's 黑暗幽冥的日子，密雲漆黑的日子; *Dies irae* noted. |
| הַס (1:7) | 肅靜 | As Habakkuk 2:20 and Zechariah 2:17. |
| שָׁב שְׁבוּת (2:7; 3:20) | 扭轉……的命運 | As Job and Psalms. |
| קָאַת; קִפֹּד (2:14) | 鵜鶘；刺蝟 | As Isaiah 34:11. |
| 3:19 | Micah 4:6's 瘸腿的……被趕散的 | |

Settled while drafting Haggai:

| Source | Rendering | Notes |
|---|---|---|
| דָּרְיָוֶשׁ | 大利烏 | Settled (REVIEW.md); the 1989 text's 大流士 noted at Haggai 1:1 and Zechariah 1:1. |
| פַּחַת יְהוּדָה | 猶大省長 | As Ezra and Nehemiah; *pechah* noted at 1:1 (Malachi 1:8 省長). |
| יְהוֹשֻׁעַ בֶּן־יְהוֹצָדָק | 約撒答的兒子約書亞 | 和合本 Haggai and Zechariah; Ezra's 耶書亞, 約薩達 noted at Haggai 1:1. |
| Dates | 大利烏王第二年六月初一 | The date BC in a note. |
| בְּיַד חַגַּי | 藉着哈該 | 「藉着……的手」 noted. |
| Dialogue (2:12–19) | 「」 | As in English. |
| חוֹתָם (2:23) | 帶印的戒指 | As Jeremiah 22:24, noted. |

Settled while drafting Zechariah:

| Source | Rendering | Notes |
|---|---|---|
| Numbering | 2:1–4 = 和合本 1:18–21；2:5–17 = 和合本 2:1–13 | Noted at 1:17 and 2:1. |
| The night visions (1:7–6:15) | Dialogue in 「」, a message inside 『』 (1:14–17; 2:8–9) | 1:7 notes the eight visions. הַמַּלְאָךְ הַדֹּבֵר בִּי 那與我說話的天使; אֲדֹנִי 我主 (*adoni* noted). |
| הַשָּׂטָן (3:1–2) | 撒但 | Job 1:6's note (*ha-satan*, 那控告者). |
| צֶמַח (3:8; 6:12) | 苗 | As Isaiah 4:2 and Jeremiah 23:5; 6:12 「苗」 as a name in 「」. |
| מַשָּׂא (9:1; 12:1; Malachi 1:1) | 默示： | Heading as the first word; *massa* noted at 9:1, with the later date of 9–14. |
| 9:9 (Matthew 21:5; John 12:15) | 他是公義的，是得勝的，是謙卑的，騎着驢，騎着驢駒，就是母驢的崽子 | *nosha*, *ani* noted; the Gospels' shorter Greek in the note. |
| 11:12–13 (Matthew 27:9–10) | 三十塊銀子；陶匠 | *ha-yotser*, the Syriac 「庫房」, Exodus 21:32 and Matthew's Greek noted. Staffs 恩惠, 聯合 (和合本「榮美」「聯索」 noted). |
| 12:10 (John 19:37) | 他們必仰望我，就是他們所刺的那一位 | 「我」/「他」, the Septuagint and John's Greek noted; 13:3 *daqar* refers back. |
| 13:7 (Mark 14:27) | 擊打牧人，羊就分散了 | Mark 14:27's words; the Gospels' first person 「我要擊打」 noted. |
| Names | 細罷特月, 基斯流月, 沙利色, 利堅米勒, 黑玳 (希連), 賢, 示拿, 哈得拉, 哈達臨門, 亞薩, 便雅憫門, 第一門, 角門, 哈楠業樓 | As 和合本 Zechariah; 推羅, 大馬色 classic. |

Settled while drafting Malachi:

| Source | Rendering | Notes |
|---|---|---|
| Numbering | 3:19–24 = 和合本 4:1–6 | Noted at 3:19 (和合本 makes these verses chapter 4). |
| The disputes: וַאֲמַרְתֶּם בַּמֶּה | 你們卻說：「（我們）在甚麼事上……呢？」 | The same form for *bammeh* (1:2, 6, 7; 2:17; 3:8); 3:7 *bammeh nashuv* 我們要怎樣回來呢. |
| 3:1 (Mark 1:2) | 看哪，我差遣我的使者，他要在我前面預備道路 | Mark 1:2's 差遣我的使者 and 預備道路 kept; the Greek 「在你前面」 and Exodus 23:20 noted. |
| 3:23 | 在耶和華的日子，那大而可畏的日子來到以前，我必差遣以利亞先知 | As Joel 3:4. |
| חֵרֶם (3:24; Zechariah 14:11) | 滅絕的咒詛 | The synagogue's repeat of 3:23 noted. |
| מִנְחָה (1:10–13; 2:12–13; 3:3–4) | 供物 | *minchah* noted. |

Settled while drafting Matthew:

| Source | Rendering | Notes |
|---|---|---|
| ἡ βασιλεία τῶν οὐρανῶν | 天國 | Matthew's own phrase, kept apart from Mark's 神的國; 「諸天的國」 noted at 3:2. |
| The genealogy (1:2–16) | The Union Version's Matthew forms (亞蘭, 撒拉鐵, 所羅巴伯) | The Old Testament form noted where it differs (蘭; 亞比央; 亞撒利雅). The critical text's *Asaph*, *Amos* are 亞薩, 阿摩司, with 亞撒, 亞們 (和合本) noted. 某人生某人; 從她瑪生. |
| παρθένος (1:23) | 那童女 | Our Isaiah 7:14 has 少女 (*almah*); both noted. |
| Old Testament quotations | The Greek in the text, our Old Testament's wording kept where the Greek agrees | Our Old Testament line quoted in the note where it differs (2:6, 18; 4:4–10, 15–16; 8:17; 9:13; 10:35–36); 3:3 as Mark 1:3. |
| μάγοι | 占星家 | Noted: 傳統譯作「博士」, which now means a doctorate. |
| μακάριοι | ……的人有福了 | As *ashrei* (Psalms); *makarioi* noted at 5:3. |
| ὑποκριτής; μαμωνᾶς | 假冒為善的人；錢財 | *hypokrites* noted; 和合本「瑪門」 noted. |
| The Lord's Prayer (6:9–13) | 我們在天上的父，願人都尊你的名為聖…… 不要帶我們進入試探，救我們脫離那惡者 | *epiousios* and the doxology (not in the critical text) in notes. |
| ὁ πατὴρ ὑμῶν ὁ ἐν τοῖς οὐρανοῖς; ὁ οὐράνιος | 你們在天上的父；天父 | |
| ἀσσάριον; κοδράντης | 銅錢；小銅錢 | ¹⁄₁₆ and ¹⁄₆₄ of a denarius, noted. |
| οὐκ ἔστιν μου ἄξιος (10:37–38) | 就不配屬於我 | Not 和合本's added 「作我的門徒」. |
| ᾅδης | 陰間 | As *she'ol*; *Hades* noted (11:23; 16:18 πύλαι ᾅδου 陰間的權勢, 直譯「陰間的門」). |
| οὐαί σοι | ……你有禍了 | *ouai* noted as the prophets' *hoy* (11:21; 18:7). |
| ἐκκλησία (16:18; 18:17) | 教會 | *ekklesia* 「會眾、聚集的人」 noted. |
| Πέτρος / πέτρα (16:18) | 彼得／磐石 | The wordplay, lost in Chinese, explained in a note. |
| δέω / λύω (16:19; 18:18) | 捆綁／釋放 | Noted: the teachers' terms for forbidding and permitting. |
| Old Testament quotations (11–20) | As Matthew 1–10 | 11:10 as Mark 1:2 plus 「在你前面」; 12:7 as 9:13 (*eleos*/*chesed*); 13:14–15 shares Isaiah 6:9's 聽了又聽……看了又看; 15:8–9 = Mark 7:6–7; 19:18–19 the commandments as Exodus 20 and 5:21, 27 (不可謀殺，不可通姦，不可偷竊). |
| ζιζάνια; σάτον | 稗子；細亞 | Darnel and the seah (約 7 公升) noted. |
| τάλαντον; στατήρ (17:27) | 他連得；一塊錢 | 他連得 ≈ 6,000 denarii (Matthew; the Hebrew talent by weight is about 34 kg); stater in a note. |
| Hours (20:3–9) | 上午九時、中午十二時、下午三時、下午五時 | As Mark; the hour in a note. |
| Old Testament quotations (21–28) | Mark 11–15's wording wherever the Greek agrees | 21:9, 23:39 是應當稱頌的 as Mark 11:9 (our Psalm 118:26 是蒙福的 noted); 21:13 without 萬民; 21:42 and 22:44 as Mark 12:10–11, 36; 22:37 全心、全性、全意 (no 全力); 22:39 as 19:19 (要愛你的鄰舍，如同愛自己); 26:31 adds 羊群的. |
| 21:5 (Isaiah 62:11; Zechariah 9:9) | 是溫柔的，騎着驢，又騎着驢駒，就是負軛之驢的崽子 | Two animals in Matthew, one in Zechariah's parallel lines; our Zechariah text quoted in the note. |
| 27:9–10 (Zechariah 11:12–13; Jeremiah) | 三十塊銀子；陶匠的田；血田 | Why Jeremiah is named, and our Zechariah wording, in the note. |
| Ἠλὶ ἠλὶ λεμὰ σαβαχθάνι (27:46) | 以利，以利，拉馬撒巴各大尼？ | As Mark 15:34's 拉馬撒巴各大尼; the Hebrew *Eli* and 「以羅伊」 manuscripts noted. |
| 28:19–20 | 使萬民作我的門徒，奉父、子、聖靈的名給他們施洗……我天天與你們同在，直到這世代的終結 | 「歸入……的名」, *panta ta ethne* noted; 這世代的終結 as 13:39 and 24:3. |
| νομικός (22:35) | 律法專家 | *nomikos* noted; kept apart from 經學家 and 律法教師. |
| παρουσία (24:3, 27, 37, 39) | 來臨 | *parousia* noted. |
| ναός; κορβανᾶς; κουστωδία | 聖殿 (*naos* noted)；庫房 (with 各耳板)；衞兵 | 23:16; 27:5–6, 65. |
| χαῖρε, χαίρετε | 你好 (26:49; 28:9)；萬歲 (to the king, 27:29, as Mark 15:18) | *chairete* noted. |

Settled while drafting Luke:

| Source | Rendering | Notes |
|---|---|---|
| The prologue (1:1–4) | One sentence over four verses; 尊貴的提阿非羅 | The formal style and κράτιστε noted. |
| κύριος in Luke 1–2 | 主 | Noted at 1:6 as standing for YHWH; 7:13 notes the first time the narrative calls Jesus 主. |
| ναός (1:9, 21–22) | 聖所 | *naos* noted, kept apart from the courts (ἱερόν 聖殿). |
| The hymns (1:46–55; 1:68–79; 2:14; 2:29–32) | One verse per line, clauses kept as lines | 1:46 我的心頌揚主的偉大 (傳統「尊主為大」 noted); Latin names 〈尊主頌〉〈頌主歌〉〈西面頌〉 in notes. |
| Καῖσαρ Αὔγουστος; Τιβέριος Καῖσαρ; Κυρήνιος | 該撒奧古斯都；該撒提庇留；居里扭 | 該撒 first, as the Union Version orders the title. |
| τετραάρχης | 分封的王 | *tetraarches* noted (3:1). |
| The genealogy (3:23–38) | The Union Version's Luke forms; 甲是乙的兒子 | Critical-text names the Union Version lacks are transliterated: 約設 (*Iosech*), 約書亞 (*Iesous*, 和合本 約細), 沙拉 (*Sala*, 和合本 撒門), 亞民, 亞尼 (*Admin*, *Arni*; 和合本 亞蘭). |
| ἐπιστάτης | 師傅 | *epistates* noted (5:5); only Luke uses it. Διδάσκαλε stays 老師. |
| νομοδιδάσκαλος; νομικός | 律法教師 (5:17)；律法專家 (7:30; 10:25; 11:45–52) | As the glossary and Matthew. |
| Isaiah 61:1–2 (4:18–19) | 傳好消息給貧窮的人……向被擄的宣告自由……使受欺壓的得自由，宣告主悅納人的年 | Our Isaiah wording kept where the Greek agrees; the differences in the note. |
| The Lord's Prayer (11:2–4) | 父啊，願人都尊你的名為聖；願你的國降臨；我們每天所需的食物，求你天天賜給我們；赦免我們的罪…… | Matthew 6:9–13's wording where the Greek agrees; 赦免 for sins, 饒恕 for debtors. |
| 10:27 (Deuteronomy 6:5; Leviticus 19:18) | 全心、全性、全力、全意；要愛你的鄰舍，如同愛自己 | Luke's order of the four. |
| δοῦλος | 僕人 throughout Luke (7:2–10; 12:37–47; 14:17–23; 15:22; 17:7–10; 19:13–22; 20:10–11) | As Matthew's servant parables; 或譯「奴僕」 and *doulos* noted at the first in each passage. 22:50 the high priest's 奴僕 as Mark 14:47. |
| Old Testament quotations (13–24) | Mark's and Matthew's wording where the Greek agrees | 13:35, 19:38 是應當稱頌的 (our Psalm 118:26 是蒙福的 noted; 19:38 adds 王); 19:46 我的殿必作禱告的殿 (no 萬民); 20:17 as Psalm 118:22; 20:42–43 作你的腳凳 as our Psalm 110:1 (Mark 12:36 放在你的腳下); 22:37 他被列在不法的人之中, as our Isaiah 53:12 note; 23:30 Hosea 10:8 in reverse order; 23:46 父啊，我把我的靈交在你手裏 (Psalm 31:6). |
| δραχμή; μνᾶ | 銀錢；彌那 | Kept apart from 銀幣 (denarius) and 一塊錢 (stater); 彌那 as Ezekiel 45:12; values in notes. |
| βάτος; κόρος (16:6–7) | 簍；石 | 罷特, 柯珥 and their volumes in notes. |
| ᾅδης (16:23); κόλπος Ἀβραάμ | 陰間；亞伯拉罕的懷裏 | As Matthew; *Hades* noted. |
| SBLGNT single brackets (22:19b–20; 24:40, 51, 52) | 〔 〕 in the text | Noted: printed in brackets as uncertain. 22:43–44 and 23:34a in the text without brackets, noted as missing in some manuscripts. |
| στρατηγοὶ τοῦ ἱεροῦ | 聖殿的守衞長 | 22:4, 52. |
| Κρανίον (23:33) | 髑髏地 | As Mark 15:22; 各各他 and 加略山 noted. |
| παράδεισος (23:43) | 樂園 | Noted. |
| λεπτόν (12:59) | 小銅錢 | As Mark 12:42; ¹⁄₁₂₈ of a denarius noted. |

Settled while drafting John:

| Source | Rendering | Notes |
|---|---|---|
| λόγος (1:1–14) | 道 | As the Union Version; *logos* and "Word" noted at 1:1. Elsewhere λόγος is 話 (5:24; 8:31), except ὁ λόγος τοῦ θεοῦ 神的道 (10:35). |
| ἐσκήνωσεν ἐν ἡμῖν (1:14) | 住在我們中間 | 直譯「支搭帳幕」 noted. |
| χάρις καὶ ἀλήθεια | 恩典和真理 | Exodus 34:6 (*chesed*, *emet*) noted. |
| μονογενής | 獨生子 (1:14; 3:16, 18)；獨一的神 (1:18) | *monogenes* 「獨一的」 noted; 1:18 variant 獨生子. |
| ζωὴ αἰώνιος; ζωή | 永生；生命 | As Mark; *zoe aionios* noted at 3:15. |
| φῶς; σκοτία, σκότος | 光；黑暗 | |
| ἀλήθεια; ἀληθινός; ἀληθής | 真理；真 (真光、真糧)；真實 | |
| πιστεύω (εἰς) | 信 (信他、信他的名) | 2:24 交託, noted as the same verb. |
| μένω | 住在 wherever it carries John's sense (5:38; 6:56; 8:31); 住、停留 in plain senses (1:32, 38–39) | *meno* noted at 1:32. |
| δόξα; δοξάζω | 榮耀；榮耀、得着榮耀 | |
| ὥρα (Jesus' hour; "an hour is coming") | 時候 (我的時候還沒有到；時候將到) | Clock hours as Mark (下午四時左右), noted. καιρός (7:6, 8) is 時機, noted apart. |
| σημεῖον | 神蹟 | *semeion* 「記號」 noted at 2:11. |
| κόσμος | 世界 throughout | 3:16 神這樣愛世界，甚至賜下他的獨生子，叫一切信他的人不致滅亡，反得永生 (傳統「神愛世人」 noted). 世人 only for οἱ ἄνθρωποι (3:19). |
| οἱ Ἰουδαῖοι | 猶太人 | Noted at 1:19; the full note on its sense in John at 5:10 (the Jerusalem authorities and Jesus' opponents, not the Jewish people), and at each chapter's first use. |
| ἐγώ εἰμι + predicate | 我是…… | 6:35 我是生命的糧 (the list in the note); 8:12 我是世界的光; 10:7, 9 我是羊的門; 10:11 我是好牧人; 11:25 我是復活和生命. |
| ἐγώ εἰμι absolute | 是我 (6:20)；我就是 (4:26)；我就是那一位 (8:24, 28)；在亞伯拉罕出生以前，我就是 (8:58) | Notes link them to Exodus 3:14 (our 我就是我, the LXX *ego eimi ho on*) and Isaiah 43:10. |
| ἀμὴν ἀμὴν λέγω ὑμῖν/σοι | 我實實在在地告訴你們／你 | *amen amen* noted at 1:51. |
| ἄνωθεν (3:3, 7, 31) | 從上面 | 或譯「重生」 noted. |
| ὁ ἀμνὸς τοῦ θεοῦ; ὁ προφήτης | 神的羔羊；那位先知 (Deuteronomy 18:15–18 noted) | |
| Μεσσίας (1:41; 4:25) | 彌賽亞 | As the glossary. |
| ἄρτος in John 6 | 餅 (the loaves, 6:5–13, 23, 26)；糧 (6:31–58, the discourse) | Same Greek word, noted at 6:32; 6:31 quotes Psalm 78:24 as our Psalm note (糧食). |
| κύριε to Jesus from strangers | 先生 (4:11–49; 5:7; 6:34; 8:11; 9:36)；主啊 (disciples, Martha, 9:38) | *kyrie* noted. |
| ὑπηρέται; συνέδριον; ἀποσυνάγωγος | 差役；議會；趕出會堂 | |
| σκηνοπηγία; ἐγκαίνια | 住棚節；修殿節 (Hanukkah noted) | |
| λῃστής (10:1, 8; 18:40) | 強盜 | 或譯「叛亂分子」 noted (Mark's rendering). 18:40 Barabbas also 強盜, to keep John's echo of 10:1, 8; the note gives the sense "rebel" from Mark 15:7, where Mark has 叛亂分子. |
| 7:53–8:11 | In ⟦ ⟧, as the SBLGNT and Mark 16:9–20 | Note at 7:53 on the manuscripts; 經學家 (8:3) as elsewhere. |
| Old Testament quotations (1–11) | The Greek in the text; our Old Testament line in the note | 1:23 keeps Mark 1:3's 在曠野呼喊 and 修直; 2:17 必把我吞噬 (future; our Psalm 69:10 past); 6:31 他從天上賜下糧食給他們吃; 6:45 他們都要受神的教導 (both as our Psalm 78 and Isaiah 54 notes quote them); 10:34 我曾說：你們是神 (as our Psalm 82:6). |
| παράκλητος (14:16, 26; 15:26; 16:7) | 保惠師 | As the Union Version; *parakletos* noted at 14:16 (幫助者、辯護者、輔導者、安慰者). The Spirit is 他 (neuter *pneuma* noted, 14:17). |
| ἐγώ εἰμι + predicate (12–21) | 14:6 我是道路、真理、生命 (和合本「我就是……」 noted)；15:1, 5 我是真葡萄樹／我是葡萄樹 | γεωργός 栽培的人 (或譯「農夫」); *kathairo* 修剪乾淨 / *katharos* 乾淨 noted. |
| ἐγώ εἰμι absolute (13:19; 18:5–8) | 信我就是那一位 (13:19)；我就是 (18:5, 6, 8) | 18:17, 25 Peter's *ouk eimi* 我不是, noted against it. |
| ὁ ἄρχων τοῦ κόσμου τούτου | 這世界的統治者 | 12:31; 14:30; 16:11. |
| μονή (14:2, 23) | 住處 | Linked to *meno* in a note. |
| ἀγαπάω / φιλέω (21:15–17) | 愛 for both | The two verbs and the other variations noted at 21:15; 20:2 and 16:27 *phileo* noted. |
| The Passion (18–19) | Mark 14–15's wording where the Greek agrees | 大祭司的奴僕 (18:10, Malchus 馬勒古)；看門的女傭人；差役；總督府 (*praitorion*)；荊棘冠冕、紫袍、猶太人的王萬歲；髑髏地／各各他；酸酒；預備日；千夫長 (*chiliarchos*)；一營士兵 (*speira*, as Mark 15:16's 營). |
| 19:14 ὥρα ἕκτη | 中午十二時 | 直譯「第六個時辰」 and Mark 15:25's third hour noted. |
| 19:19–20 the title | 「拿撒勒人耶穌，猶太人的王」；希伯來文、拉丁文、希臘文 | 拉丁文 noted (直譯「羅馬文」); 希伯來話/希伯來文 noted as probably Aramaic. Names 厄巴大 (Gabbatha, classic and 1989 CUV), 革羅罷 (Clopas) added to the names table. |
| τετέλεσται (19:28, 30) | 已經完成了；完成了 | 和合本「成了」 noted; 19:30 把靈交付了 (*pneuma*). |
| 20:17 Μή μου ἅπτου; 20:28; 20:31 | 不要拉住我不放 (或譯「不要摸我」)；我的主！我的神！；使你們信 (the present/aorist variant and 19:35 noted) | |
| Old Testament quotations (12–21) | The Greek in the text; our Old Testament line in the note | 12:13 是應當稱頌的 as Mark 11:9 (Psalm 118:26 是蒙福的 noted); 12:15 錫安的女兒，不要懼怕！看哪，你的王騎着驢駒來了 (as our Zechariah 9:9 note quotes it); 12:38 主啊，我們所傳的，有誰相信呢？ (as our Isaiah 53:1 note); 12:40 他使他們瞎了眼，使他們的心剛硬; 13:18 吃我飯的人，舉起腳跟踢我 (Psalm 41:10's 舉起腳跟踢我 kept); 15:25 他們無緣無故地恨我 (Psalm 69:5); 19:24 identical with our Psalm 22:19; 19:36 他的骨頭，一根也不會折斷; 19:37 他們要仰望自己所刺的人 (as our Zechariah 12:10 note). |
| Chapter 21 | 後記 noted at 21:1 | 約翰的兒子西門 (約拿 noted); 二百肘, 一百五十三條. |

Settled while drafting Acts:

| Source | Rendering | Notes |
|---|---|---|
| The prologue (1:1) | 提阿非羅啊，我在前一本書裏…… | Continues Luke 1:1–4 and 24:49–53; Luke 1:3 noted. |
| ἀπόστολος; ἐκκλησία | 使徒；教會 | *apostolos* noted at 1:2; *ekklesia* noted at 5:11, its first use for the believers. 7:38 ἡ ἐκκλησία ἐν τῇ ἐρήμῳ is 曠野的會眾, noted as the same word. |
| ἡ ὁδός (9:2; 19:9, 23; 22:4; 24:14, 22) | 這道 (屬於這道的人) | *hodos* 「道路」 noted, kept apart from *logos* (ὁ λόγος τοῦ θεοῦ 神的道). |
| πνεῦμα ἅγιον; πνεῦμα | 聖靈；靈 | 6:3 πνεύματος without ἅγιον is 靈 (神的靈), with 「聖靈」 manuscripts noted. |
| Ἑλληνισταί; Ἑβραῖοι (6:1; 9:29) | 說希臘話的猶太人；說希伯來話的猶太人 | 11:20 Ἑλληνισταί (Gentiles there) 說希臘話的人, noted. |
| προσήλυτοι; οἱ φοβούμενοι / σεβόμενοι τὸν θεόν | 進猶太教的人；敬畏神的人、敬拜神的…… | *proselytoi* noted at 2:11; God-fearing Gentiles noted (10:2; 13:16, 50). |
| ἄνδρες ἀδελφοί; ἄνδρες Ἰσραηλῖται | 弟兄們；以色列人哪 | 直譯「人們、弟兄們」 noted. |
| παῖς (of Jesus, 3:13, 26; 4:25–30) | 僕人 (聖僕) | *pais* 「僕人、孩子」 noted; Isaiah 52:13 LXX noted. |
| ἀρχηγός | 創始者 (3:15)；元首 (5:31) | *archegos* noted both times. |
| ἑκατοντάρχης; σπεῖρα; ἀνθύπατος | 百夫長；營；總督 | *anthypatos* noted (和合本「方伯」), kept for the Senate's provinces. |
| κοινός (10:14–28; 11:8–9); ἔκστασις | 俗物；魂遊象外 | |
| κλάσις τοῦ ἄρτου; Χριστιανοί | 擘餅；基督徒 | 2:42, 46; 11:26. |
| Old Testament quotations (1–14) | The Greek in the text; our Old Testament wording where the Greek agrees, and the wording our Old Testament notes already give for these verses | 1:20 Psalm 69:26; 109:8; 2:17–21 as the Joel 3:1–5 note (在末後的日子，神說…… 顯赫的); 2:25–28 Psalm 16 LXX (我的舌頭快樂；安居在盼望中；你的聖者見朽壞); 2:34–35 as Luke 20:42–43 (主對我的主說……作你的腳凳); 4:11 輕視 (*exoutheneo*) for Psalm 118:22's 丟棄; 4:25–26 Psalm 2 LXX 一同聚集; 7:42–43 Amos 5:25–27 LXX (摩洛的帳幕和理番神的星；巴比倫以外); 7:49–50 as the Isaiah 66:1 note; 8:32–33 as the Isaiah 53:7 note; 13:33 Psalm 2:7; 13:34 as the Isaiah 55:3 note; 13:41 Habakkuk 1:5 LXX; 13:47 as the Isaiah 49:6 note. |
| Stephen's speech (7) | Our Old Testament's names (哈蘭、迦勒底人的地、示劍、哈抹、米甸、紅海、約書亞) | The differences noted as the English: the call before Haran (7:2), Terah's death (7:4), 400 years (7:6), 75 souls (7:14), the tomb at Shechem (7:16), Moses' forty years (7:23), Sinai/Horeb (7:30), Babylon for Damascus (7:43). |
| Verses absent from the critical text | Skipped with a note, as Mark 7:16 | 8:37 (TR) noted at 8:36; the TR addition at 9:5–6 noted. |
| Names (classic Union Version forms) | 居比路、埃提阿伯、干大基、革老丟、丟斯、希耳米、推羅、大馬色、巴耶穌、士求保羅 | Today's forms (塞浦路斯、克勞狄、宙斯) in notes where useful; 米底亞人, 克里特人, 阿拉伯人 as the Union Version's Acts 2. |
| ἀνθύπατος (13:7; 18:12; 19:38) | 總督 | Noted each time; 19:38's plural noted as general. ἡγεμών (Felix, Festus, 23:24–26:30) is also 總督. |
| χιλίαρχος; παρεμβολή; στρατηγοί (16:20–38); ῥαβδοῦχοι; πολιτάρχαι (17:6, 8) | 千夫長；營樓；官長；衙役；地方官 | Each noted at its first use. |
| βῆμα; πραιτώριον (23:35) | 審判台 (as 12:21)；官邸 | *bema* noted (18:12; 25:6). |
| Καῖσαρ; Σεβαστός (25:21, 25); κύριος of the emperor (25:26) | 該撒；皇上；皇上 | Καίσαρα ἐπικαλοῦμαι 上訴於該撒 (25:11–12, 21; 26:32; 28:19). κράτιστε 大人 (23:26; 24:3; 26:25). |
| The "we" passages | 我們 | Noted at 16:10, 20:5, 27:1 and their end at 28:16. |
| Old Testament quotations (15–28) | The Greek in the text; our Old Testament wording in the note | 15:16–17 as our Amos 9:12 note (重建大衛那倒塌的棚子；使餘剩的人和所有稱為我名下的外邦人都尋求主); 23:5 Exodus 22:27 LXX (不可惡言毀謗); 28:26–27 identical with Matthew 13:14–15, with 你去告訴這百姓說 and 「『「」』」 nesting. |
| 17:23, 28 (the Areopagus) | 『未識之神』；『我們也是他所生的』 | Aratus' *Phaenomena* and Epimenides noted; 亞略巴古 without a dot. |
| Verses absent from the critical text (15–28) | Skipped with a note, as 8:37 | 15:34 (at 15:33); 24:7 with the TR words of 24:6b–8a (at 24:6; 24:8 kept); 28:29 (at 28:28). 19:40b noted （和合本作第41節）. |
| ἐκκλησία (19:32, 39, 40); γραμματεύς (19:35) | 集會；書記 | The citizens' assembly and the city clerk, both noted apart from 教會 and 經學家. |
| Names (15–28) | Classic Union forms: 居比路、推羅、該撒利亞、大馬色、革老丟呂西亞、百尼基、革哩底、米利大、非尼基、亞底亞海、丟斯雙子 | No middle dot in compound names (提多猶士都、波求非斯都). The 1989 forms (塞浦路斯、泰爾、凱撒利亞、克勞第、百妮基、克里特、馬耳他) are not used. |
| The voyage (27) | 船長；船主；救生艇；噚；友拉革羅 | Plain terms; uncertain gear (*boetheiai*, *artemon*, *dithalassos*) explained in notes; 一噚約 1.8 米. |

Settled while drafting Romans (for all of Paul's letters):

| Source | Rendering | Notes |
|---|---|---|
| The opening and closing (1:1–7; 16:1–24) | 基督耶穌的僕人保羅……致在羅馬所有為神所愛、蒙召作聖徒的人：願恩典和平安從我們的父神和主耶穌基督歸給你們！ ；問候某某 | 致…… for the addressees, no verb added; greetings 問候 (ἀσπάζομαι), names in the Union Version's forms. *christos* noted at 1:1 as in each book. |
| δοῦλος (of Paul, 1:1); δουλεύω, δοῦλος (6:6–22) | 僕人；作……的奴僕 | 或譯「奴僕」 at 1:1; the slavery picture of chapter 6 keeps 奴僕. |
| ἀδελφοί; ἀδελφός (a fellow believer) | 弟兄姊妹 | As the glossary and the Gospels; *adelphoi* noted at the first in each chapter. Paul's fellow Jews (9:3) also 弟兄姊妹, noted. |
| ἅγιοι | 聖徒 | 直譯「聖潔的人」 noted (1:7; 8:27; 12:13; 15:25; 16:2). |
| δικαιοσύνη; δικαιοσύνη θεοῦ | 義；神的義 | *dikaiosyne* 「義、公義」 noted at 1:17, with the senses of 神的義 (God's justice and faithfulness, or the standing he gives). 公義 kept for δίκαιος of God's judgment (2:5 δικαιοκρισία 公義審判) and ἀδικία 不義／不公義 (9:14). |
| δικαιόω; δικαίωσις; δίκαιος | 稱義 (使……稱義、得稱為義)；稱義；義人、義的 | *dikaioo* 「宣告為義」 noted at 2:13, a court word; 3:4 顯為公義 and 6:7 脫離 noted as the same verb. |
| λογίζομαι (4:3–24) | 算 (算為義) | *logizomai* noted at 4:3. |
| πίστις; πιστεύω | 信、信心；信 | 1:17 從信到信 (*pistis* 「信心、信實」 noted); 3:3 τὴν πίστιν τοῦ θεοῦ 神的信實. |
| πίστις Ἰησοῦ Χριστοῦ (3:22, 26) | 信耶穌基督；信耶穌的人 | 或譯「耶穌基督的信實」 in the note, as the English. |
| Habakkuk 2:4 (1:17) | 義人必因信而活 | As our Habakkuk note; the Hebrew 「他的信實」, the Septuagint 「我的信實」 and 「因信而成為義人的，必得生存」 noted. |
| χάρις; χάρισμα | 恩典；恩賜 | |
| ἁμαρτία; παράπτωμα; παράβασις | 罪；過犯；違命、過犯 | Sin personified (5:12–7:25) keeps 罪 as the subject. |
| σάρξ | 肉體 | Kept for the imagery and for 按肉體 (descent, 1:3; 9:3–8). The moral sense noted at 7:5 and 8:3 (人的本性在軟弱中與神敵對; 或譯「人的本性」); 3:20 πᾶσα σάρξ 沒有一個人 (直譯 noted); 6:19 人性的軟弱 (直譯 noted). σάρκινος 屬肉體的. |
| πνεῦμα | 聖靈；靈 (the human spirit; ambiguous places noted) | 1:4 聖善的靈; 8:4–13 隨從聖靈, 以聖靈為念; 15:19 SBLGNT's bare *pneuma* 聖靈 with 直譯「靈」 noted. |
| φρονέω τὰ τῆς σαρκός; φρόνημα (8:5–7) | 以肉體（的事）為念；以聖靈（的事）為念 | |
| νόμος | 律法 (of Moses)；律 (a principle: 3:27; 7:21–23; 8:2)；法律 (7:1–3) | Each sense noted with *nomos*; 神的律法 (7:22, 25). |
| ἔργα νόμου | 遵行律法 | 直譯「律法的工作」 noted (2:15; 3:20). |
| ἱλαστήριον (3:25) | 施恩座 | As our Exodus 25:17 (*kapporet*); the Septuagint's use, 或譯「贖罪祭」, 和合本「挽回祭」 noted. |
| περὶ ἁμαρτίας (8:3) | 作贖罪祭 | As Leviticus; 或譯「為了罪」 noted. |
| ἀπολύτρωσις; καταλλαγή, καταλλάσσω | 救贖、得贖；和好 | 5:1 εἰρήνην πρὸς τὸν θεόν 與神相和. |
| υἱοθεσία | 兒子的名分 | *huiothesia* 「收養為兒子」 noted (8:15, 23; 9:4); 8:14 υἱοί 神的兒子 / 8:19 神的眾子, with *tekna* 兒女 noted. Ἀββα 阿爸 as Mark 14:36. |
| κληρονόμος | 繼承人 | 4:14; 8:17. |
| τὰ ἔθνη | 外邦人 | As Mark; 1:5 「萬國」 noted. In Old Testament quotations (15:9–12) 外邦人 too, where our Old Testament has 列國／萬國 (noted). |
| μὴ γένοιτο | 絕對不是！ | *me genoito* noted at 3:4. |
| ὦ ἄνθρωπε | 你這（個）人哪 | 2:1, 3; 9:20, noted. |
| καυχάομαι | 誇口 (2:17, 23; 3:27; 4:2)；誇耀 (5:2–11) | Noted at 5:2. |
| σπέρμα (of Abraham) | 後裔 | 直譯「種子」 noted; our Genesis has 後代 (noted at 4:18; 9:7). |
| γράμμα | 條文 (2:29; 7:6)；成文律法 (2:27) | *gramma* noted. |
| Old Testament quotations | The Greek in the text; our Old Testament line in the note where it differs | Wording our Old Testament notes already give is kept: 2:24 (Isaiah 52:5); 3:4 (Psalm 51:6); 3:15–17 (Isaiah 59:7–8); 9:25 (Hosea 2:25); 9:27–28 (Isaiah 10:22–23); 10:15, 16, 20–21; 11:26–27 (救主從錫安出來); 11:34; 12:19 (伸冤是我的事，我必報應); 14:11 (萬口必向神承認); 15:12. Joel 3:5 (10:13) as Acts 2:21 (凡求告主名的，都必得救). |
| 16:24; 16:25–27 | 16:24 kept, no 25–27 | As the SBLGNT (Byzantine 16:24); the doxology translated in the note at 16:24, with its place after 14:23 noted there and at 14:23. |
| Names (16) | 非比、堅革哩、百基拉 (*Priska*)、亞居拉、以拜尼土、安多尼古、猶尼亞 (a woman, noted)、暗伯利、耳巴奴、士大古、亞比利、亞利多布、希羅天、拿其數、土非拿、土富撒、彼息、魯孚、亞遜其土、弗勒干、黑米、八羅巴、黑馬、非羅羅古、猶利亞、尼利亞、阿林巴、路求、耶孫、所西巴德、德提、該猶、以拉都、括土；以利哩古；士班雅 | Union Version forms; 士班雅 the classic form (the 1989 text has 西班牙). |

Settled while drafting 1 Corinthians:

| Source | Rendering | Notes |
|---|---|---|
| The Corinthians' slogans (6:12, 13; 7:1; 8:1, 4; 10:23) | In 「」 within Paul's sentence: 「凡事我都可以做」；「食物是為肚腹，肚腹是為食物」；「男人不親近女人倒是好的」；「我們都有知識」；「偶像在世上算不得甚麼」 | Noted each time: most interpreters take it as a Corinthian saying; the Greek has no quotation marks. 6:18 left unmarked, with the suggestion in a note, as the English. |
| χάρισμα, χαρίσματα; πνευματικά (12:1; 14:1) | 恩賜；屬靈的恩賜 | As Romans; 「屬靈的人」 noted at 12:1. χαρίσματα ἰαμάτων 醫病的恩賜. |
| γλώσσαις λαλεῖν; γένη γλωσσῶν; (δι)ερμηνεύω, ἑρμηνεία | 說方言；說各種方言；翻譯（方言） | As Acts 10:46 and 19:6 and the Union Version. Noted at 12:10 (the debate over human or unknown languages) and that 方言 here is not a regional dialect; 13:1 and 14:2 note 或譯「語言」. |
| προφητεία; προφητεύω; προφήτης | 預言；說預言；先知 | As Acts 2:17 and Romans 12:6; the sense (speech the church understands, weighed by others, 14:3, 24–25, 29) noted at 12:10. |
| διακρίσεις πνευμάτων; δυνάμεις (12:10, 28–29) | 辨別諸靈；行神蹟 | 直譯「能力的運作」「都是能力嗎」 noted. |
| ἀγάπη (13) | 愛 | 13:4 愛是恆久忍耐，愛是恩慈，愛是不嫉妒 keeps the Greek's three 愛; 13:7 凡事包容……凡事忍耐; 13:13 如今常存的，有信，有望，有愛，這三樣；其中最大的是愛. Native readers should read it aloud. |
| ψυχικός; πνευματικός; σάρκινος, σαρκικός | 屬血氣的；屬靈的；屬肉體的 | 2:14; 15:44–46 (屬血氣的身體); *psychikos* noted. χοϊκός 屬塵土的 (15:47–49, Genesis 2:7 noted). |
| ναός (3:16–17; 6:19) | 殿 (神的殿；聖靈的殿) | *naos* noted, as the Gospels. |
| κοινωνία (10:16); κοινωνοί (10:18, 20) | 同享；有分 | |
| εἰδωλόθυτα; ἱερόθυτον (10:28) | 祭過偶像的食物；獻過祭的 | As Acts 15:29. |
| δαιμόνια (10:20–21) | 鬼魔 | To keep our Deuteronomy 32:17 (他們祭祀鬼魔), which Paul echoes; the Gospels' 鬼 noted. |
| πορνεία; πόρνοι; μαλακοί; ἀρσενοκοῖται (5:1; 6:9) | 淫亂；淫亂的人；柔弱的男子；與男人同睡的男人 | 6:9 renders the two rare words literally (the second echoes our Leviticus 18:22 不可與男人同睡), with the debate and 和合本「作孌童的」「親男色的」 in the notes. |
| The Lord's Supper (11:23–25) | Luke 22:19–20's wording where the Greek agrees | 這是我的身體，是為你們的 (no 捨的; Luke noted); 這杯是用我的血所立的新約 as Luke; 為的是記念我; 主耶穌被出賣的那一夜 (*paradidomi* 「交出去」 noted). |
| The creed (15:3–5) | 基督照聖經所說，為我們的罪死了，而且埋葬了，而且照聖經所說，第三天復活了，並且向磯法顯現…… | 而且 for the repeated *hoti*; the tradition noted. ἐγήγερται 復活了 (perfect noted); οἱ δώδεκα 十二門徒 as Mark. κοιμάομαι 睡了 (noted: died). |
| Old Testament quotations | The Greek in the text; our Old Testament wording, and the wording our Old Testament notes already give, where the Greek agrees | 1:19 (Isaiah 29:14 note); 1:31 誇口的，應當指着主誇口 (Jeremiah 9:23 note); 2:9 (Isaiah 64:3 note); 3:19 = Job 5:13; 6:16 = Genesis 2:24 (二人成為一體); 9:9 = Deuteronomy 25:4; 10:7 = Exodus 32:6; 14:21 (Isaiah 28:11 note); 15:27 = Psalm 8:7; 15:32 = Isaiah 22:13; 15:45 (頭一個人亞當成了有生命的活人, Genesis 2:7); 15:54 死亡被吞滅，得了勝利 (Isaiah 25:8 note); 15:55 死亡啊，你的勝利在哪裏？死亡啊，你的毒鉤在哪裏？ (Hosea 13:14 note). |
| Names | 所提尼、革來氏（家裏的人）、亞波羅、磯法、基利司布、該猶、司提反 (Stephanas)、福徒拿都、亞該古、亞居拉、百基拉 | Stephanas is 司提反, the classic Union Version form (the 1989 text has 司提法那), told apart from Stephen in a note at 1:16; the names table follows. Chloe 革來 with the Union Version's 氏. 16:22 Μαράνα θά 瑪拉那他, the meaning noted. |

Settled while drafting 2 Corinthians:

| Source | Rendering | Notes |
|---|---|---|
| παράκλησις, παρακαλέω; θλῖψις | 安慰；患難 | 1:3–7 keeps 安慰 throughout (*paraklesis* noted); 13:11 παρακαλεῖσθε 要彼此勸勉 (或譯「要受安慰」). |
| διακονία; διάκονος | 職事 (3:7–9; 4:1; 5:18; 6:3)；僕人 (3:6; 6:4; 11:15, 23) | As Romans 13:4 and 1 Corinthians 3:5; *diakonoi* noted (或譯「執事」). The collection's διακονία is 供應 (8:4; 9:1, 12–13). |
| ἱκανός, ἱκανότης (2:16; 3:5–6) | 勝任 | *hikanos* noted. |
| καταργέω (3:7–14) | 要廢去的；被廢去 | As 1 Corinthians 15:24's 廢掉; 「逐漸褪去」 noted. |
| κάλυμμα (3:13–16; 4:3) | 帕子 | As our Exodus 34:33–35 (*masveh*); 3:7 摩西臉上的榮光 with Exodus 34:29's 發光 and the Septuagint's 得了榮耀 noted. ἡ παλαιὰ διαθήκη 舊約; καινὴ διαθήκη 新約 (Jeremiah 31:31 noted). |
| ἀρραβών (1:22; 5:5) | 訂金 | 和合本「質」 noted. |
| καινὴ κτίσις (5:17) | 新造的人 | 直譯「新的創造」 and 或譯「就有新的創造」 noted. |
| 5:21 | 神使那不知罪的，替我們成為罪，好讓我們在他裏面成為神的義 | 「作贖罪祭」 and *dikaiosyne theou* (as Romans 1:17) noted. |
| χάρις for the collection (8–9) | 恩惠 (8:4)；這恩惠的事 (8:6, 7, 19)；恩典 (8:1, 9; 9:8, 14)；感謝 (8:16; 9:15) | The senses listed in a note at 8:4; 1 Corinthians 16:3's 捐獻 linked. ἁπλότης 慷慨 (8:2; 9:11, 13), 專一 (11:3); εὐλογία 厚禮 (9:5, 直譯「祝福」). |
| Old Testament quotations | The Greek in the text; our Old Testament wording, and the wording our notes give, where the Greek agrees | 4:6 光要從黑暗裏照出來 (Genesis 1:3 要有光 noted); 4:13 我信了，所以我說 (our Psalm 116:10 note); 6:2 在悅納的時候，我垂聽了你 (our Isaiah 49:8 note; the text has 應允); 6:16 Leviticus 26:12 and Ezekiel 37:27 (作他們的神……作我的子民); 6:17 不要觸摸不潔淨的東西 (Isaiah 52:11); 6:18 作你們的父親……兒子和女兒, 全能的主 (*kyrios pantokrator*, 萬軍之耶和華 noted); 8:15 = Exodus 16:18; 9:9 = Psalm 112:9a; 10:17 as 1 Corinthians 1:31; 13:1 as Deuteronomy 19:15. |
| ὑπερλίαν ἀπόστολοι (11:5; 12:11) | 那些超等的使徒 | Paul's irony noted; 和合本「那些最大的使徒」. The "fool's speech" (11:1–12:13) keeps 愚妄 (ἀφροσύνη, ἄφρων) and its sarcasm (11:19–21; 12:13, 16) without softening. |
| τρίτος οὐρανός; παράδεισος (12:2–4) | 第三層天；樂園 | 樂園 as Luke 23:43. |
| σκόλοψ τῇ σαρκί (12:7) | 一根刺加在我的肉體上；撒但的差役 | The suggested meanings in a note. |
| 13:12–13 | 13:13 the grace: 願主耶穌基督的恩典、神的愛、聖靈的相交，與你們眾人同在！ | As the SBLGNT and the English (13 verses); 和合本 13:12–14 noted. κοινωνία 相交 (as 1 Corinthians 1:9; 和合本「聖靈的感動」 noted). |
| Names | 提多、西拉 (*Silvanus*, as the Union Version)、彼列 (*Beliar*)、亞哩達、大馬色、特羅亞 | ἐθνάρχης (11:32) 總管 (和合本「提督」 noted). Silvanus and Beliar added to the names table. |

Settled while drafting Galatians:

| Source | Rendering | Notes |
|---|---|---|
| πίστις Ἰησοῦ Χριστοῦ (2:16; 3:22); ἐν πίστει ζῶ τῇ τοῦ υἱοῦ τοῦ θεοῦ (2:20) | 信耶穌基督；因信基督；是因信神的兒子而活 | As Romans 3:22; 「耶穌基督的信實」 in the note each time. |
| ἔργα νόμου; δικαιόω | 遵行律法 (靠遵行律法)；稱義 | As Romans; 2:16 ends as Romans 3:20 (沒有一個人能靠遵行律法稱義). |
| Old Testament quotations | As Romans where Paul quotes the same verse | 3:6 = Romans 4:3; 3:11 = Romans 1:17; 5:14 = Romans 13:9 and our Leviticus 19:18; 3:8 萬國都要因你得福; 3:10 堅守遵行……必受咒詛 (our Deuteronomy 27:26); 3:12 遵行這些的人，就必因此存活; 3:13 受咒詛 (our Deuteronomy 21:23 詛咒 noted); 4:27 the wording our Isaiah 54:1 note gives; 4:30 Genesis 21:10's 女奴. |
| σπέρμα (3:16, 19, 29) | 後裔 | The singular/plural argument (「和你的眾後裔」／「和你的後裔」) explained in a note at 3:16. |
| παιδαγωγός (3:24–25); ἐπίτροποι καὶ οἰκονόμοι (4:2) | 監護人；受託人和管家 | *paidagogos* noted (和合本「訓蒙的師傅」). |
| τὰ στοιχεῖα τοῦ κόσμου (4:3, 9) | 世上的基本原則 | 或譯「統治世界的靈力」 and 和合本「世俗的小學」 noted. |
| παιδίσκη; ἡ ἐλευθέρα (4:22–31) | 女奴；自由的婦人 | As Genesis 21:10; Genesis 16's 使女 noted. ἀλληγορέω 有寓意. |
| 3:28 | 不再分猶太人或希臘人，不再分奴僕或自由人，也不再分男或女；因為你們在基督耶穌裏都是一 | Genesis 1:27's 有男有女 noted. |
| The works of the flesh; the fruit of the Spirit (5:19–23) | 淫亂、污穢、放蕩……紛爭、嫉妒、怒氣、自私的野心 (as 2 Corinthians 12:20–21)；仁愛、喜樂、平安、忍耐、恩慈、良善、信實、溫柔、節制 | Two-character list for reading aloud; 仁愛 for *agape* (1 Corinthians 13's 愛 noted), 平安 as in the greetings. |
| καινὴ κτίσις (6:15) | 新造的人 | As 2 Corinthians 5:17. |
| Names | 磯法、巴拿巴、提多、安提阿、敘利亞、基利家、阿拉伯、大馬色、夏甲、西奈山 | 阿拉伯 as the rest of this translation (classic Union Version 亞拉伯). |

Settled while drafting Ephesians:

| Source | Rendering | Notes |
|---|---|---|
| [ἐν Ἐφέσῳ] (1:1) | 〔在以弗所〕 | The SBLGNT's brackets printed 〔 〕 as in Luke; the manuscripts that lack the words noted. |
| 1:3–14 (one Greek sentence) | Broken into Chinese sentences | The refrain 為要讚美他的榮耀 (1:12, 14; 1:6 讚美他榮耀的恩典) and 在基督裏／在他裏面 kept; the one-sentence form noted at 1:6. |
| ἐν τοῖς ἐπουρανίοις | 在天上 | 直譯「在天上的〔領域〕裏」 noted (1:3, 20; 2:6; 3:10; 6:12). |
| ἀρραβών (1:14); σφραγίζω (1:13; 4:30) | 訂金；蓋上了印 | As 2 Corinthians 1:22. κληρονομία 產業 (as Galatians 3:18), not 和合本「基業」. |
| μυστήριον; οἰκονομία | 奧祕；安排、管理 (by context) | As 1 Corinthians; *oikonomia* noted (1:10; 3:2, 9). |
| ἀρχαί, ἐξουσίαι, δυνάμεις, κυριότητες (1:21; 3:10; 6:12) | 統治的、掌權的、有能力的、主治的 | As 1 Corinthians 15:24. |
| 2:8–9 | 你們得救是本乎恩，也因着信；這並不是出於你們自己，而是神所賜的；也不是出於行為，免得有人自誇 | |
| Old Testament quotations | Our Old Testament wording, and our notes' wording, where the Greek agrees | 1:22 = Psalm 8:7 (and 1 Corinthians 15:27); 4:8 他升上高處，擄走了俘虜，把禮物賜給人 (our Psalm 68:19 note; 受了/賜給 noted); 4:25 = Zechariah 8:16; 4:26 生氣卻不要犯罪 (our Psalm 4:5 note); 4:30 不要使神的聖靈擔憂 (our Isaiah 63:10 note); 5:31 = Matthew 19:5 (Genesis 2:24's 緊密結合 noted); 6:2–3 要孝敬父母……使你得福，在地上得以長久活着 (Exodus 20:12, Deuteronomy 5:16). |
| 5:14 | 「你這睡着的人，要醒過來，從死人中起來，基督就要光照你！」 | Not in the Old Testament; noted as perhaps an early hymn. |
| ὑποτάσσομαι (5:21–24) | 順服 | 5:21 ends the sentence begun at 5:18 (verses 19–20 end in commas); 5:22's missing verb noted. κεφαλή 頭 (元首 for Christ over all things, 1:22; 4:15). |
| The household code (5:22–6:9) | 作妻子的／作丈夫的／作兒女的／作父親的／作奴僕的／作主人的 | *douloi* noted on slavery (6:5); *kyrioi* 主人, *kyrios* 主. |
| The armor of God (6:11–17) | 神所賜的全副軍裝；真理作帶子束腰，義作鎧甲……信心作盾牌，救恩作頭盔，聖靈的寶劍 | 鎧甲 and 頭盔 as our Isaiah 59:17. |
| Names | 以弗所、推基古 | |

Settled while drafting Philippians:

| Source | Rendering | Notes |
|---|---|---|
| ἐπίσκοποι καὶ διάκονοι (1:1) | 監督和執事 | 監督 as Acts 20:28 (傳統「主教」 noted); *diakonoi* noted as a recognized role (傳統「執事」), as Romans 16:1. |
| 1:21 | 活着就是基督，死了就有益處 | |
| The Christ hymn (2:6–11) | 他本有神的形像，並不把與神同等看作要抓住不放的，反而倒空自己，取了奴僕的形像，成為人的樣式 | Prose verses, as the English. *morphe* 形像 (kept apart from *eikon* 像, Colossians 1:15); *harpagmos* (和合本「強奪的」) and *kenoo* (和合本「虛己」) noted; the participle 本有 (雖然有／正因為有) noted. |
| 2:10–11 (Isaiah 45:23) | 萬膝都要跪拜，萬口都要承認「耶穌基督是主」 | As Romans 14:11's 萬膝必向我跪拜，萬口必向神承認; our Isaiah's 起誓 and *kyrios* for YHWH noted. |
| σπένδομαι (2:17) | 像奠祭一樣被澆 | 奠祭 as Exodus 29:40. *leitourgia*, *leitourgos* 事奉；供應……的人. |
| σκύβαλα (3:8) | 糞土 | Noted as a coarse word (垃圾、糞便). |
| κατατομή / περιτομή (3:2–3) | 殘害肉體的；受割禮的 | The wordplay noted. *sarx* here outward descent, noted (3:3–4). |
| πολιτεύομαι (1:27); πολίτευμα (3:20) | 生活為人；國籍 | Philippi a Roman colony, noted. |
| 4:4; 4:6–7; 4:13 | 你們要常常在主裏喜樂；我再說，你們要喜樂……神那超越人一切理解的平安，必在基督耶穌裏保守你們的心懷意念……我靠着那加給我力量的，凡事都能做 | 「基督」 manuscripts noted at 4:13. |
| Names | 友阿爹、循都基、革利免、以巴弗提、腓立比、馬其頓、帖撒羅尼迦；該撒家裏的人 | 友阿爹 the classic Union form (1989 友阿蝶); Euodia and Syntyche added to the names table. *syzygos* (4:3) 同伴, the possible name noted. |

Settled while drafting Colossians:

| Source | Rendering | Notes |
|---|---|---|
| The Christ hymn (1:15–20) | 他是那不能看見的神的像，是一切受造之物中首生的……他是元始，是從死人中首生的 | Prose verses; the hymn's two parts noted. *eikon* 像 (also 3:10; 2 Corinthians 4:4's 形像 and Philippians 2:6's *morphe* noted). *prototokos* 首生的, with Romans 8:29's 長子 and Psalm 89:28 noted as the same word. θρόνοι, κυριότητες, ἀρχαί, ἐξουσίαι 坐王位的、主治的、統治的、掌權的, as Ephesians. |
| κλῆρος (1:12); κληρονομία (3:24) | 產業 | As Ephesians. |
| τὰ στοιχεῖα τοῦ κόσμου (2:8, 20) | 世上的基本原則 | As Galatians 4:3, 9, with the same notes. |
| 2:16 | 節期、月朔、安息日 | 月朔 as Isaiah 1:13; plural *sabbata* noted. |
| χειρόγραφον (2:14); θριαμβεύω (2:15) | 債據；凱旋遊行 | Both noted. |
| 3:1–4 | 尋求上面的事……你們的生命與基督一同藏在神裏面 | τὰ ἄνω 上面的事. |
| 3:11 | 在這裏，不再分希臘人或猶太人，不再分受割禮的或未受割禮的，不再分未開化的人、西古提人、奴僕、自由人；唯有基督是一切，又在一切之中 | Galatians 3:28's pattern. |
| ψαλμοί, ὕμνοι, ᾠδαὶ πνευματικαί (3:16) | 詩章、頌詞和靈歌 | As Ephesians 5:19. |
| The household code (3:18–4:1) | 作妻子的……順服；作丈夫的；作兒女的……聽從；作父親的；作奴僕的……肉身的主人；不要只在人眼前工作，像是要討人喜歡；作主人的 | Ephesians 5:22–6:9's wording and notes where the Greek is parallel; 3:21 *erethizo* 激怒 (Ephesians 6:4 *parorgizo* 惹……發怒). |
| 4:16 | 從老底嘉來的那封信 | Noted: lost, or perhaps Ephesians. |
| Names | 歌羅西、老底嘉、希拉坡里、以巴弗、推基古、阿尼西母、亞里達古、馬可、巴拿巴、耶數（稱為猶士都的）、路加、底馬、寧法、亞基布、西古提人 | 阿尼西母 the classic Union form (1989 阿尼西謀); the names table changed, and Colossae added. 耶數 noted as the Greek *Iesous*. |

Settled while drafting 1 Thessalonians:

| Source | Rendering | Notes |
|---|---|---|
| παρουσία (2:19; 3:13; 4:15; 5:23) | 來臨 (主耶穌來臨的時候) | As Matthew 24:3 and 1 Corinthians 15:23; *parousia* noted each time, fully at 2:19. |
| 1:3; 5:8 | 因信而做的工作、因愛而受的勞苦，以及因盼望……而有的忍耐；用信和愛作鎧甲……用得救的盼望作頭盔 | 1 Corinthians 13:13's 信、望、愛 linked in the notes. |
| κοιμάομαι (4:13–15) | 睡了的人 | As 1 Corinthians 15:6, 18, 20; noted: died. |
| ἀρχάγγελος; σάλπιγξ θεοῦ (4:16) | 天使長；神的號角 | 號角 as 1 Corinthians 15:52. |
| ἁρπάζω (4:17); ἀπάντησις | 被提；迎見 | 被提 as 2 Corinthians 12:2, 4; the later term ("rapture", *rapiemur*) noted as going beyond the text; *apantesis* (meeting an arriving dignitary) noted. |
| ἡμέρα κυρίου (5:2) | 主的日子 | As 1 Corinthians 5:5; the thief 就像賊在夜裏來一樣, as Matthew 24:43; the Old Testament's 耶和華的日子 noted. |
| 5:16–18 | 要常常喜樂，不住地禱告，凡事感恩 | Three short lines. |
| 5:19 | 不要熄滅聖靈 | The fire picture and 和合本「不要消滅聖靈的感動」 noted. |
| πνεῦμα, ψυχή, σῶμα (5:23) | 靈、魂和身體 | ψυχή 魂 as Colossians 3:23's note; the debate over three parts noted. |
| ἄτακτοι (5:14) | 游手好閒的人 | 或譯「不守規矩的人」 noted; 2 Thessalonians 3:6–11 linked. |
| Names | 西拉 (*Silvanus*, as 2 Corinthians)、提摩太、帖撒羅尼迦、馬其頓、亞該亞、腓立比、雅典 | |

Settled while drafting 2 Thessalonians:

| Source | Rendering | Notes |
|---|---|---|
| ἀποστασία (2:3) | 背道的事 | Plainer than 和合本「離道反教」 (noted); *apostasia* 「叛亂、背叛」, political or against God, noted. |
| ὁ ἄνθρωπος τῆς ἀνομίας; ὁ υἱὸς τῆς ἀπωλείας; ὁ ἄνομος (2:3, 8) | 那不法的人；那滅亡之子 (as John 17:12)；那不法的人 | 「那罪惡的人」 manuscripts noted. |
| τὸ κατέχον; ὁ κατέχων (2:6–7) | 那攔阻他的；那攔阻的 | Neuter and masculine, the unknown referent and the other senses of *katecho* noted. |
| παρουσία (2:1, 8, 9) | 來臨 | As 1 Thessalonians; 2:9 the same word for the lawless one, noted. ἐπιφάνεια (2:8) 顯現. |
| παράδοσις (2:15; 3:6) | 傳統 | As 1 Corinthians 11:2. |
| Old Testament echoes | Noted with our Old Testament's wording | 1:8 Isaiah 66:15, Jeremiah 10:25; 1:9 Isaiah 2:10, 19, 21 (Septuagint 權能的榮光, our 威嚴的榮光); 2:4 Daniel 11:36 (一切神明 / 一切稱為神的), Ezekiel 28:2; 2:8 用口中的氣殺死他 as our Isaiah 11:4 (用嘴唇的氣殺死惡人). |
| 2:2; 3:17 | 好像是我們寄來的書信；我保羅親筆問候你們 | 3:17 as Colossians 4:18; the notes link the signature to 2:2. |
| 3:10 | 「若有人不肯工作，就不可吃飯。」 | |
| ἀτάκτως; περιεργάζομαι (3:6–11) | 游手好閒；只管閒事 | As 1 Thessalonians 5:14; 3:11 甚麼事都不做，只管閒事 keeps a wordplay (*ergazomai*/*periergazomai* noted). |

Settled while drafting 1 Timothy:

| Source | Rendering | Notes |
|---|---|---|
| πιστὸς ὁ λόγος (1:15; 3:1; 4:9) | 這話是可信的 (1:15 and 4:9 add 值得完全接受) | The formula for all five (also 2 Timothy 2:11; Titus 3:8), noted at 1:15. |
| εὐσέβεια; εὐσεβέω (5:4); θεοσέβεια (2:10) | 敬虔；盡孝；敬畏神 | *eusebeia* noted at 2:2 (Acts 3:12 虔誠). |
| σωφροσύνη, σώφρων; νηφάλιος | 自律；頭腦清醒 | 2:9, 15; 3:2, 11. |
| ὑγιαίνουσα διδασκαλία; ὑγιαίνοντες λόγοι; ἑτεροδιδασκαλέω; μῦθοι | 健全的教導；健全的話；傳別的教義；無稽的傳說 | *hygiaino* noted at 6:3. |
| σωτήρ | 救主 (我們的救主神) | |
| μεσίτης (2:5); ἀντίλυτρον (2:6) | 中保；贖價 | Galatians 3:19–20's 中間人 and Mark 10:45 noted. |
| 2:8–15 | 男人；女人；管轄 (*authenteo*)；在安靜中……順服 | Man/husband, *authenteo* and the readings of 2:15 in notes, as the English. |
| ἐπίσκοπος, ἐπισκοπή; διάκονοι; γυναῖκες (3:11) | 監督、監督的職分；執事；女人 | As Philippians 1:1; 3:11 wives or women deacons noted. μιᾶς γυναικὸς ἀνήρ 只作一個妻子的丈夫 (直譯 noted). |
| πρεσβύτερος; πρεσβυτέριον | 長老 (5:17, 19)；年老的人 (5:1)；長老團 (4:14) | As Acts. |
| 3:16 | 他在肉體裏顯現，在靈裏被證實為義，被天使看見，在外邦人中被傳揚，在世上被人信服，被接到榮耀裏 | Prose; Ὃς as the SBLGNT, the 神 reading (ΟΣ/ΘΣ) noted. |
| 5:18 | Deuteronomy 25:4 as 1 Corinthians 9:9; 做工的人得工錢是應當的 as Luke 10:7 | |
| χῆραι (5:3–16) | 真正無依無靠的寡婦 | 直譯「真是寡婦的」 noted. |
| ὁμολογία (6:12–13); ἐπιφάνεια (6:14) | 宣認；顯現 | 顯現 as 2 Thessalonians 2:8. |
| ἄνθρωπε θεοῦ (6:11); 6:10 | 屬神的人；貪愛錢財是萬惡之根 | The Old Testament's 神人 noted. |

Settled while drafting 2 Timothy:

| Source | Rendering | Notes |
|---|---|---|
| παραθήκη (1:12, 14) | 託付 (我所交託他的；那美好的託付) | As 1 Timothy 6:20; 「他所交託我的」 noted. |
| 2:11–13 | 這話是可信的：我們若與他同死，也必與他同活…… | Prose; the formula as 1 Timothy 1:15; 2:13 ἀπιστέω/πιστός 不信實／信實. |
| 2:19 (Numbers 16:5) | 主認識屬他的人 | The Septuagint (神認識) and our Numbers (耶和華必指明誰是屬他的) noted. |
| θεόπνευστος (3:16); ἱερὰ γράμματα (3:15) | 全部聖經都是神所默示的；聖經 | *theopneustos* 「神所呼出的」 and the two readings of the verbless sentence noted. |
| 4:6–8 | 像奠祭一樣被澆出來；那美好的仗我已經打過了，當跑的路我已經跑盡了，信仰我已經守住了；義的冠冕……公義的審判者 | 奠祭 as Philippians 2:17; δικαιοσύνη 義, δίκαιος of God's judgment 公義, as Romans. |
| Names | 羅以、友尼基、腓吉路、黑摩其尼、阿尼色弗、許米乃、腓理徒、雅尼、佯庇、底馬、革勒士、撻馬太、加布、亞歷山大、友布羅、布田、利奴、革老底亞 | 友尼基 the classic Union form (1989 友妮基); the names table changed, and Hermogenes added. |

Settled while drafting Titus:

| Source | Rendering | Notes |
|---|---|---|
| πρεσβύτεροι; ἐπίσκοπος (1:5–7); πρεσβῦται (2:2) | 長老；監督；年老的男人 | As 1 Timothy; the shift from elders to overseer and *presbytai* noted. ἐγκρατής 有節制 (as Galatians 5:23). |
| 1:12 (Epimenides) | 「革哩底人常說謊話，是兇惡的野獸，又懶又貪吃。」 | 革哩底 as Acts 27; the poet noted (埃庇米尼得斯, as the Acts 17:28 note). |
| 2:13 | 我們偉大的神和救主耶穌基督榮耀的顯現 | One article, as 2 Thessalonians 1:12; the two-person reading noted. |
| λαὸς περιούσιος (2:14) | 作屬他自己的子民，作他的珍寶 | As our Deuteronomy 14:2. |
| 3:5 | 重生的洗和聖靈的更新 | *palingenesia* noted, linked to Matthew 19:28 (萬物更新) and kept apart from John 3's *anothen* (從上面生). 3:6 傾倒 as Joel 3:1. |
| καλῶν ἔργων προΐστασθαι (3:8, 14); αἱρετικός; νομικός (3:13) | 致力行善；分門結黨的人；律法專家 | 「從事正當的職業」 noted; 律法專家 as Matthew 22:35. |
| Names | 革哩底、尼哥坡里、亞提馬、推基古、西納、亞波羅 | |

Settled while drafting Philemon:

| Source | Rendering | Notes |
|---|---|---|
| δέσμιος Χριστοῦ Ἰησοῦ (1, 9) | 為基督耶穌被囚的 | As 2 Timothy 1:8. |
| Ὀνήσιμος; ἄχρηστος / εὔχρηστος (10–11); ὀναίμην (20) | 阿尼西母；沒有益處／有益處；得益處 | The name's meaning and both wordplays (*chrestos*/*Christos* too) in notes. |
| σπλάγχνα (7, 12, 20) | 心；我的心肝 (12) | 直譯「心腸」 noted, as Philippians 1:8. |
| πρεσβύτης (9) | 老人 | 「使者」 (*presbeutes*) noted. |
| Names | 腓利門、亞腓亞、亞基布、阿尼西母、以巴弗、馬可、亞里達古、底馬、路加 | 阿尼西母 the classic form, as Colossians 4:9. |

Settled while drafting Hebrews:

| Source | Rendering | Notes |
|---|---|---|
| ἀρχιερεύς; ἱερωσύνη; τάξις Μελχισέδεκ | 大祭司；祭司職分；按照麥基洗德的等次 | 等次 (和合本) from the Septuagint's *taxis*; our Psalm 110:4's 方式 noted at 5:6. 7:15 κατὰ τὴν ὁμοιότητα 像麥基洗德那樣. |
| διαθήκη; καινὴ / νέα διαθήκη; μεσίτης; ἔγγυος | 約；新約；中保；保證人 | 中保 as 1 Timothy 2:5 (8:6; 9:15; 12:24). 9:16–17 遺囑, the covenant/will wordplay noted at 9:16. *nea* (12:24) noted against *kaine*. |
| ἱλαστήριον (9:5); ἱλάσκομαι (2:17); θρόνος τῆς χάριτος (4:16) | 施恩座；贖罪；施恩的寶座 | 施恩座 as Romans 3:25 and Exodus 25:17; 4:16's throne told apart from it in a note. |
| σκηνή; ἡ πρώτη σκηνή; τὰ ἅγια; ἅγια ἁγίων; καταπέτασμα | 帳幕；外層的帳幕；聖所；至聖所；幔子 | *ta hagia* (the heavenly sanctuary or the most holy place) noted each time; *thymiaterion* 金香壇 (香爐 noted); 約櫃、約版 (our Exodus 法版 noted). |
| τελειόω; τέλειος | 使……完全、得以完全；成熟的人 | *teleioo* noted at 2:10. |
| ἀρχηγός (2:10; 12:2); πρόδρομος (6:20) | 創始者 (救他們的創始者；信心的創始者和完成者)；先鋒 | As Acts 3:15; 和合本「元帥」「創始成終」 noted. |
| ὁμολογία | 所宣認的 (信仰、盼望) | As 1 Timothy 6:12. |
| ὑπόστασις | 本質 (1:3)；確信 (3:14)；把握 (11:1) | 11:1 信，就是對所盼望的事有把握，對看不見的事有確信 (和合本「實底」「確據」 noted). Πίστει 因着信 throughout chapter 11. |
| κατάπαυσις; σαββατισμός (4:9) | 安息；安息日的安息 | Psalm 95's 安息. |
| Old Testament quotations | Hebrews' Greek (mostly the Septuagint) in the text; the wording our Old Testament notes already give is kept | Our Old Testament's Hebrew-based line in the note where it differs: 1:6 神的使者都要拜他; 1:7 他以他的使者為風; 1:10–12 主啊……捲起來; 2:6–8 比天使微小一點 (世人, 直譯「人子」 noted); 2:13 我要倚靠他; 3:7–11 像在惹我發怒的時候，像在曠野試探的日子; 8:8–12 訂立新約……因為他們不恆守我的約，我也就不理他們……放在他們的思想裏; 10:5 你卻為我預備了身體; 10:30 as Romans 12:19; 10:38 我的義人必因信而活；他若退縮，我心裏就不喜悅他; 11:21 扶着杖頭; 12:5–6 不要灰心……鞭打; 12:12–13 as our Isaiah 35:3 and Proverbs 4:26 notes; 12:26 再一次我不單要震動地，還要震動天; 13:5 我決不撇下你，也決不丟棄你; 13:6 主是幫助我的. |
| Names (11) | 亞伯、該隱、以諾、挪亞、撒拉、以掃、喇合、基甸、巴拉、參孫、耶弗他、撒母耳；意大利 (13:24, as Acts) | Our Old Testament forms. 4:8 *Iesous* 約書亞, noted. |

Settled while drafting James:

| Source | Rendering | Notes |
|---|---|---|
| χαίρειν (1:1) | 問候……：願你們安好！ | As Acts 15:23; *chairein* and its link to 1:2's 喜樂 noted. |
| πειρασμός; πειράζω (1:2–15) | 試煉；引誘 | 1:12 試煉, 1:13–14 引誘, the one word family noted at 1:2. δίψυχος 三心兩意 (1:8; 4:8). |
| πίστις; ἔργα; δικαιόω (2:14–26) | 信心；行為；稱義 (因行為稱義) | Romans' words kept so the reader sees the same terms (Romans 4:2 因行為稱義; 3:28 人稱義是因着信). 2:24 人稱義是因着行為，不是單因着信. The relation to Paul noted briefly at 2:21. 2:20 *arge* 無用的 (*a-ergos* noted). |
| Old Testament quotations | Paul's and the Old Testament notes' wording | 2:8 = Romans 13:9 (要愛你的鄰舍，如同愛自己); 2:11 不可通姦……不可謀殺 (Exodus 20; 傳統「殺人」 noted); 2:23 = Romans 4:3 (亞伯拉罕信了神，這就算為他的義); 4:6 神抵擋驕傲的人，賜恩給謙卑的人 (our Proverbs 3:34 note; 1 Peter 5:5 the same); 5:20 遮掩許多的罪 as 1 Peter 4:8. 4:5 (no known source) noted with its readings. |
| νόμος βασιλικός (2:8); νόμος ἐλευθερίας (1:25; 2:12) | 至尊的律法；使人自由的律法 | 直譯「君王的律法」 noted. |
| δαιμόνια (2:19); δαιμονιώδης (3:15); ψυχικός (3:15) | 鬼魔；屬鬼魔的；屬血氣的 | As 1 Corinthians 10:20 and 2:14. γέεννα (3:6) 地獄 as Mark. |
| Κύριος Σαβαώθ (5:4); παρουσία (5:7–8) | 萬軍之主；主來臨 | *YHWH tseva'ot* noted; *parousia* as 1 Thessalonians. |
| πρεσβύτεροι τῆς ἐκκλησίας (5:14) | 教會的長老 | As Acts and Titus; anointing 用油抹他. 5:15 *sozo* 救 (或譯「醫好」 noted). |
| Names | 雅各、亞伯拉罕、以撒、喇合、約伯、以利亞 | *Iakobos* = Jacob noted at 1:1. |

Settled while drafting 1 Peter:

| Source | Rendering | Notes |
|---|---|---|
| παρεπίδημοι; πάροικοι; παροικία (1:1, 17; 2:11) | 寄居的人；寄居的外人，暫住的客旅；在世寄居的日子 | Genesis 23:4's 寄居的外人 (LXX *paroikos kai parepidemos*) noted at 2:11. *diaspora* as James 1:1. |
| ἀναγεννάω (1:3, 23) | 重生 | Kept apart from John 3's 從上面生 (*anothen*). |
| Old Testament quotations | Our Old Testament wording and our notes' wording where the Greek agrees | 1:16 你們要聖潔，因為我是聖潔的 (= our Leviticus 11:45); 1:24–25 草必枯乾，花必凋謝，惟有主的話永遠長存 (our Isaiah 40:8 note); 2:3 Psalm 34:9; 3:10–12 Psalm 34:13–17 in the third person; 4:18 the wording our Proverbs 11:31 note gives; 5:5 = James 4:6. |
| The stone catena (2:6–8) | 看哪，我在錫安放一塊揀選的、寶貴的房角石，信靠他的人必不至於羞愧；建築工人丟棄的石頭，已經成了房角的基石；絆腳的石頭，跌人的磐石 | Our Isaiah 28:16 note's wording; Psalm 118:22 = Matthew 21:42 and Mark 12:10; Isaiah 8:14 = Romans 9:33. 2:7 *time* 尊貴, linked to *entimos* 寶貴. |
| 2:9 (Exodus 19:5–6; Isaiah 43:20–21) | 蒙揀選的族類，作君王的祭司，聖潔的國民，屬神自己的子民……美德 | 聖潔的國民 as our Exodus 19:6; 和合本「君尊的祭司」 and our 祭司的國度 noted. |
| 2:22–25 (Isaiah 53) | 他沒有犯罪，口裏也沒有詭詐；因他受的鞭傷，你們得了醫治；你們從前好像迷路的羊 | The wording our Isaiah 53:5–6, 9 notes give; ξύλον 木頭 as Acts 5:30, noted as the cross. |
| 3:18–22 | 按肉體說，他被處死；按靈性說，他卻復活了；向那些在監獄裏的靈宣告；八個人；洗禮……向神求得無愧的良心 | The three readings of 3:19 in one note (fallen angels and 1 Enoch; the dead; Christ in Noah); *eperotema* noted. |
| οἰκέται (2:18); συμπρεσβύτερος (5:1); ἀρχιποίμην (5:4); ἐπίσκοπος (2:25) | 家僕；同作長老的；牧長；監督 | 5:5 *presbyteroi* 年長的 (the link to 長老 noted). |
| 4:8 (Proverbs 10:12) | 愛能遮掩許多的罪 | As our Proverbs note; James 5:20 the same. Χριστιανός 基督徒 as Acts 11:26. |
| Names | 彼得、本都、加拉太、加帕多家、亞細亞、庇推尼、撒拉、亞伯拉罕、挪亞、西拉 (*Silouanos*, as 2 Corinthians 1:19)、巴比倫 (noted as Rome)、馬可 | |

Settled while drafting 2 Peter:

| Source | Rendering | Notes |
|---|---|---|
| Συμεὼν Πέτρος (1:1) | 西面彼得 | The Hebrew form, as Acts 15:14; 和合本「西門彼得」 noted. 1:1 我們的神和救主耶穌基督 (one article, as Titus 2:13; the two-person reading noted). |
| ἐπίγνωσις; ἀρετή; θείας κοινωνοὶ φύσεως (1:3–4) | 認識；美德；分享神的本性 | The ladder of 1:5–7: 信心、美德、知識、節制、忍耐、敬虔、愛弟兄姊妹的心、愛. |
| 1:17 (the transfiguration) | 這是我的兒子，是我所愛的，我喜悅他 | = Matthew 17:5; the Greek order and the unfinished sentence noted. ἡ μεγαλοπρεπὴς δόξα 那至高的榮耀. |
| 1:20–21 | 經上所有的預言，都不是出於個人的解釋；人被聖靈感動，說出從神而來的話 | The two readings of *idias epilyseos* and the *phero* wordplay noted. |
| 2:1–18 (parallel to Jude 4–16) | Shared wording kept for Jude: 主宰 (*despotes*)；放蕩；藐視主權 (*kyriotes*)；毀謗那些有尊榮的；沒有理性的畜類；毀謗自己所不知道的事；一同吃喝；巴蘭；無水的泉源；漆黑的幽暗；誇大的話 | Each parallel noted. |
| ταρταρόω (2:4) | 丟進地獄 | As 和合本; *Tartarus* noted and kept apart from *geenna*. σειραὶ ζόφου 黑暗的鎖鏈. |
| 2:5–8 | 傳義道的挪亞一家八口；所多瑪和蛾摩拉；義人羅得 | 直譯「第八位挪亞」 noted. |
| Βαλαὰμ τοῦ Βοσόρ (2:15) | 比珥的兒子巴蘭 | 比珥 as Numbers 22:5 and 和合本, with *Bosor* (SBLGNT) and *Beor* noted; Bosor added to the names table. |
| 2:22 | 狗轉過來吃自己所吐的；豬洗淨了，又回到泥裏打滾 | Our Proverbs 26:11 and its note. 2:20 = Matthew 12:45 (後來的景況就比先前更糟了). |
| 3:8; 3:10 | 在主看來，一日如千年，千年如一日；主的日子要像賊一樣來到 | Psalm 90:4 and 1 Thessalonians 5:2 noted. στοιχεῖα 元素; 3:10 εὑρεθήσεται 顯露出來, with the variants. |
| 3:16 | 別的經書 | Noted as the one New Testament reference to a collection of Paul's letters. |

Settled while drafting Jude:

| Source | Rendering | Notes |
|---|---|---|
| Wording shared with 2 Peter 2 | 放蕩；主宰 (*despotes*)；輕視主權；毀謗那些有尊榮的；毀謗自己所不知道的事；沒有理性的畜類；一同吃喝；巴蘭；漆黑的幽暗；口出誇大的話；好嘲笑的人隨從……私慾而行 | Each parallel noted to 2 Peter. *spilades* 暗礁 (12; 2 Peter 2:13's *spiloi* 污點); ἀγάπαι 愛筵. |
| Ἰησοῦς (5) | 耶穌 | The SBLGNT (NA28); 「約書亞」 and 「主」 in the note. |
| 6 | 不守本位……他用永遠的鎖鏈把他們拘禁在黑暗裏，等候那大日的審判 | *tereo* wordplay and 1 Enoch 6–16 noted. |
| 9 | 天使長米迦勒為了摩西的屍體與魔鬼爭辯……「願主斥責你！」 | Zechariah 3:2's 願耶和華斥責你 and the Assumption of Moses noted. |
| 14–15 (1 Enoch 1:9) | 亞當的第七代孫以諾……「看哪，主帶着他千萬的聖者來了」 | 《以諾一書》 noted (Ethiopic, Greek, Aramaic). Book titles outside the Bible in 《》. |
| 22–23 | Three groups, as the SBLGNT | The manuscripts' two- and three-group forms noted. |
| The doxology (24–25) | 那能保守你們不失腳，叫你們無瑕無疵、歡歡喜喜地站在他榮耀之前的，就是獨一的神、我們的救主，願榮耀、威嚴、能力、權柄，藉着我們的主耶穌基督歸給他，從萬古以前，到現在，直到永永遠遠！阿們。 | For reading aloud. |
| Names | 猶大、雅各、米迦勒、摩西、該隱、巴蘭、可拉、以諾、亞當、所多瑪、蛾摩拉、埃及 | |

Settled while drafting 1 John:

| Source | Rendering | Notes |
|---|---|---|
| 1:1–4 | 那從起初就有的……就是論到生命之道；與父同在；永生 | John 1:1–2's 起初, 道, 與神同在 echoed; 道 here with 「生命的話」 in the note (John's table: *logos* elsewhere 話, 2:7; 2:5 遵守他話的; 2:14 神的道 as John 10:35). κοινωνία 相交. |
| John's vocabulary | 光／黑暗；真理 (行真理, 1:6 直譯 noted)；真光 (2:8)；遵守命令；住在 (*meno*)；世界；永生；生命 | As John's table throughout. 2:17 μένει εἰς τὸν αἰῶνα 永遠長存. |
| ἐκ τοῦ θεοῦ γεγέννηται | 從神生的 | As John 1:13 (從神生的); kept apart from John 3's 從上面生 (*anothen*) and 1 Peter's 重生. ἐκ τοῦ θεοῦ / τοῦ διαβόλου without the verb: 出於神的；屬魔鬼的 (3:8 note). |
| παράκλητος (2:1) | 保惠師 | As John 14–16; the sense here (辯護者) in the note. |
| ἱλασμός (2:2; 4:10) | 贖罪祭 (為我們的罪作贖罪祭) | As the Chinese New Version; 和合本「挽回祭」 noted. Linked in the note to Romans 3:25 and Hebrews 9:5 *hilasterion* 施恩座, Hebrews 2:17 *hilaskomai* 贖罪, and the Septuagint's 贖罪日 (Leviticus 25:9). |
| ἀντίχριστος (2:18, 22; 4:3) | 敵基督 | *antichristos* noted at 2:18; χρῖσμα 恩膏, its link to *christos* noted (2:20, 27). |
| τεκνία; παιδία; ἀγαπητοί; πατέρες; νεανίσκοι | 孩子們 (as John 13:33)；小孩子們；親愛的；父老們；青年人 | 2:12–14 *hoti* 因為, with 「寫信告訴你們」 in the note. |
| ἀδελφός | 弟兄姊妹 | By the Romans rule, noted (直譯「他的弟兄」) at the first in each chapter; Abel (3:12) 兄弟. |
| ἐκεῖνος (of Jesus) | 那一位 | Noted at 2:6 (2:6; 3:3, 5, 7, 16; 4:17). |
| 3:16 | 那一位為我們捨了命 | John 10:11 and 15:13 (捨命) quoted in the note. 3:14 出死入生 as John 5:24. |
| 4:8, 16 | 神是愛 | Plain, as 1:5 神是光. |
| μονογενής (4:9) | 獨生子 | As John 3:16; *monogenes* noted. |
| 5:6–8 | 藉着水和血來的……作見證的有三個：就是聖靈、水和血，而這三者是一致的 | Water and blood noted (John 19:34). The Johannine Comma (TR, KJV) not in the text, translated in the note at 5:7, as the English; 和合本 numbering (5:6b = its 7; 5:7–8 = its 8) noted. |
| Names | 該隱 | |

Settled while drafting 2 and 3 John:

| Source | Rendering | Notes |
|---|---|---|
| ὁ πρεσβύτερος (2 John 1; 3 John 1) | 作長老的，致…… | *presbyteros* noted; the opening as Romans (致……, no verb). |
| ἐκλεκτὴ κυρία (2 John 1, 5); ἡ ἀδελφή σου ἡ ἐκλεκτή (13) | 蒙揀選的夫人；夫人哪；你那蒙揀選的姊妹 | The readings as names (*Kyria*, *Electa*) and as a figure for a church (1 Peter 5:13) noted; 和合本「太太」 noted. |
| ἐν ἀληθείᾳ; περιπατέω ἐν ἀληθείᾳ | 在真理中 (或譯「真誠地」)；在真理中行 | 1 John's vocabulary throughout (住在, 敵基督, 迷惑人的, 在肉身中來的). |
| χαίρειν λέγω (2 John 10–11) | 問安 | 直譯「說『願你喜樂！』」 noted, as James 1:1. |
| στόμα πρὸς στόμα | 當面 | 直譯「口對口」 noted. |

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
