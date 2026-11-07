# Learnings

Notes from planning, researching, building and testing this site, November 2026. Most recent decisions first where it matters.

## Decisions

| Decision | Why |
| --- | --- |
| Static HTML, CSS and JS. No framework, no build step. | One page with four tabs doesn't need more. The whole site is about 70 KB compressed, fonts included. |
| Content lives in `index.html`, not Notion. | Will's call. Keeping it in the repo means no API token, no sync job, and no Notion image URLs that expire after an hour. |
| Tabs are plain links (`#work`), not an ARIA tab widget. | Each tab acts like a page: it needs deep links, a working back button and `aria-current="page"`. The ARIA tabs pattern is for widgets inside a page. |
| On phones the tabs stay at the top, not in a bottom bar. | A fixed bottom bar fights the iOS Safari toolbar. Four short labels fit in one row at 320 px. |
| Typewriter kept from the old site, but it runs once and stops. | Will likes it. Running once, with a pause button, avoids the WCAG 2.2.2 problem with looping motion. |
| No project images. | The images in Notion were press photos of real athletes and stock photos. Real screenshots weren't possible from the cloud session (see "Couldn't check"). |
| No made-up copy. | Every line on the site comes from Will's Notion page, his old site, his GitHub repo list or his spec. Where there wasn't enough to say (the Omni role), the entry stays short. |

## Hosting: Vercel over GitHub Pages

Both are free for a public static site, and both handle a custom domain and HTTPS. Vercel wins here for three reasons:

- **Preview links.** Vercel builds a separate URL for every branch and pull request, so a change (or the `mockups/` folder) can be checked on a phone before it goes live. GitHub Pages publishes one branch and has no previews.
- **Already in use.** About a dozen of Will's projects (The Bracket Lab, All My Flights, Georgia Swarm, ...) are on Vercel, so it's the same account and workflow.
- **Simple domain setup.** www-to-root redirect and HTTPS are settings in the dashboard.

GitHub Pages would also work: the repo is public, so it's free. Setup there is Settings → Pages, four A records (185.199.108.153 to 185.199.111.153) and a `www` CNAME to `willyclayton.github.io`. One caution: ten of Will's repos already use GitHub Pages at `willyclayton.github.io/<repo>`. Putting the custom domain on this repo is fine, but putting it on a `willyclayton.github.io` user-site repo would move all ten under `willyclayton.com/<repo>`.

## Cleanup pass (minimalist, nothing given away on Home)

- **Home** is only the typewriter hello, centered. No intro paragraph, no at-a-glance list, no links in the body. LinkedIn and GitHub moved to the footer on every tab.
- **Work** keeps four Accenture bullets instead of six. Coursework and college activities are gone; the MS line just says it was completed while working full time.
- **Projects** dropped the filter buttons and the "Learned" lines. Each project is a name, one sentence, and its stack and code link.
- **About** is the bio, one line of interests, the testimonials (the "Works with data" quote is now one of them), and contact.
- The link-preview image only says "hello.... I'm Will Clayton." and the domain.
- Unused CSS and the filter JavaScript were deleted.

## Content: what was cut, and why

The first draft had AI-sounding filler. Will asked for no AI slop, so these went:

- An invented bio ("realized I liked the spreadsheets more than the machines"). Replaced with Will's own intro from Notion.
- Cute intros under headings ("Most started as 'wouldn't it be cool if…'").
- A 404 joke.
- A "data nerd" typewriter line. The lines now come from his old site ("a lifelong learner", "a passionate golfer") or are plain facts.
- Visual template habits: pill-shaped tabs, grey rounded cards, a glow that followed the mouse, a red "Biggest one" badge, small uppercase letter-spaced labels, boxed quotes.

Rules used for the rewrite:

- Use the owner's words when they exist. His Notion bullets for Accenture and his "Learned" notes per project are better than anything rewritten.
- One fact per sentence. No "not just X, but Y", no lists of three for rhythm, no em dashes.
- Keep humor to the parts he wrote himself (the testimonials), clearly labeled as jokes.

