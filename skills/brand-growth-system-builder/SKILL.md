---
name: brand-growth-system-builder
description: "Route requests across 13 brand and growth modules. Use when an SME needs help choosing branding, website, local SEO, content, or cloud-planning workflows."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-27"
author: WHOISABHISHEKADHIKARI
tags: [sme, brand, design-system, logo, print, website, gbp, local-seo, backlinks, citations, email, deck, social-media, code-of-conduct, observability, cloud, wcag, seo]
tools: []
---

# Brand & Growth System Builder

Router for 13 brand and growth modules: the design theme, the logo and image library, the
print brand kit, the business website, the Google Business Profile, the backlink and
citation directories, the email templates, the presentation deck, the social channels, the
professional code of conduct, the observability and cloud plan, and the free design
resource map.

It works out what the business actually needs, then hands off to the one module skill that
matches. It never builds anything itself.

## Overview

A small business does not need 13 brand systems. It needs the two or three that make
someone pick it: a theme it can build against, a profile Google can rank, and one asset
set it does not re-make every month. This skill identifies the intent, asks only what is
still missing one question at a time, stops as soon as the answers stop changing the
route, then recommends two or three modules and waits for the user to pick.

Each module skill then runs the same contract: context first, a recommendation, and
artifacts only on request. This skill never emits a schema, a CSV, a token file or a
Notion template.

## When to Use This Skill

- "Set up our branding and website"
- "I need a Google Business Profile that ranks"
- "Where do I list my business for backlinks?"
- "Design a logo, letterhead and visiting card"
- "Set up our Facebook, LinkedIn and TikTok"
- "I need a code of conduct and email templates"
- "Plan our cloud spend and monitoring"

Do not use it when the user has already named one specific asset and just wants it - go
straight to that module skill.

## How It Works

Follow the [shared execution contract](../../references/execution-contract.md). The module-specific rules below define only domain fields, decisions, calculations, and safety constraints.

### Step 1 - Identify intent

Read the request and pick the intent before asking anything.

- "set up" / "build" / "create" -> artifacts wanted; go to Step 2.
- "review" / "is this right" / "audit" -> a check, not a build; answer from what they share.
- "how do I ..." -> advice question; answer directly, offer the build only if it helps.
- "fix" -> something already exists and is wrong; capture the current state, then Step 2.

### Step 2 - Ask only what is missing

One question per message. Skip anything already answered in any earlier message. The five
groups below are the only intake; take only the ones that change the answer.

- **Business** - What does the business do, in one line? / Who is the customer? / Physical
  address customers can visit, or service-area only? / City, country.
- **Brand** - Name as it must appear everywhere, spelling included? / One primary colour
  already decided? / Any logo, colours or documents in use today?
- **Digital** - Is there a website today, on which platform? / Who writes the copy? / Any
  social accounts already open?
- **Reach** - How many people, and how many locations or staff? / One office or several?
  / B2B, retail, service or mixed?
- **Outcome** - What has to exist in 30 days? / Who signs off on brand decisions?

Never invent a business fact. Names, addresses, phone numbers, colours, domains and
follower counts that the user has not supplied are `Unknown` and stay that way.

### Step 3 - Hold the internal context

```yaml
module: brand-growth-system-builder
intent: null            # set up | fix | review | report | import
scale: null             # Starter | Growth | Scale, only if it changes the answer
areas:
  "Business": null
  "Brand": null
  "Digital": null
  "Reach": null
  "Outcome": null
requested_outputs: []
confirmed_facts: []
open_questions: []
```

### Step 4 - Recommend two or three modules

Pick the smallest set that gets to a live profile and a usable asset set. Rank them by
what unblocks the rest. Then stop and wait for the user to choose. Examples of the shape
of a route:

- Nothing exists: `design-theme-guide` -> `gbp-local-seo-intent` -> `business-website-setup`
- Profile live, no assets: `logo-image-design` -> `brand-kit-print-collateral` -> `linktree-link-hub`
- Website live, not ranking: `gbp-local-seo-intent` -> `seo-directory-backlinks` -> `presentation-deck`
- Team growing: `code-of-conduct` -> `business-email-template` -> `observability-cloud-planning`

### Step 5 - Never build here

This router produces no files. When the user picks a module, say so and stop. Each module
skill owns its own artifacts and its own field list.

**Notion is the module's step, not this one's.** If the user wants the build in
Notion, hand off twice: the module emits the connection prerequisite and waits for
"Notion connected.", and the Notion step itself runs in `notion-manual-import`,
which renders the module's field list. This router never prints the prerequisite
itself and never restates the mapping.

## Examples

**Prompt**

```
We are launching a local service business. We need a consistent identity, a website,
and a Google Business Profile, but nothing exists yet.
```

**Route**

```
design-theme-guide -> logo-image-design -> gbp-local-seo-intent
```

## The Dependency Order

Brand decisions travel one way. Nothing later can be built before the token set exists,
and nothing visual can be finalised before the logo does.

