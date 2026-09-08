---
name: ui-reverse-engineer
description: Reverse-engineer a UI screenshot or design mockup into a production-ready single-file HTML artifact with design tokens, component architecture, pixel-accurate line breaks, intentional "artistic chaos" preserved, and bulletproof image sourcing. Use this skill whenever the user uploads a UI design, screenshot, Figma export, Dribbble shot, or mockup image and asks to "rebuild", "clone", "recreate", "reproduce", "code this", "convert to HTML", "turn this design into code", or "reverse engineer" it — even if they don't explicitly mention HTML, Tailwind, or design tokens. Also trigger when the user asks for a "design analysis", "design breakdown", "design spec", or "component spec" of an uploaded UI image.
---

# UI Reverse Engineer

Convert a UI reference image into a production-grade single-file HTML artifact, following a disciplined Senior-Design-Engineer workflow: analyze semantics → extract tokens → spec components → produce code that is faithful to the original *including its intentional imperfections*.

## When to use this skill

Activate whenever there is a UI reference image (screenshot, mockup, Dribbble shot, Figma export) and the user wants code from it. Phrases that should trigger: "rebuild this", "code this design", "reverse engineer", "reproduce as HTML", "turn this into code", "design breakdown", "extract the design system". Activate even if the user doesn't explicitly mention HTML, Tailwind, or tokens — if they uploaded a design and want something that resembles it, this skill applies.

## Workflow (5 phases, always in this order)

### Phase 1 — Analyze Intent & Semantics

Before touching code, state:
- **Context**: What interface category is this? (Hero, B2B SaaS, marketing section, dashboard, etc.)
- **Mental Model**: A one-sentence conceptual description (e.g., *"Layered surfaces on dark canvas with a single chromatic focal point"*).
- **Core Action**: The primary user behavior this view drives (click-through, read-to-absorb, form-fill, etc.).

This phase forces conscious design thinking before reflexive copying.

### Phase 2 — Typography & Line Control (CRITICAL)

Typography fidelity is the #1 differentiator between a convincing reproduction and an obvious AI clone.

For every heading:
- **Count lines exactly** in the reference image
- **Note exact break points** (e.g., Line 1 = *"Boost Your Brand"*, Line 2 = *"with Our Expertise"*)
- **Use `<br>` tags** to enforce these breaks — do not rely on natural wrapping
- **Check for widows/orphans** and preserve them if intentional

Build a typographic scale table with role, size, weight, line-height (leading), and letter-spacing (tracking) for every text role. Match the *density* of the reference image — tight headlines at `line-height: 1.05` look very different from loose ones at `1.3`.

### Phase 3 — Design Tokens (JSON)

Extract a normalized design system. See **references/design-tokens.md** for the full JSON schema and naming conventions.

Token categories to always extract:
- **Colors** mapped to functional roles (`surface-primary`, `text-vibrant`, `brand-accent`, `on-accent`, etc.) — never raw hex names
- **Spacing scale** derived from a base unit (usually 4px or 8px)
- **Radius tokens** (`sm`, `md`, `lg`, `full`)
- **Typography scale** (family, sizes, weights, line-heights, tracking)
- **Z-index layers** if the design has overlapping elements
- **Motion tokens** (durations, easing) inferred from interaction cues

### Phase 4 — Component Architecture & Artistic Chaos

For every unique element, write a component spec with:
- **Anatomy**: sub-elements (Button = Label + Icon + Surface)
- **Variants**: props driving visual change (size, color, state, emphasis)
- **Aspect-ratio control** for image containers
- **Constraints**: fixed vs. flexible dimensions

**Artistic Chaos** is the critical step most AI clones fail at. Scan the reference for:
- Elements that intentionally break the grid (floating badges, partial overlaps)
- Decorative graphics (sparkles, arabesques, dots, squiggles) that bleed off frames
- Asymmetric photo collages, rotated stamps, negative-margin offsets

**Preserve these exactly.** Do not align them to the grid. Use `position: absolute`, `transform: translate()`, `negative margins`, or `z-index` to replicate their exact depth and offset. If in doubt, see **references/artistic-chaos.md** for patterns.

### Phase 5 — Production Code (Single-File HTML)

Generate the final artifact as ONE self-contained HTML file:
- Semantic HTML5 structure
- Tailwind CSS via CDN (`<script src="https://cdn.tailwindcss.com"></script>`)
- Custom `<style>` block for shapes, animations, absolute positioning, `@font-face`
- Headings use the exact `<br>` breaks identified in Phase 2
- Artistic chaos elements positioned precisely per Phase 4
- Full accessibility: ARIA labels, semantic roles, alt text, focus states
- All images sourced per the **Image Sourcing Protocol** (below) — **never** hardcoded Unsplash photo IDs

## Image Sourcing Protocol (MANDATORY — prevents broken-link failures)

