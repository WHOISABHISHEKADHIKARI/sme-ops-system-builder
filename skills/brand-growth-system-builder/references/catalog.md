# Brand & Growth Module Catalog

13 brand and growth skills, one per step of the chain from design tokens to a ranked
profile and a reusable asset set. Each one identifies intent, asks only what is missing,
recommends the smallest workflow, and builds artifacts only when asked.

Route from `brand-growth-system-builder`; do not load this file at runtime unless the user
asks what is available.

Where a module produces a tracker, it ships CSV + SQL DDL + JSON Schema + Notion mapping
together, derived from one field list. Where a module produces a design or content asset
rather than a record, it ships the asset plus a register that tracks where the asset is
used, so the asset has an owner and a version.

## Reference Tooling
Layer 1: Foundation - Tool choice, libraries and reference material the others read.

| Module | Fits | Fields | Skill |
|---|---|---:|---|
| Free Design Resources | Starter | 18 | `skills/brand-growth-system-builder/skills/reference-tooling/free-design-resources/SKILL.md` |

## Brand Design
Layer 2: Brand & Design - The tokens, the mark, and everything printed from them.

| Module | Fits | Fields | Skill |
|---|---|---:|---|
| Brand Kit & Print Collateral | Starter | 23 | `skills/brand-growth-system-builder/skills/brand-design/brand-kit-print-collateral/SKILL.md` |
| Design Theme Guide | Starter | 24 | `skills/brand-growth-system-builder/skills/brand-design/design-theme-guide/SKILL.md` |
| Logo & Image Design | Starter | 20 | `skills/brand-growth-system-builder/skills/brand-design/logo-image-design/SKILL.md` |

## Listings Citations
Layer 3: Acquire - The listings and citations that make the business findable.

| Module | Fits | Fields | Skill |
|---|---|---:|---|
| GBP & Local SEO Intent | Starter | 26 | `skills/brand-growth-system-builder/skills/listings-citations/gbp-local-seo-intent/SKILL.md` |
| Link-in-Bio Hub | Starter | 16 | `skills/brand-growth-system-builder/skills/listings-citations/linktree-link-hub/SKILL.md` |
| SEO Directories & Backlinks | Growth | 22 | `skills/brand-growth-system-builder/skills/listings-citations/seo-directory-backlinks/SKILL.md` |

## Delivery Projects
Layer 5: Fulfil - Doing and evidencing the work that was sold.

| Module | Fits | Fields | Skill |
|---|---|---:|---|
| Business Website Setup | Growth | 24 | `skills/brand-growth-system-builder/skills/delivery-projects/business-website-setup/SKILL.md` |

## Communications
Layer 6: Engage - How the business speaks, inside and out.

| Module | Fits | Fields | Skill |
|---|---|---:|---|
| Business Email Templates | Starter | 22 | `skills/brand-growth-system-builder/skills/communications/business-email-template/SKILL.md` |

## Culture Channels
Layer 6: Engage - Culture, belonging and the public channels.

| Module | Fits | Fields | Skill |
|---|---|---:|---|
| Presentation Deck | Growth | 18 | `skills/brand-growth-system-builder/skills/culture-channels/presentation-deck/SKILL.md` |
| Social Media Setup | Starter | 22 | `skills/brand-growth-system-builder/skills/culture-channels/social-media-setup/SKILL.md` |

## Data Tax Conduct
Layer 7: Protect - Personal data, tax registers, documents and conduct.

| Module | Fits | Fields | Skill |
|---|---|---:|---|
| Professional Code of Conduct | Starter | 17 | `skills/brand-growth-system-builder/skills/data-tax-conduct/code-of-conduct/SKILL.md` |

## Vendors Platform
Layer 8: Operate - Suppliers, customers and the platform it all runs on.

| Module | Fits | Fields | Skill |
|---|---|---:|---|
| Observability & Cloud Planning | Growth | 24 | `skills/brand-growth-system-builder/skills/vendors-platform/observability-cloud-planning/SKILL.md` |

## Totals

- Categories: 8
- Modules: 13
- Fields: 276
- Starter: 9
- Growth: 4

## Cross-module rules

- **NAP** - name, address, phone identical across site, GBP, directories, social and print.
  One canonical block, copied, never retyped.
- **Tokens before pixels** - no colour, size or spacing value ships that is not in the
  token file.
- **Accessibility** - WCAG 2.2 AA is the floor for every colour pair that carries text,
  and the measured ratio is recorded.
- **No ranking purchase** - local rank and organic rank cannot be bought, and this pack
  never suggests otherwise.
- **No invented facts** - NAP values, metrics, follower counts, DR scores and benchmarks
  stay `Unknown` until supplied or measured.

## Reference files

| File | What it holds |
|---|---|
| `references/free-design-resource-map.md` | Every free design guideline, token tool, stock source, contrast checker and template library, with what it is good for and its licence |
| `references/backlink-directory-master-list.md` | Tiered directory and citation list with the DR/DA range, link type and approval behaviour for each tier, plus the NAP rules that apply across all of them |
| `references/print-brand-kit-specs.md` | Trim sizes, bleed, colour mode, stock weight, finish and export settings for letterhead, visiting card, employee card, folder, invoice and email signature |
