(() => {
  'use strict';

  const STORAGE_KEY = 'typing-lab-settings-v0';

  const FINGER_LABELS = {
    leftPinky: { name: '左手小指', short: '小', hand: 'left', handName: 'LEFT HAND', letter: 'L1' },
    leftRing: { name: '左手無名指', short: '無', hand: 'left', handName: 'LEFT HAND', letter: 'L2' },
    leftMiddle: { name: '左手中指', short: '中', hand: 'left', handName: 'LEFT HAND', letter: 'L3' },
    leftIndex: { name: '左手食指', short: '食', hand: 'left', handName: 'LEFT HAND', letter: 'L4' },
    rightIndex: { name: '右手食指', short: '食', hand: 'right', handName: 'RIGHT HAND', letter: 'R4' },
    rightMiddle: { name: '右手中指', short: '中', hand: 'right', handName: 'RIGHT HAND', letter: 'R3' },
    rightRing: { name: '右手無名指', short: '無', hand: 'right', handName: 'RIGHT HAND', letter: 'R2' },
    rightPinky: { name: '右手小指', short: '小', hand: 'right', handName: 'RIGHT HAND', letter: 'R1' },
    thumb: { name: '拇指', short: '拇', hand: 'thumb', handName: 'THUMB', letter: 'TH' }
  };

  const FINGER_MAP = {};
  const assignFinger = (finger, codes) => codes.forEach((code) => { FINGER_MAP[code] = FINGER_LABELS[finger]; });

  assignFinger('leftPinky', ['Backquote', 'Digit1', 'KeyQ', 'KeyA', 'KeyZ', 'Tab', 'CapsLock', 'ShiftLeft']);
  assignFinger('leftRing', ['Digit2', 'KeyW', 'KeyS', 'KeyX']);
  assignFinger('leftMiddle', ['Digit3', 'KeyE', 'KeyD', 'KeyC']);
  assignFinger('leftIndex', ['Digit4', 'Digit5', 'KeyR', 'KeyT', 'KeyF', 'KeyG', 'KeyV', 'KeyB']);
  assignFinger('rightIndex', ['Digit6', 'Digit7', 'KeyY', 'KeyU', 'KeyH', 'KeyJ', 'KeyN', 'KeyM']);
  assignFinger('rightMiddle', ['Digit8', 'KeyI', 'KeyK', 'Comma']);
  assignFinger('rightRing', ['Digit9', 'KeyO', 'KeyL', 'Period']);
  assignFinger('rightPinky', ['Digit0', 'Minus', 'Equal', 'KeyP', 'BracketLeft', 'BracketRight', 'Backslash', 'Semicolon', 'Quote', 'Slash', 'Enter', 'Backspace', 'ShiftRight']);
  assignFinger('thumb', ['Space', 'AltLeft', 'AltRight']);

  const KEY_LABELS = {
    Backquote: '`', Digit1: '1', Digit2: '2', Digit3: '3', Digit4: '4', Digit5: '5', Digit6: '6', Digit7: '7', Digit8: '8', Digit9: '9', Digit0: '0', Minus: '-', Equal: '=',
    KeyQ: 'Q', KeyW: 'W', KeyE: 'E', KeyR: 'R', KeyT: 'T', KeyY: 'Y', KeyU: 'U', KeyI: 'I', KeyO: 'O', KeyP: 'P', BracketLeft: '[', BracketRight: ']', Backslash: '\\',
    KeyA: 'A', KeyS: 'S', KeyD: 'D', KeyF: 'F', KeyG: 'G', KeyH: 'H', KeyJ: 'J', KeyK: 'K', KeyL: 'L', Semicolon: ';', Quote: "'",
    KeyZ: 'Z', KeyX: 'X', KeyC: 'C', KeyV: 'V', KeyB: 'B', KeyN: 'N', KeyM: 'M', Comma: ',', Period: '.', Slash: '/',
    Tab: 'TAB', CapsLock: 'CAPS', Enter: 'ENTER', Backspace: '⌫', ShiftLeft: 'SHIFT', ShiftRight: 'SHIFT', ControlLeft: 'CTRL', ControlRight: 'CTRL', AltLeft: 'ALT', AltRight: 'ALT', Space: 'SPACE'
  };

  const KEYBOARD_ROWS = [
    [
      ['Backquote', ''], ['Digit1', ''], ['Digit2', ''], ['Digit3', ''], ['Digit4', ''], ['Digit5', ''], ['Digit6', ''], ['Digit7', ''], ['Digit8', ''], ['Digit9', ''], ['Digit0', ''], ['Minus', ''], ['Equal', ''], ['Backspace', 'key-wide-1']
    ],
    [
      ['Tab', 'key-wide-1'], ['KeyQ', ''], ['KeyW', ''], ['KeyE', ''], ['KeyR', ''], ['KeyT', ''], ['KeyY', ''], ['KeyU', ''], ['KeyI', ''], ['KeyO', ''], ['KeyP', ''], ['BracketLeft', ''], ['BracketRight', ''], ['Backslash', '']
    ],
    [
      ['CapsLock', 'key-wide-1'], ['KeyA', ''], ['KeyS', ''], ['KeyD', ''], ['KeyF', ''], ['KeyG', ''], ['KeyH', ''], ['KeyJ', ''], ['KeyK', ''], ['KeyL', ''], ['Semicolon', ''], ['Quote', ''], ['Enter', 'key-wide-1']
    ],
    [
      ['ShiftLeft', 'key-wide-2'], ['KeyZ', ''], ['KeyX', ''], ['KeyC', ''], ['KeyV', ''], ['KeyB', ''], ['KeyN', ''], ['KeyM', ''], ['Comma', ''], ['Period', ''], ['Slash', ''], ['ShiftRight', 'key-wide-2']
    ],
    [
      ['ControlLeft', 'key-wide-1'], ['AltLeft', 'key-wide-1'], ['Space', 'key-wide-4'], ['AltRight', 'key-wide-1'], ['ControlRight', 'key-wide-1']
    ]
  ];

  const ZHUYIN_TO_KEY = {
    'ㄅ': { key: '1', code: 'Digit1' }, 'ㄆ': { key: 'q', code: 'KeyQ' }, 'ㄇ': { key: 'a', code: 'KeyA' }, 'ㄈ': { key: 'z', code: 'KeyZ' },
    'ㄉ': { key: '2', code: 'Digit2' }, 'ㄊ': { key: 'w', code: 'KeyW' }, 'ㄋ': { key: 's', code: 'KeyS' }, 'ㄌ': { key: 'x', code: 'KeyX' },
    'ㄍ': { key: 'e', code: 'KeyE' }, 'ㄎ': { key: 'd', code: 'KeyD' }, 'ㄏ': { key: 'c', code: 'KeyC' },
    'ㄐ': { key: 'r', code: 'KeyR' }, 'ㄑ': { key: 'f', code: 'KeyF' }, 'ㄒ': { key: 'v', code: 'KeyV' },
    'ㄓ': { key: '5', code: 'Digit5' }, 'ㄔ': { key: 't', code: 'KeyT' }, 'ㄕ': { key: 'g', code: 'KeyG' }, 'ㄖ': { key: 'b', code: 'KeyB' },
    'ㄗ': { key: 'y', code: 'KeyY' }, 'ㄘ': { key: 'h', code: 'KeyH' }, 'ㄙ': { key: 'n', code: 'KeyN' },
    'ㄧ': { key: 'u', code: 'KeyU' }, 'ㄨ': { key: 'j', code: 'KeyJ' }, 'ㄩ': { key: 'm', code: 'KeyM' },
    'ㄚ': { key: '8', code: 'Digit8' }, 'ㄛ': { key: 'i', code: 'KeyI' }, 'ㄜ': { key: 'k', code: 'KeyK' }, 'ㄝ': { key: ',', code: 'Comma' },
    'ㄞ': { key: '9', code: 'Digit9' }, 'ㄟ': { key: 'o', code: 'KeyO' }, 'ㄠ': { key: 'l', code: 'KeyL' }, 'ㄡ': { key: '.', code: 'Period' },
    'ㄢ': { key: '0', code: 'Digit0' }, 'ㄣ': { key: 'p', code: 'KeyP' }, 'ㄤ': { key: ';', code: 'Semicolon' }, 'ㄥ': { key: '/', code: 'Slash' }, 'ㄦ': { key: '-', code: 'Minus' },
    'ˊ': { key: '6', code: 'Digit6' }, 'ˇ': { key: '3', code: 'Digit3' }, 'ˋ': { key: '4', code: 'Digit4' }, '˙': { key: '7', code: 'Digit7' }
  };

  const ENGLISH_FRAGMENTS = [
    'keep your hands quiet and let each key arrive under the right finger',
    'small pauses are enough to make room for a careful practice session',
    'steady movement is more useful than rushing toward a faster number',
    'the keyboard becomes familiar when every letter has a place to land',
    'return to the home row and let your hands learn the shape of the work',
    'a clear rhythm starts with a light touch and a relaxed wrist',
    'practice one clean phrase, then allow the next phrase to appear',
    'good typing feels quiet because the fingers already know where to go',
    'when the workday gives you a minute, use it to build a little ease',
    'look ahead, breathe once, and keep the movement smaller than the thought'
  ];

  const ZHUYIN_SAMPLES = [
    { text: '今天', syllables: ['ㄐㄧㄣ', 'ㄊㄧㄢ'] },
    { text: '慢慢來', syllables: ['ㄇㄢˋ', 'ㄇㄢˋ', 'ㄌㄞˊ'] },
    { text: '專注', syllables: ['ㄓㄨㄢ', 'ㄓㄨˋ'] },
    { text: '保持節奏', syllables: ['ㄅㄠˇ', 'ㄔˊ', 'ㄐㄧㄝˊ', 'ㄗㄡˋ'] },
    { text: '指法練習', syllables: ['ㄓˇ', 'ㄈㄚˇ', 'ㄌㄧㄢˋ', 'ㄒㄧˊ'] },
    { text: '工作順利', syllables: ['ㄍㄨㄥ', 'ㄗㄨㄛˋ', 'ㄕㄨㄣˋ', 'ㄌㄧˋ'] },
    { text: '你好', syllables: ['ㄋㄧˇ', 'ㄏㄠˇ'] },
    { text: '謝謝', syllables: ['ㄒㄧㄝˋ', 'ㄒㄧㄝˋ'] },
    { text: '現在', syllables: ['ㄒㄧㄢˋ', 'ㄗㄞˋ'] },
    { text: '每天', syllables: ['ㄇㄟˇ', 'ㄊㄧㄢ'] },
    { text: '練習', syllables: ['ㄌㄧㄢˋ', 'ㄒㄧˊ'] },
    { text: '休息', syllables: ['ㄒㄧㄡ', 'ㄒㄧˊ'] },
    { text: '桌面', syllables: ['ㄓㄨㄛ', 'ㄇㄧㄢˋ'] },
    { text: '應該', syllables: ['ㄧㄥ', 'ㄍㄞ'] },
    { text: '放鬆', syllables: ['ㄈㄤˋ', 'ㄙㄨㄥ'] },
    { text: '打字', syllables: ['ㄉㄚˇ', 'ㄗˋ'] },
    { text: '中文', syllables: ['ㄓㄨㄥ', 'ㄨㄣˊ'] },
    { text: '輸入法', syllables: ['ㄕㄨ', 'ㄖㄨˋ', 'ㄈㄚˇ'] },
    { text: '手指', syllables: ['ㄕㄡˇ', 'ㄓˇ'] },
    { text: '正確', syllables: ['ㄓㄥˋ', 'ㄑㄩㄝˋ'] },
    { text: '專心', syllables: ['ㄓㄨㄢ', 'ㄒㄧㄣ'] },
    { text: '一點', syllables: ['ㄧˋ', 'ㄉㄧㄢˇ'] },
    { text: '不急', syllables: ['ㄅㄨˋ', 'ㄐㄧˊ'] }
  ];

  const savedSettings = (() => {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
    } catch (error) {
      return {};
    }
  })();

  const state = {
    mode: savedSettings.mode === 'zhuyin' ? 'zhuyin' : 'english',
    paused: false,
    target: '',
    index: 0,
    zhuyinStream: [],
    zhuyinUnits: [],
    typed: 0,
    wrong: 0,
    lastFeedback: '準備好了就開始輸入',
    feedbackKind: 'idle',
    showFingerLabels: savedSettings.showFingerLabels !== false,
    errorTimer: null,
    promptTimer: null
  };

  const elements = {
    englishMode: document.querySelector('#english-mode'),
    zhuyinMode: document.querySelector('#zhuyin-mode'),
    settingsButton: document.querySelector('#settings-button'),
    settingsPanel: document.querySelector('#settings-panel'),
    settingsClose: document.querySelector('#settings-close'),
    showFingerLabels: document.querySelector('#show-finger-labels'),
    modeKicker: document.querySelector('#mode-kicker'),
    practiceTitle: document.querySelector('#practice-title'),
    promptCaption: document.querySelector('#prompt-caption'),
    promptCard: document.querySelector('#prompt-card'),
    promptDisplay: document.querySelector('#prompt-display'),
    zhuyinGuide: document.querySelector('#zhuyin-guide'),
    guideSymbols: document.querySelector('#guide-symbols'),
    guideKeys: document.querySelector('#guide-keys'),
    pauseButton: document.querySelector('#pause-button'),
    resetButton: document.querySelector('#reset-button'),
    currentKey: document.querySelector('#current-key'),
    fingerName: document.querySelector('#finger-name'),
    handName: document.querySelector('#hand-name'),
    feedbackMessage: document.querySelector('#feedback-message'),
    keyboardNote: document.querySelector('#keyboard-note'),
    keyboard: document.querySelector('#keyboard'),
    sessionStatus: document.querySelector('#session-status'),
    typedCount: document.querySelector('#typed-count'),
    wrongCount: document.querySelector('#wrong-count'),
    modeStat: document.querySelector('#mode-stat'),
    fingerStatus: document.querySelector('#finger-status'),
    fingerOrb: document.querySelector('#finger-orb'),
    fingerOrbLetter: document.querySelector('#finger-orb-letter'),
    orbLabel: document.querySelector('#orb-label'),
    footerModeNote: document.querySelector('#footer-mode-note')
  };

  function randomItem(items) {
    return items[Math.floor(Math.random() * items.length)];
  }

  function saveSettings() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      mode: state.mode,
      showFingerLabels: state.showFingerLabels
    }));
  }

  function ensureEnglishBuffer() {
    while (state.target.length < state.index + 540) {
      const fragment = randomItem(ENGLISH_FRAGMENTS);
      state.target += `${state.target ? ' ' : ''}${fragment}`;
    }
  }

  function appendZhuyinUnit() {
    const sample = randomItem(ZHUYIN_SAMPLES);
    const unitIndex = state.zhuyinUnits.length;
    const unit = { ...sample, unitIndex };
    state.zhuyinUnits.push(unit);

    sample.syllables.forEach((syllable, syllableIndex) => {
      Array.from(syllable).forEach((symbol) => {
        const mapping = ZHUYIN_TO_KEY[symbol];
        if (!mapping) return;
        state.zhuyinStream.push({
          code: mapping.code,
          display: mapping.key,
          symbol,
          unitIndex,
          syllableIndex,
          isCommit: false
        });
      });
      state.zhuyinStream.push({
        code: 'Space',
        display: '␠',
        symbol: '·',
        unitIndex,
        syllableIndex,
        isCommit: true
      });
    });
  }

  function ensureZhuyinBuffer() {
    while (state.zhuyinStream.length < state.index + 180) {
      appendZhuyinUnit();
    }
  }

  function resetPractice() {
    state.paused = false;
    state.index = 0;
    state.typed = 0;
    state.wrong = 0;
    state.lastFeedback = '準備好了就開始輸入';
    state.feedbackKind = 'idle';
    state.target = '';
    state.zhuyinStream = [];
    state.zhuyinUnits = [];

    if (state.mode === 'english') ensureEnglishBuffer();
    else ensureZhuyinBuffer();

    elements.promptCard.focus({ preventScroll: true });
    render();
  }

  function codeForEnglishCharacter(character) {
    if (character === ' ') return 'Space';
    if (character >= 'a' && character <= 'z') return `Key${character.toUpperCase()}`;
    const punctuation = { ',': 'Comma', '.': 'Period', "'": 'Quote', ';': 'Semicolon', '/': 'Slash', '-': 'Minus', '=': 'Equal', '[': 'BracketLeft', ']': 'BracketRight', '\\': 'Backslash' };
    return punctuation[character] || '';
  }

  function getCurrentToken() {
    if (state.mode === 'english') {
      ensureEnglishBuffer();
      const character = state.target[state.index];
      return {
        code: codeForEnglishCharacter(character),
        display: character === ' ' ? 'SPACE' : character.toUpperCase(),
        raw: character,
        finger: FINGER_MAP[codeForEnglishCharacter(character)]
      };
    }
    ensureZhuyinBuffer();
    const token = state.zhuyinStream[state.index];
    return token ? { ...token, finger: FINGER_MAP[token.code] } : null;
  }

  function createKeyboard() {
    elements.keyboard.innerHTML = KEYBOARD_ROWS.map((row) => {
      const keys = row.map(([code, size]) => {
        const finger = FINGER_MAP[code];
        const label = KEY_LABELS[code] || code;
        const fingerLabel = state.showFingerLabels && finger ? `<span class="key-finger">${finger.short}</span>` : '';
        return `<div class="keyboard-key ${size}" data-code="${code}" data-hand="${finger ? finger.hand : ''}" title="${finger ? finger.name : ''}"><span>${label}</span>${fingerLabel}</div>`;
      }).join('');
      return `<div class="keyboard-row">${keys}</div>`;
    }).join('');
  }

  function escapeText(text) {
    return String(text).replace(/[&<>"']/g, (character) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[character]));
  }

  function renderEnglishPrompt() {
    ensureEnglishBuffer();
    const start = Math.max(0, state.index - 5);
    const end = Math.min(state.target.length, state.index + 78);
    const content = [];

    for (let index = start; index < end; index += 1) {
      const character = state.target[index];
      const classes = ['prompt-char'];
      if (index < state.index) classes.push('is-typed');
      if (index === state.index) classes.push('is-current');
      if (character === ' ') classes.push('is-space');
      const display = character === ' ' ? '<span class="space-glyph">·</span>' : escapeText(character);
      content.push(`<span class="${classes.join(' ')}">${display}</span>`);
    }

    elements.promptDisplay.innerHTML = content.join('');
    elements.zhuyinGuide.classList.add('is-hidden');
  }

  function renderZhuyinGuide() {
    ensureZhuyinBuffer();
    const currentToken = getCurrentToken();
    const unitIndex = currentToken ? currentToken.unitIndex : 0;
    const start = Math.max(0, unitIndex - 1);
    const end = Math.min(state.zhuyinUnits.length, unitIndex + 6);
    const textContent = [];

    for (let index = start; index < end; index += 1) {
      const unit = state.zhuyinUnits[index];
      const className = index < unitIndex ? 'is-typed' : index === unitIndex ? 'is-current' : '';
      textContent.push(`<span class="prompt-char ${className}">${escapeText(unit.text)}</span>`);
    }
    elements.promptDisplay.innerHTML = textContent.join('');

    const currentUnitTokens = state.zhuyinStream.filter((token) => token.unitIndex === unitIndex);
    elements.guideSymbols.innerHTML = currentUnitTokens.map((token, tokenIndex) => {
      const classes = ['guide-token'];
      if (state.index > state.zhuyinStream.indexOf(token)) classes.push('is-typed');
      if (state.zhuyinStream.indexOf(token) === state.index) classes.push('is-current');
      if (token.isCommit) classes.push('is-commit');
      return `<span class="${classes.join(' ')}">${escapeText(token.symbol)}</span>`;
    }).join('');

    elements.guideKeys.innerHTML = currentUnitTokens.map((token) => `<span class="guide-token">${escapeText(token.display)}</span>`).join('');
    elements.zhuyinGuide.classList.remove('is-hidden');
  }

  function renderKeyboardState(currentToken) {
    const allKeys = elements.keyboard.querySelectorAll('.keyboard-key');
    allKeys.forEach((key) => key.classList.remove('is-next'));
    if (currentToken && currentToken.code) {
      const currentKey = elements.keyboard.querySelector(`[data-code="${currentToken.code}"]`);
      if (currentKey) currentKey.classList.add('is-next');
    }
  }

  function flashWrongKey(code) {
    const key = elements.keyboard.querySelector(`[data-code="${code}"]`);
    if (!key) return;
    key.classList.remove('is-wrong');
    void key.offsetWidth;
    key.classList.add('is-wrong');
    window.clearTimeout(state.errorTimer);
    state.errorTimer = window.setTimeout(() => key.classList.remove('is-wrong'), 220);
  }

  function renderFocus(currentToken) {
    const fallback = FINGER_LABELS.rightIndex;
    const finger = (currentToken && currentToken.finger) || fallback;
    const displayKey = currentToken ? currentToken.display : '—';
    elements.currentKey.textContent = displayKey;
    elements.fingerName.textContent = finger.name;
    elements.handName.textContent = finger.handName;
    elements.fingerOrbLetter.textContent = finger.letter;
    elements.orbLabel.textContent = finger.name;
    elements.fingerOrb.classList.toggle('is-left', finger.hand === 'left');
    elements.fingerOrb.classList.toggle('is-thumb', finger.hand === 'thumb');
  }

  function renderMode() {
    const isZhuyin = state.mode === 'zhuyin';
    elements.englishMode.classList.toggle('is-active', !isZhuyin);
    elements.zhuyinMode.classList.toggle('is-active', isZhuyin);
    elements.englishMode.setAttribute('aria-selected', String(!isZhuyin));
    elements.zhuyinMode.setAttribute('aria-selected', String(isZhuyin));
    elements.modeKicker.textContent = isZhuyin ? 'ZHuyin / 大千式' : 'ENGLISH / QWERTY';
    elements.practiceTitle.textContent = isZhuyin ? '先把注音，交給正確的手指。' : '讓每一個鍵，都回到正確的手指。';
    elements.promptCaption.textContent = isZhuyin ? '看中文與注音鍵位，不必切換系統輸入法' : '先看清楚指法，再開始輸入';
    elements.keyboardNote.textContent = isZhuyin ? '大千式注音鍵位' : 'QWERTY 標準指法';
    elements.modeStat.textContent = isZhuyin ? '注音' : '英文';
    elements.footerModeNote.textContent = isZhuyin ? '注音大千式 · 自由練習 · 不結束' : '英文 QWERTY · 自由練習 · 不結束';
  }

  function render() {
    const currentToken = getCurrentToken();
    renderMode();
    if (state.mode === 'english') renderEnglishPrompt();
    else renderZhuyinGuide();
    renderFocus(currentToken);
    createKeyboard();
    renderKeyboardState(currentToken);

    elements.typedCount.textContent = String(state.typed);
    elements.wrongCount.textContent = String(state.wrong);
    elements.feedbackMessage.textContent = state.paused ? '已暫停，按 Esc 繼續' : state.lastFeedback;
    elements.feedbackMessage.classList.toggle('is-error', state.feedbackKind === 'error');
    elements.feedbackMessage.classList.toggle('is-good', state.feedbackKind === 'good');
    elements.pauseButton.textContent = state.paused ? '繼續' : '暫停';
    elements.pauseButton.insertAdjacentHTML('beforeend', ' <span class="shortcut">Esc</span>');
    elements.sessionStatus.textContent = state.paused ? 'PAUSED' : state.typed > 0 ? 'ACTIVE' : 'IDLE';
    elements.sessionStatus.classList.toggle('is-active', !state.paused && state.typed > 0);
    elements.sessionStatus.classList.toggle('is-paused', state.paused);
    elements.fingerStatus.textContent = state.paused ? 'PAUSE' : 'GUIDE';
  }

  function setMode(mode) {
    if (state.mode === mode) return;
    state.mode = mode;
    saveSettings();
    resetPractice();
  }

  function togglePause() {
    state.paused = !state.paused;
    state.lastFeedback = state.paused ? '已暫停' : '繼續保持輕鬆';
    state.feedbackKind = state.paused ? 'idle' : 'good';
    render();
  }

  function expectedCodeForEvent(event) {
    return event.code || '';
  }

  function handleKeydown(event) {
    if (event.code === 'Escape') {
      event.preventDefault();
      togglePause();
      return;
    }

    if (state.paused || event.repeat || elements.settingsPanel.classList.contains('is-hidden') === false) return;

    const currentToken = getCurrentToken();
    if (!currentToken || !currentToken.code) return;

    const pressedCode = expectedCodeForEvent(event);
    if (!FINGER_MAP[pressedCode] && pressedCode !== currentToken.code) return;

    event.preventDefault();
    if (pressedCode === currentToken.code) {
      state.index += 1;
      state.typed += 1;
      state.lastFeedback = currentToken.code === 'Space' ? '節奏穩定，繼續下一個音節' : '很好，手指位置正確';
      state.feedbackKind = 'good';
      if (state.mode === 'english') ensureEnglishBuffer();
      else ensureZhuyinBuffer();
      render();
    } else {
      state.wrong += 1;
      state.lastFeedback = `請用${currentToken.finger ? currentToken.finger.name : '提示的手指'}按 ${currentToken.display}`;
      state.feedbackKind = 'error';
      render();
      flashWrongKey(pressedCode);
    }
  }

  function toggleSettings(force) {
    const shouldOpen = typeof force === 'boolean' ? force : elements.settingsPanel.classList.contains('is-hidden');
    elements.settingsPanel.classList.toggle('is-hidden', !shouldOpen);
    elements.settingsButton.setAttribute('aria-expanded', String(shouldOpen));
  }

  elements.englishMode.addEventListener('click', () => setMode('english'));
  elements.zhuyinMode.addEventListener('click', () => setMode('zhuyin'));
  elements.pauseButton.addEventListener('click', togglePause);
  elements.resetButton.addEventListener('click', resetPractice);
  elements.settingsButton.addEventListener('click', () => toggleSettings());
  elements.settingsClose.addEventListener('click', () => toggleSettings(false));
  elements.showFingerLabels.checked = state.showFingerLabels;
  elements.showFingerLabels.addEventListener('change', (event) => {
    state.showFingerLabels = event.target.checked;
    saveSettings();
    createKeyboard();
    renderKeyboardState(getCurrentToken());
  });
  elements.promptCard.addEventListener('click', () => elements.promptCard.focus({ preventScroll: true }));
  document.addEventListener('keydown', handleKeydown, { capture: true });
  document.addEventListener('click', (event) => {
    if (!elements.settingsPanel.classList.contains('is-hidden') && !elements.settingsPanel.contains(event.target) && !elements.settingsButton.contains(event.target)) {
      toggleSettings(false);
    }
  });

  resetPractice();
})();
