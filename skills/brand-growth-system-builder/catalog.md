# Brand & Growth Module Catalog

13 brand, visibility and credibility skills. Each one identifies intent, asks only what is
missing, holds the internal context, recommends the smallest workflow, and builds
CSV + SQL DDL + JSON Schema + Notion template only when asked.

Route from `brand-growth-system-builder`; do not load this file at runtime unless the user
asks what is available.

This pack is the brand-side companion to the 71 operational skills in
`../../references/catalog.md` and to the 16 accounting skills in
`../../accounting-audit-system-builder/catalog.md`. Where a module exists in more than one
pack, use this pack when the question is about appearance, discovery or evidence, and the
operational pack when the question is about the ongoing process.

## Layer 1: Foundation

The licensed inputs everything else is built from. Consult before an asset is made.

| Module | Code | Fits | Fields | Skill |
|---|---|---|---:|---|
| Free Design Resources | - | Starter | 18 | `skills/free-design-resources/SKILL.md` |

## Layer 2: Brand Design

Tokens, then the mark, then what gets printed. This layer is upstream of all the others.

| Module | Code | Fits | Fields | Skill |
|---|---|---|---:|---|
| Design Theme Guide | - | Starter | 24 | `skills/design-theme-guide/SKILL.md` |
| Logo & Image Design | - | Starter | 20 | `skills/logo-image-design/SKILL.md` |
| Brand Kit & Print Collateral | - | Starter | 23 | `skills/brand-kit-print-collateral/SKILL.md` |

## Layer 3: Acquire

Being found. The profile, the pages and the citations have to agree with each other.

| Module | Code | Fits | Fields | Skill |
|---|---|---|---:|---|
| Business Website Setup | - | Growth | 24 | `skills/business-website-setup/SKILL.md` |
| GBP & Local SEO Intent | - | Starter | 26 | `skills/gbp-local-seo-intent/SKILL.md` |
| SEO Directories & Backlinks | - | Growth | 22 | `skills/seo-directory-backlinks/SKILL.md` |
| Link-in-Bio Hub | - | Starter | 16 | `skills/linktree-link-hub/SKILL.md` |

## Layer 5: Fulfil

The page register is the only module in this layer, and it is the handoff between brand and
acquire: it records what each page is for so the citations have something to point at.

| Module | Code | Fits | Fields | Skill |
|---|---|---|---:|---|
| Business Website Setup | - | Growth | 24 | `skills/business-website-setup/SKILL.md` |

## Layer 6: Engage

The channels that carry the identity outward.

| Module | Code | Fits | Fields | Skill |
|---|---|---|---:|---|
| Business Email Templates | - | Starter | 22 | `skills/business-email-template/SKILL.md` |
| Presentation Deck | - | Growth | 18 | `skills/presentation-deck/SKILL.md` |
| Social Media Setup | - | Starter | 22 | `skills/social-media-setup/SKILL.md` |

## Layer 7: Protect

The rule, and the evidence that it was read and followed up.

| Module | Code | Fits | Fields | Skill |
|---|---|---|---:|---|
| Professional Code of Conduct | - | Starter | 17 | `skills/code-of-conduct/SKILL.md` |

## Layer 8: Operate

What is critical, what is measured, and what wakes a human.

| Module | Code | Fits | Fields | Skill |
|---|---|---|---:|---|
| Cloud and Observability Planning | - | Growth | 24 | `skills/observability-cloud-planning/SKILL.md` |

## Working categories

The 13 arrived under 8 working categories. Paths are flat inside the pack, so this is the
grouping, not the URL.

| Working category | Modules | Count |
|---|---|---:|
| Foundation & reference | `free-design-resources` | 1 |
| Brand design | `design-theme-guide`, `logo-image-design`, `brand-kit-print-collateral` | 3 |
| Visibility & listings | `business-website-setup`, `gbp-local-seo-intent`, `seo-directory-backlinks`, `linktree-link-hub` | 4 |
| Channels & content | `business-email-template`, `presentation-deck`, `social-media-setup` | 3 |
| Governance | `code-of-conduct` | 1 |
| Operations | `observability-cloud-planning` | 1 |

## Build order

| # | Module | Depends on |
|---:|---|---|
| 1. Free Design Resources | - |
| 2. Design Theme Guide | Free Design Resources |
| 3. Logo & Image Design | Design Theme Guide |
| 4. Brand Kit & Print Collateral | Logo & Image Design |
| 5. Business Website Setup | Design Theme Guide |
| 6. GBP & Local SEO Intent | Business Website Setup |
| 7. SEO Directories & Backlinks | GBP & Local SEO Intent |
| 8. Link-in-Bio Hub | Business Website Setup |
| 9. Business Email Templates | Brand Kit & Print Collateral |
| 10. Presentation Deck | Logo & Image Design |
| 11. Social Media Setup | Link-in-Bio Hub |
| 12. Professional Code of Conduct | - |
| 13. Cloud and Observability Planning | - |

## Overall brand flow

| # | Module | Records |
|---:|---|---|
| 1. Free Design Resources | the licensed inputs available |
| 2. Design Theme Guide | the tokens every asset inherits |
| 3. Logo & Image Design | the mark, its lockups and the rights |
| 4. Brand Kit & Print Collateral | the printed items derived from the mark |
| 5. Business Website Setup | the page register and its SEO fields |
| 6. GBP & Local SEO Intent | the profile elements and the searches they match |
| 7. SEO Directories & Backlinks | the citations that must agree on NAP |
| 8. Link-in-Bio Hub | the destinations posts and bios point at |
| 9. Business Email Templates | outbound mail and its deliverability records |
| 10. Presentation Deck | the ten-slide story with sources and sensitivity |
| 11. Social Media Setup | the channels and the posting plan |
| 12. Professional Code of Conduct | the policy version and the acknowledgements |
| 13. Cloud and Observability Planning | what is critical and what wakes a human |
| 14. Overall Brand Flow | this router, `brand-growth-system-builder` |
