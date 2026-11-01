# Where each icon goes

Every icon in this library, the file it is in, and every place in the app that draws it (the code location, as `file:line TABLE.key` at the time the set was made). The app draws them from the same shapes (see `iconkit.js` and the tables named here).

## 00-app-icon

| File | Icon | Where it goes in the app |
|---|---|---|
| [app-icon.svg](00-app-icon/app-icon.svg) | BibleData.org app icon | The site’s identity: favicon, brand image beside “BibleData.org” in the bar, home-screen icon, mark on shared images. icon-192.png / icon-512.png are the raster versions (apple-touch-icon, manifest).<br><sub>icons/icon.svg</sub> |
| [icon-192.png](00-app-icon/icon-192.png) | icon-192.png | apple-touch-icon (192) and the web-app manifest icons.<br><sub>icons/icon-192.png</sub> |
| [icon-512.png](00-app-icon/icon-512.png) | icon-512.png | apple-touch-icon (192) and the web-app manifest icons.<br><sub>icons/icon-512.png</sub> |

## 01-navigation-menu

| File | Icon | Where it goes in the app |
|---|---|---|
| [atlas-two-pages.svg](01-navigation-menu/atlas-two-pages.svg) | Atlas | Defined as `ICON.atlas` in nav.js; no menu item uses it at present (the Maps item covers the atlas).<br><sub>nav.js:24 ICON.atlas</sub> |
| [book-open-with-lines.svg](01-navigation-menu/book-open-with-lines.svg) | Read | Menu “Read”: back to the Bible where you left off.<br><sub>nav.js:12 ICON.read</sub> |
| [book-open.svg](01-navigation-menu/book-open.svg) | Open book | Menu “Topics & dictionary” (Nave’s topics, Easton’s dictionary); also the emoji mark “Scripture”, the “Classic” color theme, the timeline’s Bible icon, and “Kind of writing” in the Visual Bible card. Timeline “book”: items named bible, testament, vulgate, version, biblia, graece, instrumentum; lives: wycliffe, erasmus, tyndale, tischendorf, jerome; stream “The Bible in world history” (Drawn at stroke-width 1.8, 1.9, 2 in different places.)<br><sub>nav.js:16 ICON.study; index.html:4985 EMOJI_ICONS.book; index.html:3192 SEASON_INFO.classic; scripts/templates/history.html:479 GLYPH.book; scripts/templates/visual-book.html:458 IC.book; scripts/templates/visual-letters.html:454 IC.book</sub> |
| [book-with-bars.svg](01-navigation-menu/book-with-bars.svg) | Visual Bible | Menu “Visual Bible”: each book on the shelf, and seen whole from its own words (library.html).<br><sub>nav.js:27 ICON.visual</sub> |
| [books-on-shelf.svg](01-navigation-menu/books-on-shelf.svg) | Shelf | Defined as `ICON.shelf` in nav.js; no menu item uses it at present.<br><sub>nav.js:32 ICON.shelf</sub> |
| [calendar-check.svg](01-navigation-menu/calendar-check.svg) | Reading plans | Menu “Reading plans”: through the Bible in a year, and shorter plans.<br><sub>nav.js:15 ICON.plans</sub> |
| [connections-web.svg](01-navigation-menu/connections-web.svg) | Connections | Menu “Connections” (graph.html); also the “Connections” link on every chapter heading in the reader (`WEB_ICON`, stroke 2). (Drawn at stroke-width 1.8, 2 in different places.)<br><sub>nav.js:21 ICON.web; index.html:1594</sub> |
| [cube.svg](01-navigation-menu/cube.svg) | Web in 3D | Menu “Web in 3D”: the web of Scripture in three dimensions (web3d.html).<br><sub>nav.js:22 ICON.web3d</sub> |
| [document.svg](01-navigation-menu/document.svg) | This translation | Menu “This translation”: a first draft, awaiting review.<br><sub>nav.js:34 ICON.translation</sub> |
| [envelope.svg](01-navigation-menu/envelope.svg) | Send feedback | Menu “Send feedback” (mailto); “Written to” in the Visual Bible card. (Drawn at stroke-width 1.8, 2 in different places.)<br><sub>nav.js:38 ICON.mail; scripts/templates/visual-book.html:457 IC.mail; scripts/templates/visual-letters.html:453 IC.mail</sub> |
| [family-tree.svg](01-navigation-menu/family-tree.svg) | Genealogy | Menu “Genealogy”: from Adam to Jesus, and every family.<br><sub>nav.js:26 ICON.gen</sub> |
| [folded-map.svg](01-navigation-menu/folded-map.svg) | Maps | Menu “Maps”: Bible maps and the 1915 historical atlas.<br><sub>nav.js:23 ICON.maps</sub> |
| [harp.svg](01-navigation-menu/harp.svg) | Psalms (harp) | `ICON.psalms` (not in the menu at present); used in the reader’s chapter heading of each psalm as the link “All the psalms” (this psalm among all 150). (Drawn at stroke-width 1.8, 2 in different places.)<br><sub>nav.js:28 ICON.psalms; index.html:1618 guide() chapter-head link “All the psalms”</sub> |
| [info-circle-menu.svg](01-navigation-menu/info-circle-menu.svg) | This project | Menu “This project”: who made it.<br><sub>nav.js:33 ICON.project</sub> |
| [nested-arcs.svg](01-navigation-menu/nested-arcs.svg) | Cross-refs | Menu “Cross-refs”: every cross-reference in the Bible as an arc (arcs.html).<br><sub>nav.js:31 ICON.arcs</sub> |
| [pencil-on-line.svg](01-navigation-menu/pencil-on-line.svg) | Highlights & notes | Menu “Highlights & notes”: your highlights and notes, saved on this device.<br><sub>nav.js:13 ICON.mine</sub> |
| [shapes-and-wavy-line.svg](01-navigation-menu/shapes-and-wavy-line.svg) | Study markings | Menu “Study markings”: key words marked through the whole Bible. (The markings themselves are drawn with CSS text decoration, not SVG; see the notes at the end.)<br><sub>nav.js:18 ICON.marks</sub> |
| [shield-check.svg](01-navigation-menu/shield-check.svg) | Privacy | Menu “Privacy”: what this site keeps about you.<br><sub>nav.js:35 ICON.privacy</sub> |
| [sketchbook.svg](01-navigation-menu/sketchbook.svg) | Sketchbook | Menu “Sketchbook”: your sketches, to share or print.<br><sub>nav.js:37 ICON.sketchbook</sub> |
| [squiggle-with-pen-stroke.svg](01-navigation-menu/squiggle-with-pen-stroke.svg) | Draw on the page | Menu “Draw on the page”: write and draw over the text with a finger or a pen (reader only).<br><sub>nav.js:36 ICON.draw</sub> |
| [star.svg](01-navigation-menu/star.svg) | Star | Emoji mark “Promise”; the “Theme” row of the Visual Bible’s “About the book” card. Also defined as `ICON.mymarks` in nav.js, which no menu item uses at present. (Drawn at stroke-width 1.8, 1.9, 2 in different places.)<br><sub>nav.js:19 ICON.mymarks; index.html:4977 EMOJI_ICONS.star; scripts/templates/visual-book.html:459 IC.star; scripts/templates/visual-letters.html:455 IC.star</sub> |
| [sync-arrows.svg](01-navigation-menu/sync-arrows.svg) | Sign in & sync | Menu “Sign in & sync”: keep highlights and notes on every device (shown only when accounts are available).<br><sub>nav.js:20 ICON.sync</sub> |
| [timeline-streams.svg](01-navigation-menu/timeline-streams.svg) | Timeline | Menu “Timeline”: world history beside the Bible, from Creation (history.html).<br><sub>nav.js:25 ICON.time</sub> |
| [two-columns.svg](01-navigation-menu/two-columns.svg) | Parallel passages | Menu “Parallel passages”: the Gospels side by side; Kings beside Chronicles.<br><sub>nav.js:17 ICON.parallels</sub> |

## 02-reader-and-page-controls

