# Lote 3.2 — Otimização de desempenho das Comparáveis e dos Desvios %

Data: 05/11/2026. Decisão do usuário: aplicar as duas otimizações prototipadas (opção recomendada), com backup e regressão completa. Estado: **aplicado e validado no modelo; aguardando salvamento do PBIP (R02).**

Diagnóstico e protótipo: [diagnostico-fase3.md](diagnostico-fase3.md), seções 3 e 6; expressões de teste em `testes/lote3-2/prototipo-l32-medidas.dax`.

## 1. Alterações

| Medida | Antes | Depois |
| --- | --- | --- |
| M37 `DRE \| Realizado Comparável` | Verificava presença de valor com um `CALCULATE` por par filial/mês, para Realizado, Orçado e Previsto | Uma única tabela agrupada (`SUMMARIZE` + `ADDCOLUMNS` sob a máscara) só com o Realizado |
| M38 `DRE \| Orçado Comparável` | Idem | Tabela agrupada com Realizado e Orçado |
| M39 `DRE \| Previsto Comparável` | Idem | Tabela agrupada com Realizado e Previsto |
| M41 `DRE \| Desvio Realizado x Orçado (%)` | Chamava M37, M38 e M40 (que recalculava M37 e M38) | `DIVIDE ( R − O, ABS ( O ) )` com as variáveis já obtidas |
| M43 `DRE \| Desvio Realizado x Previsto (%)` | Idem com Previsto | Idem |

Contratos inalterados: mesma máscara de cobertura, mesmas guardas (configuração, mês parcial, lacuna, posição/descrição, EBIT/EBITDA), mesma regra de falta (um par sem valor → BLANK), mesmo cálculo final. Nomes, pastas, formatos, descrições e lineageTags preservados. Nenhuma outra medida, tabela ou relacionamento alterado.

Backup: `backups/lote3-2-pre-20261105-1315/` (32 arquivos + manifesto SHA-256; 3 hashes relidos). Estado de partida: commit `82203c9`.

## 2. Regressão

| ID | Teste | Resultado |
| --- | --- | --- |
| P01 | Protótipo × medidas originais (12 medidas M37–M48, 605 linhas filial × mês × posição com subtotais, 2022–2023) | 0 diferenças |
| R01 | Foto das 50 medidas antes × depois (filial × ano × mês com subtotais × posição × descrição, 2022–2023) | **53.300/53.300 idênticas**, diferença máxima 0 |
| Q01 | SQL independente (Databricks, roteiros 05/07): M41, M43, M44–M48 em 5 grupos × 9 recortes agregados × 13 posições + mensal 2021 dos grupos Consolidado e 01+02 | **6.279/6.279** (4.095 agregadas + 2.184 mensais); 2.267 NULL/BLANK coincidentes; dif. máx. R$ 1,5E-7, razão 2,2E-15 |
| G01 | Total entre posições, datas parciais, Jun–Dez/2023, EBITDA, posição × descrição conflitantes | Todos BLANK |
| C01 | Controles: RL 5.038.227,39 / 6.622.493,82 / 6.157.931,19; Comparável RL 2023 819.957,24 / 813.676,11 / 15 pares; Desvio % RL 2022 −5,04% | Idênticos aos lotes anteriores |
| R02 | Persistência em arquivo | Pendente: salvar o PBIP |

## 3. Desempenho (cache aquecido)

| Cenário | Antes | Depois |
| --- | --- | --- |
| Matriz pesada: 3 filiais × 36 meses × 13 posições com subtotais, 10 medidas | 3.074 ms | **2.293 ms** (−25%) |
| Matriz DRE × 12 meses de 2023: Comparáveis, Desvio R$/%, Classificação, Status | 602 ms | **273 ms** (−55%) |

O custo restante é a montagem da grade de cobertura a cada célula. Reduzir mais exigiria pré-calcular a cobertura filial × mês numa tabela oculta (não aprovado neste lote).

## 4. Rollback

Com o Desktop fechado, restaurar `DRE Moderno - Databricks2.SemanticModel/definition/tables/_Medidas.tmdl` de `backups/lote3-2-pre-20261105-1315/`. Reabrir e conferir a foto R01.

Aceite técnico/didático; não homologa fechamento, EBITDA, EBIT ou Resultado Líquido.