## Research findings

Three research agents ran in parallel. None of them could open w3.org, web.dev or most portfolio sites from the cloud session, so these findings come from search results that quote those pages, not full reads.

### Portfolio patterns worth using

- Brittany Chiang's site (brittanychiang.com) is the best-known "résumé as a website": pinned name and nav, roles that scan quickly.
- Amelia Wattenberger (wattenberger.com) shows a data person's work as the decoration. A good model if a chart or map ever goes on the home page.
- Eugene Yan (eugeneyan.com) keeps a plain site with side projects in their own tab.
- Patterns used here: hash-routed tabs, a line that slides under the current tab, a staggered fade-in when a tab opens, a light/dark toggle that remembers the choice.
- Patterns avoided: splash screens, intros that block clicks, scroll hijacking, custom cursors, 3D or "desktop OS" layouts, and information that only shows on hover.

### Typewriter

- Screen readers read whatever is on screen at that moment, so they hear half-typed words. Hide the animated text with `aria-hidden="true"` and put the full sentence in visually hidden text. Don't use `aria-live` for it (it either interrupts or queues up), and don't use `aria-label` on a heading (it replaces the heading's content). Sources: dev.to/savvasstephnds (typewriter problem), w3.org/WAI/ARIA/apg/patterns/carousel, benmyers.dev (aria-label on static text), gomakethings.com.
- WCAG 2.2.2 Pause, Stop, Hide covers anything that moves on its own for more than 5 seconds next to other content. A full pass takes about 18 seconds here, so there is a visible pause/replay button, and any click or key finishes it. A caret that keeps blinking after 5 seconds counts too, so it blinks three times at the end and stops.
- A 1 Hz caret blink is well under the 3-flashes-per-second limit (WCAG 2.3.1).
- Timing used: 55 to 100 ms per character with random jitter, about 260 ms after punctuation, 30 ms per deleted character, 1.6 s hold per line. Typing libraries use similar numbers (Typed.js back delay 700 ms; TypewriterJS pause 1500 ms).
- Only delete back to the shared start of the next line ("a "), like a person would. Typed.js calls this smart backspace.
- Show the name in the HTML from the start and animate after. Otherwise there is a flash of text, then a blank, then typing.
- Keep the untyped rest of the line in the layout with `visibility: hidden`, so a word never starts on one line and jumps to the next while it's being typed.
- Use `setTimeout`, not `requestAnimationFrame`: the delays vary per character and there are only 10 to 20 updates a second. Pause on `visibilitychange`. Skip the animation when `prefers-reduced-motion` is on, and after the first time in a visit (`sessionStorage`).

### Tabs, focus and search

- Move focus to the new tab's heading after a switch and update `document.title`. In Gatsby's user testing, screen readers announced nothing after client-side route changes when focus stayed on the clicked link (gatsbyjs.com blog, 2019 and 2020).
- Google ignores the part after `#`, so this is one indexable page. Content hidden in tabs is still indexed with full weight under mobile-first indexing, as long as it's in the HTML (seroundtable.com coverage of Google statements).
- `hidden="until-found"` keeps closed tabs searchable with Ctrl+F. The browser fires `beforematch`, and the page opens the right tab. Supported in Chrome and Edge 102+; sources disagree on Firefox and Safari, where it falls back to normal `hidden`.
- Same-document View Transitions became Baseline in October 2025 (Chrome/Edge 111, Safari 18, Firefox 144). Feature-detect `document.startViewTransition` and keep the fade short (about 200 ms).

### Presenting work and projects

- Recruiters do a first scan of about 6 to 7 seconds, mostly on name, titles, companies, dates and education (TheLadders 2012 and 2018 studies). The studies are small and vendor-run, so treat this as a rough guide. It's why Home has a four-line "Now / Before / School / Side projects" list.
- 3 to 5 bullets for most roles, 1 to 2 for old ones, numbers where possible.
- A résumé PDF linked from Home and Work is recommended. Export a real text PDF so its links work. Not done yet: needs Will's file.
- Projects: name, one line on what it is, stack, live and code links. Order by relevance, not date.
- Tone: NN/g found playful, irreverent copy reads as friendlier but less trustworthy. Keep jokes out of job details and contact info.

### Static site basics

- Open Graph image 1200×630 with absolute URL, width, height and alt, plus `twitter:card` = `summary_large_image`.
- Favicons: 32×32 `favicon.ico`, an SVG icon, and a 180×180 `apple-touch-icon.png`.
- `ProfilePage` structured data with a `Person` as `mainEntity`.
- Self-host fonts as WOFF2 with `font-display: swap`, preload with `crossorigin` so they don't download twice.
- Core Web Vitals "good" thresholds: LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1 at the 75th percentile.

## Bugs found in testing, and the fixes

Tested with Playwright at 320, 390, 768 and 1280 px, light and dark, with motion on and off, and with JavaScript off.

1. **Back button needed two presses.** Following a link into a hidden `until-found` tab also fires `beforematch`, and the handler added a second history entry. Fix: in `beforematch`, do nothing if the URL already points into that tab; otherwise use `replaceState`, not `pushState`.
2. **Big blank gap above Work and Projects.** Closed tabs with `hidden="until-found"` still take up space, and `#home`'s `min-height` (an ID selector) beat the class rule that removed it. Fix: `!important` on the collapse rule.
3. **Opening `/#home` scrolled the page down.** The browser scrolls to the element in the URL. Fix: `scroll-margin-top: 100vh` on each tab, so the target position is above the top and the browser stays at 0.
4. **Home cards invisible with reduced motion on.** The reduced-motion rule shortened animations but kept their delays, and `animation-fill-mode: both` held them at opacity 0. Fix: also set `animation-delay: 0s`.
5. **Focus ring box around headings after switching tabs.** Fix: no outline on elements focused by script (`[tabindex="-1"]:focus`). Real controls keep their focus ring; every link and button was checked with Tab.
6. **"School" shortcut changed the URL to `#work`.** A deferred `beforematch` handler ran before the browser's own hash change. Fix: check the URL synchronously instead of in a `setTimeout`.
7. **A caret as `inline-block` adds a line-break point**, so words could split at the caret. Fix: draw the caret as a zero-width left border on an inline span.
8. **Dividers with curved ends** where rounded hover cards met border lines. Gone with the cards.

## Content found while gathering

- Notion's Atlanta Braves Custom Site summary is leftover template text ("A collaborative drawing and brainstorming tool…"). Left off the site.
- Notion has two "Untitled" project rows, and several rows have no date.
- Notion links the Personal Dashboard code to `personal-dashboard`, but GitHub has `personal_dashboard` (last pushed 2024). No code link on the site.
- Georgia Tech Football 2026 moved from GitHub Pages to `gt-football.vercel.app` (an Expo app). The site uses the new link.
- Chicago Time Map, Flight Aware and Carrier Tracker came from the original spec and the GitHub repo list; they aren't in Notion.
- Other repos not on the site yet: braves-app, NHL-goal-graph, echl-bracket, chi-planner, mlb-player-stats-live, spire.

## Couldn't check

- The cloud session's network blocks the project hosts (vercel.app, netlify.app, railway.app, onrender.com, web.app, github.io), LinkedIn and photos.willyclayton.com. So the project links haven't been opened, and no real screenshots were taken. Check every link on the Vercel preview before pointing the domain.
- Find-in-page was tested by firing `beforematch` directly, not by a real Ctrl+F.

## Open items

- Pick one variation per tab from `mockups/` (5 each for Home, Work, Projects, About), then rebuild the site from that mix.
- Omni role: one line now. Needs 2 to 3 real bullets from Will.
- Résumé PDF.
- Whether to list an email address.
- Vercel deploy (preset "Other", no build command, repo root), then the GoDaddy DNS steps from the original spec. Leave the `photos` CNAME alone.