```
free-design-resources          (read-only research, safe to start at any time)
        |
design-theme-guide             (tokens: colour, type, space, contrast)
        |
logo-image-design              (mark, lockups, image library)
        |
brand-kit-print-collateral     (letterhead, visiting card, employee card, signature)
business-email-template        (templates + SPF/DKIM/DMARC)
linktree-link-hub              (single destination for every bio link)
        |
business-website-setup         (site structure, schema, NAP on every page)
gbp-local-seo-intent           (profile, categories, services, posts, reviews)
seo-directory-backlinks        (citations, directories, link profile)
social-media-setup            (Facebook, LinkedIn, TikTok, Facebook Page)
presentation-deck              (the 10-slide story built from all of the above)
        |
code-of-conduct                (independent, but needs the real role names)
observability-cloud-planning   (independent, needs real cost ceilings)
```

**Category map** - modules are published as
`skills/brand-growth-system-builder/<slug>/`. Their categories describe the workflow
stage rather than adding another directory level. Counts are modules in this pack:

Layer 1 Foundation: Reference Tooling (1)
Layer 2 Brand & Design: Brand Design (3)
Layer 3 Acquire: Listings Citations (3)
Layer 5 Fulfil: Delivery Projects (1)
Layer 6 Engage: Communications (1), Culture Channels (2)
Layer 7 Protect: Data Tax Conduct (1)
Layer 8 Operate: Vendors Platform (1)

Full index: `references/catalog.md`. Three read-only reference files sit behind it -
`references/free-design-resource-map.md`, `references/print-brand-kit-specs.md` and
`references/backlink-directory-master-list.md`. Load one only when the module that needs it
is the module being run.

## Rules Every Module Holds To

- One name, one spelling, one phone number, one address, everywhere - the NAP rule. A
  variation is a defect, not a local preference.
- A design system is tokens first, components second, and never a one-off. If it is not
  written as a value, it is not part of the system.
- Contrast is a test, not an opinion. Body text 4.5:1, large text and UI components 3:1,
  per WCAG 2.2 AA - and the ratio gets recorded in the token file.
- A Google Business Profile is a completeness and accuracy problem before it is a keyword
  problem. Nobody can buy a better local rank.
- Never keyword-stuff the business name. Use the real name, and put the keywords in the
  description, the services and the posts.
- A directory link is worth nothing without a real listing. A fake listing is a liability.
- Never invent a business fact, a NAP value, a metric, a benchmark or a score.
- Selection, sign-off and legal conclusions stay with a human.

## Owner and Cadence

- Owner: whoever owns the brand and the website. Small businesses usually fold this into
  the founder or an operations lead.
- Cadence: the router runs per request. Each module reviews itself when the business
  changes - new location, new service, rebrand, headcount growth - not on a fixed date.

## Best Practices

- Start with the dependency that unlocks the requested downstream assets.
- Keep every recommendation tied to a confirmed business need.
- Run one module intake at a time and let that module own its artifacts.
- Keep unknown business facts unknown rather than filling them with plausible values.

## Limitations

- It routes work but does not create brand assets or operational records itself.
- It cannot guarantee rankings, directory approval, legal compliance, or platform availability.
- Local advertising, privacy, accessibility, and employment requirements need human review.
- The catalog is intentionally SME-focused and is not a full enterprise brand platform.

## Security & Safety Notes

- Do not request credentials, unpublished customer data, or unnecessary personal information.
- Treat domains, social accounts, DNS, analytics, and cloud resources as external systems that
  require explicit authorization before mutation.
- Never publish invented contact details, addresses, testimonials, metrics, or legal claims.
- Human approval is required before publishing, purchasing, changing DNS, or enabling services.

## Common Pitfalls

- Two modules look equally right - pick the one the others depend on, and say why.
- The user asks for everything at once - propose the first three, in the order above, and
  build those before the rest.
- The user has no logo yet but wants print collateral - route to `logo-image-design` first;
  letterhead without a mark is a rewrite later.
- GBP needs an address the business does not physically occupy - that is a service-area
  business, and the module records it as such. Never advise a virtual address for ranking.
- Social is requested before the website exists - acceptable for a launch page, but the
  module says the website is still the ranking asset.

## Related Skills

- [@SME Ops System Builder](../../SKILL.md) - the operational router this pack sits beside.
- [@Accounting & Audit System Builder](../accounting-audit-system-builder/SKILL.md) - the 16-module accounting cycle this pack feeds.
- `@company-email-accounts` (operational pack) - the account register behind the email
  templates in `business-email-template`.
- `@asset-it-management` (operational pack) - holds the issued laptops, cards and devices
  that carry the brand kit.

## Reusable Prompt

```
I want to set up the brand and online presence for my small business. Ask me one short
question at a time, only about what I have not already told you, and never invent
anything about my business. Then recommend the two or three modules that matter first, in
the order they depend on each other, and wait for me to pick before you build anything.
When I pick a module, output only the artifacts I asked for.
```
