# Free Design Resource Map

Everything here is free to read, copy or use. Grouped by what the business needs it for.
Read this file when a module says "use the free resources" - `free-design-resources` is
the module that hands this out, and it is the one module with no build step.

Licences are stated because they decide what the business may do with the result. A
resource marked *permissive* (MIT, Apache 2.0, ISC, BSD, OFL) can go into a commercial
product. Anything marked *free to use* may have its own terms - read them before the asset
ships.

---

## 1. Accessibility standards - the floor, not the nice-to-have

| Resource | What it is | Licence |
|---|---|---|
| WCAG 2.2 (W3C) | The normative accessibility standard. Every colour pair, focus state and alt text in this pack is judged against it | Free, W3C Document Licence |
| WCAG 2 at a Glance | One-page summary of the four principles - the fastest briefing for a non-designer | Free |
| How to Meet WCAG 2 (Quick Reference) | Filterable list of success criteria with techniques. Use this in the theme build | Free |
| WAI Resources for Designers | The designer-specific entry point, plus the free Digital Accessibility Foundations course | Free |
| WAI-ARIA Authoring Practices | Component behaviour, keyboard patterns, focus management. The reference for building anything interactive | Free |
| W3C Design System Community Group | The open design-system community - patterns, tokens, governance | Free |

**The four numbers that decide a theme:**

| Content | AA minimum | AAA enhanced |
|---|---|---|
| Body text | 4.5 : 1 | 7 : 1 |
| Large text (18pt, or 14pt bold) | 3 : 1 | 4.5 : 1 |
| UI components and graphical objects | 3 : 1 | not defined |
| Logo and decorative text | exempt | exempt |

The European Accessibility Act references EN 301 549, which references WCAG contrast. In
practice that makes the 4.5:1 floor a legal question in EU-facing work, not a preference.

---

## 2. Colour - palettes and checking

| Resource | What it is | Licence |
|---|---|---|
| WebAIM Contrast Checker | Paste two hex values, get a pass/fail per WCAG level | Free |
| Colour Contrast Analyser (TPGi) | Desktop app, also simulates colour-vision deficiency. The one to check a whole theme with | Free, open source |
| Colour Contrast Analyser (CCA) | Desktop app, window-level inspection over any app | Free, open source |
| getwcag.com contrast checker | Browser checker aligned to WCAG 2.1/2.2 and EN 301 549 | Free |
| Adobe Color | Palette generator with accessibility check and contrast scoring, plus palettes extracted from images | Free to use |
| Coolors | Fast palette generator, shareable links, so a palette can be handed over as a URL | Free to use |
| Khroma | AI palette generator - generate by mood or from a photo, exports to Figma, Adobe, CSS, SVG | Free to use |
| ColorHunt | Curated four-colour palettes | Free to use |
| Coblis | Simulate six colour-vision deficiency types on a real page | Free online |
| Color Oracle | Windows/Mac colour-vision simulator | Free |
| Material Theme Builder | Generates a full accessible light/dark palette from one seed colour | Free, Apache 2.0 |

**Rule:** the ratio gets written into the token file next to the colour. A palette that has
not been measured is not a theme.

---

## 3. Design systems to crib the structure from

Study the *structure*, not the brand. These are the reference implementations.

| System | Why it is worth reading | Licence |
|---|---|---|
| Material Design 3 | The most complete free spec - colour roles, type scale, motion, elevation tokens | Apache 2.0 |
| Carbon Design System | The clearest accessibility documentation of any system; its contrast table is public | Apache 2.0 |
| Polaris (Shopify) | Commerce patterns, dense-data components | MIT |
| USWDS | Government system, unusually good on forms and public-service content | Public domain |
| GOV.UK Design System | Content-first design, excellent on writing and error messages | MIT |
| Open Props | CSS custom properties library - a ready-made token set to fork | MIT |
| Shoelace / Web Awesome | Themeable, accessible web components with CSS custom properties as the API | MIT |
| Radix Primitives | Unstyled accessible behaviour, styled by your tokens | MIT |
| shadcn/ui | Copy-in components - the tokens stay in your repo | MIT |
| daisyUI | Themeable component classes over Tailwind | MIT |
| Untitled UI | Free Figma design system (MIT) | MIT |

