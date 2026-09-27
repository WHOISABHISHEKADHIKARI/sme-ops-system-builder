---
name: brand-growth-system-builder
description: "Routes a brand or visibility request to the right module skill, from design tokens through local search and channels. Asks only what is missing. Use for a logo, brand guidelines, print collateral, a business profile, citations or social accounts."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-27"
author: WHOISABHISHEKADHIKARI
tags: [sme, brand, design, logo, print, seo, local, citations, social, email, database, csv, sql, router]
tools: [claude, cursor, gemini, antigravity]
---

# Brand & Growth System Builder

Router for 13 brand, visibility and credibility skills. It works out whether the request is
about how the business looks, how it gets found, or whether it can be believed, then hands
off to the one or two modules that do that job. It never builds an asset itself.

## Overview

A small business does not need 13 brand systems. It needs the two or three that are
currently inconsistent, and a record of the decisions so the next person inherits them
rather than reinvents them. This skill identifies the job, asks only what is still missing
one question at a time, stops as soon as the remaining answers stop changing the route,
then recommends two or three modules and waits for the user to pick.

The three jobs:

```
Consistent   - the same colour, type, mark and voice everywhere
Findable     - the profile, the site and the citations that agree with each other
Credible     - a deck, a policy and a monitor that survive being questioned
```

Most requests are really one of these with a different word on it. "Our logo looks wrong on
a invoice" is consistency. "Nobody can find us" is findability. "The investor asked for
something we cannot evidence" is credibility.

## When to Use This Skill

- "we need a logo and brand guidelines"
- "the cards, the letterhead and the invoice all look different"
- "nobody can find us when they search for us"
- "should we be on LinkedIn, and what should we post"
- "can we use this image or this font we found"
- "we have a pitch in three weeks and nothing to show"
- "an employee says they never signed the code of conduct"

Do not use it for the operational records themselves - invoices, attendance, recruitment.
Those are in the companion pack at `../../`. Use this pack when the question is about
appearance, discovery or evidence.

## How It Works

### Step 1 - Identify the job, not the tool

The user usually arrives naming a tool or a deliverable. The route depends on the job
behind it, and the same deliverable can sit in two different jobs.

Ask which of the three it is before anything else. If the answer is ambiguous, it is
usually consistency: when two assets disagree, the disagreement is upstream.

- **Consistent** - two or more assets use different colours, type, a different mark, or
  different contact details. Route to the tokens or the mark, not to the asset that looks
  wrong.
- **Findable** - the business exists but does not appear for the searches its customers
  make. Route to the profile, the page register or the citations.
- **Credible** - someone external needs to be convinced, or an internal rule has to be
  evidenced. Route to the deck, the policy record or the criticality plan.

### Step 2 - Ask only what is missing

One question per message. Stop as soon as the remaining answers would not change the
route. Do not ask for a brand budget, a colour preference or a posting calendar unless the
route depends on it.

- **Identity** - Exact spelling of the name, and any tagline? / What the business does, in
  one line? / Any name or trading-name change coming?
- **Current state** - Is there a mark today, and who made it? / Where is the brand used -
  sign, vehicle, invoice, app, uniform? / Does the editable file still exist?
- **Rights** - Does the business own the marks and names it uses? / Any prior designer
  whose rights were not transferred in writing? / Which fonts and images are licensed for
  what?
- **Visibility** - Should customers find the business by place, by service, or both? / Is
  a Business Profile claimed? / Which citations already exist?
- **Channels** - Which accounts are live, and what is each for? / Who approves a post
  before it goes out?
- **Constraints** - Anything that must not be published? / A deadline that fixes the order?

### Step 3 - Hold the internal context

State what is already known and what it implies, without producing anything yet. The user
has usually supplied more than they think, and the recommendation should show that the
earlier answers were used rather than repeated.

Cover, briefly:

- **What already exists** - the assets, tokens, listings and accounts that are in place
  today, and which of them are recorded versus merely existing.
- **What is inconsistent** - the specific pairs that disagree, and which one is upstream.
- **What is missing that blocks the route** - a licence you cannot verify, a mark nobody
  owns, a profile that is unclaimed.
- **What the route excludes** - the jobs in this pack that are not being asked for, and why
  they are not needed yet.

Keep this to the decisions, not the deliverables. It exists so the user can correct the
premise before three modules get built on it.

### Step 4 - Recommend the smallest workflow

Two or three modules, in dependency order, with the reason each one is in the list. Then
wait for the user to pick. Do not build artifacts here.

The ordering rule is upstream first. Tokens and the mark come before collateral, the
profile and the citations come before the channels, and the deck comes last because it
reuses everything above it.

For each recommendation give:

- the module and the single job it does
- why it is in the list, tied to something the user said
- what it will not cover
- the order, and which module becomes unnecessary if an earlier one is skipped

If one module answers the whole request, say so and recommend only that one. A pack of
thirteen is not a default.

### Step 5 - Output

Artifacts are built only when the user asks, and only for the modules they picked. Each
module emits CSV + SQL DDL + JSON Schema + Notion template on request, never all four
unprompted. State which module each artifact came from, and what the user still has to
decide.

## The order this pack encodes

```
Free design resources      - the licensed inputs, consulted before an asset is made
  -> Design theme guide    - colour, type, spacing, contrast tokens
    -> Logo & image design - the mark, its lockups, and the rights behind every asset
      -> Brand kit & print collateral
        -> Business website setup
          -> Google Business Profile intent
            -> SEO directory & backlinks
              -> Link hub
                -> Business email template
                  -> Presentation deck
                    -> Social media setup
```

