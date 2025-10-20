-- ======================================================================
--  Neovim Initialization (init.lua)
-- ======================================================================

-- Set <leader> first (must come before plugins/keymaps)
vim.g.mapleader = " "
vim.opt.termguicolors = true

-- Load core settings
require("core.options")
require("core.keymaps")

-- Load plugin manager (lazy.nvim)
require("core.lazy")

