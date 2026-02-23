import unittest

import packaging_config


class TestPackagingConfig(unittest.TestCase):
    def test_load_project_metadata(self):
        metadata = packaging_config.load_project_metadata()

        self.assertEqual(metadata["name"], "token-icon")
        self.assertEqual(metadata["version"], "0.1.0")

    def test_bundle_metadata(self):
        metadata = packaging_config.get_bundle_metadata(version="0.1.0")

        self.assertTrue(metadata["LSUIElement"])
        self.assertEqual(metadata["CFBundleIdentifier"], "com.zjffdu.token-icon")
        self.assertEqual(metadata["CFBundleShortVersionString"], "0.1.0")

    def test_hidden_imports_include_required_modules(self):
        includes = set(packaging_config.get_hidden_imports())

        self.assertIn("api", includes)
        self.assertIn("config", includes)
        self.assertIn("settings_window", includes)

    def test_build_pyinstaller_command(self):
        cmd = packaging_config.build_pyinstaller_command(version="0.1.0")
        cmd_text = " ".join(cmd)

        self.assertIn("--windowed", cmd)
        self.assertIn("--name", cmd)
        self.assertIn("Token Icon", cmd)
        self.assertIn("--osx-bundle-identifier", cmd)
        self.assertIn("com.zjffdu.token-icon", cmd)
        self.assertIn("app.py", cmd)
        self.assertIn("--hidden-import api", cmd_text)
        self.assertIn("--icon", cmd)
        self.assertIn("assets/icon-token-orbit-a.icns", cmd)


if __name__ == "__main__":
    unittest.main()
