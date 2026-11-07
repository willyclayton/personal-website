# willyclayton.com

My personal site. One static page with four tabs (Home, Work, Projects, About) and no framework or build step. Home is only the typewriter hello; everything else is one click away.

## Files

| Path | What it is |
| --- | --- |
| `index.html` | All the content. Every tab is real HTML, so search engines and no-JS visitors see everything. |
| `assets/style.css` | Styles, light and dark themes, phone layout. |
| `assets/main.js` | Tabs, typewriter, theme toggle, testimonials. |
| `assets/fonts/` | Geist and Geist Mono (SIL Open Font License, see `LICENSE-OFL.txt`). |
| `assets/og.png` | The preview image for links shared on LinkedIn, iMessage, Slack and so on. |
| `404.html` | Shown for any URL that doesn't exist. |

## Editing

Everything you'd want to change is in `index.html`:

- **Typewriter lines:** the `lines` list near the top of the typewriter section in `assets/main.js`.
- **A new job:** copy one `<li class="role">` block in the Work section.
- **A new project:** copy one `<li>` block in the Projects list.
- **A new testimonial:** add an `<li>` to the `quote-list`.

To preview locally, run `python3 -m http.server` in this folder and open http://localhost:8000.

## How it works

- **Tabs** are plain links (`#work`, `#projects`, ...), so the back button, bookmarks and shared links all work. JavaScript shows one section at a time; without it the page is one long scroll.
- **Typewriter** shows "Will." right away, types a few lines once, then settles back on "Will." and stops. Any click or key finishes it, there's a pause button, it's skipped for people who turn on reduced motion, and it only plays once per visit.
- **Screen readers** get the full text, not half-typed words. Switching tabs moves focus to the new heading.
- **Ctrl+F** still finds text in closed tabs (in browsers that support `hidden="until-found"`) and opens the right tab.
- **Theme** follows the device setting, and the toggle remembers the visitor's choice.

## Mockups

`mockups/` has five design variations for each tab (Home, Work, Projects, About), all using the real content. Open `mockups/index.html` in a browser, or visit `/mockups/` once deployed. The folder isn't linked from the site and is blocked in `robots.txt`.

## Hosting

Static files only, hosted on Vercel (why: see `LEARNINGS.md`).

1. In Vercel, import `willyclayton/personal-website`. Framework preset "Other", no build command, output directory is the repo root.
2. Settings → Domains: add `willyclayton.com` and `www.willyclayton.com`, with www redirecting to the root.
3. At GoDaddy: turn off the forwarding to Notion, set the `@` A record to the value Vercel shows (usually `76.76.21.21`), delete any `@` AAAA records, and point the `www` CNAME at the target Vercel shows. Leave the `photos` CNAME alone.
