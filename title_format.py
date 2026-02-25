TITLE_VALUE_WIDTH = 4


def format_menu_title(remain) -> str:
    value = "—" if remain is None else str(remain)
    return f"𝗧 {value.rjust(TITLE_VALUE_WIDTH)}"
