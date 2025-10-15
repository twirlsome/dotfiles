-- ======================================================================
--  Neovim Initialization (init.lua)
-- ======================================================================

-- Set <leader> first (must come before plugins/keymaps)
vim.g.mapleader = " "

-- Load core settings
require("core.options")
require("core.keymaps")

-- Load plugin manager (lazy.nvim)
require("core.lazy")

