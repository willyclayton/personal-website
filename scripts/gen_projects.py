"""Generate the Projects section of index.html from one list.

Run `python3 scripts/gen_projects.py` and paste its output over the
<!-- PROJECTS --> section, or ask Claude to. Each project shows its name and
a one-sentence hook; tapping it opens a screenshot, tools, why and the link.
Screenshots live in assets/projects/<key>.webp (1152x720).
"""
import html, sys

# (key, name, url, hook, built with, why)
GROUPS = [
    ('featured', [
        ('bracket-lab', 'The Bracket Lab', 'https://the-bracket-lab.vercel.app/',
         'Six AI models fill out a March Madness bracket and get scored as the games play out.',
         'Next.js, Claude, Stripe, Redis',
         'March Madness is unpredictable, which makes it a good test for AI.'),
        ('lego-it', 'Lego It', 'https://lego-it.vercel.app/',
         'Pick a Chicago building, or type any idea, and get a brick model with step-by-step instructions.',
         'React, Three.js, Claude',
         'To turn Chicago landmarks, or any idea, into a set you could actually build.'),
        ('chicago-time-map', 'Chicago Time Map', 'https://willyclayton.github.io/chicago-history/',
         "Drag a timeline from 1780 to today and watch Chicago's history appear on the map.",
         'TypeScript, MapLibre',
         "To see Chicago's history where it actually happened."),
        ('golf-fly', 'Golf Fly', 'https://willyclayton.github.io/Golf-fly/',
         "Chicago's public golf courses as a 3D yardage book you can spin around.",
         'Python, OpenStreetMap, lidar',
         'Public courses rarely have a good yardage book.'),
        ('hockey-atlas', 'Hockey Atlas', 'https://willyclayton.github.io/hockey-map/',
         'Every hockey team from the NHL to juniors on one map, linked by the players they share.',
         'D3, TopoJSON, Python, GitHub Actions',
         'To see how the hockey world connects, from the NHL down to juniors.'),
    ]),
    ('sports', [
        ('masters', 'Masters 2026', 'https://green-jacket-lab.vercel.app/',
         'AI picks, live odds and a bet tracker for the 2026 Masters.',
         'Next.js, odds API, ESPN', 'To follow the tournament and research bets.'),
        ('braves', 'Braves', 'https://braves-app.vercel.app',
         'A clean Braves app: lineup, standings and schedule, updated every morning.',
         'Expo, React Native, GitHub Actions', 'The Braves essentials without a big sports app.'),
        ('synccast', 'SyncCast', 'https://braves-sync.vercel.app',
         'Watch the Braves on TV with the radio call lined up to the picture.',
         'Next.js, Web Audio API', 'To watch the TV broadcast with the radio call.'),
        ('gt-football', 'GT Football 2026', 'https://gt-football.vercel.app',
         "Georgia Tech's roster, depth chart and playbook in one app.",
         'Expo, React Native', 'Most fan apps are paywalled or full of ads.'),
        ('georgia-swarm', 'Georgia Swarm', 'https://georgia-swarm.vercel.app/',
         "Scores, roster and highlights for Atlanta's pro lacrosse team.",
         'Next.js, GitHub Actions', 'The NLL has no good app for following one team. Idea from Johnny U.'),
        ('nhl-goal-graph', 'NHL Goal Graph', 'https://nhl-goal-graph.vercel.app',
         'Pick any two NHL players and see how they connect through goals.',
         'Next.js, D3', 'To see how any two players connect through goals.'),
        ('mlb-live', 'MLB Live Stats', 'https://mlb-player-stats-live.vercel.app',
         "Tap any player for live numbers and a stat you didn't know.",
         'Next.js, MLB Stats API', "A fun stat for whoever's at the plate."),
        ('echl', 'ECHL Bracket', 'https://echl-bracket.vercel.app',
         'The 2026 Kelly Cup playoffs, all in one bracket.',
         'HTML, Vercel', 'To follow the Kelly Cup in one place.'),
    ]),
    ('maps & travel', [
        ('only-trains', 'Only Trains', 'https://only-trains.vercel.app/',
         'Pick two points anywhere and get there using only trains and walking.',
         'Next.js, MapLibre, Transitous', 'To see how far trains alone can take you.'),
        ('carrier-tracker', 'Carrier Tracker', 'https://navy-ship-tracker.vercel.app',
         'See where the USS George Washington is right now.',
         'Next.js, Leaflet, daily cron', 'Fleet reports are hard to read. This puts them on a map.'),
        ('flightly', 'Flightly', 'https://flightly-seven.vercel.app',
         'Track your trips like Flighty Pro, for free.',
         'Next.js, Leaflet', 'Flighty Pro features without the subscription.'),
        ('flight-aware', 'Flight Aware', 'https://flight-aware.onrender.com/',
         'A live map of the planes in the sky, free to run.',
         'React, Leaflet, ADS-B data', 'FlightAware premium map features, free to run.'),
        ('all-my-flights', 'All My Flights', 'https://all-my-flights.vercel.app/',
         "Log every flight you've taken and see your stats and routes.",
         'Next.js, Recharts', 'A free, private take on a Flighty-style log.'),
    ]),
    ('chicago', [
        ('chi-this-week', 'Chi This Week', 'https://chi-planner.vercel.app',
         "What's worth doing in Chicago this week, with the weather flagged.",
         'Python, Open-Meteo', 'Event sites show everything. This shows only what I care about.'),
        ('spire', 'Spire', 'https://spire-phi.vercel.app',
         'Point your phone at the skyline to learn what each building is.',
         'React, MapLibre, phone sensors', 'To answer "what is that building?"'),
        ('wall-dashboard', 'Wall Dashboard', 'https://effortless-parfait-18ceea.netlify.app/',
         'Trains, weather and scores on a tablet by the door.',
         'HTML, CTA API', 'A use for an old Android tablet.'),
    ]),
    ('tools & ideas', [
        ('movie', 'Movie Recommender', 'https://movie-picker-seven-gilt.vercel.app',
         'Answer a few picture questions and get a movie for your mood.',
         'Next.js, TMDB', 'Most recommenders ask what you watched, not how you feel.'),
        ('beer', 'Beer Style Atlas', 'https://willyclayton.github.io/beer/',
         'Every beer style on one map of where it came from.',
         'D3, GitHub Pages', 'To see where IPA, stout and the rest came from.'),
        ('song-pics', 'Song Pics', 'https://willyclayton.github.io/song-pics/',
         "Watch a song's lyrics turn into pictures as it plays.",
         'JavaScript, LRCLIB lyrics, YouTube', 'To turn lyrics into something you watch.'),
        ('trading-bot', 'Trading Bot', 'https://trading-bot-alpha-wine.vercel.app',
         'A paper-trading simulator that proposes trades for you to approve.',
         'Python, Vercel', 'To test the plan on paper first.'),
        ('trade-assistant', 'Trade Assistant', 'https://matt-trading.onrender.com/',
         'A live checklist that tells a trader when the conditions line up.',
         'Python, Render', 'To keep the trading rules in front of you before every entry.'),
        ('filterdrop', 'FilterDrop', 'https://dad-idea.vercel.app',
         'The right AC filter, shipped to your door on schedule.',
         'Next.js, Supabase, Stripe', "My dad's business idea."),
    ]),
    ('photography', [
        ('photography', 'Photography', 'https://photos.willyclayton.com',
         '146 photos from trips, on a wall and a map.',
         'Cloudflare Pages', 'My semi-professional attempt at a photography site.'),
    ]),
]