| File | Icon | Where it goes in the app |
|---|---|---|
| [account-person.svg](02-reader-and-page-controls/account-person.svg) | Account | “Sign in to sync across devices” in the reader’s bar and in the site menu’s header.<br><sub>index.html:935; nav.js:225</sub> |
| [arrow-left.svg](02-reader-and-page-controls/arrow-left.svg) | Back | “Back” in the Connections and word-map panels of the reader; “Back to the plates” in the atlas; “All the Bible maps” on each map page, and the back button of map panels. (Drawn at stroke-width 2, 2.2 in different places.)<br><sub>index.html:1234,1244; scripts/templates/atlas.html:100; scripts/templates/map.html:261,893</sub> |
| [book-open-read.svg](02-reader-and-page-controls/book-open-read.svg) | Read | The “Read” action in the cards of Connections, Genealogy and Timeline (opens the passage in the reader).<br><sub>scripts/templates/genealogy.html:570; scripts/templates/graph.html:912; scripts/templates/history.html:941</sub> |
| [chevron-down.svg](02-reader-and-page-controls/chevron-down.svg) | Chevron down | After the book-and-chapter name in the reader’s bar: “Choose a book and chapter”.<br><sub>index.html:929</sub> |
| [chevron-left-tall.svg](02-reader-and-page-controls/chevron-left-tall.svg) | Back to the list | “Back to the list” in Topics & dictionary and Parallel passages; “Earlier” on the timeline (stroke 2.2). (Drawn at stroke-width 2, 2.2 in different places.)<br><sub>index.html:1058,1079; scripts/templates/history.html:344</sub> |
| [chevron-left.svg](02-reader-and-page-controls/chevron-left.svg) | Chevron left | “Previous plate” in the atlas (2.2); the margin tab “Notes in the margin” at the right edge of the reader (stroke 3). (Drawn at stroke-width 2.2, 3 in different places.)<br><sub>index.html:4752 ink-tab “Notes in the margin”; scripts/templates/atlas.html:102</sub> |
| [chevron-right-tall.svg](02-reader-and-page-controls/chevron-right-tall.svg) | Later | “Later” step button on the timeline (stroke 2.2).<br><sub>scripts/templates/history.html:349</sub> |
| [chevron-right.svg](02-reader-and-page-controls/chevron-right.svg) | Chevron right | `CHEV` on each book row of the chapter picker (2.4); `TUCK` button that tucks a card aside in Connections, Genealogy and Timeline (2); “Next plate” in the atlas (2.2); the margin tab “Notes in the margin” at the left edge of the reader (stroke 3). (Drawn at stroke-width 2, 2.2, 2.4, 3 in different places.)<br><sub>index.html:4752 ink-tab “Notes in the margin”; index.html:2885; scripts/templates/atlas.html:103; scripts/templates/genealogy.html:551; scripts/templates/graph.html:895; scripts/templates/history.html:922</sub> |
| [clock-recent.svg](02-reader-and-page-controls/clock-recent.svg) | Recent | Before each recently read chapter in the chapter picker.<br><sub>index.html:2925</sub> |
| [close-x.svg](02-reader-and-page-controls/close-x.svg) | Close | Close button of every sheet and panel (reader, Connections, Genealogy, Timeline, Maps, web3d “Leave AR”); also “Stop listening” in the audio bar (stroke 2.2). (Drawn at stroke-width 2, 2.2, 2.4 in different places.)<br><sub>index.html:962,1026,1032,1048,1060,1081…; scripts/templates/genealogy.html:345,357,573; scripts/templates/graph.html:258,943; scripts/templates/history.html:381,389,944; scripts/templates/map.html:288,297,311,318,887; scripts/templates/web3d.html:131</sub> |
| [envelope-contact.svg](02-reader-and-page-controls/envelope-contact.svg) | Contact | “Contact” in the welcome dialog; “Send feedback” in About this project.<br><sub>index.html:1283,1299</sub> |
| [fit-corners.svg](02-reader-and-page-controls/fit-corners.svg) | Fit to view | “Show everything / everyone / the whole sheet / All of history / Whole plate / See it all”: fit the whole picture on screen.<br><sub>scripts/templates/atlas.html:111; scripts/templates/genealogy.html:338; scripts/templates/graph.html:252; scripts/templates/history.html:369; scripts/templates/map.html:283; scripts/templates/web3d.html:112</sub> |
| [headphones-listen.svg](02-reader-and-page-controls/headphones-listen.svg) | Listen | Listen / read aloud: the reading-plan bar, the verse panel (“listen-verse”) and the auto-scroll bar (“Listen: read aloud from here”).<br><sub>index.html:944,969,1371</sub> |
| [heart-donate.svg](02-reader-and-page-controls/heart-donate.svg) | Donate | “Donate” in the welcome dialog.<br><sub>index.html:1284</sub> |
| [info-circle.svg](02-reader-and-page-controls/info-circle.svg) | About | “About this chart / view / map” on Genealogy, Connections, Timeline and the maps.<br><sub>scripts/templates/genealogy.html:314; scripts/templates/graph.html:239; scripts/templates/history.html:339; scripts/templates/map.html:272</sub> |
| [menu-hamburger.svg](02-reader-and-page-controls/menu-hamburger.svg) | Menu | Opens the site menu (reader bar, and the menu button nav.js adds to every other page).<br><sub>index.html:936; nav.js:190</sub> |
| [next-verse.svg](02-reader-and-page-controls/next-verse.svg) | Next verse | Listening bar: go to the next verse.<br><sub>index.html:1364</sub> |
| [open-full-page.svg](02-reader-and-page-controls/open-full-page.svg) | Open as a full page | Opens the reader’s Connections panel as the full graph.html page.<br><sub>index.html:1236</sub> |
| [pause.svg](02-reader-and-page-controls/pause.svg) | Pause | Auto-scroll “Stop scrolling”, and pause in the listening bar.<br><sub>index.html:1850,3741</sub> |
| [play.svg](02-reader-and-page-controls/play.svg) | Play | Auto-scroll “Scroll by itself”, and play in the listening bar.<br><sub>index.html:1851,3742</sub> |
| [previous-verse.svg](02-reader-and-page-controls/previous-verse.svg) | Previous verse | Listening bar: go to the previous verse.<br><sub>index.html:1362</sub> |
| [search.svg](02-reader-and-page-controls/search.svg) | Search | Search the Bible (reader bar), the picker’s filter field, the search fields of Genealogy, Connections and Timeline, and “Find a place” on the maps.<br><sub>index.html:933,1034; scripts/templates/genealogy.html:303; scripts/templates/graph.html:229; scripts/templates/history.html:329; scripts/templates/map.html:269</sub> |
| [share.svg](02-reader-and-page-controls/share.svg) | Share | Share a verse (verse panel), share a plate (atlas), share a card (Connections), share an item or year (Timeline).<br><sub>index.html:970; scripts/templates/atlas.html:104; scripts/templates/graph.html:911; scripts/templates/history.html:366,940</sub> |
| [text-size-aa.svg](02-reader-and-page-controls/text-size-aa.svg) | Text and display settings | Opens the Display sheet (text size, font, theme, etc.).<br><sub>index.html:934</sub> |
| [zoom-in-plus.svg](02-reader-and-page-controls/zoom-in-plus.svg) | Zoom in | Zoom in on Connections, Genealogy, Timeline, the maps and the atlas.<br><sub>scripts/templates/atlas.html:109; scripts/templates/genealogy.html:336; scripts/templates/graph.html:250; scripts/templates/history.html:367; scripts/templates/map.html:281</sub> |
| [zoom-out-minus.svg](02-reader-and-page-controls/zoom-out-minus.svg) | Zoom out | Zoom out on the same pages.<br><sub>scripts/templates/atlas.html:110; scripts/templates/genealogy.html:337; scripts/templates/graph.html:251; scripts/templates/history.html:368; scripts/templates/map.html:282</sub> |

## 03-marking-and-notes

