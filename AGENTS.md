# Instruções para agentes

Use a skill versionada em `.agents/skills/advplab/SKILL.md` para mudanças neste repositório.

- Leia `docs/AI_RULES.md`, `docs/CONTEXT.md`, `docs/TODO.md` e as decisões relacionadas antes de editar.
- Mantenha no AdvPLab apenas recursos ligados a testes Protheus, fixtures, MVC, browse e integrações; linguagem AdvPL pura pertence ao LivrePL.
- Toda mudança nova deve atualizar a documentação pertinente em `docs/`.
- Preserve o README como entrada pública de instalação e uso. Detalhes de implementação, decisões, migrações, caminhos locais, tokens e configuração da máquina pertencem a `docs/`.
- Rode `python -m unittest discover -s tests -v` antes de concluir.
