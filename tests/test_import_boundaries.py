import unittest
from pathlib import Path

import diagnostics
import fixture_runtime
import interpreter


ROOT = Path(__file__).resolve().parents[1]
LIVREPL_ROOT = ROOT.parent / "livrePL"


class ImportBoundaryTests(unittest.TestCase):
    def test_advplab_modules_win_when_livrepl_has_same_filename(self):
        self.assertEqual(ROOT, Path(diagnostics.__file__).resolve().parent)
        self.assertEqual(LIVREPL_ROOT, Path(interpreter.__file__).resolve().parent)
        self.assertIsNotNone(fixture_runtime.Fixture)


if __name__ == "__main__":
    unittest.main()