Two modules sit outside that line. `Professional Code of Conduct` is independent - it is needed when a
rule has to be evidenced, which is a credibility question with no brand dependency. And
`Cloud and Observability Planning` is the credibility module for a technology business,
where "can you evidence this" usually means "do you know what breaks when it is down".

## Rules the modules hold to

- A token is recorded once. If two assets disagree, the token is wrong, not the assets.
- Clear space and minimum size are usage rules, not preferences.
- Every asset carries its source, rights owner and licence. "We found it online" is not a
  source.
- Name, address and phone are identical across the profile, the site and every citation.
- A trademark search precedes the mark being used in public.
- Free does not mean unrestricted. Commercial use and attribution are separate answers.
- A deck slide carries its sensitivity marking and data source, not only the number.
- One approved source of truth per fact. Links rather than copies.

## Examples

**"We need a logo."**

Job: consistent. There is no mark, so the route starts at the trademark search and the
tokens, not at the drawing. Ask what the business does in one line and whether the name is
final. Hold: nothing exists yet, so the risk is a name that cannot be registered, not an
inconsistency. Recommend `logo-image-design` first with `design-theme-guide` behind it,
and note that `brand-kit-print-collateral` is not needed until there is a mark to print.
Do not produce artwork.

**"Nobody can find us."**

Job: findable. Ask whether customers search by place or by service - that single answer
decides the route, because a service-area business with no premises should not be building
a Business Profile. Hold: check whether a profile already exists unclaimed, and whether
the site and any existing citations agree on the address. Recommend
`gbp-local-seo-intent` and `business-website-setup`; mention `seo-directory-backlinks` as
the third only if there are already listings to correct.

**"Our investor meeting is on the 14th."**

Job: credible. The deadline fixes the order. Ask what evidence exists today and whether
any figure is sensitive. Hold: a deck reusing assets nobody has rights to is the risk, not
the slide count. Recommend `presentation-deck`, and check `logo-image-design` for
`Trademark Status` before the mark goes on a slide shown outside the business.

**"Can we use this photo from a search result?"**

Job: consistent, narrowly. This is a rights question, not a design one. Hold: "found on a
search result" is not a source and there is no licence record. Recommend
`free-design-resources` for what is actually licensed, and `logo-image-design` to record
whichever asset is chosen. Do not answer the licensing question from memory.

## Best Practices

- Fix the token before the asset. Rebuilding one printed item costs more than recording one
  decision.
- Check rights before the asset exists, not when someone asks who owns it.
- Record NAP once and copy it everywhere; never retype it per channel.
- Start the profile and the site before paying for citations. Unaligned listings are worse
  than none.
- Keep the deck's data sources live. A number that cannot be traced is the first thing an
  investor finds.
- Ask for two or three modules. Recommending all thirteen is a failure to choose.

## Limitations

- This pack does not design, draw, write, publish, post, submit or send. It records the
  specification and the decision; the work happens in the user's own tools.
- It does not clear a trademark or give legal advice. `Trademark Status` records the
  result of a search someone else ran.
- It does not do keyword research, rank tracking or competitor analysis. It records the
  intent you decided on.
- It cannot verify a licence. Licence terms change without notice and the register is a
  record of what you checked, not a guarantee.
- It does not manage social accounts, hosting or DNS.
- One module here is not a brand module at all: `observability-cloud-planning` is included
  because credibility questions for a technology business land there.

## Security & Safety Notes

- Never put unpublished pricing, salaries, runway or customer names into a deck that will
  leave the business. `Sensitivity` exists for this.
- Treat an address, a phone number and a personal name as personal data. Publish only what
  the business has decided is public.
- Do not scrape, crawl or bulk-submit to directories. Submissions are manual and
  `Listing Status` records the outcome.
- A trademark search is not a clearance. Never tell the user a name is available; say the
  search came back clear on the date checked, and that `Trademark Status` is
  `Searched - clear`, not `Registered`.
- Do not connect to social platforms or DNS. This pack records intent; it holds no
  credentials.

## Common Pitfalls

- **Starting at the asset.** "The invoice header looks wrong" is a token or mark problem.
  Fixing the header alone guarantees the next one drifts.
- **Treating free as unrestricted.** Commercial use and attribution are different
  questions, and a free font is frequently not usable on a client invoice.
- **Paying for citations before the profile is right.** A NAP mismatch across listings
  costs more than the listings earn.
- **Being on a platform you cannot maintain.** An abandoned account is worse than none,
  because it is a live wrong answer.
- **Reusing a slide without its data source.** The number travels; the citation does not.
- **Building all thirteen.** Two or three, in upstream order, and wait.

## Related Skills

- `accounting-audit-system-builder` - the entry, the reconciliation and the audit trail
- `../` - the 71 operational modules this pack sits beside
- `website-builder` and `seo-audit` for deeper site and search work
- `legal-compliance-vault` for the policy documents behind `code-of-conduct`

## Reusable Prompt

> I help small businesses look consistent, get found locally, and evidence what they
> claim. Ask me one question at a time, and only for what is still missing. Then tell me
> which two or three of my brand modules to use, in dependency order, and what each one
> will not cover. Do not build anything until I pick.
