vim.g.mapleader = " "
vim.g.maplocalleader = " "

vim.opt.encoding = "utf-8"
vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.expandtab = true
vim.opt.tabstop = 4
vim.opt.shiftwidth = 4
vim.opt.softtabstop = 4
vim.opt.history = 50
vim.opt.laststatus = 1
vim.opt.termguicolors = true

vim.keymap.set({"i", "o"}, "jk", "<Esc>", { noremap=true, silent=true})
vim.keymap.set({"n", "x"}, "J", "5j", { noremap=true, silent=true })
vim.keymap.set({"n", "x"}, "K", "5k", { noremap=true, silent=true })
vim.keymap.set({"n", "x"}, "H", "^", { noremap=true, silent=true })
vim.keymap.set({"n", "x"}, "L", "$", { noremap=true, silent=true })
vim.keymap.set("n", "<leader>e", ":Lex<CR>", { noremap = true, silent = true })

local Plug = vim.fn["plug#"]
vim.call("plug#begin", "~/.local/share/nvim/plugged")

Plug("tomasiser/vim-code-dark")
Plug("windwp/nvim-autopairs")
Plug("kylechui/nvim-surround")
Plug("catgoose/nvim-colorizer.lua")
Plug("folke/flash.nvim")

vim.call("plug#end")

-- theme
vim.cmd("colorscheme codedark")

for _, group in ipairs({
    "Normal",
    "LineNr",
    "SignColumn",
    "EndOfBuffer",
    "TabLineFill",
    "FoldColumn"
}) do
    vim.api.nvim_set_hl(0, group, { bg = "none" })
end

vim.api.nvim_set_hl(0, "LineNr", { bold = true })
vim.api.nvim_set_hl(0, "LineNrAbove", { fg = "#aaaaaa" })
vim.api.nvim_set_hl(0, "LineNrBelow", { fg = "#aaaaaa"})

-- netrw
vim.g.netrw_banner = 0
vim.g.netrw_liststyle = 3
vim.g.netrw_winsize = 15

require("colorizer").setup()
require("nvim-autopairs").setup()
require("nvim-surround").setup()
require("plugins.flash").setup()
