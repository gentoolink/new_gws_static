/* Motion layer for gentoolinkwebservices.com — see assets/css/motion.css.

   Progressive enhancement only: nothing here is needed to read the site.
   Elements are hidden for a scroll reveal only if they start below the fold,
   so nothing already on screen ever blinks out and back in, and crawlers
   (which never scroll a page into view) still get the full static HTML. */

(function () {
  'use strict';

  var doc = document.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var small = window.matchMedia('(max-width: 768px)').matches;

  /* ─── Aurora ─────────────────────────────────────────
     Curtains of light drawn as thin vertical strips, each strip offset by a
     pair of slow sine waves and brightened by faster ones so the ribbon shows
     the striations a real aurora has. Rendered at reduced resolution (which
     also gives the softness for free) and paused whenever it is off screen. */

  var PALETTES = {
    hero: [
      { rgb: '45,212,191',  y: 0.18, amp: 0.07, f: 1.0, sp: 0.16, ph: 0.0, len: 0.55, a: 0.55 },
      { rgb: '52,211,153',  y: 0.30, amp: 0.09, f: 0.7, sp: 0.11, ph: 2.1, len: 0.45, a: 0.35 },
      { rgb: '240,192,64',  y: 0.10, amp: 0.05, f: 1.4, sp: 0.21, ph: 4.2, len: 0.35, a: 0.30 },
      { rgb: '120,140,255', y: 0.24, amp: 0.06, f: 0.9, sp: 0.09, ph: 5.3, len: 0.40, a: 0.14 }
    ]
  };

  function aurora(section, strength) {
    var canvas = document.createElement('canvas');
    canvas.className = 'aurora-canvas';
    canvas.setAttribute('aria-hidden', 'true');
    section.insertBefore(canvas, section.firstChild);
    section.classList.add('has-aurora');

    var ctx = canvas.getContext('2d');
    var ribbons = PALETTES.hero;
    var scale = small ? 0.35 : 0.5;
    var step = small ? 3 : 2;
    var w = 0, h = 0, stars = [], grads = [];
    var mx = 0, tmx = 0, running = false, visible = false, t0 = performance.now();

    function resize() {
      w = Math.max(1, Math.ceil(section.clientWidth * scale));
      h = Math.max(1, Math.ceil(section.clientHeight * scale));
      canvas.width = w;
      canvas.height = h;
      grads = ribbons.map(function (r) {
        var g = ctx.createLinearGradient(0, 0, 0, h * r.len);
        g.addColorStop(0, 'rgba(' + r.rgb + ',0)');
        g.addColorStop(0.07, 'rgba(' + r.rgb + ',0.9)');
        g.addColorStop(0.22, 'rgba(' + r.rgb + ',0.35)');
        g.addColorStop(1, 'rgba(' + r.rgb + ',0)');
        return g;
      });
      var n = small ? 40 : 90;
      stars = [];
      for (var i = 0; i < n; i++) {
        stars.push({ x: Math.random() * w, y: Math.random() * h * 0.75, r: Math.random() * 0.9 + 0.2, p: Math.random() * 6.28, s: Math.random() * 1.5 + 0.5 });
      }
    }

    function frame(now) {
      var t = (now - t0) / 1000;
      mx += (tmx - mx) * 0.04;
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.clearRect(0, 0, w, h);

      ctx.globalCompositeOperation = 'source-over';
      for (var s = 0; s < stars.length; s++) {
        var st = stars[s];
        ctx.globalAlpha = 0.25 + 0.55 * (0.5 + 0.5 * Math.sin(t * st.s + st.p));
        ctx.fillStyle = '#fff';
        ctx.fillRect(st.x - mx * 6, st.y, st.r, st.r);
      }

      ctx.globalCompositeOperation = 'lighter';
      for (var k = 0; k < ribbons.length; k++) {
        var r = ribbons[k];
        ctx.fillStyle = grads[k];
        var colH = h * r.len;
        for (var x = 0; x < w; x += step) {
          var nx = x / w;
          var y = h * (r.y
            + r.amp * Math.sin(nx * 5.2 * r.f + t * r.sp + r.ph + mx * 0.6)
            + r.amp * 0.45 * Math.sin(nx * 12.5 * r.f - t * r.sp * 1.8 + r.ph * 1.7));
          var envelope = 0.5 + 0.5 * Math.sin(nx * 2.6 + t * 0.07 + r.ph);
          var rays = 0.55 + 0.45 * Math.sin(nx * 46 + t * 0.9 + r.ph) * Math.sin(nx * 19 - t * 0.5);
          var a = envelope * envelope * rays * r.a * strength;
          if (a < 0.01) continue;
          ctx.globalAlpha = a;
          ctx.setTransform(1, 0, 0, 1, 0, y);
          ctx.fillRect(x, 0, step + 0.5, colH);
        }
      }
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.globalAlpha = 1;

      if (running) requestAnimationFrame(frame);
    }

    function start() {
      if (running || reduce || !visible || document.hidden) return;
      running = true;
      requestAnimationFrame(frame);
    }
    function stop() { running = false; }

    // Paint one still frame straight away (and after every resize, which
    // clears the canvas) so the hero is never blank while the loop is paused
    // in a background tab or has not started yet.
    resize();
    frame(t0 + 14000);
    setTimeout(function () { canvas.classList.add('is-on'); }, 30);

    new IntersectionObserver(function (entries) {
      visible = entries[0].isIntersecting;
      visible ? start() : stop();
    }).observe(section);

    document.addEventListener('visibilitychange', function () {
      document.hidden ? stop() : start();
    });

    var rt;
    window.addEventListener('resize', function () {
      clearTimeout(rt);
      rt = setTimeout(function () { resize(); if (!running) frame(performance.now()); }, 150);
    });

    if (finePointer) {
      window.addEventListener('pointermove', function (e) {
        tmx = (e.clientX / window.innerWidth) * 2 - 1;
      }, { passive: true });
    }
  }

  document.querySelectorAll('main > section#hero, main > section#cta').forEach(function (s) {
    aurora(s, s.id === 'hero' ? 1 : 0.7);
  });

  if (reduce) return;

  /* ─── Scroll progress and nav ─────────────────────── */

  var bar = document.createElement('div');
  bar.className = 'scroll-progress';
  bar.setAttribute('aria-hidden', 'true');
  document.body.appendChild(bar);
  var nav = document.querySelector('body > nav');
  var ticking = false;

  function onScroll() {
    ticking = false;
    var max = doc.scrollHeight - window.innerHeight;
    bar.style.transform = 'scaleX(' + (max > 0 ? Math.min(1, window.scrollY / max) : 0) + ')';
    if (nav) nav.classList.toggle('is-scrolled', window.scrollY > 40);
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; requestAnimationFrame(onScroll); }
  }, { passive: true });
  onScroll();

  /* ─── Scroll reveal ───────────────────────────────── */

  var GROUPS = '.never-list ul, .services-grid, .audit-grid, .door-grid, .quote-bar, .review-grid, .objections-list, .compare-grid, .link-chips, .steps, .post-grid, .stats-bar';
  var SINGLES = [
    'main section:not(#hero) .section-label',
    'main section:not(#hero) h2',
    'main section:not(#hero) .lead',
    'main section:not(#hero) .hook',
    'main section:not(#hero) .chips-label',
    'main section:not(#hero) .plan-note',
    'main section:not(#hero) .cta-center',
    '.prose-dark h2',
    '.video-embed',
    '.article-cta-box'
  ].join(',');

  var fold = window.innerHeight * 0.92;
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      var el = en.target;
      io.unobserve(el);
      el.classList.add('in');
      var d = parseFloat(el.style.getPropertyValue('--d')) || 0;
      setTimeout(function () {
        el.classList.remove('rv', 'rv-blur', 'rv-left', 'rv-right', 'rv-pop');
        el.classList.add('rv-done');
      }, 1000 + d * 1000);
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });

  function prime(el, delay, variant) {
    if (el.closest('#hero') || el.classList.contains('rv')) return;
    if (el.getBoundingClientRect().top < fold) return;
    el.classList.add('rv');
    if (variant) el.classList.add(variant);
    el.style.setProperty('--d', delay.toFixed(2) + 's');
    io.observe(el);
  }

  document.querySelectorAll(GROUPS).forEach(function (g) {
    var kids = Array.prototype.slice.call(g.children);
    // Slide in from the sides only when the pair really sits side by side;
    // stacked on a phone, a sideways start would push the page wider.
    var two = kids.length === 2 && g.matches('.compare-grid, .door-grid, .quote-bar') &&
      kids[0].offsetTop === kids[1].offsetTop;
    kids.forEach(function (el, i) {
      var variant = two ? (i === 0 ? 'rv-left' : 'rv-right') : (g.matches('.link-chips, .never-list ul') ? 'rv-pop' : null);
      var per = g.matches('.link-chips') ? 0.035 : g.matches('.never-list ul') ? 0.12 : 0.09;
      prime(el, Math.min(i * per, 0.6), variant);
    });
  });

  var bySection = new Map();
  document.querySelectorAll(SINGLES).forEach(function (el) {
    var host = el.closest('section, .article-wrap') || document.body;
    var n = bySection.get(host) || 0;
    bySection.set(host, n + 1);
    prime(el, Math.min(n * 0.07, 0.35), el.tagName === 'H2' ? 'rv-blur' : null);
  });

  /* ─── Count-ups ───────────────────────────────────── */

  function countUp(el) {
    var text = el.textContent;
    var m = text.match(/^([^\d]*)([\d,]*\.?\d+)(.*)$/);
    if (!m) return;
    var pre = m[1], raw = m[2], post = m[3];
    var commas = raw.indexOf(',') > -1;
    var target = parseFloat(raw.replace(/,/g, ''));
    var dec = (raw.split('.')[1] || '').length;
    var dur = 1700, t0 = null;
    el.style.minWidth = el.offsetWidth + 'px';
    el.style.display = 'inline-block';
    function fmt(v) {
      var s = v.toFixed(dec);
      if (commas) s = s.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
      return pre + s + post;
    }
    function tick(now) {
      if (!t0) t0 = now;
      var p = Math.min(1, (now - t0) / dur);
      var e = 1 - Math.pow(2, -10 * p);
      el.textContent = fmt(target * (p === 1 ? 1 : e));
      if (p < 1) requestAnimationFrame(tick);
      else el.textContent = text;
    }
    requestAnimationFrame(tick);
  }

  var cio = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      cio.unobserve(en.target);
      countUp(en.target);
    });
  }, { threshold: 0.8 });
  document.querySelectorAll('[data-count]').forEach(function (el) { cio.observe(el); });

  if (!finePointer) return;

  /* ─── Card spotlight and tilt ─────────────────────── */

  var CARDS = '.service-card, .audit-section, .door-card, .review-card, .quote-card, .compare-col, .objection, .post-card, .tier-card, .agent-console';

  document.querySelectorAll(CARDS).forEach(function (card) {
    card.classList.add('fx-card');
    var max = card.classList.contains('agent-console') ? 7 : 5;
    var raf = 0, px = 0.5, py = 0.5;

    function apply() {
      raf = 0;
      card.style.setProperty('--mx', (px * 100).toFixed(1) + '%');
      card.style.setProperty('--my', (py * 100).toFixed(1) + '%');
      if (card.classList.contains('rv')) return;
      var rx = (0.5 - py) * max, ry = (px - 0.5) * max;
      card.style.transform = 'perspective(1000px) rotateX(' + rx.toFixed(2) + 'deg) rotateY(' + ry.toFixed(2) + 'deg) translateY(-3px)';
    }

    card.addEventListener('pointerenter', function () {
      card.style.setProperty('--glow', '1');
      card.style.transition = 'transform 0.12s ease-out, border-color 0.2s, box-shadow 0.25s';
      card.classList.add('fx-tilting');
    });
    card.addEventListener('pointermove', function (e) {
      var r = card.getBoundingClientRect();
      px = (e.clientX - r.left) / r.width;
      py = (e.clientY - r.top) / r.height;
      if (!raf) raf = requestAnimationFrame(apply);
    });
    card.addEventListener('pointerleave', function () {
      card.style.setProperty('--glow', '0');
      card.style.transition = 'transform 0.6s cubic-bezier(0.2, 0.7, 0.2, 1), border-color 0.2s, box-shadow 0.25s';
      card.style.transform = '';
      card.classList.remove('fx-tilting');
    });
  });

  /* ─── Magnetic buttons ────────────────────────────── */

  document.querySelectorAll('.btn-primary, .btn-secondary, .nav-cta, .email-fab').forEach(function (btn) {
    btn.classList.add('magnetic');
    btn.addEventListener('pointermove', function (e) {
      var r = btn.getBoundingClientRect();
      var dx = e.clientX - (r.left + r.width / 2);
      var dy = e.clientY - (r.top + r.height / 2);
      btn.style.transform = 'translate(' + (dx * 0.18).toFixed(1) + 'px,' + (dy * 0.3 - 2).toFixed(1) + 'px)';
    });
    btn.addEventListener('pointerleave', function () { btn.style.transform = ''; });
  });
})();
