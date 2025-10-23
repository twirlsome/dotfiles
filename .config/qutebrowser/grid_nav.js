(() => {
    'use strict';

    // === Configuration ===
    const COLS = 30;             // number of grid columns
    const ROWS = 20;             // number of grid rows
    const EXPIRE_SECS = 10;      // overlay expires after this many seconds of inactivity
    const BUFFER_SECS = 4;       // buffer before auto-selection
    const TEXT_COLOR = 'rgba(0,123,239,1)';
    const GRID_COLOR = 'rgba(0,123,239,0.35)';
    const BG_COLOR = 'rgba(82,148,226,0.7)'; // highlight background (slightly translucent)

    // === Derived values ===
    const MAX_CELLS = COLS * ROWS;
    const MAX_DIGITS = String(MAX_CELLS).length;

    // === Remove old overlay if present ===
    const oldOverlay = document.getElementById('qute-grid-overlay');
    if (oldOverlay) oldOverlay.remove();

    // === Create overlay ===
    const overlay = document.createElement('div');
    overlay.id = 'qute-grid-overlay';
    Object.assign(overlay.style, {
        position: 'fixed',
        left: '0',
        top: '0',
        right: '0',
        bottom: '0',
        zIndex: '2147483647',
        pointerEvents: 'none',
        fontFamily: 'Noto Sans CJK JP',
        background: 'rgba(0,0,0,0.4)',
        display: 'grid',
        gridTemplateColumns: `repeat(${COLS}, 1fr)`,
        gridTemplateRows: `repeat(${ROWS}, 1fr)`,
    });

    // Use document.body — generally safe and visible across pages
    document.body.appendChild(overlay);

    const cells = [];
    const cellWidth = window.innerWidth / COLS;
    const cellHeight = window.innerHeight / ROWS;
    let n = 1;

    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
            const box = document.createElement('div');
            box.dataset.index = n;
            // IMPORTANT: interpolate GRID_COLOR with template literal
            Object.assign(box.style, {
                border: `1px solid ${GRID_COLOR}`,
                boxSizing: 'border-box',
                background: 'transparent',            // ensure it's not filled
                color: TEXT_COLOR,
                fontSize: `${Math.min(cellWidth, cellHeight) / 2}px`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                pointerEvents: 'none',
                userSelect: 'none',
            });
            box.textContent = n <= MAX_CELLS ? n : '';
            overlay.appendChild(box);
            cells.push(box);
            n++;
        }
    }

    // quick debug info so you can confirm what's created
    console.info('qute-grid: created', cells.length, 'cells. sample cell styles:');
    for (let i = 0; i < Math.min(5, cells.length); i++) {
        console.info(i + 1, cells[i].dataset.index, window.getComputedStyle(cells[i]).cssText);
    }

    // === Focus capture element ===
    const focusCapture = document.createElement('div');
    focusCapture.id = 'qute-focus-capture';
    focusCapture.tabIndex = 0;
    Object.assign(focusCapture.style, {
        position: 'fixed',
        left: '-9999px',
        top: '-9999px',
        width: '1px',
        height: '1px',
        opacity: '0',
        pointerEvents: 'none',
    });
    document.body.appendChild(focusCapture);

    // === Buffers and timers ===
    let buffer = '';
    let selectTimer = null;
    let expireTimer = null;

    function resetExpire() {
        if (expireTimer) clearTimeout(expireTimer);
        expireTimer = setTimeout(cleanup, EXPIRE_SECS * 1000);
    }

    function cleanup() {
        if (selectTimer) clearTimeout(selectTimer);
        if (expireTimer) clearTimeout(expireTimer);
        removeKeyListeners();
        if (overlay.parentNode) overlay.remove();
        if (focusCapture.parentNode) focusCapture.remove();
    }

    function highlight(num) {
        cells.forEach(c => (c.style.background = ''));
        if (num >= 1 && num <= MAX_CELLS) {
            cells[num - 1].style.background = BG_COLOR;
        }
    }

    function select(num) {
        if (!num || num < 1 || num > MAX_CELLS) return cleanup();
        const idx = num - 1;
        const r = Math.floor(idx / COLS);
        const c = idx % COLS;

        const x = (c + 0.5) * (window.innerWidth / COLS);
        const y = (r + 0.5) * (window.innerHeight / ROWS);

        overlay.style.display = 'none';
        const target = document.elementFromPoint(x, y);
        overlay.style.display = '';

        if (!target) return cleanup();
        focusSmart(target);
        cleanup();
    }

    function focusSmart(target) {
        if (target.tabIndex >= 0 || /^(input|textarea|select|button|a)$/i.test(target.tagName)) {
            target.focus();
            return;
        }

        let el = target;
        while (el && el !== document.body) {
            const style = window.getComputedStyle(el);
            const wraps = /(normal|pre-wrap|break-spaces)/.test(style.whiteSpace);
            const hasText = el.textContent && el.textContent.trim().length > 0;
            const visible = style.display !== 'none' && style.visibility !== 'hidden';
            if (hasText && wraps && visible) {
                if (el.tabIndex < 0) el.tabIndex = -1;
                el.focus({ preventScroll: true });
                return;
            }
            el = el.parentElement;
        }

        if (document.activeElement) document.activeElement.blur();
        focusCapture.focus();
    }

    function keyHandler(e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        resetExpire();

        if (e.key === 'Escape') return cleanup();
        if (e.key === 'Backspace') {
            buffer = buffer.slice(0, -1);
            highlight(parseInt(buffer, 10));
            return;
        }
        if (e.key === 'Enter') {
            select(parseInt(buffer, 10));
            return;
        }
        if (/^[0-9]$/.test(e.key)) {
            buffer += e.key;
            highlight(parseInt(buffer, 10));

            if (buffer.length >= MAX_DIGITS) {
                select(parseInt(buffer, 10));
            } else {
                if (selectTimer) clearTimeout(selectTimer);
                selectTimer = setTimeout(() => {
                    select(parseInt(buffer, 10));
                }, BUFFER_SECS * 1000);
            }
        }
    }

    // === Attach key listener only to top-level document ===
    function attachTopListener() {
        document.addEventListener('keydown', keyHandler, true);
    }

    function removeKeyListeners() {
        document.removeEventListener('keydown', keyHandler, true);
    }

    // === Optional: attach to same-origin iframe when focused ===
    document.addEventListener('focusin', () => {
        const active = document.activeElement;
        if (active && active.tagName === 'IFRAME') {
            try {
                const fd = active.contentDocument;
                if (fd && !fd.quteListenerAttached) {
                    fd.addEventListener('keydown', keyHandler, true);
                    fd.quteListenerAttached = true;
                }
            } catch (e) {
                // cross-origin iframe; ignore
            }
        }
    }, true);

    // === Initialize ===
    focusCapture.focus();
    attachTopListener();
    resetExpire();
})();

