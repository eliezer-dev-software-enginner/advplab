import json
import re
from pathlib import Path

from fixture_runtime import FixtureError


MVC1_SOURCE = '''#Include "TOTVS.CH"
#Include "FWMVCDef.ch"

User Function @TABLE@MVC()
    Local oBrowse := FWMBrowse():New()
    oBrowse:SetAlias('@TABLE@')
    oBrowse:SetDescription('Cadastro @TABLE@')
    oBrowse:Activate()
Return NIL

Static Function MenuDef()
    Local aRotina := {}
    ADD OPTION aRotina TITLE 'Visualizar' ACTION 'VIEWDEF.@TABLE@MVC' OPERATION 2 ACCESS 0
    ADD OPTION aRotina TITLE 'Incluir' ACTION 'VIEWDEF.@TABLE@MVC' OPERATION 3 ACCESS 0
    ADD OPTION aRotina TITLE 'Alterar' ACTION 'VIEWDEF.@TABLE@MVC' OPERATION 4 ACCESS 0
    ADD OPTION aRotina TITLE 'Excluir' ACTION 'VIEWDEF.@TABLE@MVC' OPERATION 5 ACCESS 0
Return aRotina

Static Function ModelDef()
    Local oStruct := FWFormStruct(1, '@TABLE@')
    Local oModel := MPFormModel():New('MODEL_@TABLE@', , {|oModel| .T.})
    oModel:AddFields('@TABLE@MASTER', , oStruct)
    oModel:SetPrimaryKey({'@TABLE@_FILIAL', '@TABLE@_COD'})
    oModel:SetDescription('Cadastro @TABLE@')
Return oModel

Static Function ViewDef()
    Local oModel := FWLoadModel('@TABLE@MVC')
    Local oStruct := FWFormStruct(2, '@TABLE@')
    Local oView := FWFormView():New()
    oView:SetModel(oModel)
    oView:AddField('VIEW_@TABLE@', oStruct, '@TABLE@MASTER')
    oView:CreateHorizontalBox('BOX_@TABLE@', 100)
    oView:SetOwnerView('VIEW_@TABLE@', 'BOX_@TABLE@')
Return oView
'''


MVC1_README = """# Cadastro @TABLE@ - MVC tipo 1

Projeto gerado pelo AdvPLab para a tabela `@TABLE@`.

## Estrutura

```text
Fontes/
    @TABLE@MVC.prw
.agents/
    skills/
        monasteiro/
            SKILL.md
.gitignore
AGENTS.md
mock.jsonc
README.md
```

O fonte inclui browse, MenuDef, ModelDef e ViewDef para um cadastro de uma tabela.
`mock.jsonc` define os dados simulados e aceita comentarios.
Ele inclui valores locais de exemplo para `FwGetUserName`, `DDATABASE`, `TIME` e
`CUSERLOCAL`. Ajuste-os ao cenario do teste; eles nao consultam o Protheus real.

## Executar localmente

Com o comando `advplab` instalado, abra o terminal na raiz deste projeto:

```bash
advplab -validate Fontes/@TABLE@MVC.prw
advplab --preview Fontes/@TABLE@MVC.prw
advplab -run Fontes/@TABLE@MVC.prw
advplab -run Fontes/@TABLE@MVC.prw --mvc-case incluir-registro
```

A validacao deve indicar quatro funcoes. O browse inicial mostra a tabela vazia.
O cenario `incluir-registro` espera `salvou=true, totalRegistros=1`.
Sem `--persist`, os registros ficam apenas em memoria e o mock nao e alterado.

## Ajustar a tabela

Os campos `@TABLE@_FILIAL`, `@TABLE@_COD` e `@TABLE@_DESC` sao exemplos.
Ajuste `tabelas`, `campos` e `cenariosMvc` no mock e a chave primaria em
`ModelDef` conforme o SX3 da tabela real. Acrescente as regras de negocio
na pos-validacao do modelo, que inicialmente aceita qualquer registro.

## Persistencia opcional

```bash
advplab -run Fontes/@TABLE@MVC.prw --mvc-case incluir-registro --persist
advplab -run Fontes/@TABLE@MVC.prw --persist
```

A inclusao grava `state.json` na raiz. O segundo comando exibe o estado salvo.
Repetir a inclusao com `--persist` pode falhar na expectativa de um registro.
Para reiniciar, guarde ou remova conscientemente `state.json`; o mock e preservado.

## Limites

Os testes locais simulam o ambiente sem AppServer e sem banco real.
O menu inclui visualizar, incluir, alterar e excluir; o cenario automatizado
cobre inclusao e nao reproduz a interface grafica MVC.
O gerador nao consulta SX3 nem cria tabelas no Protheus. A compilacao no RPO
exige um ambiente Protheus configurado e os campos reais da tabela.

## Skill Monasteiro

O projeto inclui a skill `.agents/skills/monasteiro/SKILL.md`, com o fluxo de trabalho
para fontes AdvPL, fixtures, MVC, browse, validacao local e compilacao. O `AGENTS.md`
orienta agentes que trabalham neste repositorio a ler a skill antes de alterar o projeto.

Para instalar a skill no Codex do usuario, execute na raiz do projeto:

```bash
mkdir -p ~/.codex/skills/monasteiro
cp .agents/skills/monasteiro/SKILL.md ~/.codex/skills/monasteiro/SKILL.md
```

No PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME/.codex/skills/monasteiro"
Copy-Item ".agents/skills/monasteiro/SKILL.md" "$HOME/.codex/skills/monasteiro/SKILL.md" -Force
```

Abra uma nova conversa do Codex depois da instalacao. A copia local no projeto continua
sendo a fonte de verdade; repita a copia quando ela for atualizada.
"""