---

## 4. Tokens and build pipeline

| Resource | What it does | Licence |
|---|---|---|
| W3C Design Tokens Community Group format | The interchange format for tokens - the shape a token file should take | Free spec |
| Tokens Studio for Figma | Designers and developers share one token file, in Figma | Free tier |
| Style Dictionary | Design tokens to CSS, SCSS, JS, iOS, Android. The standard build step | Apache 2.0 |
| Chrome DevTools CSS Overview | Inspect the exact custom properties a live site resolves to | Free |
| Firefox Accessibility Inspector | Contrast and focus issues on the live page | Free |

---

## 5. Typefaces - free, licensed for commercial use

| Resource | Notes | Licence |
|---|---|---|
| Google Fonts | 1,500+ families. Filter by `OFL` or `Apache` for commercial embedding | OFL / Apache 2.0 |
| Inter | The default UI sans - pairs with almost anything | OFL |
| Source Sans 3 | Adobe's open family, good for body copy and long documents | OFL |
| Atkinson Hyperlegible | Designed for low vision. Free to use and genuinely different in character | OFL |
| Atkinson Hyperlegible Next | The 2024 revision | OFL |
| IBM Plex | A full superfamily - Sans, Serif, Mono, Condensed. Coherent across a whole brand | OFL |
| Manrope | Geometric, good for headings and short marketing copy | OFL |
| Libre Franklin | Versatile, calm at small sizes | OFL |
| EB Garamond | A workhorse serif for letterhead and print | OFL |
| Fraunces | A characterful display serif | OFL |
| Font Squirrel | Finds commercially licensed free fonts, generates webfont kits | Free |
| type-scale.com | Type scale calculators; also base-ratio and modular-scale tools | Free |

**Print note:** Google Fonts web files are fine on screen. For letterhead, cards and
anything offset-printed, use the desktop static TTF/OTF or the licensed print kit - screen
hinting changes the printed result.

---

## 6. Icons

| Resource | Notes | Licence |
|---|---|---|
| Lucide | Consistent 24px grid stroke icons, tree-shakeable | ISC |
| Heroicons | Two weights - outline and solid, same grid | MIT |
| Feather Icons | The original minimal set, still widely used | MIT |
| Tabler Icons | ~5,000 icons, very consistent | MIT |
| Material Symbols | Variable font, thousands of icons, can be filled or outlined | Apache 2.0 |
| Font Awesome Free | The free tier's solid set, plus the Pro look by association | Free for non-commercial; CC BY 4.0 for Free icons |
| Simple Icons | Brand marks - the one to use for a "follow us" row | CC0 |
| Phosphor Icons | Six weights, including duotone | MIT |

---

## 7. Illustration, avatars and imagery

| Resource | Notes | Licence |
|---|---|---|
| unDraw | Open illustration system, recolourable to any brand hex, SVG source | MIT / unDraw licence |
| Humaaans | Customisable people illustrations | Free |
| Storyset | Animated illustration by Freepik, editable in SVG | Free with attribution |
| DiceBear | Generated avatars - an easy, consistent employee-photo stand-in | CC0 / MIT |
| ManyPixels Gallery | Animated SVG illustrations, brand recolour | Free |
| Blush | Illustration library with a free tier | Free tier |
| ImageKit / Unsplash | Photography - Unsplash licence, no attribution required | Free to use |
| Pexels | Photography and video, free licence | Free to use |
| Pixabay | Photography, video, audio, no attribution required | Free to use |
| Burst by Shopify | Free stock photography, Shopify-curated | Free to use |
| Coverr | Free stock video | Free to use |
| Mixkit | Free stock video and music | Free to use |
| Unsplash Source alternative: `loremflickr` | Drop-in placeholder images while the real photos are being shot | Free |

