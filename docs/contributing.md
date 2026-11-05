# Contribuição e pull requests

## Validação automática

Pull requests executam `.github/workflows/pull-request.yml` em Python 3.10 e 3.12. O workflow cria checkouts irmãos de AdvPLab e LivrePL, instala ambos em modo editável e executa a suíte própria do AdvPLab:

```bash
python -m unittest discover -s tests -v
```

Esse desenho não depende de uma pasta, instalação ou token existente no computador do autor. Integrações reais com VS Code, TDS, AppServer e RPO continuam fora do CI porque dependem do ambiente Protheus autenticado.

## Skill do projeto

A skill `.agents/skills/advplab/SKILL.md` orienta agentes sobre o limite com o LivrePL, fixtures, testes e documentação. Para instalá-la no Codex:

```bash
mkdir -p ~/.codex/skills/advplab
cp .agents/skills/advplab/SKILL.md ~/.codex/skills/advplab/SKILL.md
```

## Política de documentação

Mudanças novas devem atualizar os documentos pertinentes:

- `docs/CONTEXT.md`: estado e arquitetura atuais;
- `docs/DECISIONS.md`: decisões duradouras e seus motivos;
- `docs/TODO.md`: pendências e entregas concluídas;
- documento específico em `docs/`: desenho, validação e limites de uma mudança relevante.

O README deve permanecer público e portátil. Ele pode explicar instalação, comandos e comportamento observável, mas não deve conter caminhos absolutos, arquivos exclusivos da máquina, tokens, detalhes de sessão, histórico interno da implementação ou instruções que presumam o checkout do autor. Informações desse tipo ficam em `docs/` e não devem ser usadas pelo workflow de pull request.
