// ==UserScript==
// @name         YouTube 5-Column Homepage Layout (Refined)
// @namespace    http://tampermonkey.net/
// @version      1.1
// @description  Force 5 videos per row on YouTube homepage grid (works with SPA navigation)
// @author       Refined
// @match        https://www.youtube.com/
// @match        https://www.youtube.com/?*
// @grant        GM_addStyle
// ==/UserScript==

(function () {
    'use strict';

    const COLUMNS = 5;

    const applyStyle = () => {
        GM_addStyle(`
            /* Only affect homepage video grid */
            .style-scope.ytd-two-column-browse-results-renderer {
                --ytd-rich-grid-items-per-row: ${COLUMNS} !important;
                --ytd-rich-grid-gutter-margin: 0px !important;
            }

            ytd-rich-grid-media {
                max-width: initial !important;
                width: 100% !important;
                margin: 0 auto !important;
            }
        `);
    };

    // Apply once immediately
    applyStyle();

    // Detect URL changes (YouTube SPA navigation)
    let lastUrl = location.href;
    new MutationObserver(() => {
        const currentUrl = location.href;
        if (currentUrl !== lastUrl) {
            lastUrl = currentUrl;

            // Only apply on homepage
            if (location.pathname === "/" && !location.search.includes("watch")) {
                applyStyle();
            }
        }
    }).observe(document, { subtree: true, childList: true });
})();