| File | Icon | Where it goes in the app |
|---|---|---|
| [bookmark.svg](03-marking-and-notes/bookmark.svg) | Bookmark | Same file as in 03-marking-and-notes/. “Bookmark” in the marking menu (`ICON_BM`); menu “Bookmarks” (the passages you bookmarked). (Drawn at stroke-width 1.8, 2 in different places.)<br><sub>nav.js:14 ICON.bookmarks; index.html:4917</sub> |
| [copy.svg](03-marking-and-notes/copy.svg) | Copy | “Copy the selected words” in the marking menu (`ICON_COPY`).<br><sub>index.html:4918</sub> |
| [note-mark-verse.svg](03-marking-and-notes/note-mark-verse.svg) | Verse note mark | CSS `.has-note::after`: shown after a verse that carries the reader’s own verse note.<br><sub>index.html:264 CSS .has-note::after</sub> |
| [picker-sign-bookmarked.svg](03-marking-and-notes/picker-sign-bookmarked.svg) | Bookmarked (picker sign) | Chapter picker: tiny sign (12 px, stroke 2.6) on a chapter that has a bookmark.<br><sub>index.html:2931 PK_MARK.bm</sub> |
| [picker-sign-highlights.svg](03-marking-and-notes/picker-sign-highlights.svg) | Highlights (picker sign) | Chapter picker: the chapter has highlights.<br><sub>index.html:2933 PK_MARK.hl</sub> |
| [picker-sign-notes.svg](03-marking-and-notes/picker-sign-notes.svg) | Notes (picker sign) | Chapter picker: the chapter has notes.<br><sub>index.html:2932 PK_MARK.note</sub> |
| [picker-sign-sketches.svg](03-marking-and-notes/picker-sign-sketches.svg) | Sketches (picker sign) | Chapter picker: the chapter has sketches.<br><sub>index.html:2934 PK_MARK.draw</sub> |
| [sketch-mark-pencil.svg](03-marking-and-notes/sketch-mark-pencil.svg) | Sketch mark | `PENCIL_SVG`: the mark placed in the text where a sketch is attached to words (aria-label “Sketch”).<br><sub>index.html:4195</sub> |
| [sticky-note.svg](03-marking-and-notes/sticky-note.svg) | Note (sticky note) | “Note on these words” in the marking menu (`ICON_STICKY`). The same shape (`STICKY_SVG(color)`, lines at 70% opacity) marks a note in the text, colored in the note’s highlight color (yellow, green, blue, pink, orange, purple, red, teal, gray).<br><sub>index.html:4196 STICKY_SVG(color); index.html:4927</sub> |

## 04-emoji-marks

| File | Icon | Where it goes in the app |
|---|---|---|
| [emoji-anchor-hope.svg](04-emoji-marks/emoji-anchor-hope.svg) | Hope | Emoji mark “Hope” (was ⚓).<br><sub>index.html:4992 EMOJI_ICONS.anchor</sub> |
| [emoji-bread.svg](04-emoji-marks/emoji-bread.svg) | Bread | Emoji mark “Bread” (was 🍞).<br><sub>index.html:4983 EMOJI_ICONS.bread</sub> |
| [emoji-cross.svg](04-emoji-marks/emoji-cross.svg) | Cross | Emoji mark “Cross” (was ✝️).<br><sub>index.html:4973 EMOJI_ICONS.cross</sub> |
| [emoji-dove-spirit.svg](04-emoji-marks/emoji-dove-spirit.svg) | Spirit | Emoji mark “Spirit” (was 🕊️).<br><sub>index.html:4974 EMOJI_ICONS.dove</sub> |
| [emoji-exclamation-important.svg](04-emoji-marks/emoji-exclamation-important.svg) | Important | Emoji mark “Important” (was ❗).<br><sub>index.html:4979 EMOJI_ICONS.alert</sub> |
| [emoji-fire.svg](04-emoji-marks/emoji-fire.svg) | Fire | Emoji mark “Fire” (was 🔥).<br><sub>index.html:4980 EMOJI_ICONS.fire</sub> |
| [emoji-heart-love.svg](04-emoji-marks/emoji-heart-love.svg) | Love | Emoji mark “Love” (was ❤️); also the heart on the “Support” button of About this project, and “Its word above all” in the Visual Bible. (Drawn at stroke-width 1.9, 2, 2.2 in different places.)<br><sub>index.html:4971 EMOJI_ICONS.heart; scripts/templates/visual-book.html:399 ICONS.heart; scripts/templates/visual-letters.html:391 ICONS.heart; index.html:1306</sub> |
| [emoji-lightbulb-insight.svg](04-emoji-marks/emoji-lightbulb-insight.svg) | Insight | Emoji mark “Insight” (was 💡).<br><sub>index.html:4976 EMOJI_ICONS.light</sub> |
| [emoji-music-notes-song.svg](04-emoji-marks/emoji-music-notes-song.svg) | Song | Emoji mark “Song” (was 🎵).<br><sub>index.html:4994 EMOJI_ICONS.song</sub> |
| [emoji-praying-hands-prayer.svg](04-emoji-marks/emoji-praying-hands-prayer.svg) | Prayer | Emoji mark “Prayer” (was 🙏).<br><sub>index.html:4972 EMOJI_ICONS.pray</sub> |
| [emoji-question-mark.svg](04-emoji-marks/emoji-question-mark.svg) | Question | Emoji mark “Question” (was ❓).<br><sub>index.html:4978 EMOJI_ICONS.question</sub> |
| [emoji-raised-hands-praise.svg](04-emoji-marks/emoji-raised-hands-praise.svg) | Praise | Emoji mark “Praise” (was 🙌).<br><sub>index.html:4989 EMOJI_ICONS.praise</sub> |
| [emoji-sad-face-sorrow.svg](04-emoji-marks/emoji-sad-face-sorrow.svg) | Sorrow | Emoji mark “Sorrow” (was 😢).<br><sub>index.html:4988 EMOJI_ICONS.sorrow</sub> |
| [emoji-sheep.svg](04-emoji-marks/emoji-sheep.svg) | Sheep | Emoji mark “Sheep” (was 🐑).<br><sub>index.html:4984 EMOJI_ICONS.sheep</sub> |
| [emoji-shield-protection.svg](04-emoji-marks/emoji-shield-protection.svg) | Protection | Emoji mark “Protection” (was 🛡️).<br><sub>index.html:4991 EMOJI_ICONS.shield</sub> |
| [emoji-smiling-face-joy.svg](04-emoji-marks/emoji-smiling-face-joy.svg) | Joy | Emoji mark “Joy” (was 😊); also the sample shown on the “emoji” style button of the marking menu.<br><sub>index.html:4987 EMOJI_ICONS.joy</sub> |
| [emoji-sparkles-glory.svg](04-emoji-marks/emoji-sparkles-glory.svg) | Glory | Emoji mark “Glory” (was ✨).<br><sub>index.html:4986 EMOJI_ICONS.glory</sub> |
| [emoji-sprout-growth.svg](04-emoji-marks/emoji-sprout-growth.svg) | Growth | Emoji mark “Growth” (was 🌱); also the “Spring” color theme. (Drawn at stroke-width 1.8, 1.9 in different places.)<br><sub>index.html:4981 EMOJI_ICONS.sprout; index.html:3194 SEASON_INFO.spring</sub> |
| [emoji-sunrise-morning.svg](04-emoji-marks/emoji-sunrise-morning.svg) | Morning | Emoji mark “Morning” (was 🌅).<br><sub>index.html:4993 EMOJI_ICONS.morning</sub> |
| [emoji-warning-triangle.svg](04-emoji-marks/emoji-warning-triangle.svg) | Warning | Emoji mark “Warning” (was ⚠️).<br><sub>index.html:4990 EMOJI_ICONS.warn</sub> |
| [emoji-water-drop.svg](04-emoji-marks/emoji-water-drop.svg) | Water | Emoji mark “Water” (was 💧).<br><sub>index.html:4982 EMOJI_ICONS.water</sub> |

## 05-sketch-tools

| File | Icon | Where it goes in the app |
|---|---|---|
| [eraser.svg](05-sketch-tools/eraser.svg) | Eraser | Sketch toolbar “Eraser”.<br><sub>sketch.js:262</sub> |
| [margin-left.svg](05-sketch-tools/margin-left.svg) | Left margin | “Left margin” in the drawing bar on narrow screens: slides the page aside to draw in the left margin.<br><sub>index.html:4784</sub> |
| [margin-right.svg](05-sketch-tools/margin-right.svg) | Right margin | “Right margin”: slides the page aside to draw in the right margin.<br><sub>index.html:4785</sub> |
| [pencil.svg](05-sketch-tools/pencil.svg) | Pen | Same file as in 05-sketch-tools/. Sketch toolbar “Pen”; “Sketch for these words” in the marking menu (`ICON_PENCIL`; `ICON_NOTE` is the same drawing but is not used); “Written by” in the Visual Bible card.<br><sub>scripts/templates/visual-book.html:455 IC.pen; scripts/templates/visual-letters.html:451 IC.pen; index.html:4916,4928; sketch.js:261</sub> |
| [redo.svg](05-sketch-tools/redo.svg) | Redo | Sketch toolbar “Redo”.<br><sub>sketch.js:264</sub> |
| [trash-clear.svg](05-sketch-tools/trash-clear.svg) | Clear the page | Sketch toolbar “Clear the page”.<br><sub>sketch.js:265</sub> |
| [undo.svg](05-sketch-tools/undo.svg) | Undo | Sketch toolbar “Undo”.<br><sub>sketch.js:263</sub> |

