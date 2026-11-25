/* Csabagyöngye – webes felület. Kérdéssor: választott számú kérdés, minden válasz
   után visszajelzés és magyarázat, a végén szőlőfürt. Külön játék a 9+1: tíz beírós
   kérdés egy oldalon, a válaszokat összefüggés köti össze, kiértékelés a végén. */
(function () {
  'use strict';

  var MEDIA_BASE = '../';            // a médiafájlok a repó gyökeréhez képest vannak megadva
  var MIN_N = 5, MAX_N = 50;
  var ADVANCE_MS = 2000;            // válasz után ennyi idővel jön a következő kérdés
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
  var npData = null;                 // 9+1 játékok: { games } (ha a fájl hiányzik, a kártya nem jelenik meg)
  var nine = null;                   // folyó 9+1 játék: { game, answers, result, warned }
  var free = false;                  // „3. blokk”: beírós válaszok a kérdéssorban
  var advanceTimer = null;          // automatikus továbblépés időzítője
  var scrubbing = false;            // éppen húzza-e a lejátszási csúszkát
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
    // Enter-nyíl egy szikrázó csillaggal: a szabad szöveges válasz beküldőgombja.
    enter: '<svg aria-hidden="true" class="go-ico" width="40" height="34" viewBox="0 0 40 34" fill="none">' +
      '<path d="M26 6v9a4 4 0 0 1-4 4H9" stroke="currentColor" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>' +
      '<path d="M14 13l-6 6 6 6" stroke="currentColor" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>' +
      '<path class="star" d="M34 1l1.6 4.1L40 6.5l-4.4 1.4L34 12l-1.6-4.1L28 6.5l4.4-1.4z" fill="currentColor"/></svg>',
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
  function pool(k) { return (byTopic[k] || []).filter(function (q) { return !free || freeFits(q); }); }
  function available() {
    var n = 0;
    sel.forEach(function (k) { n += pool(k).length; });
    return n;
  }

  function renderHome() {
    holdAdvance();
    stopAudio();
    round = null;
    nine = null;
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
      '<div class="groups">' + npHomeHTML() +
      '<label class="mode"><input type="checkbox" id="free"' + (free ? ' checked' : '') + '><span>3. blokk – szabad szöveges válasszal</span></label>' +
      groups + '</div>' +
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
      ? sel.size + ' témakör, ' + avail + (free ? ' beírós' : '') + ' kérdés közül sorsolunk.'
      : sel.size && free ? 'A kiválasztott témákban nincs beírós kérdés.' : 'Válassz legalább egy témakört.';
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

  function startRound(questions, isFree) {
    round = { items: questions.map(makeItem), idx: 0, results: [], off: 0, free: !!isFree };
    renderQuestion();
  }

  function drawQuestions(n) {
    // A kérdések a kiválasztott témák között egyenletesen oszlanak el.
    var pools = shuffle(Array.from(sel)).map(function (k) { return shuffle(pool(k)); }).filter(function (p) { return p.length; });
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
        '<div class="meter"><div class="meter-top"><span class="time disp" id="time">0:00</span><div class="eq" aria-hidden="true">' + bars + '</div></div>' +
        '<div class="seek"><input type="range" id="seek" min="0" max="90" step="0.1" value="0" aria-label="Lejátszási pozíció" aria-valuetext="0:00">' +
        '<span class="dur" id="dur">–:––</span></div></div></div>' +
        '<p class="audio-err" id="aerr" hidden>A hangfájl nem tölthető be.</p>';
    } else if (q.i) {
      media = '<figure class="picture"><img src="' + esc(mediaUrl(q.i)) + '" alt="A kérdéshez tartozó kép">' +
        (q.cr ? '<figcaption>' + (q.cru ? '<a href="' + esc(q.cru) + '" target="_blank" rel="noopener">' + esc(q.cr) + '</a>' : esc(q.cr)) + '</figcaption>' : '') + '</figure>';
    }
    var opts = it.order.map(function (oi, pos) {
      return '<button class="opt" data-pos="' + pos + '"><span class="key disp">' + KEYS[pos] + '</span><span class="lbl">' + esc(q.o[oi]) + '</span></button>';
    }).join('');
    var wide = q.o.some(function (o) { return o.length > 26; });
    var answerBox = round.free
      // Beküldés Enterrel, a billentyűzet „Kész/Ugrás” gombjával vagy a kerek gyöngy-gombbal – mind a form submit eseménye.
      ? '<form class="free" id="freeform" autocomplete="off"><input class="free-in" id="freein" type="text" aria-label="A válaszod" ' +
        'placeholder="Írd be a választ" autocapitalize="off" autocorrect="off" spellcheck="false" enterkeyhint="done">' +
        '<button class="free-go" id="freego" type="submit" aria-label="Beküldés (Enter)">' + ICON.enter + '<span class="disp">Mehet</span></button></form>'
      : '<div class="opts' + (wide ? ' wide' : '') + '" id="opts">' + opts + '</div>';
    app.innerHTML =
      '<div class="qhead"><div class="qhead-left"><div class="qhead-row">' +
      '<button class="close" id="quit" aria-label="Kilépés a körből">' + ICON.x + '</button>' +
      '<span class="topic-label">' + esc(topicName[q.t] || q.t) + '</span></div>' + palsHTML() + '</div>' + cl.html + '</div>' +
      '<div class="qline' + (tclass === ' long' ? ' stack' : '') + '"><div class="qnum disp" aria-hidden="true">' + pad2(round.idx + 1) + '<small>/' + n + '</small></div>' +
      '<h1 class="qtext disp' + tclass + '"><span class="sr">' + (round.idx + 1) + '. kérdés a ' + n + '-ből: </span>' + rich(q.q) + '</h1></div>' +
      media + answerBox +
      '<div id="after"></div>';
    window.scrollTo(0, 0);
    if (newOff !== round.off) {
      var strand = app.querySelector('.strand');
      requestAnimationFrame(function () { requestAnimationFrame(function () { strand.style.transform = 'translateY(' + (-newOff * cl.dy).toFixed(1) + 'px)'; }); });
      round.off = newOff;
    }
    if (q.a) playAudio(mediaUrl(q.a)); else stopAudio();
    // Telefonon nem fókuszál magától, mert a billentyűzet eltakarná a képet.
    if (round.free && window.matchMedia && matchMedia('(pointer: fine)').matches) document.getElementById('freein').focus({ preventScroll: true });
  }

  function answer(pos) {
    var it = round.items[round.idx];
    if (!it || it.pick !== null || pos < 0 || pos >= it.order.length) return;
    it.pick = pos;
    var ok = pos === it.correctPos;
    round.results.push(ok);
    var box = document.getElementById('opts');
    box.classList.add('answered');
    var btns = box.querySelectorAll('.opt');
    for (var i = 0; i < btns.length; i++) {
      btns[i].disabled = true;
      if (i === it.correctPos) { btns[i].classList.add('correct'); btns[i].insertAdjacentHTML('beforeend', ICON.check); }
      else if (i === pos) { btns[i].classList.add('wrong'); btns[i].insertAdjacentHTML('beforeend', ICON.cross); }
    }
    feedback(it, ok);
  }

  // Beírós válasz (3. blokk).
  function answerFree() {
    var it = round.items[round.idx], el = document.getElementById('freein');
    if (!it || it.pick !== null || !el) return;
    if (!el.value.trim()) { el.focus(); return; }
    it.pick = -1;
    it.typed = el.value.trim();
    var ok = freeCorrect(it.typed, it.q);
    round.results.push(ok);
    el.disabled = true;
    el.classList.add(ok ? 'ok' : 'bad');
    var go = document.getElementById('freego');
    if (go) go.remove();
    feedback(it, ok);
  }

  // Ha a gép tévesen hibásnak ítélte a beírt választ, a játékos elfogadtathatja.
  function acceptFree() {
    var it = round.items[round.idx];
    if (!round.free || !it || it.pick === null || round.results[round.idx]) return;
    round.results[round.idx] = true;
    var el = document.getElementById('freein');
    if (el) { el.classList.remove('bad'); el.classList.add('ok'); }
    var berry = app.querySelector('.berry[data-i="' + round.idx + '"]');
    if (berry) berry.className = 'berry ok';
    var why = document.getElementById('after');
    why.classList.add('good');
    why.querySelector('h2').textContent = 'Elfogadva: ' + it.q.o[it.q.c];
    document.getElementById('accept').remove();
  }

  function feedback(it, ok) {
    var q = it.q;
    var berry = app.querySelector('.berry[data-i="' + round.idx + '"]');
    if (berry) { berry.className = 'berry pop ' + (ok ? 'ok' : 'bad'); berry.style.animationDelay = '0s'; }
    var player = document.getElementById('player');
    if (player) player.classList.remove('big');
    var last = round.idx === round.items.length - 1;
    var correctText = q.o[q.c];
    // Beírós hibás válasznál nincs automatikus továbblépés: össze kell tudni vetni a kettőt.
    var auto = !(round.free && !ok);
    document.getElementById('after').outerHTML =
      '<div class="why' + (ok ? ' good' : '') + '" id="after"><h2 class="disp">' +
      (ok ? 'Talált!' + (round.free && norm(it.typed) !== norm(correctText) ? ' ' + esc(correctText) : '') : 'Nem talált. A helyes válasz: ' + esc(correctText)) + '</h2>' +
      (q.cap ? '<p class="cap">' + esc(q.cap) + '</p>' : '') +
      (q.e ? '<p>' + rich(q.e) + '</p>' : '') +
      (auto ? '<button class="hold" id="hold">' + ICON.pause + '<span>Várj, elolvasom</span></button>'
            : '<button class="hold" id="accept">' + ICON.check + '<span>Mégis jó volt</span></button>') + '</div>' +
      '<button class="cta next' + (auto ? ' auto' : '') + '" id="next" style="--adv:' + ADVANCE_MS + 'ms">' + (last ? 'Eredmény' : 'Következő') + '</button>';
    var next = document.getElementById('next');
    next.focus({ preventScroll: true });
    next.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    clearTimeout(advanceTimer);
    advanceTimer = auto ? setTimeout(nextQuestion, ADVANCE_MS) : null;
  }

  // Megállítja az automatikus továbblépést (Várj gomb, csúszka, kilépés).
  function holdAdvance() {
    if (advanceTimer === null) return;
    clearTimeout(advanceTimer);
    advanceTimer = null;
    var next = document.getElementById('next'), hold = document.getElementById('hold');
    if (next) next.classList.remove('auto');
    if (hold) hold.remove();
  }

  function nextQuestion() {
    clearTimeout(advanceTimer);
    advanceTimer = null;
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
        '<p class="rb">A te válaszod: ' + esc(it.pick < 0 ? it.typed : q.o[it.order[it.pick]]) + '</p>' +
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

  /* ---------- 9+1 ---------- */
  // Kilenc kérdés válaszai összefüggnek, a +1 kérdés válasza is ebbe az összefüggésbe illik.
  // A „párok" játékban tíz kérdés van: az 1–6., 2–7., 3–8., 4–9. és 5–10. válasz alkot párt.
  // Beírós válaszok; a kiértékelésig mind javítható. Adat: data/kilenc_plusz_egy.json.
  var NP_RULE = 'Kilenc kérdés, amelyek válaszai összefüggnek. A tizedikre az a válasz jó, amelyik ebbe az összefüggésbe illik.';
  var NP_PAIRS_RULE = 'Tíz kérdés, öt pár: az 1–6., 2–7., 3–8., 4–9. és 5–10. válasz együtt egy ismert nevet, címet vagy kifejezést ad ki.';

  // Elnéző összehasonlítás: kis- és nagybetű, ékezet, írásjel és névelő nem számít.
  // Ugyanez a szabály fut a scripts/export_kilenc_plusz_egy.py ellenőrzésében (normalize).
  function norm(s) {
    var w = String(s).trim().toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '')
      .replace(/[^a-z0-9]+/g, ' ').trim().split(' ').filter(Boolean);
    if (w.length > 1 && (w[0] === 'a' || w[0] === 'az')) w.shift();
    return w.join('');
  }
  function npCorrect(given, item) {
    var g = norm(given);
    return !!g && item.a.some(function (a) { return norm(a) === g; });
  }

  /* ---------- 3. blokk: beírós válaszok a kérdéssorban ---------- */
  // Csak rövid, egyértelműen beírható válaszú kérdések jönnek: a kifejtős állításos,
  // tagadó („Melyik NEM…”) és kakukktojásos kérdések kimaradnak.
  var FREE_MAX = 40;
  var FREE_SKIP = /állítás|kakukk|(?:melyik|mi|ki)\s+(?:\*\*)?nem\s/i;
  function freeRaw(q) {
    var c = q.o[q.c], out = [c];
    c.split(/\s+\/\s+/).forEach(function (p) {
      out.push(p, p.replace(/\s*\([^)]*\)/g, ''), p.split(/\s+(?:ft|feat|featuring)\.?\s+/i)[0], p.replace(/^the\s+/i, ''));
    });
    return out;
  }
  function freeFits(q) {
    if (q._ff === undefined) {
      var shortest = Math.min.apply(null, freeRaw(q).map(function (a) { return a.trim().length; }));
      q._ff = shortest <= FREE_MAX && !FREE_SKIP.test(q.q) && !/\bNEM\b/.test(q.q);
    }
    return q._ff;
  }
  function lev(a, b) {
    var prev = [], cur, i, j;
    for (j = 0; j <= b.length; j++) prev[j] = j;
    for (i = 1; i <= a.length; i++) {
      cur = [i];
      for (j = 1; j <= b.length; j++) cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
      prev = cur;
    }
    return prev[b.length];
  }
  // Ugyanaz az elnéző összevetés, mint a 9+1-ben, plusz kis elgépelés (számoknál soha).
  // A helyes válasz tulajdonnév-részei (pl. „Friedrich Hecker” → „Hecker”, „Juan Martín del Potro”
  // → „del Potro”). Csak az a rész számít, amely nagybetűs szót tartalmaz, és egyik rossz
  // válaszlehetőségben sem szerepel – így az „Ulászló” nem jó a „II. Ulászló” helyett, ha a
  // lehetőségek között „I. Ulászló” is van. A római szám önmagában nem tulajdonnév.
  // A szabad szöveges összevetésben az „és”, az „and” és a „&” egyenértékű
  // (pl. „Trinidad and Tobago” = „Trinidad és Tobago”, „Above and Beyond” = „Above & Beyond”).
  function fnorm(s) { return norm(String(s).replace(/(^|\s)(?:és|and|&)(?=\s|$)/gi, '$1and')); }
  function isName(w) { var c = w.charAt(0); return c !== c.toLowerCase() && !/^[IVXLCDM]+\.?$/.test(w); }
  function freeNames(q) {
    if (q._fn) return q._fn;
    var others = q.o.filter(function (_, i) { return i !== q.c; }).map(fnorm), out = [];
    freeRaw(q).forEach(function (alt) {
      var w = alt.replace(/[(),]/g, ' ').split(/\s+/).filter(Boolean);
      for (var i = 0; i < w.length; i++) {
        for (var j = i + 1; j <= w.length; j++) {
          if (i === 0 && j === w.length) continue;
          var part = w.slice(i, j);
          if (!part.some(isName)) continue;
          var n = fnorm(part.join(' '));
          if (n.length < 3 || /^\d+$/.test(n) || out.indexOf(n) >= 0) continue;
          if (others.some(function (o) { return o.indexOf(n) >= 0; })) continue;
          out.push(n);
        }
      }
    });
    return (q._fn = out);
  }
  function freeCorrect(given, q) {
    var g = fnorm(given);
    if (!g) return false;
    return freeRaw(q).map(fnorm).concat(freeNames(q)).some(function (a) {
      if (!a) return false;
      if (a === g) return true;
      if (/\d/.test(a) || a.length < 5) return false;
      return lev(a, g) <= (a.length >= 10 ? 2 : 1);
    });
  }

  function npItems(game) { return game.closer ? game.items.concat([game.closer]) : game.items; }
  function npLabel(game, i) { return game.closer && i === game.items.length ? '+1' : pad2(i + 1); }
  function npGame(id) { return npData.games.filter(function (g) { return g.id === id; })[0] || null; }
  function npPlayed() { var p = load('np.played', []); return Array.isArray(p) ? p : []; }
  function npLeft() { var played = npPlayed(); return npData.games.filter(function (g) { return played.indexOf(g.id) < 0; }); }
  function npDraft() {
    var d = load('np.draft', null);
    var game = d && npData ? npGame(d.id) : null;
    return game && Array.isArray(d.answers) && d.answers.length === npItems(game).length ? { game: game, answers: d.answers } : null;
  }
  function npPick() {
    var left = npLeft();
    if (!left.length) { store('np.played', []); left = npData.games; }   // elfogytak: új kör
    return left[Math.floor(Math.random() * left.length)];
  }

  function npHomeHTML() {
    if (!npData || !npData.games.length) return '';
    var draft = npDraft(), left = npLeft().length, all = npData.games.length;
    return '<section><div class="group-head np-head"><h2>9+1</h2></div>' +
      '<button class="np-card" id="np"><span class="name disp">Kilenc kérdés, egy összefüggés</span>' +
      '<span class="sub">' + (draft ? 'Félbehagyott játék folytatása' : all + ' játék' + (left && left < all ? ', ebből ' + left + ' új' : '')) +
      ' · beírós válaszok</span></button></section>';
  }

  function startNine(fresh) {
    holdAdvance();
    stopAudio();
    round = null;
    var draft = fresh ? null : npDraft();
    var game = draft ? draft.game : npPick();
    var answers = npItems(game).map(function (_, i) { return draft && typeof draft.answers[i] === 'string' ? draft.answers[i] : ''; });
    nine = { game: game, answers: answers, result: null, warned: false };
    renderNine();
  }

  function renderNine() {
    var game = nine.game, items = npItems(game), n = items.length, pairs = !game.closer;
    var filled = nine.answers.filter(function (a) { return a.trim(); }).length;
    var cl = clusterHTML(n, nine.answers.map(function (a) { return a.trim() ? 'set' : ''; }), {
      W: 96, H: 112, top: 22, rmax: 11, roll: false, cur: 0, anim: 'pop', label: 'Kitöltve ' + filled + ' a ' + n + ' válaszból'
    });
    var rows = items.map(function (it, i) {
      var label = npLabel(game, i);
      return ((pairs ? i === 5 : i === n - 1) ? '<hr class="np-sep">' : '') +
        '<label class="np-item"><span class="np-num disp" aria-hidden="true">' + label + '</span>' +
        '<span class="np-q"><span class="sr">' + label + '. kérdés: </span>' + rich(it.q) + '</span>' +
        '<input class="np-in" type="text" data-i="' + i + '" value="' + esc(nine.answers[i]) + '" autocomplete="off" autocapitalize="off" ' +
        'autocorrect="off" spellcheck="false" enterkeyhint="' + (i === n - 1 ? 'done' : 'next') + '"></label>';
    }).join('');
    app.innerHTML =
      '<div class="qhead"><div class="qhead-left"><div class="qhead-row">' +
      '<button class="close" id="quit" aria-label="Kilépés a játékból">' + ICON.x + '</button>' +
      '<span class="topic-label">9+1' + (pairs ? ' · párok' : '') + '</span></div>' + palsHTML() + '</div>' + cl.html + '</div>' +
      '<p class="np-rule">' + (pairs ? NP_PAIRS_RULE : NP_RULE) + ' A kiértékelésig bármelyik válaszodat javíthatod.</p>' +
      '<div class="np-form" id="npform">' + rows + '</div>' +
      '<p class="np-warn" id="npwarn" role="status"></p>' +
      '<button class="cta next" id="np-check">Kiértékelés</button>';
    window.scrollTo(0, 0);
  }

  function npInput(el) {
    var i = Number(el.getAttribute('data-i'));
    nine.answers[i] = el.value;
    nine.warned = false;
    var warn = document.getElementById('npwarn');
    if (warn) warn.textContent = '';
    store('np.draft', { id: nine.game.id, answers: nine.answers });
    var berry = app.querySelector('.berry[data-i="' + i + '"]');
    if (berry) berry.className = 'berry' + (el.value.trim() ? ' set' : '');
  }

  function checkNine() {
    var game = nine.game, items = npItems(game);
    var empty = nine.answers.filter(function (a) { return !a.trim(); }).length;
    if (empty && !nine.warned) {       // véletlen koppintás ellen: üres válasznál egyszer visszakérdez
      nine.warned = true;
      document.getElementById('npwarn').textContent = empty + ' válasz még üres. Ha így is kéred a kiértékelést, koppints újra.';
      return;
    }
    nine.result = items.map(function (it, i) { return npCorrect(nine.answers[i], it); });
    var played = npPlayed();
    if (played.indexOf(game.id) < 0) played.push(game.id);
    store('np.played', played);
    store('np.draft', null);
    renderNineResult();
  }

  function renderNineResult() {
    var game = nine.game, items = npItems(game), n = items.length, pairs = !game.closer;
    var okN = nine.result.filter(Boolean).length, bad = n - okN;
    var cl = clusterHTML(n, nine.result.map(function (ok) { return ok ? 'ok' : 'bad'; }), {
      W: 240, H: 250, top: 44, rmax: 27, roll: false, cur: 0, anim: 'fall',
      label: 'A játék fürtje: ' + okN + ' helyes, ' + bad + ' hibás válasz'
    });
    var link = pairs
      ? '<div class="why good"><h2 class="disp">' + esc(game.theme) + '</h2><p>' + esc(game.pairs.join(' · ')) + '</p></div>'
      : '<div class="why good"><h2 class="disp">Összefüggés: ' + esc(game.link) + '</h2>' + (game.note ? '<p>' + esc(game.note) + '</p>' : '') + '</div>';
    var review = items.map(function (it, i) {
      var ok = nine.result[i], given = nine.answers[i].trim();
      return '<li><p class="rq">' + npLabel(game, i) + '. ' + rich(it.q) + '</p>' +
        '<p class="' + (ok ? 'ra' : 'rb') + '">A te válaszod: ' + (given ? esc(given) : '–') + '</p>' +
        (ok ? '' : '<p class="ra">Helyes: ' + esc(it.a[0]) + '</p>') +
        (it.k ? '<p class="rk">' + esc(it.k) + '</p>' : '') + '</li>';
    }).join('');
    app.innerHTML =
      '<div class="rhead"><span class="topic-label">9+1 · ' + esc(game.type) + '</span>' + palsHTML() + '</div>' +
      '<div class="rcluster">' + cl.html + '</div>' +
      '<div class="score disp"><b>' + okN + '</b><span aria-hidden="true">/' + n + '</span></div>' +
      '<h1 class="verdict disp">' + (bad ? okN + ' gyöngyszem, ' + bad + ' mazsola' : 'Hibátlan szüret: ' + n + ' gyöngyszem') + '</h1>' +
      link +
      '<section class="review-wrap"><h2>A tíz válasz</h2><ul class="review">' + review + '</ul></section>' +
      '<div class="actions"><button class="cta" id="np-again">Új 9+1</button><button class="ghost" id="home">Vissza a témákhoz</button></div>';
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
  function syncTime() {
    var t = document.getElementById('time'), sk = document.getElementById('seek');
    if (t) t.textContent = mmss(audio.currentTime);
    if (sk && !scrubbing) { sk.value = audio.currentTime; sk.setAttribute('aria-valuetext', mmss(audio.currentTime)); }
  }
  function syncDuration() {
    var sk = document.getElementById('seek'), d = document.getElementById('dur');
    if (!isFinite(audio.duration) || !audio.duration) return;
    if (sk) sk.max = audio.duration;
    if (d) d.textContent = mmss(audio.duration);
  }
  audio.addEventListener('timeupdate', syncTime);
  audio.addEventListener('loadedmetadata', syncDuration);
  audio.addEventListener('durationchange', syncDuration);
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
      if (qs.length) startRound(qs, free);
      return;
    }
    if (t.id === 'np') return startNine(false);
    if (t.id === 'np-check') return checkNine();
    if (t.id === 'np-again') return startNine(true);
    if (t.id === 'accept') return acceptFree();
    if (t.id === 'next') return nextQuestion();
    if (t.id === 'hold') return holdAdvance();
    if (t.id === 'play') { if (audio.paused) { var p = audio.play(); if (p && p.catch) p.catch(function () {}); } else audio.pause(); return; }
    if (t.id === 'quit' || t.id === 'home') return renderHome();
    if (t.id === 'retry') {
      var wrong = round.items.filter(function (it, i) { return !round.results[i]; }).map(function (it) { return it.q; });
      return startRound(shuffle(wrong), round.free);
    }
  });

  app.addEventListener('submit', function (ev) {
    if (ev.target.id !== 'freeform') return;
    ev.preventDefault();
    answerFree();
  });

  app.addEventListener('input', function (ev) {
    if (nine && ev.target.classList.contains('np-in')) return npInput(ev.target);
    if (ev.target.id === 'seek') {
      scrubbing = true;
      holdAdvance();
      var v = Number(ev.target.value);
      document.getElementById('time').textContent = mmss(v);
      ev.target.setAttribute('aria-valuetext', mmss(v));
      if (isFinite(audio.duration)) audio.currentTime = v;
      return;
    }
    if (ev.target.id !== 'n') return;
    wantN = Number(ev.target.value);
    document.getElementById('nout').textContent = wantN;
    store('n', wantN);
  });

  app.addEventListener('change', function (ev) {
    if (ev.target.id === 'free') { free = ev.target.checked; store('free', free); return updateBar(); }
    if (ev.target.id !== 'seek') return;
    scrubbing = false;
    if (isFinite(audio.duration)) audio.currentTime = Number(ev.target.value);
    if (audio.paused) { var p = audio.play(); if (p && p.catch) p.catch(function () {}); }
  });

  document.addEventListener('keydown', function (ev) {
    if (nine && ev.key === 'Enter' && ev.target.classList && ev.target.classList.contains('np-in')) {
      ev.preventDefault();             // Enter: a következő mezőre, az utolsóról a Kiértékelés gombra
      var ins = app.querySelectorAll('.np-in'), at = Number(ev.target.getAttribute('data-i'));
      (ins[at + 1] || document.getElementById('np-check')).focus();
      return;
    }
    if (!round || ev.altKey || ev.ctrlKey || ev.metaKey) return;
    if (ev.target.id === 'seek') return;
    if (ev.target.id === 'freein') return;           // Enter: a form submit eseménye küldi be
    var it = round.items[round.idx];
    if (!it) return;
    if (round.free) {
      if (it.pick !== null && ev.key === 'Enter' && ev.target.tagName !== 'BUTTON') { ev.preventDefault(); nextQuestion(); }
      return;
    }
    if (!document.getElementById('opts')) return;
    if (it.pick === null) {
      var k = ev.key.toUpperCase();
      var pos = '1234'.indexOf(k) >= 0 ? Number(k) - 1 : KEYS.indexOf(k);
      if (pos >= 0 && pos < it.order.length) { ev.preventDefault(); answer(pos); }
    } else if (ev.key === 'Enter' && ev.target.tagName !== 'BUTTON') { ev.preventDefault(); nextQuestion(); }
  });

  /* ---------- indulás ---------- */
  setPal(load('pal', 'green'));
  wantN = Math.max(1, Math.min(MAX_N, Number(load('n', 10)) || 10));
  free = load('free', false) === true;
  // A 9+1 játékok fájlja nem kötelező: ha nem tölthető be, a felület nélküle indul.
  var npReady = fetch('data/kilenc_plusz_egy.json').then(function (r) { return r.ok ? r.json() : null; })
    .then(function (d) { npData = d && Array.isArray(d.games) ? d : null; }).catch(function () { npData = null; });
  fetch('data/questions.json').then(function (r) {
    if (!r.ok) throw new Error(r.status);
    return r.json();
  }).then(function (d) {
    return npReady.then(function () { return d; });
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
