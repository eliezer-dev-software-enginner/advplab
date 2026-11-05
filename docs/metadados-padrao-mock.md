# Metadados padrao do mock

`advplab --init` e `advplab --mvc1` criam as sete secoes canonicas de `mock.jsonc` e incluem quatro valores locais de exemplo:

```jsonc
"funcoes": [
  {"FwGetUserName": "Usuario Teste"}
],
"ambiente": [
  {"DDATABASE": "2026-01-01"},
  {"TIME": "12:00:00"},
  {"CUSERLOCAL": "."}
]
```

Esses valores cobrem dependencias recorrentes encontradas nos projetos usados como corpus:

- `FwGetUserName()` devolve um nome de usuario previsivel;
- `Date()` e `dDataBase` usam `DDATABASE`;
- `Time()` usa `TIME`;
- fontes que consultam `cUserLocal` recebem um diretorio neutro.

Os valores sao fixtures. Eles nao consultam o usuario autenticado no VS Code ou Protheus, o relogio atual nem o sistema de arquivos. Cada projeto pode substitui-los no proprio `mock.jsonc`.

## Criterio de inclusao

Um metadado entra no modelo inicial quando tem significado estavel no runtime, aparece em mais de um tipo de fonte ou elimina configuracao repetitiva sem presumir uma regra de negocio.

O levantamento tambem encontrou `UsrRetMail`, configuracoes SMTP, `PARAMIXB`, `AHEADER`, `ACOLS`, respostas de dialogos e resultados de bloqueio. Eles nao possuem um valor ou formato universal e devem ser declarados somente nos projetos que os utilizam.

Ao adicionar outro padrao, atualize os dois geradores, os testes de `--init` e `--mvc1`, o README publico, esta decisao tecnica e as skills distribuida e do proprio AdvPLab.
