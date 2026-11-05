---
name: advplab
description: Desenvolver, testar e documentar o AdvPLab, incluindo fixtures JSONC, execução headless de código Protheus, MVC, browse, validação e compilação opcional no RPO. Não usar para mudanças de sintaxe ou biblioteca padrão do AdvPL puro, que pertencem ao LivrePL.
---

# Desenvolvimento do AdvPLab

Use esta skill ao trabalhar no repositório AdvPLab ou em projetos testados por sua CLI.

## Limite arquitetural

O LivrePL implementa a linguagem AdvPL e sua biblioteca padrão independente do Protheus. O AdvPLab estende essa base com fixtures, aliases e tabelas em memória, APIs Protheus simuladas, MVC, browse, cenários e integração opcional com o TDS/RPO.

Antes de implementar, classifique a mudança:

- sintaxe, AST, escopo ou função geral da linguagem: LivrePL;
- comportamento dependente de Protheus, fixture, banco simulado, MVC, browse ou compilação: AdvPLab;
- mudança que atravessa os dois limites: altere e valide cada repositório separadamente, sem duplicar a implementação.

## Fluxo de trabalho

1. Leia `docs/AI_RULES.md`, `docs/CONTEXT.md`, `docs/TODO.md` e as decisões relacionadas.
2. Preserve alterações existentes e confirme o caminho real do repositório.
3. Reproduza o caso com fonte e fixture próprios do AdvPLab. A suíte deste repositório não deve depender de fontes locais externos.
4. Mantenha as sete seções canônicas dos fixtures JSONC: `parametros`, `tabelas`, `funcoes`, `ambiente`, `dialogos`, `especificidadesPrw` e `consultas`.
5. Adicione ou ajuste um teste que observe o comportamento, evitando testes que apenas repitam a implementação.
6. Execute `python -m unittest discover -s tests -v` e o menor comando CLI que demonstre a mudança.
7. Atualize a documentação segundo a política abaixo e revise o diff antes de concluir.

Compilação no RPO é uma integração real e opcional. Não a apresente como necessária para os testes headless e não use credenciais, tokens ou arquivos locais como dados versionados.

## Documentação

Mudanças novas devem atualizar `docs/`. Registre estado consolidado em `docs/CONTEXT.md`, decisões duradouras em `docs/DECISIONS.md` e pendências em `docs/TODO.md`.

O README é a entrada pública do produto: propósito, requisitos, instalação, primeiros comandos, capacidades e links para detalhes. Não coloque nele caminhos absolutos do computador, tokens, configuração local, histórico de implementação, notas de sessão ou explicações internas de como a mudança foi construída. Esse conteúdo pertence a `docs/`, `AGENTS.md` ou documentação de contribuição. Atualize o README apenas quando a forma pública de instalar ou usar o AdvPLab mudar.

## Instalação da skill

No checkout do AdvPLab:

```bash
mkdir -p ~/.codex/skills/advplab
cp .agents/skills/advplab/SKILL.md ~/.codex/skills/advplab/SKILL.md
```

Depois, reinicie a sessão do agente para que a skill seja descoberta.
