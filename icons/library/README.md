# BibleData · Museum Icons

A complete vector redesign for the BibleData reader and visual exploration app. The direction combines museum wayfinding, engraved historical symbols, and clear data notation: restrained lapis, warm brass, deliberate negative space, and a consistent drawing system.

## Start here

Open `index.html` in a browser. It works offline and provides search by name or function, family filters, 12–64 px previews, light/dark views, individual SVG downloads, and expandable descriptions. `contact-sheet.png` shows the entire collection at a glance.

## Contents

- **253 SVG assets** in the original 14 numbered folders, including all 11 colored variants.
- **2 app-icon PNGs**, regenerated from the new vector master at 192 × 192 and 512 × 512.
- **ICONS.md**, copied verbatim from the original project so every original name, description, use, and code reference remains available.
- **manifest.json**, a machine-readable record of every asset and its original metadata.
- Light, dark, small-size, and mobile catalog previews.
- **design-tokens.json** and **design-tokens.css** for implementation.

All 255 original asset paths are preserved. The original files in the source project are untouched; this collection is a separate deliverable. No external fonts, icon libraries, or linked images are required.

## Drawing system

Most drawings use the original 24 × 24 viewBox, with optical margins rather than a rigid bounding box. The original 20 × 20 note/pencil grids, 22 × 12 timeline swatches, and 512 × 512 brand master are retained.

Primary strokes are 1.5 units for pictorial symbols and 1.75 units for compact UI controls. Interior engraving is generally 1.15 units. Round ends and joins keep the family coherent. Low-opacity fills add quiet volume without obscuring the symbol at small sizes. Filled media controls and bookmark signs remain filled. Timeline era/dynasty/reign swatches retain distinct densities; approximation remains dashed.

The app mark retains the gold open book on lapis. Curved text lines, inset page planes, a fine frame, and a secondary page edge give it more material depth. Gradients are limited to the app mark; functional symbols use currentColor.

## Integration

Use the same relative SVG/PNG paths to replace exported image assets. These are standalone exports: they do not modify the app's JavaScript icon tables or Path2D definitions.

For external SVG images, the SVG follows the system color scheme. Default monochrome ink is `#161b26` in light mode and `#e9ecf3` in dark mode. Colored variants retain the original light colors and use their documented dark counterparts. Golden note marks also adapt. The brand icon remains lapis and gold in both schemes.

For inline SVG, set CSS `color` on the SVG element to match the app's theme. If the app manually controls themes, remove the SVG's embedded `prefers-color-scheme` style so the host app owns that decision. `stroke` and tonal fills follow currentColor. For an external `<img>`, parent CSS color cannot recolor the SVG; inline it when manual recoloring is required.

Every SVG contains its original name in `<title>` and its original function in `<desc>`. IDs are unique across the asset set. If repeating an inline icon multiple times on one page, namespace its accessibility IDs per instance, or mark it decorative with `aria-hidden="true"` when the surrounding button already supplies a label. Namespace the app mark's gradient IDs if repeating it inline.

The original `ICONS.md` describes the **source** geometry and construction. It is preserved as requested, including historical style notes. This README describes the **redesigned** geometry. The functions and descriptions in the catalog and manifest remain the originals.

Preview size is not a touch target. Use the app's existing accessible button labels and adequate interaction areas. The denser illustrated symbols read best at 20–24 px or larger; reserve the small picker signs and simple controls for 12–16 px placements.

## Verification

The collection was rendered in Chromium. Catalog search, category filtering, theme controls, mobile width, image loading, SVG drawing bounds, PNG dimensions, complete asset-path coverage, and verbatim documentation preservation were checked. Previews are included for visual review. Application integration remains a separate step because this project contains exported assets rather than the reader's application source.
