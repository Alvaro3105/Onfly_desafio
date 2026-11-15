# Entrega do desafio Onfly

O CLI gerava o relatório, mas com números errados. Encontrei 5 defeitos, todos no código (os dados estavam ok, como o enunciado dizia). Hoje os 5 testes fornecidos passam, e adicionei mais 5 meus.

## Defeitos corrigidos

### 1. Noites erradas na virada de mês
`services/stay_calculator.py`

O cálculo não usava a diferença real entre as datas, então uma reserva de 30/01 a 02/02 não dava 3 noites. Troquei por `(checkout - checkin).days * rooms`, que é exatamente a regra do README.

### 2. NO_SHOW sendo cobrado
`services/status_policy.py`

A função `is_billable` retornava `status != "CANCELLED"`, ou seja, tudo que não era cancelado entrava nos totais, inclusive `NO_SHOW`. Inverti a lógica para aceitar só o que é faturável: `status == "CONFIRMED"`.

### 3. Câmbio dividindo em vez de multiplicar
`services/currency_converter.py`

O valor era **dividido** pela taxa e ainda passava por `float` no meio do caminho. Uma reserva de 100 USD virava uns 18 reais. Agora é `amount * rate`, tudo em `Decimal`.

### 4. Arquivo lido pela metade
`repositories/csv_reservation_repository.py`

Tinha um `break` quando a lista chegava a 200 linhas, e o arquivo tem 300. As últimas 100 reservas sumiam sem nenhum aviso. Removi o limite.

### 5. Ranking de hotéis de trás pra frente
`services/report_builder.py`

O `top_hotels` era ordenado do menor valor para o maior. Mudei a chave para `(-total, hotel_id)`: valor decrescente e, em caso de empate, `hotel_id` crescente. Não usei `reverse=True` porque isso inverteria também o desempate.

## Como investiguei

Comecei rodando o `pytest -q` para ver o que quebrava. O defeito das noites eu resolvi primeiro, sozinho. Para os outros, usei o Claude Code como apoio (detalhes em `uso-de-ia/`).

A abordagem foi seguir o fluxo que o README descreve (`ler → converter tipos → contar status → filtrar CONFIRMED → agregar`) e conferir cada etapa do código com a regra de negócio correspondente. Fui corrigindo um defeito por vez e rodando o teste relacionado logo depois, para ter certeza de que cada mudança resolvia o que eu achava que resolvia.

O limite de 200 linhas não aparecia em nenhum teste fornecido. Achei lendo o código de leitura do CSV e confirmei rodando o CLI no arquivo completo: `total_reservations` passou de 200 para 300.

No fim, rodei o CLI na amostra de validação e comparei campo a campo com a tabela do README. Também testei os códigos de saída (`--top 0`, `--top abc` e arquivo inexistente retornam `2`).

## Testes que adicionei

Em `tests/test_extras.py`, cobrindo o que os testes originais não pegavam:

- empate no ranking, que precisa desempatar por `hotel_id`;
- `NO_SHOW` e `CANCELLED` contam no total de reservas, mas ficam fora de noites e valores;
- virada de ano com 2 quartos (30/12 a 02/01 = 6 noites, no mês de dezembro);
- arquivo com 250 linhas, para garantir que não existe mais limite;
- conversão de USD com arredondamento half-up (0.10 × 5.42 = 0.54).

## Como validar

```bash
pip install -r requirements-dev.txt
pytest -q

PYTHONPATH=src python -m onfly_report \
  --input data/exemplo-validacao.csv \
  --rates data/taxas_cambio.csv \
  --output output/exemplo.json
```

A amostra bate com o README: 12 reservas, 9 confirmadas, 28 noites, total de `7566.00` e diária média de `270.21`.

No arquivo completo (`data/reservas_hoteis.csv`) o resultado é: 300 reservas (235 confirmadas, 31 canceladas, 34 no-show), 1347 noites e `396170.00` no total.

## Resultado do pytest

```
..........                                                               [100%]
10 passed in 4.62s
```
