(() => {
    'use strict';

    // === Configuration ===
    const COLS = 30;             // number of grid columns
    const ROWS = 20;             // number of grid rows
    const EXPIRE_SECS = 10;      // overlay expires after this many seconds of inactivity
    const BUFFER_SECS = 4;     // time to wait for more digits before selecting

    // === Derived values ===
    const MAX_CELLS = COLS * ROWS;
    const MAX_DIGITS = String(MAX_CELLS).length;

    // Remove old overlay if still present
    const old = document.getElementById('qute-grid-overlay');
    if (old) old.remove();

    const overlay = document.createElement('div');
    overlay.id = 'qute-grid-overlay';
    Object.assign(overlay.style, {
        position: 'fixed',
        inset: '0',
        zIndex: '2147483647',
        pointerEvents: 'none',
        fontFamily: 'monospace',
        background: 'rgba(0,0,0,0.70)',
    });

    const cells = [];
    const cellW = 100 / COLS;
    const cellH = 100 / ROWS;
    let n = 1;
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
            const box = document.createElement('div');
            box.dataset.index = n;
            Object.assign(box.style, {
                position: 'absolute',
                left: `${c * cellW}%`,
                top: `${r * cellH}%`,
                width: `${cellW}%`,
                height: `${cellH}%`,
                border: '1px solid rgba(255,0,0,0.2)',
                boxSizing: 'border-box',
                color: 'red',
                fontSize: '18px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                pointerEvents: 'none',
                userSelect: 'none',
            });
            box.textContent = String(n);
            overlay.appendChild(box);
            cells.push(box);
            n++;
        }
    }
    document.body.appendChild(overlay);

    // Hidden element to preserve focus context
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

    // Buffers and timers
    let buffer = '';
    let selectTimer = null;
    let expireTimer = null;

    function resetExpire() {
        if (expireTimer) clearTimeout(expireTimer);
        expireTimer = setTimeout(() => cleanup(), EXPIRE_SECS * 1000);
    }

    function cleanup() {
        if (selectTimer) clearTimeout(selectTimer);
        if (expireTimer) clearTimeout(expireTimer);
        document.removeEventListener('keydown', keyHandler, true);
        overlay.remove();
        if (focusCapture.parentNode) {
            focusCapture.remove();
        }
    }

    function highlight(num) {
        cells.forEach(c => (c.style.background = ''));
        if (num >= 1 && num <= MAX_CELLS) {
            cells[num - 1].style.background = 'rgba(255,255,0,0.3)';
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
        let target = document.elementFromPoint(x, y);
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

    focusCapture.focus();
    document.addEventListener('keydown', keyHandler, true);
    resetExpire();
})();

