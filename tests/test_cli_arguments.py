import contextlib
import io
import os
import tempfile
import unittest
from pathlib import Path

from main import main


class CliArgumentsTests(unittest.TestCase):
    def test_run_accepts_subdirectory_positional_entry_and_text_argument(self):
        with tempfile.TemporaryDirectory() as directory:
            previous = Path.cwd()
            try:
                os.chdir(directory)
                Path("Fontes").mkdir()
                Path("Fontes/Utils.prw").write_text(
                    'User Function Soma(cValor)\n? Val(cValor) + 1\nReturn NIL\n',
                    encoding="utf-8",
                )
                Path("mock.jsonc").write_text(
                    '{"parametros":[],"tabelas":[],"funcoes":[],"ambiente":[],'
                    '"dialogos":[],"especificidadesPrw":[],"consultas":[]}',
                    encoding="utf-8",
                )
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    code = main(["--run", "Fontes/Utils.prw", "Soma", "--arg", "2"])
                self.assertEqual(0, code)
                self.assertEqual("3\n", output.getvalue())
            finally:
                os.chdir(previous)

    def test_rejects_mixed_argument_formats(self):
        error = io.StringIO()
        with contextlib.redirect_stderr(error):
            code = main(["--run", "Utils.prw", "Soma", "--arg", "2", "--args-json", "[2]"])
        self.assertEqual(1, code)
        self.assertIn("nao podem ser usados juntos", error.getvalue())

    def test_rejects_two_entry_forms(self):
        error = io.StringIO()
        with contextlib.redirect_stderr(error):
            code = main(["--run", "Utils.prw", "Soma", "--entry", "Outra"])
        self.assertEqual(1, code)
        self.assertIn("nao pelos dois", error.getvalue())


if __name__ == "__main__":
    unittest.main()
