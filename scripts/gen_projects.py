"""Generate the Projects section of index.html from one list."""
import html, sys

# key, name, tag, url, what, built with, why ('' = left out)
TOP = [
    ('bracket-lab', 'The Bracket Lab', 'AI · sports', 'https://the-bracket-lab.vercel.app/',
     'AI models pick the March Madness bracket and get scored live.',
     'Next.js, Claude, Stripe, Redis',
     'March Madness is unpredictable, which makes it a good test for AI.'),
    ('lego-it', 'Lego It', '3D · Chicago', 'https://lego-it.vercel.app/',
     'Turns anything into a brick model you can build, with LEGO-style instructions. Starts with 21 Chicago landmarks.',
     'React, Three.js, Claude',
     'To turn Chicago landmarks, or any idea, into a set you could actually build.'),
    ('chicago-time-map', 'Chicago Time Map', 'history', 'https://willyclayton.github.io/chicago-history/',
     'Chicago history on a map, from 1780 to today.',
     'TypeScript, MapLibre',
     "To see Chicago's history where it actually happened."),
    ('golf-fly', 'Golf Fly', '3D · golf', 'https://willyclayton.github.io/Golf-fly/',
     'Chicago public courses as a 3D yardage book. In progress.', 'Python, OpenStreetMap, lidar',
     'Public courses rarely have a good yardage book.'),
]
FOLDERS = [
    ('Sports', [
        ('masters', 'Masters 2026', 'https://green-jacket-lab.vercel.app/',
         'AI picks and live betting odds for the Masters.', 'Next.js, odds API, ESPN',
         'To follow the tournament and research bets.'),
        ('braves', 'Braves', 'https://braves-app.vercel.app',
         'Lineup, standings and schedule, refreshed daily.', 'Expo, React Native, GitHub Actions',
         'The Braves essentials without a big sports app.'),
        ('synccast', 'SyncCast', 'https://braves-sync.vercel.app',
         'Syncs the Braves radio call with the TV broadcast.', 'Next.js, Web Audio API',
         'To watch the TV broadcast with the radio call.'),
        ('gt-football', 'GT Football 2026', 'https://gt-football.vercel.app',
         'Georgia Tech roster, depth chart and schedule.', 'Expo, React Native',
         'Most fan apps are paywalled or full of ads.'),
        ('georgia-swarm', 'Georgia Swarm', 'https://georgia-swarm.vercel.app/',
         'Scores, roster and highlights for an NLL team.', 'Next.js, GitHub Actions',
         "The NLL has no good app for following one team. Idea from Johnny U."),
        ('nhl-goal-graph', 'NHL Goal Graph', 'https://nhl-goal-graph.vercel.app',
         'Every NHL goal since 2010 as a scorer-goalie network.', 'Next.js, D3',
         'To see how any two players connect through goals.'),
        ('mlb-live', 'MLB Live Stats', 'https://mlb-player-stats-live.vercel.app',
         'Tap a player for live numbers and a stat fact.', 'Next.js, MLB Stats API',
         "A fun stat for whoever's at the plate."),
        ('echl', 'ECHL Bracket', 'https://echl-bracket.vercel.app',
         'The 2026 Kelly Cup playoff bracket.', 'HTML, Vercel',
         'To follow the Kelly Cup in one place.'),
    ]),
    ('Flights & maps', [
        ('carrier-tracker', 'Carrier Tracker', 'https://navy-ship-tracker.vercel.app',
         'Where the USS George Washington is right now.', 'Next.js, Leaflet, daily cron',
         'Fleet reports are hard to read. This puts them on a map.'),
        ('flightly', 'Flightly', 'https://flightly-seven.vercel.app',
         'A personal flight tracker with a live trip screen.', 'Next.js, Leaflet',
         'Flighty Pro features without the subscription.'),
        ('flight-aware', 'Flight Aware', 'https://flight-aware.onrender.com/',
         'A live map of planes overhead.', 'React, Leaflet, ADS-B data',
         'FlightAware premium map features, free to run.'),
        ('all-my-flights', 'All My Flights', 'https://all-my-flights.vercel.app/',
         'A log of every flight, with stats and a route map.', 'Next.js, Recharts',
         'A free, private take on a Flighty-style log.'),
    ]),
    ('Chicago', [
        ('chi-this-week', 'Chi This Week', 'https://chi-planner.vercel.app',
         'What to do in Chicago this week, flagged for weather.', 'Python, Open-Meteo',
         'Event sites show everything. This shows only what I care about.'),
        ('spire', 'Spire', 'https://spire-phi.vercel.app',
         'Point your phone at the skyline to name the buildings.', 'React, MapLibre, phone sensors',
         'To answer "what is that building?"'),
        ('wall-dashboard', 'Wall Dashboard', 'https://effortless-parfait-18ceea.netlify.app/',
         'Trains, weather and scores on a wall-mounted tablet.', 'HTML, CTA API',
         'A use for an old Android tablet.'),
    ]),
    ('Tools & ideas', [
        ('movie', 'Movie Recommender', 'https://movie-picker-seven-gilt.vercel.app',
         'Picks a movie from your mood, not your ratings.', 'Next.js, TMDB',
         'Most recommenders ask what you watched, not how you feel.'),
        ('trading-bot', 'Trading Bot', 'https://trading-bot-alpha-wine.vercel.app',
         'A paper-trading simulator for a swing-trading plan.', 'Python, Vercel',
         'To test the plan on paper first.'),
        ('trade-assistant', 'Trade Assistant', 'https://matt-trading.onrender.com/',
         "A trader's checklist for timing entries.", 'Python, Render',
         'To keep the trading rules in front of you before every entry.'),
        ('filterdrop', 'FilterDrop', 'https://dad-idea.vercel.app',
         'AC filters sized to your unit, delivered on schedule.', 'Next.js, Supabase, Stripe',
         "My dad's business idea."),
    ]),
]

