return {
  "lukas-reineke/indent-blankline.nvim",
  main = "ibl",
  config = function()
    vim.api.nvim_set_hl(0, "IblIndent", { fg = "#5c6370" })
    require("ibl").setup {
      indent = {
        char = "│",
        highlight = { "IblIndent" },
      },
    }
  end,
}

