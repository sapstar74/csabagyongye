/* Csabagyöngye – webes felület. Egy játékmód: választott számú kérdés,
   minden válasz után visszajelzés és magyarázat, a végén szőlőfürt. */
(function () {
  'use strict';

  var MEDIA_BASE = '../';            // a médiafájlok a repó gyökeréhez képest vannak megadva
  var MIN_N = 5, MAX_N = 50;
  var PALS = [['black', 'Fekete'], ['green', 'Zöld'], ['wine', 'Borvörös']];
  var GROUND = { black: '#0B0D13', green: '#0F3B2C', wine: '#4A1226' };
  var KEYS = ['A', 'B', 'C', 'D', 'E', 'F'];

  var app = document.getElementById('app');
  var data = null;                   // { groups, topics, questions }
  var byTopic = {};                  // témakulcs → kérdések
  var topicName = {};
  var sel = new Set();               // kiválasztott témakulcsok
  var wantN = 10;
  var round = null;                  // { items, idx, results, off }
  var audio = new Audio();
  audio.preload = 'auto';

  /* ---------- segédek ---------- */
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  // A kérdésbank **kiemelés** jelölését kiemeléssé alakítja (a szöveg többi része escape-elve marad).
  function rich(s) { return esc(s).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>'); }
  function store(key, val) { try { localStorage.setItem('cg.' + key, JSON.stringify(val)); } catch (e) { /* nem baj */ } }
  function load(key, fallback) {
    try { var v = localStorage.getItem('cg.' + key); return v === null ? fallback : JSON.parse(v); } catch (e) { return fallback; }
  }
  function shuffle(a) {
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }
  function pad2(n) { return n < 10 ? '0' + n : String(n); }
  function mmss(sec) { sec = Math.max(0, Math.floor(sec || 0)); return Math.floor(sec / 60) + ':' + pad2(sec % 60); }
  function mediaUrl(p) { return /^https?:/.test(p) ? p : MEDIA_BASE + p; }

  var ICON = {
    x: '<svg aria-hidden="true" width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M5 5l10 10M15 5L5 15"/></svg>',
    check: '<svg class="ico" role="img" aria-label="Helyes válasz" width="22" height="22" viewBox="0 0 22 22" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M4 11.5l4.5 4.5L18 6.5"/></svg>',
    cross: '<svg class="ico" role="img" aria-label="A te válaszod, hibás" width="22" height="22" viewBox="0 0 22 22" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"><path d="M6 6l10 10M16 6L6 16"/></svg>',
    mark: '<svg class="mark" aria-hidden="true" width="14" height="18" viewBox="0 0 14 18" fill="currentColor"><path d="M1 1l12 8-12 8z"/></svg>',
    play: '<svg aria-hidden="true" width="24" height="24" viewBox="0 0 28 28" fill="currentColor"><path d="M9 5l14 9-14 9z"/></svg>',
    pause: '<svg aria-hidden="true" width="24" height="24" viewBox="0 0 28 28" fill="currentColor"><rect x="6" y="5" width="6" height="18" rx="1.5"/><rect x="16" y="5" width="6" height="18" rx="1.5"/></svg>'
  };

  /* ---------- paletta ---------- */
  function setPal(id) {
    if (!GROUND[id]) id = 'green';
    document.documentElement.setAttribute('data-pal', id);
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', GROUND[id]);
    store('pal', id);
    var btns = document.querySelectorAll('.pal');
    for (var i = 0; i < btns.length; i++) btns[i].setAttribute('aria-pressed', btns[i].getAttribute('data-id') === id ? 'true' : 'false');
  }
  function palsHTML() {
    var cur = document.documentElement.getAttribute('data-pal');
    return '<div class="pals" role="group" aria-label="Színpaletta">' + PALS.map(function (p) {
      return '<button class="pal" data-id="' + p[0] + '" aria-label="' + p[1] + ' paletta" aria-pressed="' + (p[0] === cur) + '"><span></span></button>';
    }).join('') + '</div>';
  }

  /* ---------- szőlőfürt ---------- */
  // 10 szemig lefelé keskenyedő fürt; fölötte négy szem széles, gördülő füzér.
  function clusterRows(n, roll) {
    var rows = [], left = n;
    if (!roll) {
      var w = 1;
      while (w * (w + 1) / 2 < n) w++;
      for (var k = w; k > 0 && left > 0; k--) { var t = Math.min(k, left); rows.push(t); left -= t; }
      return rows;
    }
    var wide = true;
    while (left > 6) { var take = wide ? 4 : 3; rows.push(take); left -= take; wide = !wide; }
    return rows.concat({ 6: [3, 2, 1], 5: [3, 2], 4: [3, 1], 3: [2, 1], 2: [2], 1: [1] }[left] || []);
  }

  // states[i]: 'ok' | 'bad' | 'now' | undefined. opts: { W, H, top, rmax, roll, cur, off, anim, label }
  function clusterHTML(n, states, o) {
    var roll = !!o.roll && n > 10;
    var rows = clusterRows(n, roll);
    var maxW = Math.max.apply(null, rows);
    var vis = roll ? 4 : rows.length;
    var r = Math.min(o.rmax, o.W / (2 * 1.06 * (maxW - 1) + 2), (o.H - o.top) / (vis * 1.8 + 0.2));
    var dx = 2 * r * 1.06, dy = 2 * r * 0.9;
    var curRow = 0, acc = 0;
    rows.forEach(function (c, ri) { if (o.cur >= acc && o.cur < acc + c) curRow = ri; acc += c; });
    var off = roll ? Math.max(0, Math.min(curRow - 2, rows.length - vis)) : 0;
    var startOff = roll && typeof o.off === 'number' ? o.off : off;
    var html = '', i = 0;
    rows.forEach(function (cnt, ri) {
      var x0 = o.W / 2 - (cnt - 1) * dx / 2 - r;
      for (var j = 0; j < cnt; j++) {
        var s = states[i] || '';
        var delay = o.anim === 'fall' ? Math.min(i * 1.5 / n, 1.5) : Math.min(i * 0.05, 0.8);
        html += '<i class="berry ' + s + (o.anim ? ' ' + o.anim : '') + '" data-i="' + i + '" style="left:' + (x0 + j * dx).toFixed(1) + 'px;top:' +
          (ri * dy).toFixed(1) + 'px;width:' + (2 * r).toFixed(1) + 'px;height:' + (2 * r).toFixed(1) + 'px;animation-delay:' + delay.toFixed(2) + 's"></i>';
        i++;
      }
    });
    return {
      off: off, dy: dy,
      html: '<div class="cluster" role="img" aria-label="' + esc(o.label) + '" style="width:' + o.W + 'px;height:' + o.H + 'px">' +
        '<svg class="stem" aria-hidden="true" width="' + o.W + '" height="' + o.top + '" viewBox="0 0 96 24" preserveAspectRatio="xMidYMax meet">' +
        '<path d="M48 24C46 14 52 8 50 0" fill="none" stroke="#93AD35" stroke-width="3" stroke-linecap="round"/>' +
        '<path d="M50 12C62 0 80 4 86 14C72 22 60 20 50 12Z" fill="#7FA03A"/></svg>' +
        '<div class="window" style="top:' + o.top + 'px;' + (roll ? '' : 'overflow:visible') + '">' +
        '<div class="strand" data-dy="' + dy.toFixed(2) + '" style="transform:translateY(' + (-startOff * dy).toFixed(1) + 'px)">' + html + '</div></div></div>'
    };
  }

  /* ---------- témaválasztó ---------- */
  function available() {
    var n = 0;
    sel.forEach(function (k) { n += (byTopic[k] || []).length; });
    return n;
  }

  function renderHome() {
    stopAudio();
    round = null;
    var bulbs = '';
    for (var b = 0; b < 14; b++) bulbs += '<i class="bulb" style="animation-delay:' + (b * 0.09).toFixed(2) + 's"></i>';
    var groups = data.groups.map(function (g) {
      var ts = data.topics.filter(function (t) { return t.group === g; });
      if (!ts.length) return '';
      return '<section><div class="group-head"><h2>' + esc(g) + '</h2><button class="group-all" data-group="' + esc(g) + '">Mind</button></div>' +
        ts.map(function (t) {
          return '<button class="topic" data-key="' + esc(t.key) + '" aria-pressed="' + sel.has(t.key) + '">' + ICON.mark +
            '<span class="name disp' + (t.name.length > 26 ? ' long' : '') + '">' + esc(t.name) + '</span><span class="count">' + t.count + '</span></button>';
        }).join('') + '</section>';
    }).join('');
    app.innerHTML =
      '<div class="topbar">' + palsHTML() + '</div>' +
      '<header class="sign"><div class="bulbs" aria-hidden="true">' + bulbs + '</div>' +
      '<div class="sign-text"><small>Ma este műsoron</small><h1 class="disp">Csabagyöngye</h1></div>' +
      '<div class="bulbs" aria-hidden="true">' + bulbs + '</div></header>' +
      '<div class="groups">' + groups + '</div>' +
      '<div class="startbar"><label for="n"><span>Kérdések száma a körben</span><output class="disp" id="nout" for="n"></output></label>' +
      '<input id="n" type="range" step="1"><p class="hint" id="hint"></p>' +
      '<button class="cta" id="start">Függöny fel</button></div>';
    updateBar();
    window.scrollTo(0, 0);
  }

  function updateBar() {
    var avail = available();
    var slider = document.getElementById('n');
    if (!slider) return;
    var max = Math.min(MAX_N, avail), min = Math.min(MIN_N, Math.max(1, max));
    slider.min = min; slider.max = Math.max(min, max);
    slider.disabled = avail === 0 || max <= min;
    var n = Math.max(min, Math.min(wantN, Math.max(min, max)));
    slider.value = n;
    document.getElementById('nout').textContent = avail ? n : '–';
    document.getElementById('hint').textContent = avail
      ? sel.size + ' témakör, ' + avail + ' kérdés közül sorsolunk.'
      : 'Válassz legalább egy témakört.';
    document.getElementById('start').disabled = avail === 0;
    var heads = document.querySelectorAll('.group-all');
    for (var i = 0; i < heads.length; i++) {
      var g = heads[i].getAttribute('data-group');
      var all = data.topics.filter(function (t) { return t.group === g; }).every(function (t) { return sel.has(t.key); });
      heads[i].textContent = all ? 'Egyik sem' : 'Mind';
    }
  }

  /* ---------- kör ---------- */
  function makeItem(q) {
    var order = shuffle(q.o.map(function (_, i) { return i; }));
    return { q: q, order: order, correctPos: order.indexOf(q.c), pick: null };
  }

  function startRound(questions) {
    round = { items: questions.map(makeItem), idx: 0, results: [], off: 0 };
    renderQuestion();
  }

  function drawQuestions(n) {
    // A kérdések a kiválasztott témák között egyenletesen oszlanak el.
    var pools = shuffle(Array.from(sel)).map(function (k) { return shuffle((byTopic[k] || []).slice()); }).filter(function (p) { return p.length; });
    var out = [];
    while (out.length < n && pools.length) {
      for (var i = 0; i < pools.length && out.length < n; i++) { if (pools[i].length) out.push(pools[i].pop()); }
      pools = pools.filter(function (p) { return p.length; });
    }
    return shuffle(out);
  }

  function clusterStates() {
    var s = round.results.map(function (ok) { return ok ? 'ok' : 'bad'; });
    if (s.length < round.items.length) s.push('now');
    return s;
  }

  function renderQuestion() {
    var it = round.items[round.idx], q = it.q, n = round.items.length;
    var done = round.results.length, okN = round.results.filter(Boolean).length;
    var cl = clusterHTML(n, clusterStates(), {
      W: 96, H: 112, top: 22, rmax: 11, roll: true, cur: round.idx, off: round.off, anim: round.idx === 0 ? 'pop' : '',
      label: 'A kör fürtje: ' + okN + ' helyes, ' + (done - okN) + ' hibás, ' + (n - done) + ' szem hátravan'
    });
    var newOff = cl.off;
    var tclass = q.q.length > 90 ? ' long' : q.q.length > 40 ? ' mid' : '';
    var media = '';
    if (q.a) {
      var bars = '';
      for (var b = 0; b < 22; b++) bars += '<i style="height:' + (16 + (b * 37) % 28) + 'px;animation-delay:' + (((b * 137) % 900) / 1000).toFixed(2) + 's"></i>';
      media = '<div class="player big" id="player"><div class="deck"><div class="disc" aria-hidden="true"><i></i></div>' +
        '<button class="play" id="play" aria-label="Lejátszás">' + ICON.play + '</button></div>' +
        '<div class="meter"><span class="time disp" id="time">0:00</span><div class="eq" aria-hidden="true">' + bars + '</div></div></div>' +
        '<p class="audio-err" id="aerr" hidden>A hangfájl nem tölthető be.</p>';
    } else if (q.i) {
      media = '<figure class="picture"><img src="' + esc(mediaUrl(q.i)) + '" alt="A kérdéshez tartozó kép">' +
        (q.cr ? '<figcaption>' + (q.cru ? '<a href="' + esc(q.cru) + '" target="_blank" rel="noopener">' + esc(q.cr) + '</a>' : esc(q.cr)) + '</figcaption>' : '') + '</figure>';
    }
    var opts = it.order.map(function (oi, pos) {
      return '<button class="opt" data-pos="' + pos + '"><span class="key disp">' + KEYS[pos] + '</span><span class="lbl">' + esc(q.o[oi]) + '</span></button>';
    }).join('');
    var wide = q.o.some(function (o) { return o.length > 26; });
    app.innerHTML =
      '<div class="qhead"><div class="qhead-left"><div class="qhead-row">' +
      '<button class="close" id="quit" aria-label="Kilépés a körből">' + ICON.x + '</button>' +
      '<span class="topic-label">' + esc(topicName[q.t] || q.t) + '</span></div>' + palsHTML() + '</div>' + cl.html + '</div>' +
      '<div class="qline' + (tclass === ' long' ? ' stack' : '') + '"><div class="qnum disp" aria-hidden="true">' + pad2(round.idx + 1) + '<small>/' + n + '</small></div>' +
      '<h1 class="qtext disp' + tclass + '"><span class="sr">' + (round.idx + 1) + '. kérdés a ' + n + '-ből: </span>' + rich(q.q) + '</h1></div>' +
      media +
      '<div class="opts' + (wide ? ' wide' : '') + '" id="opts">' + opts + '</div>' +
      '<div id="after"></div>';
    window.scrollTo(0, 0);
    if (newOff !== round.off) {
      var strand = app.querySelector('.strand');
      requestAnimationFrame(function () { requestAnimationFrame(function () { strand.style.transform = 'translateY(' + (-newOff * cl.dy).toFixed(1) + 'px)'; }); });
      round.off = newOff;
    }
    if (q.a) playAudio(mediaUrl(q.a)); else stopAudio();
  }

  function answer(pos) {
    var it = round.items[round.idx];
    if (!it || it.pick !== null || pos < 0 || pos >= it.order.length) return;
    it.pick = pos;
    var ok = pos === it.correctPos, q = it.q;
    round.results.push(ok);
    var box = document.getElementById('opts');
    box.classList.add('answered');
    var btns = box.querySelectorAll('.opt');
    for (var i = 0; i < btns.length; i++) {
      btns[i].disabled = true;
      if (i === it.correctPos) { btns[i].classList.add('correct'); btns[i].insertAdjacentHTML('beforeend', ICON.check); }
      else if (i === pos) { btns[i].classList.add('wrong'); btns[i].insertAdjacentHTML('beforeend', ICON.cross); }
    }
    var berry = app.querySelector('.berry[data-i="' + round.idx + '"]');
    if (berry) { berry.className = 'berry pop ' + (ok ? 'ok' : 'bad'); berry.style.animationDelay = '0s'; }
    var player = document.getElementById('player');
    if (player) player.classList.remove('big');
    var last = round.idx === round.items.length - 1;
    var correctText = q.o[q.c];
    document.getElementById('after').outerHTML =
      '<div class="why' + (ok ? ' good' : '') + '" id="after"><h2 class="disp">' +
      (ok ? 'Talált!' : 'Nem talált. A helyes válasz: ' + esc(correctText)) + '</h2>' +
      (q.cap ? '<p class="cap">' + esc(q.cap) + '</p>' : '') +
      (q.e ? '<p>' + rich(q.e) + '</p>' : '') + '</div>' +
      '<button class="cta next" id="next">' + (last ? 'Eredmény' : 'Következő') + '</button>';
    var next = document.getElementById('next');
    next.focus({ preventScroll: true });
    next.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  }

  function nextQuestion() {
    if (!round || round.items[round.idx].pick === null) return;
    if (round.idx < round.items.length - 1) { round.idx++; renderQuestion(); }
    else renderResult();
  }

  /* ---------- eredmény ---------- */
  function renderResult() {
    stopAudio();
    var n = round.items.length, okN = round.results.filter(Boolean).length, bad = n - okN;
    var cl = clusterHTML(n, round.results.map(function (ok) { return ok ? 'ok' : 'bad'; }), {
      W: 240, H: 250, top: 44, rmax: 27, roll: false, cur: 0, anim: 'fall',
      label: 'A kör fürtje: ' + okN + ' helyes, ' + bad + ' hibás válasz'
    });
    var topics = Array.from(new Set(round.items.map(function (it) { return topicName[it.q.t] || it.q.t; })));
    var review = round.items.filter(function (it, i) { return !round.results[i]; }).map(function (it) {
      var q = it.q;
      return '<li><p class="rq">' + rich(q.q) + (q.cap ? ' (' + esc(q.cap) + ')' : '') + '</p>' +
        '<p class="rb">A te válaszod: ' + esc(q.o[it.order[it.pick]]) + '</p>' +
        '<p class="ra">Helyes: ' + esc(q.o[q.c]) + '</p>' + (q.e ? '<p>' + rich(q.e) + '</p>' : '') + '</li>';
    }).join('');
    app.innerHTML =
      '<div class="rhead"><span class="topic-label">A mai szüret · ' + esc(topics.length === 1 ? topics[0] : topics.length + ' témakör') + '</span>' + palsHTML() + '</div>' +
      '<div class="rcluster">' + cl.html + '</div>' +
      '<div class="score disp"><b>' + okN + '</b><span aria-hidden="true">/' + n + '</span></div>' +
      '<h1 class="verdict disp">' + (bad ? okN + ' gyöngyszem, ' + bad + ' mazsola' : 'Hibátlan szüret: ' + n + ' gyöngyszem') + '</h1>' +
      (review ? '<section class="review-wrap"><h2>A mazsolák</h2><ul class="review">' + review + '</ul></section>' : '') +
      '<div class="actions">' +
      (bad ? '<button class="cta" id="retry">A ' + bad + ' hiba újra</button><button class="ghost" id="home">Új kör</button>'
           : '<button class="cta" id="home">Új kör</button>') + '</div>';
    window.scrollTo(0, 0);
  }

  /* ---------- hang ---------- */
  function playAudio(url) {
    audio.src = url;
    audio.currentTime = 0;
    var p = audio.play();
    if (p && p.catch) p.catch(function () { syncPlayer(); });
  }
  function stopAudio() { audio.pause(); audio.removeAttribute('src'); }
  function syncPlayer() {
    var player = document.getElementById('player'), btn = document.getElementById('play');
    if (!player || !btn) return;
    var playing = !audio.paused && !audio.ended;
    player.classList.toggle('playing', playing);
    btn.innerHTML = playing ? ICON.pause : ICON.play;
    btn.setAttribute('aria-label', playing ? 'Szünet' : 'Lejátszás');
  }
  ['play', 'playing', 'pause', 'ended'].forEach(function (ev) { audio.addEventListener(ev, syncPlayer); });
  audio.addEventListener('timeupdate', function () { var t = document.getElementById('time'); if (t) t.textContent = mmss(audio.currentTime); });
  audio.addEventListener('error', function () {
    var e = document.getElementById('aerr');
    if (e && audio.getAttribute('src')) e.hidden = false;
    syncPlayer();
  });

  /* ---------- események ---------- */
  app.addEventListener('click', function (ev) {
    var t = ev.target.closest('button');
    if (!t) return;
    if (t.classList.contains('pal')) return setPal(t.getAttribute('data-id'));
    if (t.classList.contains('topic')) {
      var key = t.getAttribute('data-key');
      if (sel.has(key)) sel.delete(key); else sel.add(key);
      t.setAttribute('aria-pressed', sel.has(key));
      store('sel', Array.from(sel));
      return updateBar();
    }
    if (t.classList.contains('group-all')) {
      var g = t.getAttribute('data-group');
      var ts = data.topics.filter(function (x) { return x.group === g; });
      var all = ts.every(function (x) { return sel.has(x.key); });
      ts.forEach(function (x) {
        if (all) sel.delete(x.key); else sel.add(x.key);
        var b = app.querySelector('.topic[data-key="' + CSS.escape(x.key) + '"]');
        if (b) b.setAttribute('aria-pressed', sel.has(x.key));
      });
      store('sel', Array.from(sel));
      return updateBar();
    }
    if (t.classList.contains('opt')) return answer(Number(t.getAttribute('data-pos')));
    if (t.id === 'start') {
      var n = Number(document.getElementById('n').value);
      var qs = drawQuestions(n);
      if (qs.length) startRound(qs);
      return;
    }
    if (t.id === 'next') return nextQuestion();
    if (t.id === 'play') { if (audio.paused) { var p = audio.play(); if (p && p.catch) p.catch(function () {}); } else audio.pause(); return; }
    if (t.id === 'quit' || t.id === 'home') return renderHome();
    if (t.id === 'retry') {
      var wrong = round.items.filter(function (it, i) { return !round.results[i]; }).map(function (it) { return it.q; });
      return startRound(shuffle(wrong));
    }
  });

  app.addEventListener('input', function (ev) {
    if (ev.target.id !== 'n') return;
    wantN = Number(ev.target.value);
    document.getElementById('nout').textContent = wantN;
    store('n', wantN);
  });

  document.addEventListener('keydown', function (ev) {
    if (!round || ev.altKey || ev.ctrlKey || ev.metaKey) return;
    var it = round.items[round.idx];
    if (!it || !document.getElementById('opts')) return;
    if (it.pick === null) {
      var k = ev.key.toUpperCase();
      var pos = '1234'.indexOf(k) >= 0 ? Number(k) - 1 : KEYS.indexOf(k);
      if (pos >= 0 && pos < it.order.length) { ev.preventDefault(); answer(pos); }
    } else if (ev.key === 'Enter' && ev.target.tagName !== 'BUTTON') { ev.preventDefault(); nextQuestion(); }
  });

  /* ---------- indulás ---------- */
  setPal(load('pal', 'green'));
  wantN = Math.max(1, Math.min(MAX_N, Number(load('n', 10)) || 10));
  fetch('data/questions.json').then(function (r) {
    if (!r.ok) throw new Error(r.status);
    return r.json();
  }).then(function (d) {
    data = d;
    d.questions.forEach(function (q) { (byTopic[q.t] = byTopic[q.t] || []).push(q); });
    d.topics.forEach(function (t) { topicName[t.key] = t.name; });
    (load('sel', []) || []).forEach(function (k) { if (byTopic[k]) sel.add(k); });
    renderHome();
  }).catch(function () {
    app.innerHTML = '<p class="loading">A kérdések nem tölthetők be. A felületet webszerverről kell megnyitni ' +
      '(a repó gyökeréből: <code>python -m http.server</code>, majd <code>/web/</code>), és a ' +
      '<code>web/data/questions.json</code> fájlnak léteznie kell (<code>python scripts/export_web.py</code>).</p>';
  });
})();
