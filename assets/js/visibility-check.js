/* AI Visibility Readiness self-check.
   Three self-reported answers, fixed weights, arithmetic shown to the user.
   This scores readiness, not visibility — the paid audit is what actually
   queries ChatGPT, Perplexity, and Google AI Overviews. Keep that line
   intact if this file is edited; it is the difference between a lead
   magnet and a claim we can't stand behind.

   Results are shareable by URL (?vc=40-15-0). The link carries the three
   answers and nothing else — no name, no email, no site address. Keep it
   that way: a shared score is a conversation starter, not a record about
   somebody, and anything identifying would end up in browser history,
   chat logs, and referrer headers. Inbound values are validated against
   the allowed set below, because a query string is user-editable and a
   hand-crafted ?vc=999-999-999 must not render as a real score. */
(function () {
  var form = document.getElementById('vc-form');
  if (!form) return;

  var result = document.getElementById('vc-result');
  var errorEl = document.getElementById('vc-error');

  var NAMES = ['q1', 'q2', 'q3'];

  var LABELS = {
    q1: 'Bing indexing',
    q2: 'Google Business Profile',
    q3: 'Structured data'
  };

  /* The only point values each question can legitimately produce. */
  var ALLOWED = {
    q1: [40, 15, 0],
    q2: [35, 15, 0],
    q3: [25, 10, 0]
  };

  var BANDS = [
    {
      min: 85,
      name: 'Well positioned',
      tone: 'good',
      note: 'You have the three foundations covered. Honestly, at this score the $1,000 audit is unlikely to pay for itself — the gaps it finds would be small ones. Re-check in six months, or after any site rebuild.'
    },
    {
      min: 60,
      name: 'Mostly there',
      tone: 'ok',
      note: 'The foundations are largely in place, so the remaining gaps are worth fixing directly rather than investigating. Start with whichever line below scored lowest.'
    },
    {
      min: 30,
      name: 'Partly readable',
      tone: 'warn',
      note: 'Some of the groundwork is done and some of it isn’t, which usually means a machine reading your site gets a partial answer about your business. The lines below show where the points went missing.'
    },
    {
      min: 0,
      name: 'Likely invisible',
      tone: 'bad',
      note: 'On these answers, an AI assistant asked to recommend a business in your category and town has little to work with. All three are fixable, and the order matters: Bing indexing first, profile second, markup third.'
    }
  ];

  function band(score, bingBlocked) {
    var b = BANDS[BANDS.length - 1];
    for (var i = 0; i < BANDS.length; i++) {
      if (score >= BANDS[i].min) { b = BANDS[i]; break; }
    }
    /* A site Bing doesn't have can't be cited by ChatGPT Search, whatever the
       other two answers are — so a zero there caps the verdict. Without this
       a 0/35/25 answer scores 60 and reads "Mostly there", which contradicts
       the question copy calling Bing the hardest gate. */
    if (bingBlocked && score >= 60) b = BANDS[2];
    return b;
  }

  function inputFor(name, value) {
    return form.querySelector('input[name="' + name + '"][value="' + value + '"]');
  }

  function el(tag, className, text) {
    var n = document.createElement(tag);
    if (className) n.className = className;
    if (text != null) n.textContent = text;
    return n;
  }

  /* ── scoring ─────────────────────────────────────────── */

  function score(values) {
    var total = 0;
    var unsure = 0;
    var rows = [];
    for (var i = 0; i < NAMES.length; i++) {
      var name = NAMES[i];
      var v = values[i];
      var input = inputFor(name, v);
      total += v;
      if (input && input.getAttribute('data-unsure') === 'true') unsure++;
      rows.push({ name: name, got: v, max: ALLOWED[name][0] });
    }
    var bingBlocked = values[0] === 0;
    return { total: total, unsure: unsure, rows: rows, bingBlocked: bingBlocked, band: band(total, bingBlocked) };
  }

  function meterAndRows(target, s) {
    var head = el('div', 'vc-score-head');
    var num = el('div', 'vc-score-num');
    num.appendChild(el('span', 'vc-score-value', String(s.total)));
    num.appendChild(el('span', 'vc-score-max', '/100'));
    head.appendChild(num);
    head.appendChild(el('div', 'vc-band vc-band-' + s.band.tone, s.band.name));
    target.appendChild(head);

    var meter = el('div', 'vc-meter');
    var fill = el('div', 'vc-meter-fill vc-band-' + s.band.tone);
    meter.appendChild(fill);
    target.appendChild(meter);

    var list = el('ul', 'vc-breakdown');
    for (var i = 0; i < s.rows.length; i++) {
      var r = s.rows[i];
      var cls = r.got === r.max ? 'vc-row vc-row-full' : (r.got === 0 ? 'vc-row vc-row-zero' : 'vc-row vc-row-part');
      var row = el('li', cls);
      row.appendChild(el('span', 'vc-row-label', LABELS[r.name]));
      row.appendChild(el('span', 'vc-row-pts', r.got + ' / ' + r.max));
      list.appendChild(row);
    }
    target.appendChild(list);

    /* Force a reflow at width 0, then set the real width, so the bar animates
       on every run including re-runs. Done synchronously rather than in a
       requestAnimationFrame: rAF is throttled in background tabs, which left
       the bar stuck empty. */
    fill.style.width = '0%';
    void fill.offsetWidth;
    fill.style.width = s.total + '%';
  }

  /* ── sharing ─────────────────────────────────────────── */

  function shareUrl(values) {
    var path = window.location.pathname.replace(/index\.html$/, '');
    return window.location.origin + path + '?vc=' + values.join('-') + '#visibility-check';
  }

  function parseShared() {
    var m = /[?&]vc=([^&#]+)/.exec(window.location.search);
    if (!m) return null;
    var parts = decodeURIComponent(m[1]).split('-');
    if (parts.length !== 3) return null;
    var values = [];
    for (var i = 0; i < NAMES.length; i++) {
      /* Digits only — parseInt would happily read "40.5" as 40 and render a
         score the link doesn't actually say. */
      if (!/^\d{1,3}$/.test(parts[i])) return null;
      var v = parseInt(parts[i], 10);
      /* Reject anything that isn't a value this question can actually award. */
      if (ALLOWED[NAMES[i]].indexOf(v) === -1) return null;
      values.push(v);
    }
    return values;
  }

  function track(event, params) {
    if (typeof gtag === 'function') gtag('event', event, params);
  }

  function buildShareBlock(values) {
    var url = shareUrl(values);
    var wrap = el('div', 'vc-share');

    wrap.appendChild(el('h3', 'vc-share-title', 'Send this to another owner'));
    wrap.appendChild(el('p', 'vc-share-copy',
      'Know someone who would stall on question one? Most owners have never checked any of this. The link carries your three answers and nothing else — no name, no email, no website address — so it is a conversation starter, not a record about you.'));

    var row = el('div', 'vc-share-row');

    var field = el('input', 'vc-share-url');
    field.type = 'text';
    field.readOnly = true;
    field.value = url;
    field.setAttribute('aria-label', 'Link to this result');
    field.addEventListener('focus', function () { field.select(); });
    row.appendChild(field);

    var copyBtn = el('button', 'btn-secondary vc-share-btn', 'Copy link');
    copyBtn.type = 'button';
    copyBtn.addEventListener('click', function () {
      function done() {
        copyBtn.textContent = 'Copied';
        setTimeout(function () { copyBtn.textContent = 'Copy link'; }, 2200);
        track('visibility_check_share', { method: 'copy', score: values[0] + values[1] + values[2] });
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(done, function () { field.focus(); field.select(); });
      } else {
        field.focus();
        field.select();
        try { document.execCommand('copy'); done(); } catch (e) { /* leave it selected to copy by hand */ }
      }
    });
    row.appendChild(copyBtn);

    /* Native share sheet where the browser has one — mobile, mostly. */
    if (navigator.share) {
      var shareBtn = el('button', 'btn-secondary vc-share-btn', 'Share');
      shareBtn.type = 'button';
      shareBtn.addEventListener('click', function () {
        navigator.share({
          title: 'AI visibility self-check',
          text: 'I scored ' + (values[0] + values[1] + values[2]) + '/100 on this 60-second check. How would your business do?',
          url: url
        }).then(function () {
          track('visibility_check_share', { method: 'native', score: values[0] + values[1] + values[2] });
        }, function () { /* dismissed */ });
      });
      row.appendChild(shareBtn);
    }

    wrap.appendChild(row);
    return wrap;
  }

  /* ── inbound shared result ───────────────────────────── */

  function showSharedBanner(values) {
    var s = score(values);
    var box = el('div', 'vc-shared');
    box.setAttribute('role', 'note');

    box.appendChild(el('div', 'vc-shared-label', 'Someone shared their result with you'));
    meterAndRows(box, s);
    box.appendChild(el('p', 'vc-shared-note',
      'These are their own answers, passed along in the link — not a measurement of their website, and not something we verified. The interesting question is the one below: how would yours score?'));

    var jump = el('button', 'btn-primary vc-shared-cta', 'Take the 60-second check');
    jump.type = 'button';
    jump.addEventListener('click', function () {
      var first = form.querySelector('input[name="q1"]');
      form.scrollIntoView({ behavior: 'smooth', block: 'start' });
      if (first) first.focus({ preventScroll: true });
    });
    box.appendChild(jump);

    form.parentNode.insertBefore(box, form);
    track('visibility_check_shared_view', { score: s.total, band: s.band.name });
  }

  /* ── own result ──────────────────────────────────────── */

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    var values = [];
    for (var i = 0; i < NAMES.length; i++) {
      var input = form.querySelector('input[name="' + NAMES[i] + '"]:checked');
      if (!input) {
        errorEl.hidden = false;
        return;
      }
      values.push(parseInt(input.value, 10));
    }
    errorEl.hidden = true;

    var s = score(values);

    /* Rebuild the result panel from scratch each run so re-answering is clean. */
    result.textContent = '';
    meterAndRows(result, s);
    result.appendChild(el('p', 'vc-note', s.band.note));

    if (s.bingBlocked) {
      result.appendChild(el('p', 'vc-unsure',
        'Whatever else is in place, a site Bing hasn’t indexed can’t turn up in ChatGPT Search — that index is where it looks. Bing Webmaster Tools is free and submitting a sitemap takes about ten minutes; do that one first.'));
    }

    if (s.unsure > 0) {
      result.appendChild(el('p', 'vc-unsure',
        s.unsure === 3
          ? 'You answered “don’t know” to all three. That is the most common result, and it is not a failing grade — nobody checks these unprompted. But unverified counts as unready, because an AI assistant reads what is actually there, not what you assume is there.'
          : 'You answered “don’t know” on ' + s.unsure + ' of the 3. Unverified counts as unready here, because an AI assistant reads what is actually there, not what you assume is there.'));
    }

    var cta = el('div', 'vc-cta');
    if (s.total >= 85) {
      var secondary = el('a', 'btn-secondary', 'See what the audit covers →');
      secondary.href = 'ai-visibility-audit.html';
      cta.appendChild(secondary);
    } else {
      var primary = el('a', 'btn-primary', 'Get the real numbers — $1,000 audit');
      primary.href = 'contact.html';
      cta.appendChild(primary);
      var how = el('a', 'btn-secondary vc-cta-second', 'How the audit works →');
      how.href = 'ai-visibility-audit.html';
      cta.appendChild(how);
    }
    result.appendChild(cta);

    result.appendChild(buildShareBlock(values));

    result.appendChild(el('p', 'vc-disclaimer',
      'This score is worked out from your three answers and nothing else — no part of your website was scanned, and a score here is not a measurement of whether you currently appear in AI answers. The $1,000 audit is the part that actually queries ChatGPT, Perplexity, and Google AI Overviews for your category and city, checks your Bing index status directly, and validates your markup.'));

    result.hidden = false;

    track('visibility_self_check', {
      score: s.total,
      band: s.band.name,
      unsure_answers: s.unsure,
      from_shared_link: !!parseShared()
    });

    result.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  });

  /* Clear the "answer all three" warning as soon as they start fixing it. */
  form.addEventListener('change', function () {
    if (!errorEl.hidden) errorEl.hidden = true;
  });

  var shared = parseShared();
  if (shared) showSharedBanner(shared);
})();
