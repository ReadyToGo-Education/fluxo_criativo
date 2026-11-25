# Artistic Chaos Patterns

The single biggest tell that separates a convincing UI reproduction from an obvious AI clone is **how the imperfections are handled**. Perfect grids, centered everything, and aligned-to-baseline elements feel templated. Real designs breathe with intentional offsets, overlaps, and frame-breaks.

This file catalogs the common "chaos" patterns and how to implement them precisely.

## The Detection Checklist

Scan the reference image for these signals:

- Does any element **cross the boundary** of its container (negative margins, bleed)?
- Is there a **floating decoration** (sparkle, star, dot, arrow) that isn't aligned to the text grid?
- Are there **rotated elements** (stamps, badges, stickers at 3°, 8°, -12°)?
- Is one card in a grid **structurally different** from its siblings (inverted layout, different aspect)?
- Are there **overlapping layers** (text over image, badge over card corner)?
- Is spacing **deliberately uneven** between similar elements?
- Are photos **cropped asymmetrically** (one tall, one wide in the same row)?

If any answer is yes, it's artistic chaos — preserve it, don't fix it.

## Pattern 1: Frame-Breaking Sparkles/Stars

Small decorations positioned partially outside their container, usually with a twinkle animation.

```html
<div class="photo-tile" style="position: relative; overflow: visible;">
  <img src="..." alt="..." />
  <svg class="sparkle sparkle--lg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
    <path d="M12 0 L14 10 L24 12 L14 14 L12 24 L10 14 L0 12 L10 10 Z"/>
  </svg>
</div>
```

```css
.sparkle {
  position: absolute;
  color: var(--accent);
  pointer-events: none;
  animation: twinkle 3s ease-in-out infinite;
}
.sparkle--lg {
  width: 48px;
  height: 48px;
  left: -14px;       /* negative = bleeds past container edge */
  bottom: 52px;
}
@keyframes twinkle {
  0%, 100% { opacity: 0.55; transform: scale(0.92) rotate(0deg); }
  50%      { opacity: 1;    transform: scale(1)    rotate(6deg); }
}
```

**Critical**: the parent needs `overflow: visible`, and the decoration needs a negative offset to actually break the frame. Don't just place it at `left: 0`.

## Pattern 2: Rotated Stamp / Badge

Think of a "Sale!" badge tilted 8°, a price tag at -12°, a "New" sticker askew.

```html
<div class="badge" role="img" aria-label="New product">
  New
</div>
```

```css
.badge {
  position: absolute;
  top: 16px;
  right: -12px;              /* negative = hangs off the corner */
  padding: 8px 20px;
  background: var(--accent);
  color: var(--on-accent);
  font-weight: 700;
  border-radius: 9999px;
  transform: rotate(8deg);    /* the tilt */
  box-shadow: 0 4px 12px rgba(0,0,0,0.12);
  z-index: 2;
}
```

## Pattern 3: Structural Inversion Inside a Grid

One card in a row has its internal layout flipped relative to siblings. This is the trick used in the "Our Services" reference — two cards show image-then-text, the middle card shows text-then-image.

Implementation: use `display: flex; flex-direction: column;` on all cards, and simply swap the order of child blocks in the HTML for the inverted card. No CSS trickery needed — the inversion lives in the DOM.

```html
<!-- Default cards -->
<article class="card">
  <div class="image">...</div>
  <div class="content">...</div>
</article>

<!-- Inverted card -->
<article class="card card--accent">
  <div class="content">...</div>  <!-- content first -->
  <div class="image">...</div>    <!-- image second -->
</article>
```

## Pattern 4: Asymmetric Photo Collage

Photos of different aspect ratios in the same grid, creating an L-shape or T-shape rather than a uniform 2×2.

```css
.collage {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto auto;
  gap: 16px;
}
.tile--tall {
  grid-column: 1;
  grid-row: 1 / span 2;   /* spans both rows */
  aspect-ratio: 3 / 5;
}
.tile--wide {
  grid-column: 2;
  grid-row: 1;
  aspect-ratio: 4 / 3;
}
.tile--shape {
  grid-column: 2;
  grid-row: 2;
  /* decorative blob instead of a photo */
}
```

