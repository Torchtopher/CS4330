def hex_to_rgb(hex_value):
    hex_value = hex_value.lstrip('#')
    return tuple(int(hex_value[i:i+2], 16) for i in (0, 2, 4))

def main():
    color_bg = "#011627"
    color_fg = "#FF3366"
    color_selected = "#4F86C6"
    color_flag = "#83B692"
    color_mine = "#D5CFE1"

    rgb_bg = hex_to_rgb(color_bg)
    rgb_fg = hex_to_rgb(color_fg)
    rgb_selected = hex_to_rgb(color_selected)
    rgb_flag = hex_to_rgb(color_flag)
    rgb_mine = hex_to_rgb(color_mine)

    print(f"--color-bg: {rgb_bg};")
    print(f"--color-fg: {rgb_fg};")
    print(f"--color-selected: {rgb_selected};")
    print(f"--color-flag: {rgb_flag};")
    print(f"--color-mine: {rgb_mine};")

if __name__ == "__main__":
    main()
