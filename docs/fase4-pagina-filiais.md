# Fase 4 — Página Filiais

Data: 08/11/2026. Estado: **gravada nos arquivos do relatório; aguardando abertura e conferência no Desktop.** Sem medidas novas.

## Conteúdo (página `fil0pagina00000000a1`, 1920×1080; ordem: Executiva, DRE, Filiais, Page 1)
| Visual | Configuração |
| --- | --- |
| Título, segmentadores Ano/Mês, cartão de recorte (posição 13) | Sem segmentador de filial (a página compara as filiais) |
| Matriz | Linhas `dim_filial[filial]` + Total (consolidado); colunas `descricao_dre` filtradas nas posições 3, 5 e 13; valores Realizado, Orçado, Desvio x Orç. (%), Classificação (cor); subtotal de colunas desligado |
| Barras — cumprimento | `DRE \| Cumprimento Orçamentário (%)` por filial, posição 3, cor pela classificação x Orçado |
| Barras — impacto | `DRE \| Impacto Favorável x Orçado (R$)` por filial, posição 13, em milhares, cor pela classificação |
| Nota | Período comparável, Total = consolidado, legenda de cores |

## Validação prévia (DAX, 2022)
| Filial | Receita Líq. R / O | Cumprimento | Margem desvio | RL desvio | RL impacto |
| --- | --- | --- | --- | --- | --- |
| São Paulo | 35.105.382,14 / 35.015.497,29 | 100,26% | +0,70% | +0,88% | +8.263,15 |
| Rio de Janeiro | 16.909.374,66 / 17.123.263,23 | 98,75% | −1,00% | −12,40% | −86.944,66 |
| Florianópolis | 10.804.529,86 / 10.966.562,67 | 98,52% | −0,65% | −5,71% | −32.836,88 |
| Total | 62.819.286,66 / 63.105.323,19 | 99,55% | −0,006% | −5,04% | −111.518,39 |

Soma dos impactos das filiais = Total (Receita Líquida: −286.036,53; RL: −111.518,39).

## Backup e rollback
`backups/fase4-filiais-pre-20261108-2140/pages.json`. Rollback: com o Desktop fechado, apagar `definition/pages/fil0pagina00000000a1` e restaurar `pages.json`.
