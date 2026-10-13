// ==========================================================================
// IRREGULAR VERBS MUSIC ACADEMY - INTERACTIVE CONTROLLER (app.js)
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {
  // 1. Tracks definition
  const TRACKS = [
    {
      id: 0,
      title: "01. Irregular Verbs Rhyme Song",
      subtitle: "Aprende por rimas y familias de sonido",
      file: "01_Irregular_Verbs_Rhyme_Song.mp3",
      duration: "8:45",
      lyrics: (typeof RHYMES_LYRICS !== 'undefined' ? RHYMES_LYRICS.lyrics : [])
    },
    {
      id: 1,
      title: "02. Complete PDF A to Z Study Track",
      subtitle: "Los 154 verbos en el orden exacto del PDF",
      file: "02_Irregular_Verbs_Complete_A_to_Z.mp3",
      duration: "12:15",
      lyrics: (typeof ATOZ_LYRICS !== 'undefined' ? ATOZ_LYRICS.lyrics : [])
    },
    {
      id: 2,
      title: "03. Irregular Verbs Beat Challenge",
      subtitle: "Entrenamiento de memoria activa y quiz",
      file: "03_Irregular_Verbs_Challenge_Quiz.mp3",
      duration: "5:44",
      lyrics: (typeof QUIZ_LYRICS !== 'undefined' ? QUIZ_LYRICS.lyrics : [])
    }
  ];

  let currentTrackIdx = 0;
  const audio = document.getElementById('master-audio');
  let isPlaying = false;

  // DOM Elements
  const btnPlay = document.getElementById('btn-play');
  const playIcon = document.getElementById('play-icon');
  const btnRewind = document.getElementById('btn-rewind');
  const btnForward = document.getElementById('btn-forward');
  const speedSelect = document.getElementById('speed-select');
  const volumeSlider = document.getElementById('volume-slider');
  const btnMute = document.getElementById('btn-mute');
  const muteIcon = document.getElementById('mute-icon');
  const progressWrap = document.getElementById('progress-wrap');
  const progressFilled = document.getElementById('progress-filled');
  const timeCurrent = document.getElementById('time-current');
  const timeTotal = document.getElementById('time-total');
  const nowPlayingTitle = document.getElementById('now-playing-title');
  const nowPlayingDesc = document.getElementById('now-playing-desc');
  const btnDownloadActive = document.getElementById('btn-download-active');
  const karaokeList = document.getElementById('karaoke-list');
  const trackCards = document.querySelectorAll('.track-card');

  // Format seconds to mm:ss
  function formatTime(sec) {
    if (isNaN(sec) || sec < 0) return "0:00";
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return `${m}:${s < 10 ? '0' : ''}${s}`;
  }

  // Load Track
  function loadTrack(idx, autoPlay = false) {
    currentTrackIdx = idx;
    const t = TRACKS[idx];
    audio.src = t.file;
    nowPlayingTitle.textContent = t.title;
    nowPlayingDesc.textContent = t.subtitle;
    btnDownloadActive.href = t.file;
    btnDownloadActive.download = t.file;

    trackCards.forEach((c, i) => {
      c.classList.toggle('active', i === idx);
    });

    renderKaraokeLyrics(t.lyrics);

    if (autoPlay) {
      audio.play().then(() => {
        isPlaying = true;
        updatePlayStateUI();
      }).catch(err => console.log('Autoplay error:', err));
    } else {
      isPlaying = false;
      updatePlayStateUI();
    }
  }

  function updatePlayStateUI() {
    if (isPlaying) {
      playIcon.textContent = '⏸';
      startVisualizer();
    } else {
      playIcon.textContent = '▶';
      stopVisualizer();
    }
  }

  // Play / Pause Toggle
  function togglePlay() {
    if (audio.paused) {
      audio.play().then(() => {
        isPlaying = true;
        updatePlayStateUI();
      }).catch(err => console.log('Play error:', err));
    } else {
      audio.pause();
      isPlaying = false;
      updatePlayStateUI();
    }
  }

  btnPlay.addEventListener('click', togglePlay);

  btnRewind.addEventListener('click', () => {
    audio.currentTime = Math.max(0, audio.currentTime - 10);
  });

  btnForward.addEventListener('click', () => {
    audio.currentTime = Math.min(audio.duration || 0, audio.currentTime + 10);
  });

  speedSelect.addEventListener('change', (e) => {
    audio.playbackRate = parseFloat(e.target.value);
  });

  volumeSlider.addEventListener('input', (e) => {
    audio.volume = parseFloat(e.target.value);
    muteIcon.textContent = audio.volume === 0 ? '🔇' : '🔊';
  });

  btnMute.addEventListener('click', () => {
    audio.muted = !audio.muted;
    muteIcon.textContent = audio.muted ? '🔇' : '🔊';
  });

  // Track switching cards
  trackCards.forEach((card) => {
    card.addEventListener('click', () => {
      const idx = parseInt(card.getAttribute('data-track-index'), 10);
      loadTrack(idx, true);
    });
  });

  // Audio Events
  audio.addEventListener('timeupdate', () => {
    const cur = audio.currentTime;
    const dur = audio.duration || 1;
    timeCurrent.textContent = formatTime(cur);
    timeTotal.textContent = formatTime(dur);
    progressFilled.style.width = `${(cur / dur) * 100}%`;

    syncKaraoke(cur);
  });

  audio.addEventListener('loadedmetadata', () => {
    timeTotal.textContent = formatTime(audio.duration);
  });

  audio.addEventListener('ended', () => {
    isPlaying = false;
    updatePlayStateUI();
  });

  // Progress scrubbing
  progressWrap.addEventListener('click', (e) => {
    const rect = progressWrap.getBoundingClientRect();
    const pos = (e.clientX - rect.left) / rect.width;
    audio.currentTime = pos * audio.duration;
  });

  // 2. Karaoke Rendering & Sync
  function renderKaraokeLyrics(lyrics) {
    karaokeList.innerHTML = '';
    if (!lyrics || lyrics.length === 0) {
      karaokeList.innerHTML = '<div style="text-align:center; padding: 40px; color: var(--text-dim);">No lyrics available for this track.</div>';
      return;
    }

    lyrics.forEach((item, idx) => {
      const div = document.createElement('div');
      div.setAttribute('data-index', idx);
      div.setAttribute('data-start', item.start || 0);

      if (item.type === 'verse_header' || item.type === 'chapter_header' || item.type === 'intro' || item.type === 'outro' || item.type === 'chorus') {
        div.className = 'lyrics-header-item';
        div.innerHTML = `<span>${item.section || item.text}</span>`;
      } else if (item.type === 'verb') {
        div.className = 'lyrics-item';
        const trio = item.english || `${item.infinitive} · ${item.past_simple} · ${item.past_participle}`;
        const esp = item.spanish || '';
        div.innerHTML = `
          <div class="verb-trio">
            <span class="verb-form">${trio}</span>
          </div>
          <div class="verb-trans">${esp}</div>
        `;
      } else if (item.type === 'quiz_item') {
        div.className = 'lyrics-item';
        div.innerHTML = `
          <div class="verb-trio">
            <span class="verb-form">#${item.number}: ${item.infinitive} · ${item.past_simple} ➔ <strong>${item.past_participle}</strong></span>
          </div>
          <div class="verb-trans">${item.spanish}</div>
        `;
      } else {
        div.className = 'lyrics-item';
        div.innerHTML = `<div>${item.text || ''}</div>`;
      }

      div.addEventListener('click', () => {
        if (item.start !== undefined) {
          audio.currentTime = item.start;
          if (audio.paused) {
            togglePlay();
          }
        }
      });

      karaokeList.appendChild(div);
    });
  }

  let lastActiveIdx = -1;
  function syncKaraoke(time) {
    const items = TRACKS[currentTrackIdx].lyrics;
    if (!items || items.length === 0) return;

    let activeIdx = -1;
    for (let i = 0; i < items.length; i++) {
      if (time >= items[i].start) {
        activeIdx = i;
      } else {
        break;
      }
    }

    if (activeIdx !== lastActiveIdx) {
      lastActiveIdx = activeIdx;
      const allEls = karaokeList.children;
      for (let i = 0; i < allEls.length; i++) {
        if (i === activeIdx) {
          allEls[i].classList.add('active');
          // Smooth scroll active element into center
          allEls[i].scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else {
          allEls[i].classList.remove('active');
        }
      }
    }
  }

  // 3. Audio Visualizer Canvas
  const canvas = document.getElementById('audio-visualizer');
  const ctx = canvas.getContext('2d');
  let animId = null;

  function resizeCanvas() {
    canvas.width = canvas.parentElement.clientWidth;
    canvas.height = 72;
  }
  window.addEventListener('resize', resizeCanvas);
  resizeCanvas();

  function drawVisualizer() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const bars = 48;
    const barWidth = canvas.width / bars;
    const time = Date.now() * 0.005;

    for (let i = 0; i < bars; i++) {
      let h;
      if (isPlaying) {
        // Dynamic pulsating bars simulating music spectrum
        const wave = Math.sin(time * 2 + i * 0.3) * 0.5 + 0.5;
        const wave2 = Math.cos(time * 3 + i * 0.5) * 0.3 + 0.5;
        h = Math.max(6, (wave * 0.7 + wave2 * 0.3) * (canvas.height - 12));
      } else {
        h = 4;
      }

      const x = i * barWidth;
      const y = (canvas.height - h) / 2;

      const grad = ctx.createLinearGradient(0, y, 0, y + h);
      grad.addColorStop(0, '#38bdf8');
      grad.addColorStop(0.5, '#818cf8');
      grad.addColorStop(1, '#c084fc');

      ctx.fillStyle = grad;
      ctx.fillRect(x + 2, y, barWidth - 4, h);
    }

    animId = requestAnimationFrame(drawVisualizer);
  }

  function startVisualizer() {
    if (!animId) animId = requestAnimationFrame(drawVisualizer);
  }

  function stopVisualizer() {
    // Keep 1 frame of idle state
  }
  drawVisualizer();

  // 4. VERBS EXPLORER & SOUNDBOARD (154 Verbs)
  const verbsGrid = document.getElementById('verbs-grid');
  const searchInput = document.getElementById('search-verbs');
  const filterChips = document.querySelectorAll('.filter-chip');
  const expRangeBtns = document.querySelectorAll('[data-exp-start]');
  let activeFamily = 'all';
  let expStart = 1;
  let expEnd = 154;

  function speakVerb(verbObj) {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const textToSpeak = `${verbObj.infinitive}. ${verbObj.past_simple}. ${verbObj.past_participle}.`;
      const utter = new SpeechSynthesisUtterance(textToSpeak);
      utter.lang = 'en-US';
      utter.rate = 0.9;
      window.speechSynthesis.speak(utter);
    }
  }

  function renderVerbs() {
    if (typeof VERBS_DATA === 'undefined' || !VERBS_DATA.verbs) return;
    const query = searchInput.value.toLowerCase().trim();
    const verbs = VERBS_DATA.verbs;

    verbsGrid.innerHTML = '';
    let matchCount = 0;

    verbs.forEach(v => {
      const inRange = v.id >= expStart && v.id <= expEnd;
      const matchesSearch = !query || v.search_text.includes(query);
      const matchesFamily = activeFamily === 'all' || v.family_id === activeFamily;

      if (inRange && matchesSearch && matchesFamily) {
        matchCount++;
        const card = document.createElement('div');
        card.className = 'verb-card';
        card.innerHTML = `
          <div>
            <div class="verb-card-header">
              <span class="verb-num">#${v.id}</span>
              <button class="verb-speak-btn" id="speak-btn-${v.id}" title="Escuchar pronunciación">🔊</button>
            </div>
            <div class="verb-forms-row">
              <div class="verb-primary">${v.infinitive}</div>
              <div class="verb-secondary">${v.past_simple} &nbsp;·&nbsp; ${v.past_participle}</div>
            </div>
            <div class="verb-meaning">${v.spanish}</div>
          </div>
          <div class="verb-family-tag">${v.family_name}</div>
        `;

        card.querySelector('.verb-speak-btn').addEventListener('click', (e) => {
          e.stopPropagation();
          speakVerb(v);
        });

        card.addEventListener('click', () => speakVerb(v));
        verbsGrid.appendChild(card);
      }
    });

    if (matchCount === 0) {
      verbsGrid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--text-dim);">No se encontraron verbos que coincidan con la búsqueda o el rango seleccionado.</div>`;
    }
  }

  searchInput.addEventListener('input', renderVerbs);

  filterChips.forEach(chip => {
    chip.addEventListener('click', () => {
      filterChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      activeFamily = chip.getAttribute('data-family');
      renderVerbs();
    });
  });

  expRangeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      expRangeBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      expStart = parseInt(btn.getAttribute('data-exp-start'), 10);
      expEnd = parseInt(btn.getAttribute('data-exp-end'), 10);
      renderVerbs();
    });
  });

  renderVerbs();

  // 5. QUIZ ARENA (CON SELECCIÓN DE RANGO DE VERBOS)
  const quizVerbDisplay = document.getElementById('quiz-verb-display');
  const quizTransDisplay = document.getElementById('quiz-trans-display');
  const quizItemBadge = document.getElementById('quiz-item-badge');
  const quizInputPast = document.getElementById('quiz-input-past');
  const quizInputPart = document.getElementById('quiz-input-part');
  const quizFeedback = document.getElementById('quiz-feedback');
  const btnQuizCheck = document.getElementById('btn-quiz-check');
  const btnQuizNext = document.getElementById('btn-quiz-next');
  const btnQuizShow = document.getElementById('btn-quiz-show');
  const quizScoreEl = document.getElementById('quiz-score');
  const quizStreakEl = document.getElementById('quiz-streak');
  const quizTotalEl = document.getElementById('quiz-total');

  // Range controls
  const quizPoolBadge = document.getElementById('quiz-pool-badge');
  const quizRangePresets = document.querySelectorAll('#quiz-range-presets .range-preset-btn');
  const quizRangeMin = document.getElementById('quiz-range-min');
  const quizRangeMax = document.getElementById('quiz-range-max');
  const btnApplyQuizRange = document.getElementById('btn-apply-quiz-range');

  let quizMinId = 1;
  let quizMaxId = 49; // Default: Verbs 1 to 49 (Page 1)
  let quizScore = 0;
  let quizStreak = 0;
  let quizTotal = 0;
  let currentQuizVerb = null;

  function getQuizPool() {
    if (typeof VERBS_DATA === 'undefined' || !VERBS_DATA.verbs) return [];
    return VERBS_DATA.verbs.filter(v => v.id >= quizMinId && v.id <= quizMaxId);
  }

  function updateQuizPoolUI() {
    const pool = getQuizPool();
    quizPoolBadge.textContent = `${pool.length} verbos (#${quizMinId} a #${quizMaxId})`;
  }

  function setQuizRange(start, end) {
    quizMinId = Math.max(1, Math.min(start, 154));
    quizMaxId = Math.max(quizMinId, Math.min(end, 154));
    quizRangeMin.value = quizMinId;
    quizRangeMax.value = quizMaxId;
    updateQuizPoolUI();
    pickQuizVerb();
  }

  // Quiz Preset buttons
  quizRangePresets.forEach(btn => {
    btn.addEventListener('click', () => {
      quizRangePresets.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const start = parseInt(btn.getAttribute('data-start'), 10);
      const end = parseInt(btn.getAttribute('data-end'), 10);
      setQuizRange(start, end);
    });
  });

  // Apply custom range
  btnApplyQuizRange.addEventListener('click', () => {
    quizRangePresets.forEach(b => b.classList.remove('active'));
    const start = parseInt(quizRangeMin.value, 10) || 1;
    const end = parseInt(quizRangeMax.value, 10) || 49;
    setQuizRange(start, end);
  });

  function synthBeep(isGood) {
    try {
      const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      if (isGood) {
        osc.frequency.setValueAtTime(523.25, audioCtx.currentTime); // C5
        osc.frequency.exponentialRampToValueAtTime(659.25, audioCtx.currentTime + 0.15); // E5
        gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.3);
      } else {
        osc.frequency.setValueAtTime(220, audioCtx.currentTime); // A3
        osc.frequency.exponentialRampToValueAtTime(160, audioCtx.currentTime + 0.2);
        gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.25);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.25);
      }
    } catch(e) {}
  }

  function pickQuizVerb() {
    const pool = getQuizPool();
    if (pool.length === 0) {
      quizVerbDisplay.textContent = 'Sin verbos';
      quizTransDisplay.textContent = 'Ajusta el rango numérico';
      return;
    }
    currentQuizVerb = pool[Math.floor(Math.random() * pool.length)];
    quizVerbDisplay.textContent = currentQuizVerb.infinitive;
    quizTransDisplay.textContent = currentQuizVerb.spanish;
    if (quizItemBadge) {
      quizItemBadge.textContent = `Verbo #${currentQuizVerb.id} del PDF (${currentQuizVerb.family_name})`;
    }
    quizInputPast.value = '';
    quizInputPart.value = '';
    quizInputPast.focus();
    quizFeedback.textContent = '';
    quizFeedback.className = 'quiz-feedback';
  }

  function checkQuizAnswer() {
    if (!currentQuizVerb) return;
    const userPast = quizInputPast.value.trim().toLowerCase();
    const userPart = quizInputPart.value.trim().toLowerCase();

    const validPast = currentQuizVerb.past_simple.toLowerCase().split('/').map(s => s.trim());
    const validPart = currentQuizVerb.past_participle.toLowerCase().split('/').map(s => s.trim());

    const isPastCorrect = validPast.some(v => v.includes(userPast) || userPast.includes(v));
    const isPartCorrect = validPart.some(v => v.includes(userPart) || userPart.includes(v));

    quizTotal++;
    if (isPastCorrect && isPartCorrect) {
      quizScore += 10;
      quizStreak++;
      synthBeep(true);
      quizFeedback.textContent = `¡Correcto! +10 puntos 🎉 (${currentQuizVerb.infinitive} - ${currentQuizVerb.past_simple} - ${currentQuizVerb.past_participle})`;
      quizFeedback.className = 'quiz-feedback feedback-correct';
      speakVerb(currentQuizVerb);
    } else {
      quizStreak = 0;
      synthBeep(false);
      quizFeedback.textContent = `Respuesta esperada: ${currentQuizVerb.past_simple} / ${currentQuizVerb.past_participle}`;
      quizFeedback.className = 'quiz-feedback feedback-wrong';
    }

    quizScoreEl.textContent = quizScore;
    quizStreakEl.textContent = quizStreak;
    quizTotalEl.textContent = quizTotal;
  }

  btnQuizCheck.addEventListener('click', checkQuizAnswer);
  btnQuizNext.addEventListener('click', pickQuizVerb);
  btnQuizShow.addEventListener('click', () => {
    if (!currentQuizVerb) return;
    quizInputPast.value = currentQuizVerb.past_simple;
    quizInputPart.value = currentQuizVerb.past_participle;
    quizFeedback.textContent = `Formas correctas: ${currentQuizVerb.past_simple} - ${currentQuizVerb.past_participle}`;
    quizFeedback.className = 'quiz-feedback';
    speakVerb(currentQuizVerb);
  });

  [quizInputPast, quizInputPart].forEach(inp => {
    inp.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') checkQuizAnswer();
    });
  });

  updateQuizPoolUI();
  pickQuizVerb();

  // 6. Navigation Tabs
  const navTabs = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');

  navTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const target = tab.getAttribute('data-tab');
      navTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      tabContents.forEach(c => {
        c.classList.toggle('active', c.id === `tab-${target}`);
      });
    });
  });

  // Initialize First Track
  loadTrack(0, false);
});
