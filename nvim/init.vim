let g:mapleader = ' '

set encoding=utf-8
set number
set relativenumber
set expandtab
set tabstop=4
set shiftwidth=4
set softtabstop=4
set history=50
set laststatus=1

inoremap jk <Esc>
onoremap jk <Esc>
<<<<<<< HEAD
=======
noremap J 5j
noremap K 5k
>>>>>>> 7030a41 (update)

call plug#begin()

Plug 'tomasiser/vim-code-dark'
Plug 'ap/vim-css-color'
Plug 'easymotion/vim-easymotion'

call plug#end()

" theme
colorscheme codedark
hi Normal guibg=NONE ctermbg=NONE
hi LineNr guibg=NONE ctermbg=NONE
hi SignColumn guibg=NONE ctermbg=NONE
hi EndOfBuffer guibg=NONE ctermbg=NONE  " 文末空白区域
hi TabLineFill guibg=NONE ctermbg=NONE  " 标签栏填充（如果用标签）
hi FoldColumn guibg=NONE ctermbg=NONE   " 折叠列（如果用折叠）

set termguicolors

hi LineNr guifg=#DDDDDD cterm=bold      " guifg=GUI色，ctermfg=终端色
hi LineNrAbove guifg=#999999            " 上方行号（可选，区分当前行）
hi LineNrBelow guifg=#999999            " 下方行号（可选）

" easymotion
noremap  <Leader>f <Plug>(easymotion-bd-f)
nnoremap <Leader>f <Plug>(easymotion-overwin-f)
nnoremap f <Plug>(easymotion-s2)
nnoremap t <Plug>(easymotion-t2)
noremap  <Leader>l <Plug>(easymotion-lineforward)
noremap  <Leader>j <Plug>(easymotion-j)
noremap  <Leader>k <Plug>(easymotion-k)
noremap  <Leader>h <Plug>(easymotion-linebackward)

" netrw
let g:netrw_banner = 0
let g:netrw_liststyle = 3
let g:netrw_winsize = 15
nnoremap <leader>e :Lex<CR>
