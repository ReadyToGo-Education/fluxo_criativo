# Design Tokens Reference

Canonical schema and naming conventions for the Design Tokens JSON emitted in Part 1 of every response.

## Full JSON Schema

```json
{
  "color": {
    "canvas": {
      "primary":   "#HEX",
      "secondary": "#HEX",
      "inverse":   "#HEX"
    },
    "surface": {
      "card":           "#HEX or rgba(...)",
      "card-elevated":  "#HEX or rgba(...)",
      "card-accent":    "#HEX",
      "overlay":        "rgba(...)"
    },
    "border": {
      "subtle":  "rgba(...)",
      "default": "rgba(...)",
      "strong":  "rgba(...)",
      "accent":  "#HEX"
    },
    "text": {
      "on-canvas-primary":   "#HEX",
      "on-canvas-secondary": "rgba(...)",
      "on-canvas-muted":     "rgba(...)",
      "on-accent-primary":   "#HEX",
      "on-accent-muted":     "rgba(...)",
      "link":                "#HEX"
    },
    "brand": {
      "primary":   "#HEX",
      "secondary": "#HEX",
      "accent":    "#HEX"
    },
    "semantic": {
      "success": "#HEX",
      "warning": "#HEX",
      "error":   "#HEX",
      "info":    "#HEX"
    }
  },
  "spacing": {
    "base": 4,
    "scale": [4, 8, 12, 16, 20, 24, 32, 40, 48, 56, 64, 80, 96, 128]
  },
  "radius": {
    "none":   "0",
    "xs":     "4px",
    "sm":     "8px",
    "md":     "12px",
    "lg":     "16px",
    "xl":     "24px",
    "2xl":    "32px",
    "full":   "9999px"
  },
  "typography": {
    "family": {
      "sans":    "'Font Name', system-ui, sans-serif",
      "serif":   "'Font Name', Georgia, serif",
      "mono":    "'Font Name', ui-monospace, monospace",
      "display": "'Font Name', sans-serif"
    },
    "scale": {
      "display-2xl": { "size": "72px", "weight": 800, "lh": 1.02, "ls": "-0.03em" },
      "display-xl":  { "size": "56px", "weight": 800, "lh": 1.05, "ls": "-0.025em" },
      "display-lg":  { "size": "40px", "weight": 700, "lh": 1.1,  "ls": "-0.02em" },
      "heading-lg":  { "size": "32px", "weight": 700, "lh": 1.2,  "ls": "-0.015em" },
      "heading-md":  { "size": "24px", "weight": 700, "lh": 1.3,  "ls": "-0.01em" },
      "heading-sm":  { "size": "18px", "weight": 700, "lh": 1.35 },
      "body-lg":     { "size": "18px", "weight": 400, "lh": 1.6 },
      "body-md":     { "size": "15px", "weight": 400, "lh": 1.55 },
      "body-sm":     { "size": "14px", "weight": 400, "lh": 1.5 },
      "label-md":    { "size": "16px", "weight": 600 },
      "label-sm":    { "size": "13px", "weight": 600, "ls": "0.02em" },
      "caption":     { "size": "12px", "weight": 500, "lh": 1.4 }
    }
  },
  "z-index": {
    "base":      0,
    "dropdown":  10,
    "sticky":    20,
    "overlay":   30,
    "modal":     40,
    "toast":     50,
    "tooltip":   60
  },
  "elevation": {
    "none": "none",
    "sm":   "0 1px 2px rgba(0,0,0,0.05)",
    "md":   "0 4px 8px rgba(0,0,0,0.08)",
    "lg":   "0 12px 24px rgba(0,0,0,0.10)",
    "xl":   "0 24px 48px rgba(0,0,0,0.14)"
  },
  "motion": {
    "duration": {
      "instant": "100ms",
      "fast":    "150ms",
      "base":    "250ms",
      "slow":    "400ms",
      "slower":  "600ms"
    },
    "easing": {
      "standard":   "cubic-bezier(0.4, 0, 0.2, 1)",
      "decelerate": "cubic-bezier(0, 0, 0.2, 1)",
      "accelerate": "cubic-bezier(0.4, 0, 1, 1)",
      "emphasized": "cubic-bezier(0.2, 0, 0, 1)"
    }
  }
}
```

## Naming Principles

**Use functional roles, not visual descriptions.** Bad: `"green-500"`. Good: `"brand-accent"` or `"text-link"`.

Why: If the brand color changes from green to orange next quarter, every `"green-500"` reference is misleading. Functional names survive rebrands.

**Use `on-X` pattern for text on colored surfaces.** `on-accent-primary` = the primary text color to use *when the background is accent*. This is Material Design's naming convention and it scales.

**Derive spacing from a base unit.** Prefer multiples of 4 or 8. If the reference uses 23px, normalize to 24px. Pixel-perfect is only needed for artistic-chaos positioning, not for grid spacing.

## Palette Patterns by Aesthetic

### Dark-canvas with accent pop
Most common in modern B2B marketing. Deep neutral canvas, one saturated brand color used sparingly.
```
canvas-primary:   deep neutral (#0F2A1D, #111827, #18181B)
brand-accent:     single saturated color (#B8F135, #F59E0B)
text-primary:     white or near-white
text-muted:       60-65% white opacity
border-subtle:    accent color at 12-18% opacity
```

### Light-canvas editorial
Magazines, agencies, portfolios. White/off-white with high-contrast type.
```
canvas-primary:   #FFFFFF or #FAFAF7
text-primary:     near-black (#0F2A1D, #18181B)
text-muted:       60-70% black opacity
accent:           one brand color
border-subtle:    5-10% black opacity
```

### Glassmorphism
Translucent surfaces over a colorful background.
```
surface-card:     rgba(255, 255, 255, 0.08-0.12)
backdrop-filter:  blur(20px) saturate(1.5)
border-subtle:    rgba(255, 255, 255, 0.15)
```

### Brutalist / raw
High-contrast, off-kilter, sharp edges.
```
canvas:           pure white or pure black
text:             pure opposite
accent:           one vivid primary color
radius:           0 everywhere except maybe `full` pills
borders:          2-4px solid, never subtle
```

## Common Mistakes to Avoid

1. **Extracting every exact hex as a separate token.** A design has ~6-10 meaningful colors, not 40. If you see `#0F2A1D` and `#123A27`, decide which is `canvas` and which is `surface-card`, then use them consistently — don't create `green-dark-1` and `green-dark-2`.

2. **Missing the `on-X` colors.** Every filled surface needs its text color defined. A card with a lime background needs `on-accent-primary` and `on-accent-muted` tokens, not just "text should be dark here."

3. **Inventing a motion system with zero visual evidence.** If the reference is a static image, infer conservatively: `duration-base: 250ms`, `easing-standard: cubic-bezier(0.4, 0, 0.2, 1)`. Don't invent elaborate spring animations.

4. **Using pixel values everywhere instead of a scale.** If you write `padding: 23px` and `padding: 27px` in different components, the scale is broken. Normalize to 24px and 28px.
