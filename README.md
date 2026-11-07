# willyclayton.com

My personal site. One static page with four tabs (Home, Work, Projects, About), a typewriter intro, and no framework or build step.

## Files

| Path | What it is |
| --- | --- |
| `index.html` | All the content. Every tab is real HTML, so search engines and no-JS visitors see everything. |
| `assets/style.css` | Styles, light and dark themes, phone layout. |
| `assets/main.js` | Tabs, typewriter, theme toggle, project filters, testimonials. |
| `assets/fonts/` | Geist and Geist Mono (SIL Open Font License, see `LICENSE-OFL.txt`). |
| `assets/og.png` | The preview image for links shared on LinkedIn, iMessage, Slack and so on. |
| `404.html` | Shown for any URL that doesn't exist. |

## Editing

Everything you'd want to change is in `index.html`:

- **Typewriter lines:** the `lines` list near the top of the typewriter section in `assets/main.js`.
- **A new job:** copy one `<li class="role">` block in the Work section.
- **A new project:** copy one `<li class="project">` block in the Projects section. `data-tags` decides which filters it shows under: `sports`, `ai`, `maps`, `chicago`.
- **A new testimonial:** add an `<li>` to the `quote-list`.

To preview locally, run `python3 -m http.server` in this folder and open http://localhost:8000.

## How it works

- **Tabs** are plain links (`#work`, `#projects`, ...), so the back button, bookmarks and shared links all work. JavaScript shows one section at a time; without it the page is one long scroll.
- **Typewriter** shows "Will." right away, types a few lines once, then settles back on "Will." and stops. Any click or key finishes it, there's a pause button, it's skipped for people who turn on reduced motion, and it only plays once per visit.
- **Screen readers** get the full text, not half-typed words. Switching tabs moves focus to the new heading.
- **Ctrl+F** still finds text in closed tabs (in browsers that support `hidden="until-found"`) and opens the right tab.
- **Theme** follows the device setting, and the toggle remembers the visitor's choice.

## Hosting

Static files only. On Vercel: import the repo, framework preset "Other", no build command, output directory is the repo root. GitHub Pages also works from the repo root.
