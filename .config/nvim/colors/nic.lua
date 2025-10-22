-- ======================================================================
-- nic.lua – Expressive white theme with pink and blue accents
-- ======================================================================

vim.opt.termguicolors = true
vim.cmd("hi clear")

-- --------------------------------------------------
-- Color Palette
-- --------------------------------------------------
local c = {
  bg     = "#000000",
  fg     = "#ffffff",
  pink   = "#ff008c",
  blue   = "#007bef",
  torq   = "#00ffde",
  gray   = "#888888",
  border = "#737373",
}

local set = vim.api.nvim_set_hl

-- --------------------------------------------------
-- Core UI
-- --------------------------------------------------
set(0, "Normal",        { fg = c.fg, bg = c.bg })
set(0, "CursorLine",    { bg = "#111111" })
set(0, "CursorLineNr",  { fg = c.pink, bold = true })
set(0, "LineNr",        { fg = c.border })
set(0, "VertSplit",     { fg = c.border })
set(0, "Visual",        { bg = "#1a1a1a" })
set(0, "MatchParen",    { fg = c.bg, bg = c.torq, bold = true })
set(0, "StatusLine",    { fg = c.fg, bg = "#0d0d0d", bold = true })
set(0, "StatusLineNC",  { fg = c.gray, bg = "#0d0d0d" })

-- --------------------------------------------------
-- Core Syntax (general, consistent across languages)
-- --------------------------------------------------
set(0, "Comment",       { fg = c.gray, italic = true })
set(0, "String",        { fg = c.blue })         -- strings are blue
set(0, "Function",      { fg = c.pink, bold = true })
set(0, "Type",          { fg = c.pink })
set(0, "Keyword",       { fg = c.blue, bold = true })
set(0, "Statement",     { fg = c.blue })
set(0, "Identifier",    { fg = c.fg })
set(0, "Variable",      { fg = c.fg })
set(0, "Constant",      { fg = c.pink })
set(0, "Boolean",       { fg = c.pink })
set(0, "Number",        { fg = c.pink })
set(0, "PreProc",       { fg = c.border })
set(0, "Special",       { fg = c.torq })
set(0, "Delimiter",     { fg = c.border })
set(0, "Operator",      { fg = c.border })
set(0, "Error",         { fg = "#ff4d4d", bold = true })
set(0, "Todo",          { fg = c.torq, bold = true })

-- --------------------------------------------------
-- Treesitter Highlights (universal layer)
-- --------------------------------------------------
set(0, "@punctuation.bracket",   { fg = c.border })
set(0, "@punctuation.delimiter", { fg = c.border })
set(0, "@punctuation.special",   { fg = c.torq })
set(0, "@function",              { fg = c.pink, bold = true })
set(0, "@function.call",         { fg = c.pink })
set(0, "@function.builtin",      { fg = c.torq })
set(0, "@keyword",               { fg = c.blue, bold = true })
set(0, "@keyword.operator",      { fg = c.blue })
set(0, "@constant",              { fg = c.pink })
set(0, "@number",                { fg = c.pink })
set(0, "@boolean",               { fg = c.pink })
set(0, "@type",                  { fg = c.pink })
set(0, "@variable",              { fg = c.fg })
set(0, "@variable.parameter",    { fg = c.fg })
set(0, "@variable.member",       { fg = c.pink })     -- object.property
set(0, "@property",              { fg = c.pink })     -- consistent semantic
set(0, "@string",                { fg = c.blue })

-- --------------------------------------------------
-- JSON / JSONC
-- --------------------------------------------------
set(0, "@property.json",         { fg = c.pink })     -- keys
set(0, "@string.json",           { fg = c.blue })     -- values
set(0, "@number.json",           { fg = c.pink })
set(0, "@boolean.json",          { fg = c.pink })
set(0, "@punctuation.bracket.json", { fg = c.border })

-- --------------------------------------------------
-- Python
-- --------------------------------------------------
set(0, "@function.python",       { fg = c.pink, bold = true })
set(0, "@function.builtin.python", { fg = c.torq })
set(0, "@keyword.python",        { fg = c.blue, bold = true })
set(0, "@boolean.python",        { fg = c.pink })
set(0, "@number.python",         { fg = c.pink })
set(0, "@property.python",       { fg = c.pink })
set(0, "@variable.builtin.python", { fg = c.torq })
set(0, "@string.python",         { fg = c.blue })
set(0, "@operator.python",       { fg = c.border })
set(0, "@punctuation.bracket.python", { fg = c.border })

-- --------------------------------------------------
-- CSS / Config files
-- --------------------------------------------------
set(0, "cssBraces",              { fg = c.border })
set(0, "cssProp",                { fg = c.blue })
set(0, "cssAttr",                { fg = c.pink })
set(0, "cssFunctionName",        { fg = c.torq })
set(0, "cssClassName",           { fg = c.fg })
set(0, "cssIdentifier",          { fg = c.fg })

-- --------------------------------------------------
-- JavaScript / TypeScript (for object.property etc.)
-- --------------------------------------------------
set(0, "@property.javascript",   { fg = c.pink })
set(0, "@property.tsx",          { fg = c.pink })
set(0, "@string.javascript",     { fg = c.blue })
set(0, "@boolean.javascript",    { fg = c.pink })
set(0, "@number.javascript",     { fg = c.pink })
set(0, "@function.javascript",   { fg = c.pink, bold = true })
set(0, "@keyword.javascript",    { fg = c.blue })

-- --------------------------------------------------
-- Brackets / Arrays / Object consistency
-- --------------------------------------------------
set(0, "@punctuation.bracket",   { fg = c.border })  -- [ ] { } ()
set(0, "@punctuation.delimiter", { fg = c.border })
set(0, "@punctuation.special",   { fg = c.border })

-- --------------------------------------------------
-- Diagnostics / LSP
-- --------------------------------------------------
set(0, "DiagnosticError", { fg = "#ff4d4d" })
set(0, "DiagnosticWarn",  { fg = "#ffcc00" })
set(0, "DiagnosticInfo",  { fg = c.blue })
set(0, "DiagnosticHint",  { fg = c.torq })

-- --------------------------------------------------
-- End of file
-- --------------------------------------------------

