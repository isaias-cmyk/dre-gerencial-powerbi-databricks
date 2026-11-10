# Fase 3 — Diagnóstico da modelagem e desempenho

Data: 04/11/2026. Somente leitura (TMDL salvo + consultas DAX no modelo aberto). Nenhuma alteração feita.

## 1. Estrutura atual

| Item | Situação |
| --- | --- |
| Tabelas | 16: 5 de negócio usadas pelas medidas (`vw_dre_comparativo`, `dim_calendario`, `dim_filial`, `_ConfigCobertura`, `_Medidas`), 5 sem uso por medidas (`fato_lancamentos` 3.741 linhas, `fato_orcamento` 4.644, `fato_previsao` 4.644, `dim_conta` 129, `dim_dre` 39) e 6 ocultas de data automática |
| Relacionamentos | 18, todos de direção única. 5 deles ligam as tabelas de data automática; 1 inativo (`dim_conta`→`dim_filial`); 1 entre dimensões (`dim_dre`→`dim_filial`) |
| Medidas | 50, todas referenciam só `vw_dre_comparativo`, `dim_calendario`, `dim_filial` e `_ConfigCobertura` |
| Data automática | Ligada (`__PBI_TimeIntelligenceEnabled = 1`): 5 `LocalDateTable` + 1 modelo, 48 colunas ocultas. Nenhum visual usa as hierarquias automáticas |
| Tabela de datas | `dim_calendario` não está marcada como tabela de datas |
| Ordenação | `descricao_dre` sem "classificar por" `ordem_dre`: em visuais, a DRE sai em ordem alfabética. `ano_mes` sem ordenação por `numero_ano_mes`. Ambos os pares são 1:1 (verificado) |
| Agregação implícita | Colunas como `ano`, `mes`, `ordem_dre`, `subtotal`, `realizado`, `orcado` e `previsto` com "Somar" padrão; medidas implícitas permitidas |
| Cultura | Modelo en-US, fonte pt-BR (limitação já registrada) |

## 2. Achado com efeito no resultado

Filtrar pelas colunas da própria view (`vw_dre_comparativo[cod_filial]`, `[filial]`, `[ano]`, `[competencia]`) em vez das dimensões faz as medidas Comparáveis retornarem BLANK, com Status enganoso e contagem de pares errada:

| Filtro | Realizado Comparável RL | Pares |
| --- | --- | --- |
| `dim_filial` = 01, 2023 | 254.694,46 | 5 |
| `vw_dre_comparativo[cod_filial]` = 01, 2023 | BLANK | 15 (ignora o filtro) |
| `dim_calendario[ano]` = 2022 | 2.100.204,06 | — |
| `vw_dre_comparativo[ano]` = 2022 | BLANK | — |

As medidas falham de forma segura (BLANK, não número errado), mas um segmentador montado na coluna errada quebra o relatório. Correção padrão de mercado: ocultar essas colunas e expor filial/período apenas pelas dimensões.

## 3. Desempenho (consultas no formato dos visuais, cache aquecido)

| Cenário | Tempo |
| --- | --- |
| Matriz DRE × 12 meses de 2023, Realizado/Orçado/Previsto | 54 ms |
| Mesma matriz, Comparável + Desvio R$/% + Classificação + Status | 602 ms |
| Matriz pesada: 3 filiais × 36 meses × 13 linhas com subtotais, 1 medida Comparável | 135 ms |
| Mesma matriz pesada, 10 medidas (Comparáveis, Desvios, Impacto, Classificação, Cumprimento) | **4.066 ms** |

Medidas isoladas na matriz pesada: Desvio R$ 298 ms; Classificação 316 ms; Desvio % 657 ms. A causa é estrutural: cada medida de desvio/desempenho recalcula a máscara de cobertura (grade filial × mês filtrada sobre `_ConfigCobertura`) várias vezes por célula (M46 → M44 → M40 → M37 + M38). Páginas executivas típicas ficam abaixo de 1 s; matrizes mensais por filial com muitas medidas ficam lentas.

Medidas de texto sempre preenchidas (`Status Comparabilidade`) expandem a matriz: 156 linhas em vez de 55 no exemplo de 2023. Usar em cartão/tooltip, não como coluna de matriz.

