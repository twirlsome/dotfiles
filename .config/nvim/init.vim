call plug#begin('~/.local/share/nvim/plugged')
Plug 'tpope/vim-commentary'

" Tree-sitter core for advanced syntax highlighting
Plug 'nvim-treesitter/nvim-treesitter', {'do': ':TSUpdate'}

" Indentation guides (smart and Tree-sitter aware)
Plug 'lukas-reineke/indent-blankline.nvim'

call plug#end()

" Enable Tree-sitter"
lua << EOF
require'nvim-treesitter.configs'.setup {
  ensure_installed = { "c", "cpp", "lua", "python", "bash", "javascript" }, -- add more as needed
  highlight = {
    enable = true,              -- enable syntax highlighting
  },
  indent = {
    enable = true               -- experimental, can help with structure
  }
}
EOF

" Set the indent guide highlight color BEFORE setting up ibl
highlight IblIndent guifg=#5c6370 ctermfg=240

" Configure indent-blankline.nvim (ibl)
lua << EOF
require("ibl").setup {
  indent = {
    char = "│", -- Try "▏" or "┆" if preferred
    highlight = { "IblIndent" }
  }
}
EOF

set guifont=FiraCode\ Nerd\ Font:h14
set number
set relativenumber
syntax on
filetype plugin indent on
colorscheme torte
" autocmd ColorScheme * highlight IblIndent guifg=#5c6370 ctermfg=240
set mouse=
set tabstop=4       " Number of visual spaces per tab
set shiftwidth=4    " Indentation amount for >> and <<
set expandtab       " Use spaces instead of tabs

" Center on cursor when moving
nnoremap j jzz
nnoremap k kzz
nnoremap <Up> <Up>zz
nnoremap <Down> <Down>zz
nnoremap <C-d> <C-d>zz
nnoremap <C-u> <C-u>zz
nnoremap n nzzzv
nnoremap N Nzzzv
nnoremap gg ggzz
nnoremap G Gzz

command W execute 'w !sudo -S tee % > /dev/null' | edit!