## 06-bible-sections

| File | Icon | Where it goes in the app |
|---|---|---|
| [cross-gospels-2459c4.svg](06-bible-sections/colored/cross-gospels-2459c4.svg) | The Gospels (color) | Colored copy for convenience; in the app the color comes from CSS (`--c1`/`--c2` in the picker, `WEB_GROUPS` in the web).<br><sub></sub> |
| [crown-bf5a1f.svg](06-bible-sections/colored/crown-bf5a1f.svg) | History (color) | Colored copy for convenience; in the app the color comes from CSS (`--c1`/`--c2` in the picker, `WEB_GROUPS` in the web).<br><sub></sub> |
| [envelope-letter-6d43c9.svg](06-bible-sections/colored/envelope-letter-6d43c9.svg) | The Letters (color) | Colored copy for convenience; in the app the color comes from CSS (`--c1`/`--c2` in the picker, `WEB_GROUPS` in the web).<br><sub></sub> |
| [flame-0f8c83.svg](06-bible-sections/colored/flame-0f8c83.svg) | Acts (color) | Colored copy for convenience; in the app the color comes from CSS (`--c1`/`--c2` in the picker, `WEB_GROUPS` in the web).<br><sub></sub> |
| [loudspeaker-c43434.svg](06-bible-sections/colored/loudspeaker-c43434.svg) | The Prophets (color) | Colored copy for convenience; in the app the color comes from CSS (`--c1`/`--c2` in the picker, `WEB_GROUPS` in the web).<br><sub></sub> |
| [oil-lamp-on-stand-2f8a3c.svg](06-bible-sections/colored/oil-lamp-on-stand-2f8a3c.svg) | Poetry and Wisdom (color) | Colored copy for convenience; in the app the color comes from CSS (`--c1`/`--c2` in the picker, `WEB_GROUPS` in the web).<br><sub></sub> |
| [star-five-point-c23a7c.svg](06-bible-sections/colored/star-five-point-c23a7c.svg) | Revelation (color) | Colored copy for convenience; in the app the color comes from CSS (`--c1`/`--c2` in the picker, `WEB_GROUPS` in the web).<br><sub></sub> |
| [tablets-of-the-law-a8790a.svg](06-bible-sections/colored/tablets-of-the-law-a8790a.svg) | The Law (color) | Colored copy for convenience; in the app the color comes from CSS (`--c1`/`--c2` in the picker, `WEB_GROUPS` in the web).<br><sub></sub> |
| [cross-gospels.svg](06-bible-sections/cross-gospels.svg) | The Gospels | Book group “The Gospels” (Matthew–John; share.js `gospels`). Colors: #2459c4 (light mode) / #6fb0ff (dark mode)<br><sub>share.js:150 ICONS.gospels</sub> |
| [crown.svg](06-bible-sections/crown.svg) | Crown | Same file as in 06-bible-sections/. Book group “History” (share.js `ICONS.history`: picker, shelf, web); menu “Kings” (the kings of Israel and Judah); emoji mark “King”; the timeline’s default icon for dynasties, kingdoms and reigns. Colors: #bf5a1f (light mode) / #f59a62 (dark mode) · Timeline “crown”: items named crowned, coronat; items named dynasty, empire, kingdom, tsardom, duchy, raj, rule, komnenos, palaiologos, kingdoms; From Creation: “The kingdom divides”; default for reigns and unmatched items; kings and queens among Lives in the Bible (Drawn at stroke-width 1.8, 1.9, 2 in different places.)<br><sub>nav.js:30 ICON.kings; share.js:147 ICONS.history; index.html:4975 EMOJI_ICONS.crown; scripts/templates/history.html:475 GLYPH.crown</sub> |
| [envelope-letter.svg](06-bible-sections/envelope-letter.svg) | The Letters | Book group “The Letters” (Romans–Jude; share.js `letters`). Colors: #6d43c9 (light mode) / #b996ff (dark mode)<br><sub>share.js:152 ICONS.letters</sub> |
| [flame.svg](06-bible-sections/flame.svg) | Acts | Book group “Acts” (share.js `acts`: the fire of Pentecost); also the timeline’s “fire” icon (fires, destructions). Colors: #0f8c83 (light mode) / #4fd6cb (dark mode) · Timeline “fire”: items named fire, destruction, burn<br><sub>share.js:151 ICONS.acts; scripts/templates/history.html:491 GLYPH.fire</sub> |
| [loudspeaker.svg](06-bible-sections/loudspeaker.svg) | The Prophets | Book group “The Prophets” (Isaiah–Malachi; share.js `prophets`). Colors: #c43434 (light mode) / #ff7272 (dark mode)<br><sub>share.js:149 ICONS.prophets</sub> |
| [oil-lamp-on-stand.svg](06-bible-sections/oil-lamp-on-stand.svg) | Poetry and Wisdom | Book group “Poetry and Wisdom” (Job–Song of Songs; share.js `wisdom`). Colors: #2f8a3c (light mode) / #8fdc8a (dark mode)<br><sub>share.js:148 ICONS.wisdom</sub> |
| [star-five-point.svg](06-bible-sections/star-five-point.svg) | Revelation | Book group “Revelation” (share.js `revelation`); also the timeline’s “star5” icon (birth of Jesus, Soviet / People’s Republic, default for events). Colors: #c23a7c (light mode) / #ff86c0 (dark mode) · Timeline “star5”: items named birth of jesus; items named soviet, people's republic; default for events<br><sub>share.js:153 ICONS.revelation; scripts/templates/history.html:506 GLYPH.star5</sub> |
| [tablets-of-the-law.svg](06-bible-sections/tablets-of-the-law.svg) | The Law | Book group “The Law” (Genesis–Deuteronomy; share.js `torah`); also the timeline’s “tablets” icon (the law at Sinai; Moses and Aaron). Colors: #a8790a (light mode) / #f2c45a (dark mode) · Timeline “tablets”: lives: moses, aaron; From Creation: “The law at Sinai”<br><sub>share.js:146 ICONS.torah; scripts/templates/history.html:473 GLYPH.tablets</sub> |

## 07-connections-web

| File | Icon | Where it goes in the app |
|---|---|---|
| [camera.svg](07-connections-web/camera.svg) | Look through the camera | Web in 3D AR menu: look through the camera.<br><sub>scripts/templates/web3d.html:126</sub> |
| [event-burst-a87400.svg](07-connections-web/colored/event-burst-a87400.svg) | Events (color) | Colored copy for convenience; in the app the color comes from CSS (`--c1`/`--c2` in the picker, `WEB_GROUPS` in the web).<br><sub></sub> |
| [person-6b7385.svg](07-connections-web/colored/person-6b7385.svg) | People (color) | Colored copy for convenience; in the app the color comes from CSS (`--c1`/`--c2` in the picker, `WEB_GROUPS` in the web).<br><sub></sub> |
| [place-pin-3c8a6c.svg](07-connections-web/colored/place-pin-3c8a6c.svg) | Places (color) | Colored copy for convenience; in the app the color comes from CSS (`--c1`/`--c2` in the picker, `WEB_GROUPS` in the web).<br><sub></sub> |
| [cube-in-frame-ar.svg](07-connections-web/cube-in-frame-ar.svg) | See it in your room (AR) | Web in 3D: augmented-reality button (shown when AR is available).<br><sub>scripts/templates/web3d.html:114</sub> |
| [cube-on-floor.svg](07-connections-web/cube-on-floor.svg) | Place it in your room | Web in 3D AR menu: place the web in your room.<br><sub>scripts/templates/web3d.html:125</sub> |
| [event-burst.svg](07-connections-web/event-burst.svg) | Event | Web point type “Events” (share.js `event`). Colors: #a87400 (light mode) / #ffd27a (dark mode)<br><sub>share.js:156 ICONS.event</sub> |
| [help-question-circle.svg](07-connections-web/help-question-circle.svg) | How to move around | Web in 3D: help on moving around.<br><sub>scripts/templates/web3d.html:113</sub> |
| [person.svg](07-connections-web/person.svg) | Person | Web point type “People” (share.js `person`): a person in the Connections web (graph.html, reader panel, 3D web). Colors: #6b7385 (light mode) / #97a3c4 (dark mode)<br><sub>share.js:154 ICONS.person</sub> |
| [place-pin.svg](07-connections-web/place-pin.svg) | Place | Web point type “Places” (share.js `place`). Colors: #3c8a6c (light mode) / #7fd6b4 (dark mode)<br><sub>share.js:155 ICONS.place</sub> |
| [rotate-spin.svg](07-connections-web/rotate-spin.svg) | Turn slowly | Web in 3D: turn the web slowly (toggle).<br><sub>scripts/templates/web3d.html:110</sub> |
| [two-arches-threads.svg](07-connections-web/two-arches-threads.svg) | Only the cross-references | Web in 3D: show only the cross-reference threads (toggle).<br><sub>scripts/templates/web3d.html:111</sub> |
| [web-flat.svg](07-connections-web/web-flat.svg) | The web flat | Web in 3D: link to the flat web in Connections (graph.html).<br><sub>scripts/templates/web3d.html:115</sub> |