**Shoot your own for GBP.** Stock photography of a city is not a customer. A phone photo
of the actual shopfront, counter or team outperforms stock on the profile and costs nothing.

---

## 8. Image and file optimisation

| Resource | What it does | Notes |
|---|---|---|
| Squoosh | Google's in-browser image optimiser - AVIF, WebP, mozjpeg, resized | Free, open source |
| TinyPNG | Lossy compression for PNG and JPEG | Free tier |
| SVGO | Command-line SVG optimiser | Free, open source |
| Sharp | Node image pipeline for build-time resizing and format conversion | Free |
| WebP lossless `cwebp` | Batch conversion in CI | Free |
| ExifTool | Strips GPS and camera metadata out of photos before publishing | Free, open source |

---

## 9. Wireframing, mockups and design tools

| Resource | Notes | Licence |
|---|---|---|
| Figma | Free tier is enough for a small business. Community files are the design-system library | Free tier / CC BY for community |
| Penpot | Free, open-source design tool, browser-based | AGPL |
| Excalidraw | Free hand-drawn-style diagrams - useful for internal workshop flows | MIT |
| diagrams.net (draw.io) | Free diagramming, desktop or web | Apache 2.0 |
| MockupWorld | Free PSD mockups for branding presentation | Free |
| Smartmockups | Free tier, device and print mockups | Free tier |
| Device Frames | Free device mockups | Free |
| Coolors palette-to-Figma export | Drops a validated palette straight into Figma variables | Free |

---

## 10. Website, email and page speed

| Resource | What it is | Cost |
|---|---|---|
| Google Search Console | The only authoritative index of what Google thinks of the site | Free |
| Google Rich Results Test | Tests schema.org markup against Google's supported types | Free |
| Schema.org validator | Validates structured data before Google sees it | Free |
| PageSpeed Insights | Field data (CrUX) and lab data, Core Web Vitals | Free |
| Lighthouse | In-DevTools audit: performance, accessibility, best practice, SEO | Free |
| WebPageTest | Deeper Core Web Vitals and filmstrip testing | Free tier |
| WAVE | Accessibility, SEO and visual inspection in one pass | Free tier |
| MDN Web Docs | The reference for HTML, CSS and browser behaviour | Free |
| Can I Use | Feature support by browser, with global usage share | Free |
| W3C Nu HTML Checker | Validates the markup Google parses | Free |
| Cloudflare | DNS, CDN, static hosting, free tier. Also where a domain and TLS get set up | Free tier |
| Netlify / Vercel | Static hosting with a free tier and automatic HTTPS | Free tier |
| GitHub Pages | Free static hosting for a simple site | Free |
| Google Analytics 4 | Site traffic and conversion measurement | Free |
| Microsoft Clarity | Free session recordings and heatmaps | Free |
| Plausible / Umami | Privacy-first, lightweight analytics with a self-hostable or free tier | Free tier |

---

## 11. Email

| Resource | Notes | Licence |
|---|---|---|
| Litmus / Email on Acid | Preview across ~90 clients. Paid - the one genuinely useful spend in this list if a send fails | Paid |
| Mail Tester | Paste a draft, get a spam-score breakdown and the exact trigger that pushed it up | Free |
| MXToolbox | SPF, DKIM, DMARC and blacklist check for a domain | Free tier |
| Google Admin Toolbox | Check the exact DMARC record Google sees | Free |
| MJML | Framework for responsive email from one HTML source | MIT |
| Foundation Email | Zurb's responsive email framework | MIT |
| htmletailor | In-browser responsive preview while writing | Free |
| Can I Email | Per-client support for every CSS feature you might use | Free |
| SendLayer / Mailtrap / MailHog | Free tiers for sending and catching test mail safely | Free tier |
| Email signature | Build once, centralise it, never type it again - see `brand-kit-print-collateral` | - |

