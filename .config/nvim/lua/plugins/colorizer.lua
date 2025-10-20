-- ~/.config/nvim/lua/plugins/colorizer.lua
return {
  "norcalli/nvim-colorizer.lua",
  event = { "BufReadPost", "BufNewFile" },
  config = function()
    local colorizer = require("colorizer")

    colorizer.setup({
      -- Apply to all filetypes
      "*",
    }, {
      RGB = true,        -- #RGB
      RRGGBB = true,     -- #RRGGBB
      names = false,     -- Disable named colors like "red"
      RRGGBBAA = true,   -- #RRGGBBAA
      AARRGGBB = true,   -- 0xAARRGGBB
      rgb_fn = true,     -- Enable CSS rgb() function
      rgba_fn = true,    -- Enable CSS rgba() function
      hsl_fn = true,     -- Enable hsl() / hsla()
      css = true,        -- Enable all CSS features
      css_fn = true,     -- Enable all CSS functions
      mode = "background",
    })

    -- auto attach
    vim.defer_fn(function()
      colorizer.attach_to_buffer(0)
    end, 0)
  end,
}

