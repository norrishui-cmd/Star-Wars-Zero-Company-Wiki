# Round 21 — Compact Responsive Navigation

The homepage header was resized to prevent the brand, primary navigation,
language selector, and search field from competing for the same horizontal
space.

## Changes

- Reduced the desktop brand column, icon, title, subtitle, and spacing.
- Constrained the language selector to a compact fixed-width column.
- Reduced the search field width, internal padding, icon, and submit control.
- Tightened primary navigation typography and item spacing.
- Added a second compact state from 981px through 1180px.
- Preserved the existing mobile menu at 980px and below.
- Preserved all four consolidated dropdown groups, search behavior, and all
  eleven language choices.

## Quality target

At every desktop breakpoint, the three header columns have explicit size
budgets and the center navigation column may shrink without being covered by
either neighboring column. Mobile widths continue to use the existing menu
instead of forcing desktop controls into an unsafe row.
