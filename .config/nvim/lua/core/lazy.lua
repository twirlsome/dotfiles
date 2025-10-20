-- ======================================================================
--  Plugin Manager Setup (lazy.nvim)
-- ======================================================================

local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({
    "git", "clone", "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable", lazypath
  })
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup({
  -- Simple utilities
  { "tpope/vim-commentary" },

  -- Core plugins split into separate files
  require("plugins.treesitter"),
  require("plugins.indent"),
  require("plugins.nvim-tree"),
  require("plugins.telescope"),
  require("plugins.colorizer"),
})

