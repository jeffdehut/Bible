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