MONASTEIRO_AGENTS = """# Instrucoes para agentes

Antes de analisar ou alterar este projeto AdvPL, leia integralmente
`.agents/skills/monasteiro/SKILL.md` e siga o fluxo de validacao descrito nela.

Preserve os dados do usuario, nao sobrescreva o `mock.jsonc` e nao inclua artefatos
gerados em `.vscode/.advpl/` ou `.vscode/advpl/` nos commits.
"""


MONASTEIRO_SKILL = """---
name: monasteiro
description: Desenvolver e validar projetos AdvPL/Protheus gerados pelo AdvPLab, com fontes MVC, fixtures, preview, cenarios locais e compilacao opcional no RPO.
---

# Monasteiro

Use esta skill ao criar, corrigir ou testar fontes AdvPL neste projeto. Ela reune os
padroes comprovados nos projetos MVC tipo 1, mestre-detalhe, notificacoes e pontos de
entrada usados como corpus do AdvPLab.

## Comece pelo projeto real

1. Leia `README.md`, `mock.jsonc` e os fontes em `Fontes/`.
2. Confirme o alias, os campos, a chave primaria e os indices usados no fonte.
3. Preserve alteracoes existentes. Antes do commit, revise `git status` e o diff.
4. Trate o SX3 do ambiente como autoridade para tipo, tamanho, decimal, titulo,
   obrigatoriedade e visibilidade no browse. O mock documenta e simula; nao altera o SX3.

## Mantenha fonte e mock sincronizados

- Declare no `mock.jsonc` todas as tabelas, campos e indices lidos pelo fonte.
- Preserve as secoes `parametros`, `tabelas`, `funcoes`, `ambiente`, `dialogos`,
  `especificidadesPrw`, `consultas` e `cenariosMvc`, usando listas vazias quando necessario.
- Para `DbSetOrder`, `DbSeek` ou `Posicione`, declare `indices` na mesma ordem da chave real.
- Para funcoes externas sem integracao local, configure retornos deterministas em `funcoes`
  ou `especificidadesPrw`; nao invente acesso a servidor, SMTP ou banco.
- `FwGetUserName`, `DDATABASE`, `TIME` e `CUSERLOCAL` ja possuem valores locais de exemplo.
  Ajuste-os ao caso testado; nao os trate como dados do usuario ou do ambiente Protheus.
- Datas do mock usam `AAAA-MM-DD`. A persistencia opcional vai para `state.json`; o mock
  original nao deve ser reescrito pela execucao.

Exemplo de busca de descricao de produto:

```advpl
Posicione("SB1", 1, xFilial("SB1") + ZA4->ZA4_PROD, "B1_DESC")
```

O mock precisa conter `SB1`, os campos `B1_FILIAL`, `B1_COD`, `B1_DESC`, o indice 1 e
registros coerentes. `SetFields` adiciona uma coluna calculada; para ocultar o codigo
original, ajuste a visibilidade do campo no SX3, sem remover o campo do modelo.

## Estruture o AdvPL com cuidado

- Mantenha declaracoes `Local`, `Static`, `Private` e `Public` no inicio da funcao.
- Use `User Function` para entradas chamadas pelo Protheus. Uma `Static Function` pertence
  somente ao proprio `.prw`; dependencias entre arquivos devem usar funcoes publicas e
  podem ser declaradas com `//usePrw('OutroFonte.prw')` para a validacao local.
- Preserve e restaure workareas ao consultar outros aliases.
- Use indices adequados nas buscas. Filtre filial e exclusao logica nas consultas reais.
- Salve fontes destinados ao Protheus em Windows-1252 quando houver acentos; mantenha
  README, JSONC e esta skill em UTF-8.
- Legendas devem usar os codigos cadastrados no dominio do campo, e nao valores genericos
  presumidos. `AddLegend` colore o browse e `BrwLegenda` exibe o dialogo.

## Valide do menor para o maior

Na raiz do projeto, execute:

```bash
advplab -validate Fontes/ALIASMVC.prw
advplab --preview Fontes/ALIASMVC.prw
advplab -run Fontes/ALIASMVC.prw
advplab -run Fontes/ALIASMVC.prw --mvc-case incluir-registro
```

- `-validate` comprova sintaxe e simbolos cobertos pelo simulador.
- `--preview` mostra uma aproximacao textual do browse; nao comprova layout, permissoes,
  callbacks de UI, cores ou comportamento exato do WebApp.
- `-run` executa apenas a entrada e os ramos alcancados.
- `--mvc-case` verifica o cenario declarado e o estado final esperado.
- Use `--persist` somente quando quiser criar ou atualizar `state.json` conscientemente.

Quando a tarefa exigir compilacao real e o servidor estiver conectado no VS Code:

```bash
advplab -compile Fontes/ALIASMVC.prw
```

A compilacao usa a sessao em `~/.totvsls/servers.json`. Ela pode falhar se a sessao tiver
expirado ou se o usuario estiver ativo no Protheus; reconecte pelo VS Code e tente novamente.
Compilar no RPO nao substitui o teste funcional no ambiente Protheus.

## Limites que devem ser declarados

O AdvPLab trabalha em memoria. Ele nao cria tabelas, nao consulta o SX3 real, nao envia
e-mail, nao executa DBAccess e nao reproduz toda a interface MVC. Ao concluir, informe
se houve apenas validacao local, preview, cenario simulado ou compilacao real no RPO.
"""