## 08-timeline

| File | Icon | Where it goes in the app |
|---|---|---|
| [ark-on-waves.svg](08-timeline/ark-on-waves.svg) | flood | Timeline “flood”: lives: noah; From Creation: “The Flood”<br><sub>scripts/templates/history.html:468 GLYPH.flood</sub> |
| [at-sign.svg](08-timeline/at-sign.svg) | at | Timeline “at”: items named world wide web, internet<br><sub>scripts/templates/history.html:499 GLYPH.at</sub> |
| [atom.svg](08-timeline/atom.svg) | atom | Timeline “atom”: items named atomic, bombing; lives: newton, einstein<br><sub>scripts/templates/history.html:500 GLYPH.atom</sub> |
| [brick-wall.svg](08-timeline/brick-wall.svg) | wall | Timeline “wall”: items named berlin wall<br><sub>scripts/templates/history.html:498 GLYPH.wall</sub> |
| [broken-chain.svg](08-timeline/broken-chain.svg) | chain | Timeline “chain”: items named abolition, emancipation, apartheid, slavery<br><sub>scripts/templates/history.html:509 GLYPH.chain</sub> |
| [candle.svg](08-timeline/candle.svg) | candle | Timeline “candle”: items named holocaust<br><sub>scripts/templates/history.html:517 GLYPH.candle</sub> |
| [church.svg](08-timeline/church.svg) | church | Timeline “church”: items named church, revival, awakening, reformation, apostolic, nicene, vatican, trent<br><sub>scripts/templates/history.html:519 GLYPH.church</sub> |
| [city-skyline.svg](08-timeline/city-skyline.svg) | city | Timeline “city”: items named september 11; items named founding, constantinople; items named civilization, maya, teotihuacan, harappan, zimbabwe, aksum, ur, sumer<br><sub>scripts/templates/history.html:518 GLYPH.city</sub> |
| [colonnade.svg](08-timeline/colonnade.svg) | column | Timeline “column”: items named greece, greek, hellenistic, minoan, mycenaean, roman, rome, byzantine; stream “Greece”; stream “Rome”; stream “Roman officials”; stream “Byzantine Empire”; reigns/lives in “Roman officials”<br><sub>scripts/templates/history.html:481 GLYPH.column</sub> |
| [crescent.svg](08-timeline/crescent.svg) | crescent | Timeline “crescent”: items named hijrah, islam, caliphate, sultanate, ottoman, mamluk, ayyubid, fatimid, abbasid, umayyad, rashidun, mughal, delhi; lives: muhammad, avicenna, ibn khaldun; stream “Islamic world”<br><sub>scripts/templates/history.html:489 GLYPH.crescent</sub> |
| [cross-timeline.svg](08-timeline/cross-timeline.svg) | cross | Timeline “cross”: items named crucifixion, crucified; lives: luther, calvin, wesley, bonhoeffer, ignatius, justin, irenaeus, tertullian, origen, eusebius, athanasius, augustine, bede, aquinas; lives: jesus; stream “Church”<br><sub>scripts/templates/history.html:483 GLYPH.cross</sub> |
| [crossed-swords.svg](08-timeline/crossed-swords.svg) | swords | Timeline “swords”: items named battle, war, wars, revolt, rebellion, siege, invade, crusade, takes jerusalem, sack of, warring, conquest<br><sub>scripts/templates/history.html:490 GLYPH.swords</sub> |
| [dove-timeline.svg](08-timeline/dove-timeline.svg) | dove | Timeline “dove”: items named united nations, peace of, human rights; lives: gandhi, king jr<br><sub>scripts/templates/history.html:493 GLYPH.dove</sub> |
| [flag.svg](08-timeline/flag.svg) | flag | Timeline “flag”: items named independence, revolution, restoration, united states, republic<br><sub>scripts/templates/history.html:508 GLYPH.flag</sub> |
| [flame-candle-style.svg](08-timeline/flame-candle-style.svg) | flame | Timeline “flame”: stream “High priests”; reigns/lives in “High priests”<br><sub>scripts/templates/history.html:486 GLYPH.flame</sub> |
| [gear.svg](08-timeline/gear.svg) | gear | Timeline “gear”: items named industrial<br><sub>scripts/templates/history.html:512 GLYPH.gear</sub> |
| [globe.svg](08-timeline/globe.svg) | globe | Timeline “globe”: stream “World”; stream “World events”<br><sub>scripts/templates/history.html:488 GLYPH.globe</sub> |
| [harp-timeline.svg](08-timeline/harp-timeline.svg) | harp | Timeline “harp”: lives: david<br><sub>scripts/templates/history.html:520 GLYPH.harp</sub> |
| [hourglass.svg](08-timeline/hourglass.svg) | hourglass | Timeline “hourglass”: items named period, age, ages, era, middle ages<br><sub>scripts/templates/history.html:511 GLYPH.hourglass</sub> |
| [house.svg](08-timeline/house.svg) | home | Timeline “home”: From Creation: “Cyrus lets the exiles return”<br><sub>scripts/templates/history.html:477 GLYPH.home</sub> |
| [leaf.svg](08-timeline/leaf.svg) | leaf | Timeline “leaf”: items named origin of species; lives: darwin<br><sub>scripts/templates/history.html:501 GLYPH.leaf</sub> |
| [legend-approximate.svg](08-timeline/legend-approximate.svg) | Legend: Approximate dates | Timeline legend swatch “Approximate dates”.<br><sub>scripts/templates/history.html:360</sub> |
| [legend-dynasty.svg](08-timeline/legend-dynasty.svg) | Legend: Dynasty or movement | Timeline legend swatch “Dynasty or movement”.<br><sub>scripts/templates/history.html:357</sub> |
| [legend-era.svg](08-timeline/legend-era.svg) | Legend: Era | Timeline legend swatch “Era”. Color var(--faint) → #8d95a4.<br><sub>scripts/templates/history.html:356</sub> |
| [legend-event.svg](08-timeline/legend-event.svg) | Legend: Event | Timeline legend swatch “Event, with its icon”.<br><sub>scripts/templates/history.html:359</sub> |
| [legend-reign.svg](08-timeline/legend-reign.svg) | Legend: Reign or life | Timeline legend swatch “Reign or life”.<br><sub>scripts/templates/history.html:358</sub> |
| [lightbulb.svg](08-timeline/lightbulb.svg) | bulb | Timeline “bulb”: items named enlightenment<br><sub>scripts/templates/history.html:514 GLYPH.bulb</sub> |
| [list-chronicle.svg](08-timeline/list-chronicle.svg) | Chronicle | Timeline: “Chronicle of the years shown” (list view).<br><sub>scripts/templates/history.html:338</sub> |
| [menorah.svg](08-timeline/menorah.svg) | lamp | Timeline “lamp”: lives: rashi, maimonides, philo, josephus; stream “Jewish history”<br><sub>scripts/templates/history.html:485 GLYPH.lamp</sub> |
| [music-notes.svg](08-timeline/music-notes.svg) | music | Timeline “music”: lives: bach<br><sub>scripts/templates/history.html:502 GLYPH.music</sub> |
| [open-external.svg](08-timeline/open-external.svg) | Link | Timeline card action `link` (open the item’s page).<br><sub>scripts/templates/history.html:943</sub> |
| [paintbrush.svg](08-timeline/paintbrush.svg) | brush | Timeline “brush”: items named renaissance<br><sub>scripts/templates/history.html:513 GLYPH.brush</sub> |
| [parted-sea.svg](08-timeline/parted-sea.svg) | waves | Timeline “waves”: From Creation: “The Exodus”<br><sub>scripts/templates/history.html:472 GLYPH.waves</sub> |
| [people.svg](08-timeline/people.svg) | people | Timeline “people”: items named council, congress, synod<br><sub>scripts/templates/history.html:510 GLYPH.people</sub> |
| [person-timeline.svg](08-timeline/person-timeline.svg) | person | Timeline “person”: stream “Lives in the Bible”; default for lives<br><sub>scripts/templates/history.html:478 GLYPH.person</sub> |
| [pyramid.svg](08-timeline/pyramid.svg) | pyramid | Timeline “pyramid”: items named pyramid; lives: joseph; stream “Egypt”; From Creation: “Jacob's family goes down to Egypt”<br><sub>scripts/templates/history.html:471 GLYPH.pyramid</sub> |
| [quill-timeline.svg](08-timeline/quill-timeline.svg) | quill | Timeline “quill”: stream “Thinkers and writers”; reigns/lives in “Thinkers and writers”<br><sub>scripts/templates/history.html:487 GLYPH.quill</sub> |
| [rocket.svg](08-timeline/rocket.svg) | rocket | Timeline “rocket”: items named apollo, space<br><sub>scripts/templates/history.html:497 GLYPH.rocket</sub> |
| [ruin.svg](08-timeline/ruin.svg) | ruin | Timeline “ruin”: items named fall of, falls, dissolution, collapse, crisis; items named schism; From Creation: “Samaria falls”; From Creation: “Jerusalem falls”<br><sub>scripts/templates/history.html:476 GLYPH.ruin</sub> |
| [sailing-ship.svg](08-timeline/sailing-ship.svg) | ship | Timeline “ship”: items named voyage, columbus; stream “Tyre”; stream “Carthage”<br><sub>scripts/templates/history.html:482 GLYPH.ship</sub> |
| [scales.svg](08-timeline/scales.svg) | scales | Timeline “scales”: items named code of, magna carta, edict, decree, act, proclamation, theses, stele<br><sub>scripts/templates/history.html:492 GLYPH.scales</sub> |
| [scroll-timeline.svg](08-timeline/scroll-timeline.svg) | scroll | Timeline “scroll”: items named talmud, mishnah, papyrus, codex, hexapla, diatessaron, festal letter, textus, masoret, scrolls, tannaim, amoraim, geonim; stream “Bible transmission”<br><sub>scripts/templates/history.html:484 GLYPH.scroll</sub> |
| [shield-with-cross.svg](08-timeline/shield-with-cross.svg) | shield | Timeline “shield”: (no rule names it directly)<br><sub>scripts/templates/history.html:515 GLYPH.shield</sub> |
| [snowflake-timeline.svg](08-timeline/snowflake-timeline.svg) | snowflake | Timeline “snowflake”: items named cold war<br><sub>scripts/templates/history.html:516 GLYPH.snowflake</sub> |
| [span-arrows.svg](08-timeline/span-arrows.svg) | Span | Timeline card action `span` (zoom to the item’s span of years).<br><sub>scripts/templates/history.html:942</sub> |
| [star-of-david.svg](08-timeline/star-of-david.svg) | star6 | Timeline “star6”: items named zion, state of israel, israeli<br><sub>scripts/templates/history.html:505 GLYPH.star6</sub> |
| [stepped-tower.svg](08-timeline/stepped-tower.svg) | tower | Timeline “tower”: From Creation: “The tower of Babel”<br><sub>scripts/templates/history.html:469 GLYPH.tower</sub> |
| [sun-creation.svg](08-timeline/sun-creation.svg) | creation | Timeline “creation”: stream “From Creation”; From Creation: “Creation”<br><sub>scripts/templates/history.html:466 GLYPH.creation</sub> |
| [sunrise.svg](08-timeline/sunrise.svg) | sunrise | Timeline “sunrise”: items named resurrection<br><sub>scripts/templates/history.html:507 GLYPH.sunrise</sub> |
| [telescope.svg](08-timeline/telescope.svg) | telescope | Timeline “telescope”: lives: galileo<br><sub>scripts/templates/history.html:504 GLYPH.telescope</sub> |
| [temple.svg](08-timeline/temple.svg) | temple | Timeline “temple”: items named temple, dome of the rock; From Creation: “Solomon begins the temple”<br><sub>scripts/templates/history.html:474 GLYPH.temple</sub> |
| [tent.svg](08-timeline/tent.svg) | tent | Timeline “tent”: lives: abraham, sarah, isaac, israel, jacob; From Creation: “The call of Abram”<br><sub>scripts/templates/history.html:470 GLYPH.tent</sub> |
| [theatre-mask.svg](08-timeline/theatre-mask.svg) | mask | Timeline “mask”: lives: shakespeare<br><sub>scripts/templates/history.html:503 GLYPH.mask</sub> |
| [torch.svg](08-timeline/torch.svg) | torch | Timeline “torch”: items named olympic<br><sub>scripts/templates/history.html:494 GLYPH.torch</sub> |
| [tree-garden.svg](08-timeline/tree-garden.svg) | garden | Timeline “garden”: lives: adam, eve; From Creation: “The garden of Eden”<br><sub>scripts/templates/history.html:467 GLYPH.garden</sub> |
| [virus.svg](08-timeline/virus.svg) | virus | Timeline “virus”: items named black death, pandemic, plague, covid<br><sub>scripts/templates/history.html:496 GLYPH.virus</sub> |
| [volcano.svg](08-timeline/volcano.svg) | volcano | Timeline “volcano”: items named vesuvius, eruption<br><sub>scripts/templates/history.html:495 GLYPH.volcano</sub> |
| [ziggurat.svg](08-timeline/ziggurat.svg) | ziggurat | Timeline “ziggurat”: stream “Sumer and Akkad”; stream “Babylon”<br><sub>scripts/templates/history.html:480 GLYPH.ziggurat</sub> |

