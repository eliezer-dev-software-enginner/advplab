import contextlib
import io
import os
import tempfile
import sys
import unittest
from pathlib import Path

from fixture_runtime import Fixture
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
from main import main


class InitCliTests(unittest.TestCase):
    def test_creates_valid_fixture_in_current_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            previous = Path.cwd()
            try:
                os.chdir(directory)
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(0, main(['--init']))
                path = Path('mock.jsonc')
                self.assertIn('// Valores consultados por GetMV().', path.read_text())
                self.assertEqual({
                    'parametros', 'tabelas', 'funcoes', 'ambiente',
                    'dialogos', 'especificidadesPrw', 'consultas',
                }, set(Fixture.read_data(path)))
                fixture = Fixture.from_file(path)
                self.assertEqual('Usuario Teste', fixture.get_function_result('FwGetUserName'))
                self.assertEqual('2026-01-01', fixture.get_environment('DDATABASE'))
                self.assertEqual('12:00:00', fixture.get_environment('TIME'))
                self.assertEqual('.', fixture.get_environment('CUSERLOCAL'))
                Path('rotina.prw').write_text(
                    'User Function Rotina()\n'
                    '    ? FwGetUserName("000001")\n'
                    'Return NIL\n'
                )
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    self.assertEqual(0, main(['-run', 'rotina.prw']))
                self.assertEqual('Usuario Teste\n', output.getvalue())
            finally:
                os.chdir(previous)

    def test_preserves_existing_configuration(self):
        with tempfile.TemporaryDirectory() as directory:
            previous = Path.cwd()
            try:
                os.chdir(directory)
                path = Path('mock.jsonc')
                path.write_text('{"parametros": []}')
                original = path.read_bytes()
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(1, main(['--init']))
                self.assertEqual(original, path.read_bytes())
            finally:
                os.chdir(previous)

    def test_rejects_execution_options_without_creating_file(self):
        with tempfile.TemporaryDirectory() as directory:
            previous = Path.cwd()
            try:
                os.chdir(directory)
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(1, main(['--init', '--persist']))
                self.assertFalse(Path('mock.jsonc').exists())
            finally:
                os.chdir(previous)
