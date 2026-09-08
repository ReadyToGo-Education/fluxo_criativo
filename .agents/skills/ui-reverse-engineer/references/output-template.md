# Output Template

Copy this skeleton and fill in every section. Follow the order strictly — do not reorder or skip parts.

---

## Part 1 — Design Tokens (JSON)

```json
{
  "color": {
    "canvas": { "primary": "" },
    "surface": {},
    "text": {},
    "brand": {}
  },
  "spacing": {
    "base": 4,
    "scale": []
  },
  "radius": {},
  "typography": {
    "family": {},
    "scale": {}
  },
  "z-index": {},
  "motion": {}
}
```

---

## Part 2 — Component & Typography Manifest

### Typography

| Role | Size | Weight | Line-Height | Tracking | Usage |
|---|---|---|---|---|---|
| display-xl | | | | | H1/H2 headlines |
| heading-md | | | | | Card titles |
| body-md | | | | | Descriptions |
| label-md | | | | | Eyebrows, buttons |

### Heading Line-Break Map

| Heading | Line Count | Break Points |
|---|---|---|
| H1 | | Line 1: `...` / Line 2: `...` |
| H2 | | Line 1: `...` |

### Component Specs

For each unique component, provide:

**ComponentName**
- **Anatomy**: sub-element + sub-element + sub-element
- **Variants**: variant1, variant2
- **Constraints**: aspect ratio, fixed dimensions
- **Composition**: how it nests with others

### Artistic Chaos Map

| Element | Position Strategy | Exact Offset |
|---|---|---|
| Sparkle (lg) | `position: absolute` with negative left | `left: -14px; bottom: 52px` |
| Rotated badge | `transform: rotate(8deg)` + negative margin | `top: -12px; right: -12px` |
| Inverted card | DOM order swap | content before image |

---

## Part 3 — Image Manifest

Every `<img>` in Part 4 **must** have a matching row here. This manifest is non-negotiable.

| Slot | Role (A/B/C) | Tier | Source |
|---|---|---|---|
| Hero background pattern | C (Decorative) | 1 (CSS) | `repeating-linear-gradient(...)` |
| Service card 1 photo | B (Contextual) | 2 (Picsum) | `https://picsum.photos/seed/team-01/800/500?grayscale` |
| Service card 2 photo | B (Contextual) | 2 (Picsum) | `https://picsum.photos/seed/content-02/800/500?grayscale` |
| Decorative sparkle | C (Decorative) | 1 (SVG) | Inline 4-point star `<svg>` |
| Hero product shot | A (Content-Critical) | 4 (Placehold) | `https://placehold.co/600x900/0F2A1D/B8F135?text=Replace+with+Product` |

**Role legend**: A = Content-Critical, B = Contextual, C = Decorative
**Tier legend**: 1 = SVG/CSS, 2 = Picsum, 3 = Unsplash keyword, 4 = Labeled placeholder, 5 = Data-URI SVG

---

## Part 4 — Production Code

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>[Design Name]</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=[FontName]:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
  <style>
    :root {
      /* Paste design tokens as CSS custom properties */
      --canvas: #...;
      --accent: #...;
      --ease: cubic-bezier(0.4, 0, 0.2, 1);
    }
    * { box-sizing: border-box; }
    html, body { margin: 0; font-family: var(--font-sans); ... }

    /* Component classes */
    .display-xl { ... }
    .card { ... }
    /* etc */

    /* Artistic chaos */
    .sparkle { position: absolute; ... }

    /* Responsive */
    @media (max-width: 960px) { ... }
  </style>
</head>
<body>
  <section aria-labelledby="main-heading">
    <!-- Use exact line breaks per Part 2 -->
    <h1 id="main-heading" class="display-xl">
      Line One Of Heading<br />
      Line Two Of Heading
    </h1>

    <!-- Every <img> matches a row in Part 3 -->
    <img src="https://picsum.photos/seed/team-01/800/500?grayscale"
         width="800" height="500"
         alt="Descriptive alt"
         loading="lazy" decoding="async" />
  </section>
</body>
</html>
```

---

## Part 5 — Design Engineering Insights

Write 4-7 short paragraphs explaining *why* the design works. Focus on:

1. **The focal hierarchy** — what the viewer's eye hits first, second, third, and why
2. **Color-as-hierarchy moves** — is there a single chromatic anchor? Why?
3. **Structural techniques** — inversions, asymmetry, grid-breaking moves and their rhetorical purpose
4. **System discipline** — reused components across sections signaling design-system maturity
5. **Restraint choices** — what the designer *didn't* do (no CTA here, no shadow here, no extra color here)
6. **Cross-section rhythm** — how this section relates to what comes before/after on the page

Avoid generic design-school clichés. Write like a senior design engineer explaining an aesthetic decision to a junior on the team.

---

## Post-Output Self-Check

Before sending the response, verify:

- [ ] Every `<img>` src appears in the Image Manifest
- [ ] No URL of the form `images.unsplash.com/photo-{id}` anywhere
- [ ] Every heading has the exact line count from the reference
- [ ] Artistic chaos elements are not grid-aligned
- [ ] Tokens are defined as CSS custom properties in `:root`
- [ ] ARIA labels and semantic HTML5 are present
- [ ] The HTML is a single, complete `<!DOCTYPE html>` document
- [ ] Tailwind CDN is the only external dependency
- [ ] Fonts are loaded with `preconnect` + `&display=swap`
- [ ] Every `<img>` has `width`, `height`, `alt`, `loading`, `decoding`