LLMs frequently hallucinate Unsplash photo IDs from memory, causing 30–50% broken images. This skill eliminates that failure mode with a deterministic hierarchy.

**Classify every image slot first:**
- **A. Content-Critical** — must depict a specific subject (hero product photo, team portraits)
- **B. Contextual** — evokes a category, exact subject flexible (office photos in a grid)
- **C. Decorative** — texture, shape, abstract filler

**Then apply this tier hierarchy in order:**

| Priority | Source | Use For |
|---|---|---|
| **Tier 1** | Inline SVG / CSS gradients | Icons, blobs, sparkles, arrows, patterns, shapes — anything recreatable in ≤60 lines of SVG |
| **Tier 2** | Picsum with seed | Contextual photos: `https://picsum.photos/seed/{keyword}/{w}/{h}` — always works, deterministic |
| **Tier 3** | Unsplash keyword API | Subject-matter-controlled photos: `https://source.unsplash.com/{w}x{h}/?keyword1,keyword2` |
| **Tier 4** | Labeled placeholder | Content-critical slots to be replaced: `https://placehold.co/{w}x{h}/{bg}/{fg}?text=Label` |
| **Tier 5** | Data-URI SVG | Offline demos — inline SVG with labeled rect |

**BANNED pattern** (causes broken links):
```
❌ https://images.unsplash.com/photo-1552664730-d307ca884978?w=800
```
This relies on hallucinated photo IDs from training data. Never use it.

**Correct patterns:**
```
✅ https://picsum.photos/seed/team-office/800/500?grayscale
✅ https://source.unsplash.com/800x500/?office,team&sig=42
✅ https://placehold.co/800x500/0F2A1D/B8F135?text=Team+Photo
```

**Image filters**: Always match the treatment in the reference (e.g., `filter: grayscale(100%) contrast(1.02)` if photos are monochrome).

For deeper guidance on choosing between tiers and writing inline SVG for common decorative elements, see **references/image-sourcing.md**.

## Required Output Structure

Produce the response in this exact order:

### Part 1 — Design Tokens (JSON)
Clean JSON block with colors, spacing, radius, typography, z-index, motion.

### Part 2 — Component & Typography Manifest
- Table of headings with line counts and exact break points
- Map of artistic-chaos elements with their positioning strategy (which CSS property, what offset)
- Component specs (anatomy + variants) for every unique element

### Part 3 — Image Manifest (mandatory)
Every `<img>` in the HTML must have a row here. Format:

| Slot | Role (A/B/C) | Tier | Source |
|---|---|---|---|
| Hero background | C (Decorative) | 1 (CSS) | `repeating-linear-gradient(-45deg, ...)` |
| Service card 1 photo | B (Contextual) | 2 (Picsum) | `https://picsum.photos/seed/team-01/800/500?grayscale` |
| Sparkle decoration | C (Decorative) | 1 (SVG) | Inline 4-point star SVG |

This manifest prevents unconscious Unsplash-ID guessing and gives the user a replacement checklist.

### Part 4 — Production Code
Complete `<!DOCTYPE html>` document in a single code block. Every `<img>` src matches a Manifest row.

### Part 5 — Design Engineering Insights
Brief explanation of *why* the design works — focal lines, visual hierarchy logic, color-as-hierarchy tricks, structural-inversion moves. This teaches the user the reasoning, not just the output.

## Hard Rules (non-negotiable)

1. **Single file only** — all CSS, HTML, JS in one `<!DOCTYPE html>` block. Only external dependency allowed: Tailwind CDN.
2. **Line-break fidelity** — headings must have the exact line count and break points from the reference.
3. **No grid correction** — if something is misaligned in the source, keep it misaligned.
4. **No hallucinated image IDs** — `images.unsplash.com/photo-{id}` is BANNED. Use the tier hierarchy only.
5. **Image Manifest is mandatory** — every `<img>` must have a matching row.
6. **No summaries, no skipped elements** — small details (dots, sparkles, icons, dividers) must all be reproduced.
7. **Modern CSS** — use Grid, Flexbox, `aspect-ratio`, logical properties, `clamp()` for fluid type.
8. **Accessibility is not optional** — ARIA labels, semantic HTML, meaningful alt text, focus states.

## Reference Files

Read these as needed — they are not loaded by default:

- **references/design-tokens.md** — Full JSON schema for design tokens, naming conventions, and examples for common palette types (dark-canvas, light-canvas, glassmorphism, brutalist)
- **references/artistic-chaos.md** — Patterns for implementing overlaps, sparkles, rotated stamps, frame-breaking elements, with CSS/SVG code recipes
- **references/image-sourcing.md** — Expanded tier hierarchy with concrete recipes for common scenarios (team photos, hero backgrounds, decorative SVGs, icon sets)
- **references/output-template.md** — A skeleton of the full Part 1 → Part 5 output structure to copy and fill in