## Pattern 5: Custom Organic Shapes (Blobs, Arches)

Organic lime/accent shapes that aren't circles or squircles. Two approaches:

**Approach A — asymmetric border-radius** (works for arches, tombstones):
```css
.blob-arch {
  background: var(--accent);
  /* rounded top, squared bottom corners */
  border-radius: 100% 100% 20px 20px / 55% 55% 20px 20px;
  aspect-ratio: 4 / 3;
}
```

**Approach B — inline SVG with path** (works for true blobs, custom shapes):
```html
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <path d="M100,20 C160,20 180,80 160,140 C140,180 60,180 40,140 C20,80 40,20 100,20 Z"
        fill="var(--accent)"/>
</svg>
```

## Pattern 6: Overlapping Cards/Layers

Cards that overlap each other, usually with rotation and varying z-index.

```html
<div class="stack">
  <div class="card" style="--rotation: -4deg;  --z: 1; --offset: 0;">...</div>
  <div class="card" style="--rotation: 2deg;   --z: 2; --offset: -20px;">...</div>
  <div class="card" style="--rotation: -1deg;  --z: 3; --offset: -40px;">...</div>
</div>
```

```css
.stack .card {
  transform: rotate(var(--rotation));
  margin-top: var(--offset);
  z-index: var(--z);
  transition: transform 300ms var(--ease);
}
.stack .card:hover {
  transform: rotate(0deg) translateY(-8px);
  z-index: 10;
}
```

## Pattern 7: Decorative Line Work (Squiggles, Arrows, Arabesques)

Hand-drawn looking strokes that add character. Always inline SVG, never images.

**Squiggle**:
```html
<svg viewBox="0 0 100 140" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M 50 10 Q 20 25, 50 40 Q 80 55, 50 70 Q 20 85, 50 100 Q 80 115, 50 130"
        stroke="var(--forest-deep)" stroke-width="5" stroke-linecap="round" fill="none"/>
</svg>
```

**Curved arrow**:
```html
<svg viewBox="0 0 200 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M 10 50 Q 80 10, 180 50" stroke="currentColor" stroke-width="3" fill="none"/>
  <path d="M 160 35 L 180 50 L 160 65" stroke="currentColor" stroke-width="3" fill="none"/>
</svg>
```

## Pattern 8: Diagonal Stripe Bands

Texture bands at the edges of a section (not full-canvas). Used to signal "premium packaging" or "ticket-stub" edges.

```css
.stripe-band {
  position: absolute;
  left: 0;
  right: 0;
  height: 72px;
  background-image: repeating-linear-gradient(
    -45deg,
    transparent 0,
    transparent 14px,
    rgba(255,255,255,0.035) 14px,
    rgba(255,255,255,0.035) 16px
  );
  pointer-events: none;
}
.stripe-band--top { top: 0; }
.stripe-band--bottom { bottom: 0; }
```

## Pattern 9: Offset/Floating Badges

A badge that's *not* aligned with the text baseline or the card corner — hovering with a slight offset.

```css
.floating-badge {
  position: absolute;
  top: -12px;                /* sticks up past the top */
  left: 24px;                /* indented from the left edge */
  transform: rotate(-3deg);  /* slight tilt */
  padding: 6px 14px;
  background: var(--brand-accent);
  border-radius: 9999px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.10);
}
```

## What NOT to Do

- **Don't center everything.** If the source has an off-center element, keep it off-center.
- **Don't align floaters to the text grid.** A sparkle at `left: -14px` is intentional; moving it to `left: 0` ruins the design.
- **Don't use `overflow: hidden` on containers that have bleeding decorations.** It will clip them.
- **Don't round all corners equally.** If one corner is sharp and three are rounded, use asymmetric `border-radius`.
- **Don't make the rotation random.** `rotate(3deg)` reads as intentional; `rotate(0.47deg)` reads as a bug.

## Recommended Rotation Values

Rotations that look intentional, not accidental:
- Subtle: `±2deg`, `±3deg`
- Clearly tilted: `±6deg`, `±8deg`, `±12deg`
- Playful: `±15deg`, `±20deg`

Avoid: `0.5deg`, `1deg`, `45deg` (unless obviously a rotated square shape), `90deg`.
