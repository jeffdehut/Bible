# Story Board artwork: how to prepare the SVGs

The Story Board (`storyboard.html`) uses only our own artwork. Users can't upload art. Send the
files and they will be added to the drawers. Until then the board uses the placeholder pieces
in `storyboard-art.js`.

## The board

- The board is **1600 × 1000** units (16:10). A standing adult is drawn about **260 units
  tall**, so people, animals and things should be drawn to that scale. Each piece can be
  resized on the board, but its starting size comes from its drawing.
- Scenes (backgrounds) fill the whole 1600 × 1000 board.

## Each piece

- **One SVG file per piece**, with a `viewBox` that fits the drawing closely (little empty
  margin). Example: `viewBox="0 0 120 260"` for a person.
- **Flat shapes with solid fills** (`<path>`, `<circle>`, `<ellipse>`, `<rect>`,
  `<polygon>`). The board adds the felt edges, texture and shadow itself, so the art itself
  needs none of them.
- **Avoid:** embedded images (PNG/JPG inside the SVG), text, fonts, filters, masks, gradients
  that carry meaning, and scripts. Clipping paths are fine.
- **Separate shapes for separate parts** (robe, sleeve, sash, face, beard). Each shape becomes
  an outlined area in the colouring-page version, so the way the art is cut into shapes is the
  way the colouring page divides up.
- Lines drawn as **strokes** (a staff, a rope) print as a single thin line on the colouring
  page. Where that should be a shape to colour in, draw it as a filled shape.
- Faces: keep eyes and mouths as small separate shapes so they show on the colouring page.

## Optional: your own line art

The colouring page is made automatically by outlining every shape. If a piece needs a better
colouring version, send a second file named `<name>.line.svg` with the same `viewBox`: black
strokes on white (or no) fills. It replaces the automatic version for that piece.

## Naming and folders

Put files in one folder per drawer, named in lowercase with hyphens:

```
storyboard/art/people/moses.svg
storyboard/art/people/moses.line.svg      (optional)
storyboard/art/animals/donkey.svg
storyboard/art/things/ark.svg
storyboard/art/nature/palm-tree.svg
storyboard/art/scenes/desert.svg
```

Give each piece a `<title>` with the name shown in the drawer (`<title>Moses</title>`); the
Chinese name can follow as `<desc lang="zh-Hant">摩西</desc>`. Pieces that should start smaller
or larger than their drawing (a child, a giant) can say so with `data-scale="0.7"` on the
`<svg>` element.

## Licence

The artwork should be ours to publish (made for us, or licensed so we can redistribute it on
the site and in printed colouring pages). Keep a note of who made each set.