# Camera icon so the photography group stands apart from the code projects.
CAMERA = ('<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
          '<path d="M4 8h3l1.5-2h7L17 8h3a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1Z"/>'
          '<circle cx="12" cy="13" r="3.5"/></svg>')

e = html.escape


def project(key, name, url, hook, tools, why, featured):
    thumb = (f'<img class="thumb" src="/assets/projects/{key}.webp" alt="" width="1152" height="720" decoding="async">'
             if featured else '')
    return '\n'.join([
        '      <details class="row proj">',
        f'        <summary>{thumb}<span class="t"><span class="n">{e(name)}</span><span class="hook">{e(hook)}</span></span></summary>',
        '        <div class="body">',
        f'          <a class="shot" href="{url}"><img src="/assets/projects/{key}.webp" alt="{e(name)} screenshot" width="1152" height="720" loading="lazy" decoding="async"></a>',
        f'          <dl class="facts"><div><dt>built with</dt><dd>{e(tools)}</dd></div><div><dt>why</dt><dd>{e(why)}</dd></div></dl>',
        f'          <p class="meta"><a href="{url}">open site ↗</a></p>',
        '        </div>',
        '      </details>',
    ])


out = ['  <!-- PROJECTS: generated by scripts/gen_projects.py -->',
       '  <section id="projects" class="panel" data-nosnippet aria-labelledby="projects-h">',
       '    <h2 id="projects-h" class="panel-title"><span class="sr-only">Projects</span><span class="scr" aria-hidden="true">Projects</span></h2>']
for i, (group, items) in enumerate(GROUPS):
    label = (CAMERA if group == 'photography' else '') + e(group)
    out += ['', f'    <h3 class="group{" first" if i == 0 else ""}">{label}</h3>', '    <div class="rows">']
    out += [project(*p, featured=(group == 'featured')) for p in items]
    out += ['    </div>']
out += ['  </section>', '']
sys.stdout.write('\n'.join(out))
