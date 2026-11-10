# Fase 4 — Página Executiva

Data: 05/11/2026. Estado: **gravada nos arquivos do relatório; aguardando abertura e conferência no Desktop.** Sem medidas novas (usa M37–M48 e as medidas de cor).

## Conteúdo (página `exec0pagina0000000a1`, 1920×1080, primeira e ativa; ordem: Executiva, DRE, Page 1)
| Bloco | Visual | Detalhe |
| --- | --- | --- |
| Topo | Título, segmentadores Filial/Ano/Mês, cartão "Recorte comparável" (filtro visual posição 13) | Igual à página DRE |
| Receita Operacional Líquida | 4 cartões (filtro visual posição 3) | Realizado e Orçado comparáveis; Desvio x Orçado (%) com cor; Cumprimento do orçamento |
| Margem de Contribuição | 4 cartões (posição 5) | Realizado, Orçado; Desvio x Orçado (%) e x Previsto (%) com cor |
| Resultado Líquido (provisório) | 4 cartões (posição 13) | Idem |
| Gráfico de linhas | Receita Operacional Líquida Realizado/Orçado/Previsto por mês | Período inteiro (Orçado/Previsto seguem após 2023-05) |
| Cascata | `DRE \| Impacto Favorável x Orçado (R$)` por linha analítica (posições 1, 2, 4, 6, 7, 9, 10, 12) | Total = impacto do Resultado Líquido |
| Nota | Leitura do período comparável e da cascata | |

## Validação prévia (DAX)
- 2022 consolidado: Receita Líquida R 62.819.286,66 / O 63.105.323,19 / −0,45% / cumprimento 99,55%; Margem −0,006%; RL R 2.100.204,06 / O 2.211.722,45 / −5,04% (Desfavorável, vermelho).
- Cascata fecha: soma das linhas analíticas = impacto do RL (2022: −111.518,39; 2023: +6.281,13).
- Receita Líquida mensal 2023: Realizado até maio, Orçado e Previsto em 12 meses.

## Backup e rollback
`backups/fase4-executiva-pre-20261105-1600/` (pages.json e página DRE antes da alteração). Rollback: com o Desktop fechado, apagar `definition/pages/exec0pagina0000000a1` e restaurar `pages.json`.
