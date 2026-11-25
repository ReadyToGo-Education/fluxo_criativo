# Image Sourcing Deep Reference

Expanded recipes for the 5-tier image sourcing protocol. Read this when you need concrete code for a specific image scenario.

## Why This Matters

LLMs generating HTML often write URLs like:
```
https://images.unsplash.com/photo-1552664730-d307ca884978?w=800
```
This is the model *guessing* that a photo with that ID exists at that URL. In practice, ~30-50% of these IDs either 404, show an unrelated photo, or have been removed. The result is broken designs shipped to users.

This skill's protocol eliminates that by routing every image through a deterministic, testable source.

## Tier 1 — Inline SVG / CSS (Preferred Whenever Possible)

Use this tier whenever the element is:
- An icon, logo, or glyph
- A geometric shape (blob, arch, wave, spiral)
- A pattern (stripes, dots, grid)
- A gradient or atmospheric background
- A sparkle, star, arrow, or decorative mark

### Recipe: 4-point star sparkle
```html
<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
  <path d="M12 0 L14 10 L24 12 L14 14 L12 24 L10 14 L0 12 L10 10 Z"/>
</svg>
```

### Recipe: Organic blob
```html
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <path d="M160,85 C175,115 155,160 115,170 C75,180 35,150 30,110 C25,70 60,30 105,35 C150,40 145,55 160,85 Z"
        fill="var(--accent)"/>
</svg>
```

### Recipe: Mesh gradient background
```css
.hero-bg {
  background:
    radial-gradient(at 20% 30%, hsla(220, 80%, 60%, 0.4), transparent 50%),
    radial-gradient(at 80% 20%, hsla(340, 80%, 65%, 0.35), transparent 55%),
    radial-gradient(at 50% 80%, hsla(180, 70%, 55%, 0.3), transparent 60%),
    linear-gradient(135deg, #1a1a2e, #16213e);
}
```

### Recipe: Diagonal stripe pattern
```css
.stripes {
  background-image: repeating-linear-gradient(
    -45deg,
    transparent 0,
    transparent 14px,
    rgba(255,255,255,0.04) 14px,
    rgba(255,255,255,0.04) 16px
  );
}
```

### Recipe: Dot grid pattern
```css
.dot-grid {
  background-image: radial-gradient(circle, rgba(255,255,255,0.15) 1px, transparent 1px);
  background-size: 24px 24px;
}
```

### Recipe: Noise texture (SVG filter)
```html
<svg style="position: fixed; inset: 0; width: 100%; height: 100%; opacity: 0.04; pointer-events: none;">
  <filter id="noise">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2"/>
    <feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.5 0"/>
  </filter>
  <rect width="100%" height="100%" filter="url(#noise)"/>
</svg>
```

### When NOT to use Tier 1
If the element is clearly a **photograph of something in the real world** (a person, a cup of coffee, a landscape), don't try to SVG it. Use Tier 2 or 3.

## Tier 2 — Picsum with Seed (Default for Generic Photos)

`https://picsum.photos/` is a free placeholder service that always returns a real photo at the requested dimensions. It has no subject-matter guarantees, but it works 100% of the time.

### Base URL structure
```
https://picsum.photos/{width}/{height}
```

### Stable, reproducible images
**Always use a seed** so the same slot shows the same photo every reload:
```
https://picsum.photos/seed/{anything}/{width}/{height}
```

Example seeds that work well for design reviews:
- `team-01`, `team-02`, `team-03`
- `office-alpha`, `office-beta`
- `hero-autumn`, `hero-winter`
- Any short consistent keyword + number suffix

### Modifiers
- **Grayscale**: append `?grayscale`
- **Blur**: append `?blur={1-10}`
- **Combine**: `?grayscale&blur=2`

### Full example
```html
<img src="https://picsum.photos/seed/team-01/800/500?grayscale"
     width="800" height="500"
     alt="Team collaborating at a desk"
     loading="lazy" decoding="async" />
```

### When to use Tier 2
- Filler photos in a marketing grid where exact subject doesn't matter
- Hero backgrounds where the image is heavily overlaid with gradients/text
- "Three random team moments" carousel
- Any slot where "a nice-looking photo" is enough

### When NOT to use Tier 2
- When you specifically need "people in an office meeting" and getting a landscape photo would break the design → use Tier 3
- When the content-critical subject must be shown → use Tier 4

## Tier 3 — Unsplash Keyword API (Controlled Subject Matter)

`source.unsplash.com` returns a photo matching keyword(s) at request time. This is the safe way to use Unsplash — the model doesn't have to guess a specific photo ID.