---

## 12. Presentations

| Resource | Notes | Licence |
|---|---|---|
| Google Slides | Free, shared, collaborative, exports to PDF and PPTX | Free |
| Canva free tier | Brand Kit, templates, presenter view, PDF export. The pragmatic SME choice | Free tier |
| Figma | Slides in Figma, free tier | Free tier |
| Marp | Markdown to slides. A whole deck as a text file in git | MIT |
| Slidev | Markdown to slides, with Vue components and a presenter mode | MIT |
| reveal.js | The classic HTML slide framework | MIT |
| Speaker Deck | Free presentation templates | CC BY-NC |
| Unsplash / Pexels | Slide imagery - download rather than screenshot | Free to use |
| Font pairing check | Every deck pairs one display face with one body face. Two is the limit | - |

---

## 13. Brand names, logos and the early identity

| Resource | Notes | Cost |
|---|---|---|
| USPTO / EUIPO / IP India trademark search | **Run this before designing a mark.** Free, and it is the only check that matters | Free |
| WIPO Global Brand Database | Cross-border trademark and logo search in one place | Free |
| Google Fonts / Font Squirrel | Typeface sourcing | Free |
| Khroma / Coolors / Adobe Color | Palette | Free to use |
| unDraw / ManyPixels / Storyset | Illustration | Free |
| Canva free tier | A working logo, business card and letterhead template in an afternoon | Free tier |
| Looka / Hatchful (Shopify) | Logo generators - a starting point for a discussion, not a trademark | Free tier / paid |
| Custom design | A trademarkable mark usually needs a designer, and the fee is spent on the search and registration, not only the drawing | Paid |

**The one thing not to skip:** a free logo generator will hand you a mark that three other
businesses already use in the same industry. Search the trademark database first, then
design.

---

## 14. Printing the brand kit

| Resource | Notes |
|---|---|
| Canva Print | Sends the same file that designed the letterhead straight to print, with crop and bleed guides |
| Bluelight | Indian online print, auto bleed marks, free design check |
| Printful / Printify | Print-on-demand if the business is selling printed collateral rather than using it |
| FedEx Office / Staples | Walk-in print when a file must be there today |
| ICC profiles | Ask the printer for the ICC profile of the press, and export soft-proofed from it |
| Optical margin alignment | Have the printer hang a proof - a 0.3 mm error on a letterhead is visible on every page |

Full trim sizes, bleed, colour mode, stock and export settings:
`references/print-brand-kit-specs.md`.

---

## 15. Where to read the standards properly

| Resource | Why |
|---|---|
| WCAG 2.2 (normative) | w3.org/TR/WCAG22 |
| WCAG Quick Reference | w3.org/WAI/WCAG22/quickref |
| WAI Roles: Designers | w3.org/WAI/roles/designers |
| MDN | developer.mozilla.org |
| Material Design 3 | m3.material.io |
| Carbon | carbondesignsystem.com |
| GOV.UK Design System | design-system.service.gov.uk |
| USWDS | designsystem.digital.gov |
| W3C Design Tokens CG | design-tokens.github.io/community-group |
| Open Props | open-props.style |
| Style Dictionary | styledictionary.com |
| Google Search Central | developers.google.com/search |
| Google Business Profile Help | support.google.com/business |

---

## The short version for a small business

If the budget is zero, build the theme from **Open Props** or a **Material 3** token set,
type it in **Inter** or **IBM Plex Sans** with a single companion face, draw the icons from
**Lucide** or **Tabler**, pull photography from **Unsplash** and **Pexels**, and check
every colour pair with **WebAIM** and **CCA** before it ships. Take the structure from
**GOV.UK Design System** and **Carbon** for form and content patterns, because both are
built for people who did not choose the brand. Spend the first money on a trademark
search, and the second on one freelance designer for the mark.
