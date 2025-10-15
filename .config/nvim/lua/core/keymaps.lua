-- ======================================================================
--  Global Keymaps
-- ======================================================================

local map = vim.keymap.set
local opts = { noremap = true, silent = true }

-- Center cursor after motions
map("n", "j", "jzz", opts)
map("n", "k", "kzz", opts)
map("n", "<Up>", "<Up>zz", opts)
map("n", "<Down>", "<Down>zz", opts)
map("n", "<C-d>", "<C-d>zz", opts)
map("n", "<C-u>", "<C-u>zz", opts)
map("n", "n", "nzzzv", opts)
map("n", "N", "Nzzzv", opts)
map("n", "gg", "ggzz", opts)
map("n", "G", "Gzz", opts)

-- Write with sudo if forgotten
vim.api.nvim_create_user_command("W", function()
  vim.cmd('write !sudo tee % > /dev/null')
  vim.cmd('edit!')
end, {})