### URL structure
```
https://source.unsplash.com/{width}x{height}/?{keyword1},{keyword2}
```

### For stable/deterministic results
Append `&sig={any_number}` to get the same photo on reload:
```
https://source.unsplash.com/800x500/?office,team&sig=42
```

### Good keyword combinations
| Need | Keywords |
|---|---|
| Business team | `office,team,meeting` |
| Tech workspace | `laptop,desk,workspace` |
| Food blog hero | `food,restaurant,cooking` |
| Fashion/portrait | `portrait,model,fashion` |
| Nature/travel | `landscape,travel,mountain` |
| Product mockup | `product,minimal,studio` |
| Coffee shop | `cafe,coffee,interior` |

### Full example
```html
<img src="https://source.unsplash.com/800x500/?office,team&sig=42"
     width="800" height="500"
     alt="Professional team in a modern office"
     loading="lazy" decoding="async" />
```

### Known limitation
`source.unsplash.com` is sometimes slow or rate-limited. For demos that need to be rock-solid, Tier 2 (Picsum) is more reliable.

## Tier 4 — Labeled Placeholder (For Content-Critical Slots)

When the image slot will *definitely* be replaced with a real client asset, use `placehold.co` with a descriptive label. This makes the placeholder self-documenting.

### URL structure
```
https://placehold.co/{width}x{height}/{bg-hex}/{fg-hex}?text={url-encoded-label}
```

### Full example
```html
<img src="https://placehold.co/600x900/0F2A1D/B8F135?text=Hero+Product+Shot"
     width="600" height="900"
     alt="Hero product photograph (placeholder)"
     loading="lazy" />
```

### Style options
- `&font=roboto` — change font (options: `roboto`, `montserrat`, `lato`, `playfair-display`, `raleway`, etc.)
- Transparent bg: use `transparent` or `000000` with low alpha

### When to use Tier 4
- Hero product shots that the client will supply
- CEO photos, team portraits that need specific people
- Logos, brand marks
- Any slot where "placeholder that screams REPLACE ME" is the right signal

## Tier 5 — Data-URI SVG (Offline-Safe)

For demos that must work **without internet**, inline an SVG directly as the image source.

### Inline approach (recommended)
```html
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg"
     role="img" aria-label="Team photo placeholder">
  <rect width="100%" height="100%" fill="#0F2A1D"/>
  <text x="50%" y="50%" fill="#B8F135" text-anchor="middle"
        dominant-baseline="central" font-family="sans-serif" font-size="32" font-weight="600">
    Team Photo · 800×500
  </text>
</svg>
```

### Data-URI approach (for `<img src>`)
```html
<img src="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 500'><rect width='100%25' height='100%25' fill='%230F2A1D'/><text x='50%25' y='50%25' fill='%23B8F135' text-anchor='middle' font-family='sans-serif' font-size='32'>Team Photo</text></svg>"
     width="800" height="500" alt="Team photo placeholder" />
```

Note: `%23` is URL-encoded `#`, and `%25` is URL-encoded `%`.

### When to use Tier 5
- Offline demos, airgapped environments
- Email templates where external images may be blocked
- Fallback `onerror` handlers: `<img onerror="this.src='data:image/svg+xml,...'"`

## Choosing Between Tiers — Quick Decision Tree

1. **Is it a shape, icon, or pattern?** → Tier 1 (SVG/CSS)
2. **Is it a photo where any nice image works?** → Tier 2 (Picsum with seed)
3. **Is it a photo where the subject matters?** → Tier 3 (Unsplash keyword)
4. **Will the viewer replace this with a real asset?** → Tier 4 (Labeled placeholder)
5. **Must this work offline?** → Tier 5 (Data-URI SVG)

## The Banned Pattern

```
❌ https://images.unsplash.com/photo-{anyNumericId}
```

This is the pattern the model is tempted to write from memory. It is **banned** in this skill's output for one simple reason: the model cannot verify the ID exists, and guessing wrong causes broken images.

If you find yourself about to write this pattern, stop and re-route through Tier 2 or Tier 3 instead.

## Required Image Attributes

Every `<img>` must have:
- `src` — pointing to a tiered source
- `width` and `height` — explicit pixel values (prevents layout shift)
- `alt` — meaningful description (or `alt=""` + `aria-hidden="true"` if purely decorative)
- `loading="lazy"` — unless above the fold
- `decoding="async"` — always safe

And inside a container with `aspect-ratio` + `object-fit: cover` for predictable cropping.
