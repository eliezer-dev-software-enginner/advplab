import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReadmePublicContentTests(unittest.TestCase):
    def test_opening_describes_current_features_without_internal_phases(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        opening = readme.split("## Estrutura", 1)[0]
        self.assertIn("## Recursos principais", opening)
        self.assertNotIn("## Estado atual", opening)
        self.assertIsNone(re.search(r"\bFase\s+\d", opening, re.IGNORECASE))
        self.assertNotIn("Primeiro fonte real", opening)
        self.assertNotIn("extraidos do desafio", opening)
        self.assertNotIn("Consulte a ADR-", opening)


if __name__ == "__main__":
    unittest.main()
