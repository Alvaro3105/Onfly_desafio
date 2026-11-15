# Declaração de uso de IA

## Ferramenta e modelo

- Claude Code, pela extensão do VS Code
- Modelo: Claude Opus 5.5 (`claude-opus-5-5`)

## O que eu fiz

- Montei o ambiente (venv, pytest) e rodei os testes iniciais.
- Corrigi o cálculo de noites antes de usar a IA.
- Apliquei no código as correções de status, câmbio, limite de leitura e ranking.
- Criei o arquivo de testes extras e rodei a suíte.
- Revisei os textos da entrega e publiquei o repositório.

## O que a IA fez

- Me ajudou a retomar o projeto: resumiu o que eu já tinha feito e apontou os defeitos que faltavam, com arquivo e linha.
- Explicou a causa de cada defeito e o que precisava mudar, para eu aplicar.
- Testou minhas alterações (pytest, CLI na amostra e no arquivo completo, códigos de saída) e apontou quando uma correção estava errada. Por exemplo, quando troquei o status para `== "CANCELLED"` e quando mudei o limite de 200 para 300 em vez de removê-lo.
- Escreveu o código de `tests/test_extras.py` a partir dos cenários que discutimos.
- Escreveu o rascunho do `README-ENTREGA.md` e o deixou com uma linguagem mais natural a meu pedido, e também esta declaração.

A sessão completa está exportada nesta mesma pasta.
