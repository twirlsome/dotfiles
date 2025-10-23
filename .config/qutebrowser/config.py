config.load_autoconfig()

c.qt.args = ["--enable-logging", "--log-level=0"]
# c.url.start_pages = "about:blank"   # Homepage / startup
c.url.start_pages = "~/.config/qutebrowser/index.html"
c.url.default_page = "~/.config/qutebrowser/index.html"
c.editor.command = ['kitty','-e','nvim', '{}']

# searching
c.url.searchengines = {
        # 'DEFAULT': 'https://duckduckgo.com/?q={}',
        'DEFAULT': 'https://google.com/search?q={}',
        '!aw': 'https://wiki.archlinux.org/?search={}',
        '!apkg': 'https://archlinux.org/packages/?sort=&q={}&maintainer=&flagged=',
        '!yt': 'https://www.youtube.com/results?search_query={}',
}

# keybind
# config.bind('=', 'cmd-set-text -s :open')
config.unbind('q', mode='normal')
config.unbind('r', mode='normal')
config.unbind('d', mode='normal')
config.unbind('<Ctrl-^>', mode='normal')
config.bind('dd', 'tab-close')
# In insert mode → leave insert mode + blur textbox
config.bind('<Escape>', 'mode-leave ;; jseval -q document.activeElement.blur()', mode='insert')
config.bind('<Ctrl-[>', 'mode-leave ;; jseval -q document.activeElement.blur()', mode='insert')
# In normal mode → just blur textbox
config.bind('<Escape>', 'jseval -q document.activeElement.blur()', mode='normal')
config.bind('<Ctrl-[>', 'jseval -q document.activeElement.blur()', mode='normal')
config.bind('<Ctrl-g>', 'jseval -q -f ~/.config/qutebrowser/grid_nav.js')

# Enable adblocking
c.content.blocking.enabled = True
c.content.blocking.method = "adblock"

# Blocklists
c.content.blocking.adblock.lists = [
    # General
    "https://easylist.to/easylist/easylist.txt",
    "https://easylist.to/easylist/easyprivacy.txt",
    "https://secure.fanboy.co.nz/fanboy-annoyance.txt",
    "https://filters.adtidy.org/extension/ublock/filters/224.txt",
    "https://filters.adtidy.org/extension/ublock/filters/224.txt",
    "https://filters.adtidy.org/extension/ublock/filters/218.txt",
    "https://filters.adtidy.org/extension/ublock/filters/220.txt",

    # uBlock
    # "https://github.com/ewpratten/youtube_ad_blocklist/blob/master/blocklist.txt",
    # "https://github.com/Athar5443/Youtube_BlockAds_List/blob/main/blocklist.txt",
    # "https://github.com/uBlockOrigin/uAssets/raw/master/filters/legacy.txt",
    "https://github.com/uBlockOrigin/uAssets/raw/master/filters/filters.txt",
    "https://github.com/uBlockOrigin/uAssets/raw/master/filters/filters-2020.txt",
    "https://github.com/uBlockOrigin/uAssets/raw/master/filters/filters-2021.txt",
    "https://github.com/uBlockOrigin/uAssets/raw/master/filters/filters-2022.txt",
    "https://github.com/uBlockOrigin/uAssets/raw/master/filters/filters-2023.txt",
    "https://github.com/uBlockOrigin/uAssets/raw/master/filters/filters-2024.txt",
    "https://github.com/uBlockOrigin/uAssets/raw/master/filters/badware.txt",
    "https://github.com/uBlockOrigin/uAssets/raw/master/filters/privacy.txt",
    "https://github.com/uBlockOrigin/uAssets/raw/master/filters/badlists.txt",
    "https://github.com/uBlockOrigin/uAssets/raw/master/filters/annoyances.txt",
    "https://github.com/uBlockOrigin/uAssets/raw/master/filters/annoyances-cookies.txt",
    "https://github.com/uBlockOrigin/uAssets/raw/master/filters/annoyances-others.txt",
    "https://github.com/uBlockOrigin/uAssets/raw/master/filters/badlists.txt",
    "https://github.com/uBlockOrigin/uAssets/raw/master/filters/quick-fixes.txt",
    "https://github.com/uBlockOrigin/uAssets/raw/master/filters/resource-abuse.txt",
    "https://github.com/uBlockOrigin/uAssets/raw/master/filters/unbreak.txt"
]