## 09-genealogy

| File | Icon | Where it goes in the app |
|---|---|---|
| [family-tree-card.svg](09-genealogy/family-tree-card.svg) | Tree | Card action `tree` in Genealogy and Connections (show the person in the family tree).<br><sub>scripts/templates/genealogy.html:571; scripts/templates/graph.html:913</sub> |
| [hub-and-spokes.svg](09-genealogy/hub-and-spokes.svg) | Web | Genealogy card action `web` (show the person in the Connections web).<br><sub>scripts/templates/genealogy.html:572</sub> |
| [line-of-descent.svg](09-genealogy/line-of-descent.svg) | Browse | Genealogy: “From Adam to Jesus, and the largest families” (browse panel).<br><sub>scripts/templates/genealogy.html:313</sub> |
| [person-link.svg](09-genealogy/person-link.svg) | Person (link) | Reader verse panel: before each person named in the verse, linking to them in the genealogy.<br><sub>index.html:1922</sub> |

## 10-maps-and-atlas

| File | Icon | Where it goes in the app |
|---|---|---|
| [download.svg](10-maps-and-atlas/download.svg) | Download as SVG | Map page: “Download as SVG”.<br><sub>scripts/templates/map.html:274</sub> |
| [layers.svg](10-maps-and-atlas/layers.svg) | Layers | Map page: “Layers” panel.<br><sub>scripts/templates/map.html:271</sub> |
| [map-pin.svg](10-maps-and-atlas/map-pin.svg) | Map pin | Reader verse panel: before each place in the verse, linking to it on a map sheet; card action `map` in Connections.<br><sub>index.html:1920; scripts/templates/graph.html:914</sub> |
| [open-external-atlas.svg](10-maps-and-atlas/open-external-atlas.svg) | Full-size scan | Atlas viewer: “Full-size scan at the Internet Archive”.<br><sub>scripts/templates/atlas.html:105</sub> |
| [printer.svg](10-maps-and-atlas/printer.svg) | Print | Map page: “Print”.<br><sub>scripts/templates/map.html:273</sub> |
| [route-with-stops.svg](10-maps-and-atlas/route-with-stops.svg) | Journeys and routes | Map page: “Journeys and routes” panel (shown on maps that have journeys).<br><sub>scripts/templates/map.html:270</sub> |

