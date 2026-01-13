local M = {}

function M.setup()
    require("flash").setup({
        label = {
            uppercase = false,
            rainbow = { enabled = true },
            style = "overlay",
        },
        jump = {
            enabled = true,
            offset = 0,
            wrap = true,
            auto_jump = false,
        },
        modes = {
            char = {
                enabled = true,
                jump_labels = true,
                multi_line = true,
                keys = { "f", "F", "t", "T" },
            },
            search = {
                enabled = true,
                highlight = { backdrop = true },
            },
        },
    })

    vim.keymap.set({"n", "x", "o"}, "f", function()
        require("flash").jump()
    end, { noremap = true, silent = true })

end

return M
