-- ======================================================================
--  Global Keymaps
--  (Keep cursor centered after common motions and selections)
-- ======================================================================

local map = vim.keymap.set
local opts = { noremap = true, silent = true }

---------------------------------------------------------------------------
-- Normal mode: vertical and general motion
---------------------------------------------------------------------------
map("n", "j", "jzz", opts)
map("n", "k", "kzz", opts)
map("n", "<Up>", "<Up>zz", opts)
map("n", "<Down>", "<Down>zz", opts)
map("n", "<S-Up>", "<S-Up>zz", opts)
map("n", "<S-Down>", "<S-Down>zz", opts)

-- Page / half-page
map("n", "<C-d>", "<C-d>zz", opts)
map("n", "<C-u>", "<C-u>zz", opts)
map("n", "<C-f>", "<C-f>zz", opts)
map("n", "<C-b>", "<C-b>zz", opts)

-- Search navigation
map("n", "n", "nzzzv", opts)
map("n", "N", "Nzzzv", opts)
map("n", "*", "*zzzv", opts)
map("n", "#", "#zzzv", opts)
map("n", "g*", "g*zzzv", opts)
map("n", "g#", "g#zzzv", opts)

-- File navigation
map("n", "gg", "ggzz", opts)
map("n", "G", "Gzz", opts)

-- Paragraphs / blocks
map("n", "{", "{zz", opts)
map("n", "}", "}zz", opts)

-- Jumps
map("n", "<C-o>", "<C-o>zz", opts)
map("n", "<C-i>", "<C-i>zz", opts)

-- Quickfix / location list
map("n", "]q", "]qzz", opts)
map("n", "[q", "[qzz", opts)
map("n", "]l", "]lzz", opts)
map("n", "[l", "[lzz", opts)

-- Repeat f/t motions
map("n", ";", ";zz", opts)
map("n", ",", ",zz", opts)

-- Search commands (/, ?)
vim.api.nvim_create_autocmd("CmdlineLeave", {
  pattern = { "/", "?" },
  callback = function()
    vim.schedule(function()
      pcall(vim.cmd, "normal! zz")
    end)
  end,
})

---------------------------------------------------------------------------
-- Visual mode: keep selection visible & centered
---------------------------------------------------------------------------
-- Basic movements
map("v", "j", "jzz", opts)
map("v", "k", "kzz", opts)
map("v", "<Up>", "<Up>zz", opts)
map("v", "<Down>", "<Down>zz", opts)
map("v", "{", "{zz", opts)
map("v", "}", "}zz", opts)
map("v", "gg", "ggzz", opts)
map("v", "G", "Gzz", opts)

-- Page scrolling in visual mode
map("v", "<C-d>", "<C-d>zz", opts)
map("v", "<C-u>", "<C-u>zz", opts)
map("v", "<C-f>", "<C-f>zz", opts)
map("v", "<C-b>", "<C-b>zz", opts)

-- Keep blockwise selections centered
map("x", "J", "Jzz", opts)
map("x", "K", "Kzz", opts)

---------------------------------------------------------------------------
-- Operator-pending mode: center after motions (e.g. d}, yG)
---------------------------------------------------------------------------
map("o", "}", "}zz", opts)
map("o", "{", "{zz", opts)
map("o", "G", "Gzz", opts)
map("o", "gg", "ggzz", opts)
map("o", "n", "nzzzv", opts)
map("o", "N", "Nzzzv", opts)

---------------------------------------------------------------------------
-- Command: write with sudo if forgotten
---------------------------------------------------------------------------
vim.api.nvim_create_user_command("W", function()
  vim.cmd('write !sudo tee % > /dev/null')
  vim.cmd('edit!')
end, {})