## 11-themes-psalms-proverbs

| File | Icon | Where it goes in the app |
|---|---|---|
| [ant.svg](11-themes-psalms-proverbs/ant.svg) | work | Proverbs topic “Work and laziness”<br><sub>themes.js:43 Themes.icons["work"]</sub> |
| [arched-door.svg](11-themes-psalms-proverbs/arched-door.svg) | entrance | Psalm group “At the gate” (Questions and answers on who may come into God's presence.)<br><sub>themes.js:27 Themes.icons["entrance"]</sub> |
| [balance-scale.svg](11-themes-psalms-proverbs/balance-scale.svg) | honesty | Proverbs topic “Honesty and lies”<br><sub>themes.js:41 Themes.icons["honesty"]</sub> |
| [broken-heart.svg](11-themes-psalms-proverbs/broken-heart.svg) | penitential | Psalm group “Penitential” (The seven psalms of sorrow for sin, long prayed together.)<br><sub>themes.js:24 Themes.icons["penitential"]</sub> |
| [broken-wall.svg](11-themes-psalms-proverbs/broken-wall.svg) | wall | Proverbs collection “More sayings of the wise”<br><sub>themes.js:63 Themes.icons["wall"]</sub> |
| [city-gate.svg](11-themes-psalms-proverbs/city-gate.svg) | zion | Psalm group “Songs of Zion” (Psalms in praise of Jerusalem, the city of God.)<br><sub>themes.js:20 Themes.icons["zion"]</sub> |
| [coins.svg](11-themes-psalms-proverbs/coins.svg) | wealth | Proverbs topic “Wealth and poverty”<br><sub>themes.js:42 Themes.icons["wealth"]</sub> |
| [crown-on-base.svg](11-themes-psalms-proverbs/crown-on-base.svg) | royal / kings | Psalm type “Royal” · Proverbs topic “Kings and rulers” · Proverbs collection “The words of King Lemuel”<br><sub>themes.js:12 Themes.icons["royal"]; themes.js:49 Themes.icons["kings"]</sub> |
| [cup.svg](11-themes-psalms-proverbs/cup.svg) | thanksgiving | Psalm type “Thanksgiving”<br><sub>themes.js:10 Themes.icons["thanksgiving"]</sub> |
| [cymbals.svg](11-themes-psalms-proverbs/cymbals.svg) | Asaph | Psalm author “Asaph”<br><sub>themes.js:32 Themes.icons["Asaph"]</sub> |
| [dashed-circle.svg](11-themes-psalms-proverbs/dashed-circle.svg) | No name | Psalms with no author named<br><sub>themes.js:38 Themes.icons["No name"]</sub> |
| [door.svg](11-themes-psalms-proverbs/door.svg) | Sons of Korah | Psalm author “Sons of Korah”<br><sub>themes.js:33 Themes.icons["Sons of Korah"]</sub> |
| [ear.svg](11-themes-psalms-proverbs/ear.svg) | ear | Proverbs collection “Sayings of the wise”<br><sub>themes.js:62 Themes.icons["ear"]</sub> |
| [flame-themes.svg](11-themes-psalms-proverbs/flame-themes.svg) | anger | Proverbs topic “Anger and self-control”<br><sub>themes.js:44 Themes.icons["anger"]</sub> |
| [gavel.svg](11-themes-psalms-proverbs/gavel.svg) | justice | Proverbs topic “Justice”<br><sub>themes.js:50 Themes.icons["justice"]</sub> |
| [heart-themes.svg](11-themes-psalms-proverbs/heart-themes.svg) | heart | Proverbs topic “The heart”<br><sub>themes.js:57 Themes.icons["heart"]</sub> |
| [house-of-pillars.svg](11-themes-psalms-proverbs/house-of-pillars.svg) | pillars | Proverbs collection “Wisdom's call”<br><sub>themes.js:60 Themes.icons["pillars"]</sub> |
| [jester-cap.svg](11-themes-psalms-proverbs/jester-cap.svg) | fools | Proverbs topic “Fools and mockers”<br><sub>themes.js:51 Themes.icons["fools"]</sub> |
| [letters-a-b.svg](11-themes-psalms-proverbs/letters-a-b.svg) | acrostic | Psalm group “Alphabet poems” (Each line or stanza begins with the next letter of the Hebrew alphabet.)<br><sub>themes.js:25 Themes.icons["acrostic"]</sub> |
| [lightning.svg](11-themes-psalms-proverbs/lightning.svg) | imprecatory | Psalm group “Calling down judgment” (Prayers that ask God to repay the wicked.)<br><sub>themes.js:26 Themes.icons["imprecatory"]</sub> |
| [lyre.svg](11-themes-psalms-proverbs/lyre.svg) | David | Psalm author “David”<br><sub>themes.js:31 Themes.icons["David"]</sub> |
| [mountains-and-sun.svg](11-themes-psalms-proverbs/mountains-and-sun.svg) | creation | Psalm group “Creation” (Psalms that praise God as maker of the world.)<br><sub>themes.js:21 Themes.icons["creation"]</sub> |
| [mountains-radiant.svg](11-themes-psalms-proverbs/mountains-radiant.svg) | lord | Proverbs topic “The LORD”<br><sub>themes.js:53 Themes.icons["lord"]</sub> |
| [music-note.svg](11-themes-psalms-proverbs/music-note.svg) | Heman | Psalm author “Heman”<br><sub>themes.js:36 Themes.icons["Heman"]</sub> |
| [music-notes-themes.svg](11-themes-psalms-proverbs/music-notes-themes.svg) | hallel | Psalm group “The Hallel” (Psalms 113–118, sung at Passover and the great feasts.)<br><sub>themes.js:17 Themes.icons["hallel"]</sub> |
| [oil-lamp.svg](11-themes-psalms-proverbs/oil-lamp.svg) | Oil lamp | Same file as in 11-themes-psalms-proverbs/. themes.js `wisdom_lamp`; also `ICON.proverbs` in nav.js (not in the menu at present). Proverbs topic “Wisdom and knowledge”<br><sub>nav.js:29 ICON.proverbs; themes.js:52 Themes.icons["wisdom_lamp"]</sub> |
| [opposing-arrows.svg](11-themes-psalms-proverbs/opposing-arrows.svg) | but | Proverbs: chip “Turns on ‘but’” (contrasting couplets)<br><sub>themes.js:58 Themes.icons["but"]</sub> |
| [parent-and-child.svg](11-themes-psalms-proverbs/parent-and-child.svg) | family | Proverbs topic “Parents and children”<br><sub>themes.js:47 Themes.icons["family"]</sub> |
| [pointed-arch-with-bars.svg](11-themes-psalms-proverbs/pointed-arch-with-bars.svg) | Ethan | Psalm author “Ethan”<br><sub>themes.js:37 Themes.icons["Ethan"]</sub> |
| [question-circle.svg](11-themes-psalms-proverbs/question-circle.svg) | question | Proverbs collection “The words of Agur”<br><sub>themes.js:65 Themes.icons["question"]</sub> |
| [quill.svg](11-themes-psalms-proverbs/quill.svg) | quill | Proverbs collection “Solomon's, copied by Hezekiah's men”<br><sub>themes.js:64 Themes.icons["quill"]</sub> |
| [radiant-burst.svg](11-themes-psalms-proverbs/radiant-burst.svg) | final-hallel | Psalm group “The last Hallel” (Psalms 146–150: each begins and ends “Praise the LORD!”)<br><sub>themes.js:18 Themes.icons["final-hallel"]</sub> |
| [rings.svg](11-themes-psalms-proverbs/rings.svg) | marriage | Proverbs topic “Marriage and faithfulness”<br><sub>themes.js:48 Themes.icons["marriage"]</sub> |
| [scroll.svg](11-themes-psalms-proverbs/scroll.svg) | history / scroll | Psalm type “History” · Proverbs collection “The proverbs of Solomon”<br><sub>themes.js:14 Themes.icons["history"]; themes.js:61 Themes.icons["scroll"]</sub> |
| [seedling.svg](11-themes-psalms-proverbs/seedling.svg) | life | Proverbs topic “Life and death”<br><sub>themes.js:56 Themes.icons["life"]</sub> |
| [shepherds-staff.svg](11-themes-psalms-proverbs/shepherds-staff.svg) | Moses | Psalm group “#bf5a1f” (#f59a62) · Psalm author “Moses”<br><sub>themes.js:35 Themes.icons["Moses"]</sub> |
| [shield-check-themes.svg](11-themes-psalms-proverbs/shield-check-themes.svg) | trust | Psalm type “Trust”<br><sub>themes.js:11 Themes.icons["trust"]</sub> |
| [speech-bubble-exclamation.svg](11-themes-psalms-proverbs/speech-bubble-exclamation.svg) | prophetic | Psalm group “God speaks” (Psalms in which God himself speaks in judgment.)<br><sub>themes.js:28 Themes.icons["prophetic"]</sub> |
| [speech-bubble.svg](11-themes-psalms-proverbs/speech-bubble.svg) | speech | Proverbs topic “Words and the tongue”<br><sub>themes.js:40 Themes.icons["speech"]</sub> |
| [spindle.svg](11-themes-psalms-proverbs/spindle.svg) | spindle | Proverbs collection “The capable wife”<br><sub>themes.js:66 Themes.icons["spindle"]</sub> |
| [stairs-up.svg](11-themes-psalms-proverbs/stairs-up.svg) | ascents | Psalm group “Songs of Ascents” (Sung, it seems, by pilgrims going up to Jerusalem for the feasts (120–134).)<br><sub>themes.js:16 Themes.icons["ascents"]</sub> |
| [star-themes.svg](11-themes-psalms-proverbs/star-themes.svg) | messianic | Psalm group “Of the Messiah” (Psalms the New Testament or long tradition reads of the Messiah.)<br><sub>themes.js:23 Themes.icons["messianic"]</sub> |
| [sun.svg](11-themes-psalms-proverbs/sun.svg) | praise | Psalm type “Praise”<br><sub>themes.js:9 Themes.icons["praise"]</sub> |
| [tablets-themes.svg](11-themes-psalms-proverbs/tablets-themes.svg) | torah | Psalm group “God's law” (Psalms in praise of the law of the LORD.)<br><sub>themes.js:22 Themes.icons["torah"]</sub> |
| [teardrop.svg](11-themes-psalms-proverbs/teardrop.svg) | lament | Psalm type “Lament”<br><sub>themes.js:8 Themes.icons["lament"]</sub> |
| [temple-themes.svg](11-themes-psalms-proverbs/temple-themes.svg) | Solomon | Psalm author “Solomon”<br><sub>themes.js:34 Themes.icons["Solomon"]</sub> |
| [throne.svg](11-themes-psalms-proverbs/throne.svg) | kingship | Psalm group “The LORD reigns” (Psalms that hail the LORD as king of all the earth.)<br><sub>themes.js:19 Themes.icons["kingship"]</sub> |
| [tower-cracked.svg](11-themes-psalms-proverbs/tower-cracked.svg) | pride | Proverbs topic “Pride and humility”<br><sub>themes.js:45 Themes.icons["pride"]</sub> |
| [tree.svg](11-themes-psalms-proverbs/tree.svg) | wisdom | Psalm type “Wisdom”<br><sub>themes.js:13 Themes.icons["wisdom"]</sub> |
| [two-arches.svg](11-themes-psalms-proverbs/two-arches.svg) | story | Psalm group “A moment in David's life” (The heading names a moment in David's life, told in Samuel.)<br><sub>themes.js:29 Themes.icons["story"]</sub> |
| [two-people.svg](11-themes-psalms-proverbs/two-people.svg) | friends | Proverbs topic “Friends and neighbors”<br><sub>themes.js:46 Themes.icons["friends"]</sub> |
| [two-ways.svg](11-themes-psalms-proverbs/two-ways.svg) | righteous | Proverbs topic “The righteous and the wicked”<br><sub>themes.js:54 Themes.icons["righteous"]</sub> |
| [wine-glass.svg](11-themes-psalms-proverbs/wine-glass.svg) | drink | Proverbs topic “Food and drink”<br><sub>themes.js:55 Themes.icons["drink"]</sub> |

