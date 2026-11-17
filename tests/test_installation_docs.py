import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class InstallationDocumentationTests(unittest.TestCase):
    def test_linux_installation_uses_pipx_without_breaking_system_python(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("pipx install --editable .", readme)
        self.assertIn("pipx install --force --editable .", readme)
        self.assertIn("PEP 668", readme)
        self.assertIn("não use `sudo pip` nem `--break-system-packages`", readme)
        self.assertIn("python3 -m venv .venv", readme)
        self.assertEqual(1, readme.count("python -m pip install -e ."))


if __name__ == "__main__":
    unittest.main()
