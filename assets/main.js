// willyclayton.com: tabs, typewriter, theme, testimonials.
// Everything is plain DOM. With JavaScript off, every section still shows.
(() => {
  const root = document.documentElement;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  /* ---------------- Tabs (hash routing) ---------------- */

  const TABS = ['home', 'work', 'projects', 'about'];
  const TITLES = {
    home: 'Will Clayton',
    work: 'Work · Will Clayton',
    projects: 'Projects · Will Clayton',
    about: 'About · Will Clayton',
  };
  const panels = {};
  TABS.forEach((id) => { panels[id] = document.getElementById(id); });
  const nav = document.querySelector('.tabs');
  const tabLinks = Array.from(nav.querySelectorAll('a[data-tab]'));
  const ink = document.createElement('span');
  ink.className = 'ink';
  ink.setAttribute('aria-hidden', 'true');
  nav.prepend(ink);

  let current = null;

  // Browsers that support hidden="until-found" let Ctrl+F find text in closed tabs.
  const untilFound = 'onbeforematch' in document.body;

  function resolve(hash) {
    let id = '';
    try { id = decodeURIComponent((hash || '').replace(/^#/, '')); } catch (e) {}
    if (!id) return { tab: 'home', target: null };
    if (panels[id]) return { tab: id, target: null };
    const el = document.getElementById(id);
    if (!el) return { tab: 'home', target: null };
    const panel = el.closest('.panel');
    // Links outside the tabs (like "Skip to content") keep the current tab.
    if (!panel) return { tab: current || 'home', target: null, passthrough: true };
    return { tab: panel.id, target: el };
  }

  function setHidden(panel, hide) {
    if (!hide) panel.removeAttribute('hidden');
    else panel.setAttribute('hidden', untilFound ? 'until-found' : '');
  }

  function moveInk(instant) {
    const link = tabLinks.find((a) => a.dataset.tab === current);
    if (!link) return;
    if (instant) ink.style.transition = 'none';
    ink.style.width = link.offsetWidth + 'px';
    ink.style.transform = 'translateX(' + link.offsetLeft + 'px)';
    if (instant) {
      ink.getBoundingClientRect();
      ink.style.transition = '';
    }
  }

  // Tab change: children blur in one after another, and the title decodes.
  const GLYPHS = '01/\\_-=+*<>#';
  function scramble(el) {
    const text = el.dataset.text || (el.dataset.text = el.textContent);
    if (reduceMotion.matches) { el.textContent = text; return; }
    const start = performance.now();
    const dur = 420;
    const frame = (now) => {
      const p = Math.min(1, (now - start) / dur);
      const fixed = Math.floor(p * text.length);
      el.textContent = text.slice(0, fixed) + [...text.slice(fixed)].map((c) => (c === ' ' ? ' ' : GLYPHS[Math.floor(Math.random() * GLYPHS.length)])).join('');
      if (p < 1) requestAnimationFrame(frame);
    };
    requestAnimationFrame(frame);
  }
  function stagger(panel) {
    Array.from(panel.children).forEach((child, i) => {
      child.style.setProperty('--i', Math.min(i, 10));
    });
    panel.classList.remove('entering');
    void panel.offsetWidth;
    panel.classList.add('entering');
    const t = panel.querySelector('.scr');
    if (t) scramble(t);
  }

  function show(hash, opts) {
    const o = opts || {};
    const { tab, target, passthrough } = resolve(hash);
    if (passthrough && !o.initial) return;
    const changed = tab !== current;
    const panel = panels[tab];
    const focusEl = target || panel.querySelector('h1, h2');
    // Find-in-page (Ctrl+F) opens a tab itself and scrolls to the match: don't fight it.
    const quiet = o.initial || o.fromFind;
    const useVT = false; // our own blur-in replaces the browser crossfade

    const swap = () => {
      TABS.forEach((id) => setHidden(panels[id], id !== tab));
      tabLinks.forEach((a) => {
        if (a.dataset.tab === tab) a.setAttribute('aria-current', 'page');
        else a.removeAttribute('aria-current');
      });
      current = tab;
      document.title = TITLES[tab];
      // Inside a view transition the marker jumps and the transition animates it.
      moveInk(o.initial || useVT);
      if (target) target.scrollIntoView({ block: 'start' });
      else if (!quiet) window.scrollTo(0, 0);
      if (changed && !quiet) stagger(panel);
    };

    const settle = () => {
      if (!quiet && focusEl) {
        // Move focus to the new heading so keyboard and screen reader users land there.
        if (!focusEl.hasAttribute('tabindex')) focusEl.setAttribute('tabindex', '-1');
        focusEl.focus({ preventScroll: true });
      }
      if (tab === 'home') typer.resume();
      else typer.hold();
    };

    if (useVT) {
      document.startViewTransition(swap).updateCallbackDone.then(settle, settle);
    } else {
      swap();
      settle();
    }
  }

  if (untilFound) {
    TABS.forEach((id) => {
      panels[id].addEventListener('beforematch', () => {
        // Following a link into this tab also fires this event. The URL already
        // points here in that case, and the hashchange handler takes care of it.
        if (location.hash && resolve(location.hash).tab === id) return;
        // Otherwise it's a Ctrl+F match: show the tab without adding history.
        history.replaceState(null, '', '#' + id);
        show('#' + id, { fromFind: true });
      });
    });
  }

  /* ---------------- Typewriter ---------------- */

  const typer = (() => {
    const heading = document.querySelector('.type');
    const typedEl = heading.querySelector('.typed');
    const restEl = heading.querySelector('.rest');
    const toggle = document.querySelector('.type-toggle');
    const NAME = 'Will.';
    // Typed in order after the name, then it settles back on the name and stops.
    // Keep each line to 21 characters or fewer so it fits the reserved width.
    const lines = [
      'a solutions engineer.',
      'a Georgia Tech grad.',
      'based in Chicago.',
      'a Braves fan.',
      'a golfer.',
      'an OK golfer.',
      'a skier.',
      'a DIY-er.',
      'a tinkerer.',
      'a problem solver.',
      'a lifelong learner.',
      NAME,
    ];
    const BASE = 55;      // ms per character, plus up to JITTER of randomness
    const JITTER = 45;
    const PUNCT = 260;    // a beat after punctuation
    const ERASE = 30;
    const HOLD = 1300;    // how long each line stays up
    const FIRST = 1500;   // how long the name stays up before the first line

    let timer = 0;
    let pending = null;
    let started = false;
    let finished = false;
    let paused = false;
    let onHome = false;

    // [typed][caret][invisible rest]: the rest holds its space so lines never reflow.
    const afterEl = heading.querySelector('.after');
    function render(text, i) {
      typedEl.textContent = text.slice(0, i);
      if (afterEl) afterEl.textContent = '';
      restEl.textContent = text.slice(i);
    }
    // Caret in the middle of visible text, for edits like "a golfer." -> "an OK golfer."
    function renderMid(before, after) {
      typedEl.textContent = before;
      afterEl.textContent = after;
      restEl.textContent = '';
    }
    function setToggle(label, aria) {
      if (!toggle) return;
      toggle.textContent = label;
      toggle.setAttribute('aria-label', aria);
    }
    const blocked = () => paused || document.hidden || !onHome;
    // One pending step at a time; nothing runs while paused, hidden or on another tab.
    function at(ms, fn) {
      clearTimeout(timer);
      pending = fn;
      if (!blocked()) timer = setTimeout(() => { pending = null; fn(); }, ms);
    }
    const pace = (ch) => (/[.,!?]/.test(ch) ? PUNCT : BASE + Math.random() * JITTER);
    const common = (a, b) => { let k = 0; while (k < a.length && a[k] === b[k]) k += 1; return k; };

    function type(text, i, then) {
      render(text, i);
      heading.classList.add('typing');
      if (i < text.length) at(pace(text[i - 1] || ''), () => type(text, i + 1, then));
      else { heading.classList.remove('typing'); then(); }
    }
    function erase(text, i, stop, then) {
      render(text, i);
      heading.classList.add('typing');
      if (i > stop) at(ERASE, () => erase(text, i - 1, stop, then));
      else then();
    }
    function next(prev, n) {
      const text = lines[n];
      // Only delete back to what the two lines share ("a "), like a person would.
      const k = common(prev, text);
      const done = () => {
        if (n === lines.length - 1) finish();
        else at(HOLD, () => next(text, n + 1));
      };
      // If the new line is the old one with words added in the middle, move the
      // caret back and insert them instead of deleting ("a golfer." -> "an OK golfer.").
      const tail = prev.slice(k);
      const insert = text.slice(k, text.length - tail.length);
      if (afterEl && tail && insert && text.endsWith(tail)) {
        heading.classList.add('typing');
        const back = (i) => {
          renderMid(prev.slice(0, i), prev.slice(i));
          if (i > k) at(45, () => back(i - 1));
          else at(250, () => ins(1));
        };
        const ins = (j) => {
          renderMid(text.slice(0, k + j), tail);
          if (j < insert.length) at(pace(insert[j - 1]), () => ins(j + 1));
          else { heading.classList.remove('typing'); render(text, text.length); done(); }
        };
        return back(prev.length);
      }
      erase(prev, prev.length, k, () => at(200, () => type(text, k, done)));
    }

    function finish() {
      if (finished) return;
      clearTimeout(timer);
      pending = null;
      finished = true;
      render(NAME, NAME.length);
      heading.classList.remove('typing');
      heading.classList.add('done');
      setToggle('replay', 'Replay the typing animation');
    }
    function start() {
      started = true;
      finished = false;
      paused = false;
      heading.classList.remove('done');
      render(NAME, NAME.length);
      setToggle('pause', 'Pause the typing animation');
      at(FIRST, () => next(NAME, 0));
    }

    if (toggle) {
      toggle.addEventListener('click', () => {
        if (finished) start();
        else if (paused) {
          paused = false;
          setToggle('pause', 'Pause the typing animation');
          if (pending) at(200, pending);
        } else {
          paused = true;
          clearTimeout(timer);
          heading.classList.remove('typing');
          setToggle('play', 'Resume the typing animation');
        }
      });
    }

    // Any tap, click or key press (other than on the pause button) finishes it at once.
    const skip = (e) => {
      if (!started || finished || (toggle && toggle.contains(e.target))) return;
      finish();
    };
    document.addEventListener('pointerdown', skip);
    document.addEventListener('keydown', skip);
    reduceMotion.addEventListener('change', (e) => { if (e.matches) finish(); });
    // Don't type in a background tab; pick up where it left off on return.
    document.addEventListener('visibilitychange', () => {
      if (finished) return;
      if (document.hidden) clearTimeout(timer);
      else if (pending) at(300, pending);
    });

    return {
      // Called whenever the Home tab is shown: types every time you land on Home.
      resume() {
        onHome = true;
        if (!started || finished) return start();
        if (pending) at(250, pending);
      },
      // Called when another tab is shown.
      hold() {
        onHome = false;
        clearTimeout(timer);
      },
    };
  })();

  /* ---------------- Theme toggle ---------------- */

  const themeBtn = document.querySelector('.theme');
  const darkQuery = window.matchMedia('(prefers-color-scheme: dark)');
  const metaThemes = document.querySelectorAll('meta[name="theme-color"]');

  function effectiveTheme() {
    return root.dataset.theme || (darkQuery.matches ? 'dark' : 'light');
  }
  function syncThemeUI() {
    const t = effectiveTheme();
    themeBtn.setAttribute('aria-label', t === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
    metaThemes.forEach((m) => m.setAttribute('content', t === 'dark' ? '#0b0b0c' : '#ffffff'));
  }
  themeBtn.addEventListener('click', () => {
    const next = effectiveTheme() === 'dark' ? 'light' : 'dark';
    root.dataset.theme = next;
    try { localStorage.setItem('theme', next); } catch (e) {}
    syncThemeUI();
  });
  darkQuery.addEventListener('change', syncThemeUI);
  syncThemeUI();

  /* ---------------- Top bar border on scroll ---------------- */

  const bar = document.querySelector('.bar');
  const onScroll = () => bar.classList.toggle('scrolled', window.scrollY > 4);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------------- Testimonials: one at a time ---------------- */

  const quotes = document.querySelector('.quotes');
  if (quotes) {
    const items = Array.from(quotes.querySelectorAll('.quote-list li'));
    const list = quotes.querySelector('.quote-list');
    const controls = document.createElement('div');
    controls.className = 'deck-controls';
    controls.innerHTML = '<button type="button">another one</button>';
    list.after(controls);
    list.setAttribute('aria-live', 'polite');
    let i = Math.floor(Math.random() * items.length);
    const render = () => {
      items.forEach((li, n) => li.classList.toggle('on', n === i));
    };
    controls.querySelector('button').addEventListener('click', () => {
      i = (i + 1) % items.length;
      render();
    });
    quotes.classList.add('deck');
    render();
  }

  /* ---------------- Start ---------------- */

  window.addEventListener('hashchange', () => show(location.hash));
  window.addEventListener('resize', () => moveInk(true));
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => moveInk(true));
  show(location.hash, { initial: true });
})();