BOTTOM = [
    ('photography', 'Photography', '146 photos', 'https://photos.willyclayton.com',
     'Photos from trips, as a wall, a map and a top-photos page.',
     'Cloudflare Pages',
     'My semi-professional attempt at a photography site.'),
]

e = html.escape


def body(key, name, url, what, tools, why, indent):
    pad = ' ' * indent
    lines = [
        f'{pad}<div class="body">',
        f'{pad}  <a class="shot" href="{url}"><img src="/assets/projects/{key}.webp" alt="{e(name)} home page" width="1152" height="720" loading="lazy" decoding="async"></a>',
        f'{pad}  <p>{e(what)}</p>',
        f'{pad}  <dl class="facts"><div><dt>built with</dt><dd>{e(tools)}</dd></div>'
        + (f'<div><dt>why</dt><dd>{e(why)}</dd></div>' if why else '') + '</dl>',
        f'{pad}  <p class="meta"><a href="{url}">open site ↗</a></p>',
        f'{pad}</div>',
    ]
    return '\n'.join(lines)


out = ['  <!-- PROJECTS: top 3 on their own, the rest in folders. Generated from one list. -->',
       '  <section id="projects" class="panel" aria-labelledby="projects-h">',
       '    <h2 id="projects-h" class="panel-title"><span class="sr-only">Projects</span><span class="scr" aria-hidden="true">Projects</span></h2>',
       '',
       '    <div class="rows">']
for key, name, tag, url, what, tools, why in TOP:
    out += ['      <details class="row">',
            f'        <summary><span class="n">{e(name)}</span><span class="y">{e(tag)}</span></summary>',
            body(key, name, url, what, tools, why, 8),
            '      </details>']
for folder, items in FOLDERS:
    out += ['', '      <details class="row folder">',
            f'        <summary><span class="n">{e(folder)}</span><span class="y">{len(items)}</span></summary>',
            '        <div class="sub">']
    for key, name, url, what, tools, why in items:
        out += ['          <details class="row">',
                f'            <summary><span class="n">{e(name)}</span><span class="y"></span></summary>',
                body(key, name, url, what, tools, why, 12),
                '          </details>']
    out += ['        </div>', '      </details>']
for key, name, tag, url, what, tools, why in BOTTOM:
    out += ['', '      <details class="row">',
            f'        <summary><span class="n">{e(name)}</span><span class="y">{e(tag)}</span></summary>',
            body(key, name, url, what, tools, why, 8),
            '      </details>']
out += ['    </div>', '  </section>', '']
sys.stdout.write('\n'.join(out))