## 4. Propostas

| Lote | Conteúdo | Risco | Autorização |
| --- | --- | --- | --- |
| 3.1 Higiene do modelo | Ocultar colunas de filial/período/valores da view e colunas técnicas das fatos; "Não resumir" nas colunas numéricas de atributo; ordenar `descricao_dre` por `ordem_dre` e `ano_mes` por `numero_ano_mes`; marcar `dim_calendario` como tabela de datas; desestimular medidas implícitas | Baixo: só metadados, nenhuma expressão muda | Sim (mudança estrutural leve) |
| 3.1b Data automática | Desligar em Opções → Arquivo atual → Carregamento de dados; remove 6 tabelas ocultas e 5 relacionamentos | Baixo (nenhum visual usa) | Sim; feito na interface do Desktop |
| 3.2 Desempenho | Pré-calcular a cobertura filial × mês em tabela oculta e simplificar a máscara de M37–M39/M49/M50 | Médio: altera medidas homologadas; exige regressão completa (14.625 + 11.700 + 2.340 células) | Sim (medidas homologadas) |
| 3.3 Tabelas sem uso | `fato_*`, `dim_conta`, `dim_dre`: manter ocultas para futuro detalhamento por conta, ou remover | Remoção: médio (exclusão, refresh) | Sim (exclusão) |

Ordem recomendada: 3.1 + 3.1b → 3.2 (com protótipo medido antes de alterar) → 3.3 conforme a Fase 4 precisar de detalhamento por conta.

## 5. Lote 3.1 — aplicado em 04/11/2026 (aguardando salvamento)

Backup `backups/lote3-1-pre-20261104-1745/` (38 arquivos + manifesto; 4 hashes relidos). Alterações via MCP, só metadados:

- `vw_dre_comparativo`: ocultas `cod_filial`, `filial`, `competencia`, `ano`, `subtotal`, `realizado`, `orcado`, `previsto`; `descricao_dre` ordenada por `ordem_dre`; "Não resumir" em `ordem_dre`, `ano`, `subtotal`.
- `dim_calendario`: `ano_mes` ordenada por `numero_ano_mes` (oculta); "Não resumir" em `ano`, `mes`, `dia`, `trimestre`.
- Colunas técnicas `_arquivo_origem`, `_aba_origem`, `_data_ingestao`, `_tabela_origem` ocultas nas três fatos; "Não resumir" em atributos de `dim_conta` e `dim_dre`.
- Tabelas `fato_lancamentos`, `fato_orcamento`, `fato_previsao`, `dim_conta`, `dim_dre` ocultas (mantidas).
- Modelo: `discourageImplicitMeasures = true`.

Regressão: foto das 50 medidas antes e depois (filial × ano × mês com subtotais × posição × descrição, 2022–2023): **1.066 linhas, 53.300 células, 0 divergências**.

Pendente: desligar data automática no Desktop, salvar, marcar `dim_calendario` como tabela de datas e conferir o arquivo.

## 6. Lote 3.2 — protótipo (somente consulta, nada gravado)

Duas mudanças, testadas como `DEFINE MEASURE` em `prototipo-l32-medidas.dax`:

1. M41/M43 calculam `(R − X) / |X|` com as variáveis já obtidas, em vez de chamar M40/M42 (que recalculavam as Comparáveis). Matematicamente idêntico.
2. M37–M39 verificam a presença de valor por par filial/mês numa única tabela agrupada (`SUMMARIZE` + `ADDCOLUMNS` sob a máscara), em vez de um `CALCULATE` por par para os três cenários; cada medida só calcula os cenários que usa.

| Teste | Resultado |
| --- | --- |
| Equivalência: 12 medidas (M37–M48) × 605 linhas com valor (filial × mês × posição com subtotais, 2022–2023) | 0 diferenças (tolerância 1E-9; texto idêntico) |
| Matriz pesada, 10 medidas, cache aquecido | 3.074 ms (atual) → 2.289 ms (protótipo), cerca de −25% |

Ganho moderado. O custo restante está na montagem da grade de cobertura a cada célula; reduzir mais exigiria pré-calcular a cobertura filial × mês numa tabela oculta (mudança estrutural maior).
