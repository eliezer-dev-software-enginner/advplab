import unittest

from fixture_runtime import Fixture, build_interpreter
from interpreter import AdvPLRuntimeError


SOURCE = """User Function Teste()
Local cDescricao := Posicione("SB1", 1, xFilial("SB1") + ZA4->ZA4_PROD, "B1_DESC")
Return cDescricao
"""


def fixture():
    return Fixture.from_dict({"tabelas": [
        {"ZA4": {
            "campos": [{"nome": "ZA4_PROD", "tipo": "C"}],
            "registros": [{"ZA4_PROD": "PROD1"}],
        }},
        {"SB1": {
            "campos": [
                {"nome": "B1_FILIAL", "tipo": "C"},
                {"nome": "B1_COD", "tipo": "C"},
                {"nome": "B1_DESC", "tipo": "C"},
            ],
            "indices": {"1": ["B1_FILIAL", "B1_COD"]},
            "registros": [
                {"B1_FILIAL": "01", "B1_COD": "MON1", "B1_DESC": "Monitor"},
                {"B1_FILIAL": "01", "B1_COD": "PROD1", "B1_DESC": "Produto de teste"},
            ],
        }},
    ]})


class PosicioneTests(unittest.TestCase):
    def runtime(self, source=SOURCE):
        return build_interpreter(source, fixture=fixture(), entry="Teste")

    def test_uses_fixture_index_and_returns_requested_field(self):
        runtime = self.runtime()
        runtime._current_alias = "ZA4"

        self.assertEqual("Produto de teste", runtime.run("Teste"))
        self.assertEqual("ZA4", runtime._current_alias)
        self.assertEqual(1, runtime._aliases["SB1"].order)
        self.assertEqual("PROD1", runtime._aliases["SB1"].field("B1_COD"))

    def test_returns_empty_text_when_key_is_not_found(self):
        source = SOURCE.replace("ZA4->ZA4_PROD", "'INEXISTENTE'")
        self.assertEqual("", self.runtime(source).run("Teste"))

    def test_rejects_missing_alias_and_field(self):
        runtime = self.runtime()
        with self.assertRaisesRegex(AdvPLRuntimeError, "Alias 'SA1'"):
            runtime.call_function("Posicione", ["SA1", 1, "010001", "A1_NOME"])
        with self.assertRaisesRegex(AdvPLRuntimeError, "campo 'B1_X'"):
            runtime.call_function("Posicione", ["SB1", 1, "01PROD1", "B1_X"])


if __name__ == "__main__":
    unittest.main()
