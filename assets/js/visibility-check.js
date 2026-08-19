/* AI Visibility Readiness self-check.
   Three self-reported answers, fixed weights, arithmetic shown to the user.
   This scores readiness, not visibility — the paid audit is what actually
   queries ChatGPT, Perplexity, and Google AI Overviews. Keep that line
   intact if this file is edited; it is the difference between a lead
   magnet and a claim we can't stand behind. */
(function () {
  var form = document.getElementById('vc-form');
  if (!form) return;

  var result = document.getElementById('vc-result');
  var errorEl = document.getElementById('vc-error');

  var LABELS = {
    q1: 'Bing indexing',
    q2: 'Google Business Profile',
    q3: 'Structured data'
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

  function band(score) {
    for (var i = 0; i < BANDS.length; i++) {
      if (score >= BANDS[i].min) return BANDS[i];
    }
    return BANDS[BANDS.length - 1];
  }

  function checked(name) {
    return form.querySelector('input[name="' + name + '"]:checked');
  }

  function el(tag, className, text) {
    var n = document.createElement(tag);
    if (className) n.className = className;
    if (text != null) n.textContent = text;
    return n;
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    var names = ['q1', 'q2', 'q3'];
    var picks = [];
    for (var i = 0; i < names.length; i++) {
      var input = checked(names[i]);
      if (!input) {
        errorEl.hidden = false;
        return;
      }
      picks.push({ name: names[i], input: input });
    }
    errorEl.hidden = true;

    var total = 0;
    var unsure = 0;
    for (var j = 0; j < picks.length; j++) {
      total += parseInt(picks[j].input.value, 10);
      if (picks[j].input.getAttribute('data-unsure') === 'true') unsure++;
    }

    var b = band(total);

    /* A site Bing doesn't have can't be cited by ChatGPT Search, whatever the
       other two answers are — so a zero there caps the verdict. Without this
       a 0/35/25 answer scores 60 and reads "Mostly there", which contradicts
       the question copy calling Bing the hardest gate. */
    var bingBlocked = checked('q1').value === '0';
    if (bingBlocked && total >= 60) {
      b = BANDS[2];
    }

    /* Rebuild the result panel from scratch each run so re-answering is clean. */
    result.textContent = '';

    var head = el('div', 'vc-score-head');
    var num = el('div', 'vc-score-num');
    num.appendChild(el('span', 'vc-score-value', String(total)));
    num.appendChild(el('span', 'vc-score-max', '/100'));
    head.appendChild(num);

    var badge = el('div', 'vc-band vc-band-' + b.tone, b.name);
    head.appendChild(badge);
    result.appendChild(head);

    var meter = el('div', 'vc-meter');
    var fill = el('div', 'vc-meter-fill vc-band-' + b.tone);
    meter.appendChild(fill);
    result.appendChild(meter);

    var breakdown = el('ul', 'vc-breakdown');
    for (var k = 0; k < picks.length; k++) {
      var p = picks[k];
      var got = parseInt(p.input.value, 10);
      var max = parseInt(p.input.getAttribute('data-max'), 10);
      var row = el('li', got === max ? 'vc-row vc-row-full' : (got === 0 ? 'vc-row vc-row-zero' : 'vc-row vc-row-part'));
      row.appendChild(el('span', 'vc-row-label', LABELS[p.name]));
      row.appendChild(el('span', 'vc-row-pts', got + ' / ' + max));
      breakdown.appendChild(row);
    }
    result.appendChild(breakdown);

    result.appendChild(el('p', 'vc-note', b.note));

    if (bingBlocked) {
      result.appendChild(el(
        'p',
        'vc-unsure',
        'Whatever else is in place, a site Bing hasn’t indexed can’t turn up in ChatGPT Search — that index is where it looks. Bing Webmaster Tools is free and submitting a sitemap takes about ten minutes; do that one first.'
      ));
    }

    if (unsure > 0) {
      result.appendChild(el(
        'p',
        'vc-unsure',
        unsure === 3
          ? 'You answered “don’t know” to all three. That is the most common result, and it is not a failing grade — nobody checks these unprompted. But unverified counts as unready, because an AI assistant reads what is actually there, not what you assume is there.'
          : 'You answered “don’t know” on ' + unsure + ' of the 3. Unverified counts as unready here, because an AI assistant reads what is actually there, not what you assume is there.'
      ));
    }

    var cta = el('div', 'vc-cta');
    if (total >= 85) {
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

    result.appendChild(el(
      'p',
      'vc-disclaimer',
      'This score is worked out from your three answers and nothing else — no part of your website was scanned, and a score here is not a measurement of whether you currently appear in AI answers. The $1,000 audit is the part that actually queries ChatGPT, Perplexity, and Google AI Overviews for your category and city, checks your Bing index status directly, and validates your markup.'
    ));

    result.hidden = false;

    /* Force a reflow at width 0, then set the real width, so the bar animates
       on every run including re-runs. Done synchronously rather than in a
       requestAnimationFrame: rAF is throttled in background tabs, which left
       the bar stuck empty. */
    fill.style.width = '0%';
    void fill.offsetWidth;
    fill.style.width = total + '%';

    if (typeof gtag === 'function') {
      gtag('event', 'visibility_self_check', {
        score: total,
        band: b.name,
        unsure_answers: unsure
      });
    }

    result.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  });

  /* Clear the "answer all three" warning as soon as they start fixing it. */
  form.addEventListener('change', function () {
    if (!errorEl.hidden) errorEl.hidden = true;
  });
})();
