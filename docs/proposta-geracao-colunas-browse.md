# Proposta: gerar colunas calculadas no browse

Estado em 05/11/2026: o Protheus Mega Brain possui um editor de colunas calculadas no gerador MVC. A CLI AdvPLab ainda não tem uma opção para gerar essas definições. O suporte do runtime a SetFields e ao preview não equivale a uma flag de geração.

O exemplo de referência usa SetFields com code blocks para trocar a apresentação de códigos de usuários pelos respectivos nomes:

```advpl
oBrowse:SetFields({ ;
    { 'Solicitante', {|| FwGetUserName(Z04->Z04_USER)}, 'C', '@!', 1, 60, 0 }, ;
    { 'Aprovador', {|| FwGetUserName(Z04->Z04_APROVA)}, 'C', '@!', 1, 60, 0 } ;
})
```

Uma futura opção de geração deve receber título, campo de origem e modo (nome de usuário, valor do campo ou expressão caractere). A sintaxe ainda não está definida. Deve preservar a geração atual sem colunas adicionais por padrão e inserir o trecho antes do Activate. Para testar localmente resoluções e consultas, use os retornos simulados correspondentes na fixture.

SetFields adiciona colunas; não oculta automaticamente as originais. Documentar a necessidade de desabilitar no SX3 a exibição dos campos de código quando se deseja mostrar somente o nome. A personalização pertence ao browse, sem depender do tipo de MVC, e não altera os dados persistidos.
