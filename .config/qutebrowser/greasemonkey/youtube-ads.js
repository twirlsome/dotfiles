// ==UserScript==
// @name         Skip YouTube ads (improved)
// @namespace    http://tampermonkey.net/
// @version      1.1
// @description  Click skip buttons and fast-forward true ad videos only (avoids skipping main content).
// @run-at       document-start
// @match        *://*.youtube.com/*
// @grant        none
// ==/UserScript==

(function() {
  'use strict';

  function clickSkipButtons(root = document) {
    const sel = '.videoAdUiSkipButton, .ytp-ad-skip-button-modern, .ytp-ad-overlay-close-button';
    const buttons = root.querySelectorAll(sel);
    buttons.forEach(btn => {
      try { btn.click(); } catch (e) { /* ignore */ }
    });
  }

  function finishAdOnPlayer(player) {
    if (!player || !player.classList || !player.classList.contains('ad-showing')) return;
    const v = player.querySelector('video');
    if (!v) return;
    try {
      // Only fast-forward if duration is finite and looks reasonable for an ad.
      if (isFinite(v.duration) && v.duration > 0 && v.duration < 60 * 10) {
        // Jump to just before end to mark ad finished (safer than a huge number).
        v.currentTime = Math.max(0, v.duration - 0.05);
      } else {
        // If uncertain, try to click skip buttons and nudge playback instead of a big jump.
        clickSkipButtons(player);
        v.pause(); v.play().catch(()=>{});
      }
    } catch (e) { /* ignore errors */ }
  }

  const observer = new MutationObserver(mutations => {
    for (const m of mutations) {
      if (m.type === 'childList') {
        for (const node of m.addedNodes) {
          if (!(node instanceof Element)) continue;
          // If a skip button is added, click it immediately
          if (node.matches && node.matches('.videoAdUiSkipButton, .ytp-ad-skip-button-modern, .ytp-ad-overlay-close-button')) {
            try { node.click(); } catch (e) {}
          } else {
            const nested = node.querySelector && node.querySelector('.videoAdUiSkipButton, .ytp-ad-skip-button-modern, .ytp-ad-overlay-close-button');
            if (nested) nested.click();
          }
        }
      } else if (m.type === 'attributes' && m.attributeName === 'class') {
        const el = m.target;
        if (el && (el.id === 'movie_player' || el.classList.contains('html5-video-player'))) {
          if (el.classList.contains('ad-showing')) {
            finishAdOnPlayer(el);
          }
        }
      }
    }
  });

  function startObserving() {
    const root = document.body || document.documentElement;
    if (!root) return;
    observer.observe(root, { childList: true, subtree: true, attributes: true, attributeFilter: ['class'] });
  }

  // Periodic fallback for edge cases
  const interval = setInterval(() => {
    clickSkipButtons();
    const player = document.getElementById('movie_player') || document.querySelector('.html5-video-player');
    if (player && player.classList.contains('ad-showing')) finishAdOnPlayer(player);
  }, 1000);

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', startObserving, { once: true });
  } else {
    startObserving();
  }

})();