MVC1_GITIGNORE = """# Estado local do AdvPLab
state.json

# Binarios e metadados gerados pela extensao AdvPL/TLPP
.vscode/.advpl/
.vscode/advpl/
"""


def legend_source(table):
    return "\n".join(
        f"    oBrowse:AddLegend(\"{table}_STATUS == '{code}'\", '{color}', '{label}')"
        for code, color, label in [('1', 'GREEN', 'Disponivel'),
                                   ('2', 'YELLOW', 'Em uso'), ('3', 'RED', 'Baixado')])


def legend_function(table):
    return f"""
/*/{{Protheus.doc}} {table}LEG
Exibe as legendas de situacao do cadastro.
@type Function
@param Nenhum
@return Nil
@author EliezerDev
@since 28/10/2026
@example U_{table}LEG()
/*/
User Function {table}LEG()
    Local aLegenda := {{ ;
        {{ 'BR_VERDE', 'Disponivel' }}, ;
        {{ 'BR_AMARELO', 'Em uso' }}, ;
        {{ 'BR_VERMELHO', 'Baixado' }} ;
    }}
    BrwLegenda('Cadastro {table}', 'Legenda', aLegenda)
Return NIL
"""


def create_mvc1(table='ZA1', legendas=False):
    table = table.upper()
    if not re.fullmatch(r'[A-Z][A-Z0-9]{2}', table, flags=re.ASCII):
        raise FixtureError('--table deve ser um alias de tres caracteres, como ZA4')
    source_directory = Path.cwd() / 'Fontes'
    source_path = source_directory / f'{table}MVC.prw'
    fixture_path = Path.cwd() / 'mock.jsonc'
    readme_path = Path.cwd() / 'README.md'
    agents_path = Path.cwd() / 'AGENTS.md'
    gitignore_path = Path.cwd() / '.gitignore'
    skill_directory = Path.cwd() / '.agents' / 'skills' / 'monasteiro'
    skill_path = skill_directory / 'SKILL.md'
    directories = (
        source_directory,
        skill_directory.parent.parent,
        skill_directory.parent,
        skill_directory,
    )
    for directory in directories:
        if directory.is_symlink() or (directory.exists() and not directory.is_dir()):
            raise FixtureError(
                f'Diretorio invalido para geracao: {directory}; nenhum arquivo foi criado'
            )
    for path in (source_path, fixture_path, readme_path, agents_path,
                 gitignore_path, skill_path):
        if path.exists() or path.is_symlink():
            raise FixtureError(f'Arquivo ja existe: {path}; nenhum arquivo foi criado')
    record = {f'{table}_FILIAL': '01', f'{table}_COD': '000001',
              f'{table}_DESC': 'Exemplo de cadastro'}
    if legendas:
        record[f'{table}_STATUS'] = '1'
    source = MVC1_SOURCE.replace('@TABLE@', table)
    readme = MVC1_README.replace('@TABLE@', table)
    if legendas:
        source = source.replace('    oBrowse:Activate()', legend_source(table) + '\n    oBrowse:Activate()')
        source = source.replace('Return aRotina', f"    ADD OPTION aRotina TITLE 'Legenda' ACTION 'U_{table}LEG' OPERATION 2 ACCESS 0\nReturn aRotina")
        source += legend_function(table)
        readme = readme.replace('quatro funcoes', 'cinco funcoes')
        readme += f'\n## Legendas\n\nGerado com -legendas. Campo {table}_STATUS: 1=Disponivel (verde), 2=Em uso (amarelo), 3=Baixado (vermelho). Ajuste os codigos ao SX3 do ambiente. O menu Legenda abre BrwLegenda; AddLegend define as cores do browse.\n'
    fixture = {
        'parametros': [],
        'tabelas': [{table: {
            'campos': [{'nome': field, 'tipo': 'C'} for field in record],
            'registros': [],
        }}],
        'funcoes': [{'FwGetUserName': 'Usuario Teste'}],
        'ambiente': [
            {'DDATABASE': '2026-01-01'},
            {'TIME': '12:00:00'},
            {'CUSERLOCAL': '.'},
        ],
        'dialogos': [],
        'especificidadesPrw': [], 'consultas': [],
        'cenariosMvc': [{
            'nome': 'incluir-registro', 'operacao': 'incluir',
            'dados': {f'{table}MASTER': record},
            'esperado': {'salvou': True, 'totalRegistros': 1, 'registro': record},
        }],
    }
    comments = {
        'parametros': 'Valores consultados por GetMV().',
        'tabelas': 'Campos de exemplo: ajuste ao SX3 da tabela real.',
        'funcoes': 'Retornos simulados de funcoes; ajuste ao cenario local.',
        'ambiente': 'Data, hora e diretorio deterministas; nao representam o Protheus real.',
        'dialogos': 'Respostas de dialogos simulados.',
        'especificidadesPrw': 'Configuracoes especificas por fonte PRW.',
        'consultas': 'Resultados simulados de consultas.',
        'cenariosMvc': 'Inclusao simulada; nao cria tabela no Protheus.',
    }
    fixture_text = json.dumps(fixture, indent=2, ensure_ascii=False) + '\n'
    for key, comment in comments.items():
        fixture_text = fixture_text.replace(f'  "{key}":', f'  // {comment}\n  "{key}":', 1)
    created = []
    created_directories = []
    try:
        for directory in directories:
            if not directory.exists():
                directory.mkdir()
                created_directories.append(directory)
        for path, content in (
            (source_path, source),
            (fixture_path, fixture_text),
            (readme_path, readme),
            (agents_path, MONASTEIRO_AGENTS),
            (gitignore_path, MVC1_GITIGNORE),
            (skill_path, MONASTEIRO_SKILL),
        ):
            with path.open('x', encoding='utf-8') as output:
                created.append(path)
                output.write(content)
    except OSError:
        for path in reversed(created):
            path.unlink()
        for directory in reversed(created_directories):
            directory.rmdir()
        raise
    return source_path, fixture_path, readme_path
