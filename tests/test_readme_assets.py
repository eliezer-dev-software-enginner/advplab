import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReadmeAssetTests(unittest.TestCase):
    def test_versioned_mascot_is_a_valid_linked_png(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        match = re.search(r'<img src="([^"]+)" alt="([^"]+)" width="320">', readme)
        self.assertIsNotNone(match)
        asset = ROOT / match.group(1)
        self.assertTrue(asset.is_file())
        self.assertTrue(match.group(2).strip())
        data = asset.read_bytes()
        self.assertTrue(data.startswith(b"\x89PNG\r\n\x1a\n"))
        self.assertEqual(
            "5b17cb19c27a56a970de6bdbc132ce60cb7f486dca301b8826577c1b06c60a34",
            hashlib.sha256(data).hexdigest(),
        )


if __name__ == "__main__":
    unittest.main()
