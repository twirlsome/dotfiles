-- ======================================================================
--  Global Keymaps
--  (Keep cursor centered after common motions)
-- ======================================================================

local map = vim.keymap.set
local opts = { noremap = true, silent = true }

-- Basic vertical movement
map("n", "j", "jzz", opts)
map("n", "k", "kzz", opts)
map("n", "<Up>", "<Up>zz", opts)
map("n", "<Down>", "<Down>zz", opts)

-- Shift + Arrow (faster movement by line)
-- <S-Up> and <S-Down> normally move faster or scroll depending on terminal
map("n", "<S-Up>", "<S-Up>zz", opts)
map("n", "<S-Down>", "<S-Down>zz", opts)

-- Page / half-page scrolling
map("n", "<C-d>", "<C-d>zz", opts)  -- half page down
map("n", "<C-u>", "<C-u>zz", opts)  -- half page up
map("n", "<C-f>", "<C-f>zz", opts)  -- full page down
map("n", "<C-b>", "<C-b>zz", opts)  -- full page up

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

-- Paragraph and block navigation
map("n", "{", "{zz", opts)
map("n", "}", "}zz", opts)

-- Jump list navigation
map("n", "<C-o>", "<C-o>zz", opts)
map("n", "<C-i>", "<C-i>zz", opts)

-- Location list / Quickfix navigation
map("n", "]q", "]qzz", opts)
map("n", "[q", "[qzz", opts)
map("n", "]l", "]lzz", opts)
map("n", "[l", "[lzz", opts)

-- Repeat last f/t motion
map("n", ";", ";zz", opts)
map("n", ",", ",zz", opts)

-- Center cursor after initial search (/, ?)
vim.api.nvim_create_autocmd("CmdlineLeave", {
  pattern = { "/", "?" },
  callback = function()
    vim.schedule(function()
      vim.cmd("normal! zz")
    end)
  end,
})

-- Write with sudo if forgotten
vim.api.nvim_create_user_command("W", function()
  vim.cmd('write !sudo tee % > /dev/null')
  vim.cmd('edit!')
end, {})