## 12-visual-bible

| File | Icon | Where it goes in the app |
|---|---|---|
| [balance-scale-letters.svg](12-visual-bible/balance-scale-letters.svg) | Sets side by side | At a glance (letters): “Sets side by side” (contrasting pairs).<br><sub>scripts/templates/visual-letters.html:396 ICONS.scale</sub> |
| [bar-chart.svg](12-visual-bible/bar-chart.svg) | Visual | `VIS_ICON`: the “Visual” link on every chapter heading in the reader (this book in the Visual Bible).<br><sub>index.html:1595</sub> |
| [calendar.svg](12-visual-bible/calendar.svg) | When | “About the book” card: “When”.<br><sub>scripts/templates/visual-book.html:456 IC.cal; scripts/templates/visual-letters.html:452 IC.cal</sub> |
| [chain-link.svg](12-visual-bible/chain-link.svg) | Linked book | At a glance: “Most tied to {book}” / “Closest in wording to {book}”.<br><sub>scripts/templates/visual-book.html:406 ICONS.link; scripts/templates/visual-letters.html:398 ICONS.link</sub> |
| [flag-start.svg](12-visual-bible/flag-start.svg) | Beginning / end | At a glance (books): “How it begins”, “How it ends”.<br><sub>scripts/templates/visual-book.html:407 ICONS.start</sub> |
| [oil-lamp-no-handle.svg](12-visual-bible/oil-lamp-no-handle.svg) | By topic | Reader chapter heading in Proverbs: link “By topic” (every proverb, by topic) to proverbs.html.<br><sub>index.html:1619 guide() chapter-head link “By topic”</sub> |
| [people-visual.svg](12-visual-bible/people-visual.svg) | People | At a glance: “Who is in it most” / “Who is in it”; in letters also “What it calls its readers”.<br><sub>scripts/templates/visual-book.html:403 ICONS.people; scripts/templates/visual-letters.html:395 ICONS.people</sub> |
| [place-pin-visual.svg](12-visual-bible/place-pin-visual.svg) | Places | At a glance (books): “Where it happens most”.<br><sub>scripts/templates/visual-book.html:404 ICONS.pin</sub> |
| [quotation-marks.svg](12-visual-bible/quotation-marks.svg) | Why it was written | At a glance: “Why it was written, in its own words”.<br><sub>scripts/templates/visual-book.html:401 ICONS.quote; scripts/templates/visual-letters.html:393 ICONS.quote</sub> |
| [repeat-arrows.svg](12-visual-bible/repeat-arrows.svg) | Patterns | At a glance: “Ways of speaking it repeats”.<br><sub>scripts/templates/visual-book.html:405 ICONS.repeat; scripts/templates/visual-letters.html:397 ICONS.repeat</sub> |
| [speech-bubble-voice.svg](12-visual-bible/speech-bubble-voice.svg) | Voice | At a glance: who it speaks as (“Told mostly as …”, “It speaks most as …”).<br><sub>scripts/templates/visual-book.html:402 ICONS.voice; scripts/templates/visual-letters.html:394 ICONS.voice</sub> |
| [text-lines.svg](12-visual-bible/text-lines.svg) | Its next words | At a glance: “Its next words” (the book’s next most frequent words).<br><sub>scripts/templates/visual-book.html:400 ICONS.words; scripts/templates/visual-letters.html:392 ICONS.words</sub> |

## 13-color-themes

| File | Icon | Where it goes in the app |
|---|---|---|
| [season-autumn-leaf.svg](13-color-themes/season-autumn-leaf.svg) | Autumn | Color theme “Autumn” (harvest and turning leaves).<br><sub>index.html:3196 SEASON_INFO.autumn</sub> |
| [season-summer-sun.svg](13-color-themes/season-summer-sun.svg) | Summer | Color theme “Summer” (clear sky and sun).<br><sub>index.html:3195 SEASON_INFO.summer</sub> |
| [season-winter-snowflake.svg](13-color-themes/season-winter-snowflake.svg) | Winter | Color theme “Winter” (snow and evening light).<br><sub>index.html:3197 SEASON_INFO.winter</sub> |
