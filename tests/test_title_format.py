import unittest

import title_format


class TestTitleFormat(unittest.TestCase):
    def test_format_menu_title_uses_fixed_width_padding(self):
        self.assertEqual(title_format.format_menu_title("71"), "𝗧   71")
        self.assertEqual(title_format.format_menu_title("3003"), "𝗧 3003")

    def test_format_menu_title_handles_none(self):
        self.assertEqual(title_format.format_menu_title(None), "𝗧    —")


if __name__ == "__main__":
    unittest.main()
