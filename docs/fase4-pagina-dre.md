# Fase 4 — Página DRE

Data: 05/11/2026. Estado: **gravada nos arquivos do relatório; aguardando abertura e conferência no Desktop.**

## Decisões do usuário
- Colunas com valores **comparáveis** (Realizado, Orçado, Previsto Comparável), para que Realizado − Orçado = Desvio em toda linha.
- Cor da classificação por **2 medidas de formatação** (pasta `DRE\Formatação`): `DRE | Cor Classificação x Orçado` e `DRE | Cor Classificação x Previsto`. Mesma regra de M46/M47 sobre M44/M45: verde `#107C10` favorável, cinza `#605E5C` em linha, vermelho `#C50F1F` desfavorável; BLANK sem impacto. Não são medidas financeiras. Modelo: 52 medidas.

## Conteúdo (página `dre0pagina00000000a1`, 1920×1080, primeira e ativa)
| Visual | Configuração |
| --- | --- |
| Título | "DRE — Realizado × Orçado × Previsto (período comparável)" |
| Segmentadores | Filial (`dim_filial[filial]`), Ano (`dim_calendario[ano]`), Mês (`dim_calendario[ano_mes]`), lista suspensa |
| Cartão | `DRE \| Status Comparabilidade` ("Recorte comparável") |
| Matriz | Linhas `vw_dre_comparativo[descricao_dre]` (ordenada por `ordem_dre`); valores Realizado, Orçado, Desvio x Orç. (R$/%), Classificação x Orç., Previsto, Desvio x Prev. (R$/%), Classificação x Prev.; subtotal de linhas desligado (total entre posições é BLANK por contrato); cor da fonte das classificações pelas medidas de cor |
| Nota | Período comparável, convenção de sinal, faixa "Em linha", EBITDA/EBIT em homologação, RL provisório |

EBITDA e EBIT não aparecem (todas as medidas BLANK). Filtros usam só as dimensões (colunas da view ocultas no Lote 3.1).

## Validação prévia (DAX)
Cores × classificação 2022 consolidado: 11 linhas coerentes (ex.: Receita Bruta Desfavorável/vermelho; Custos Favorável/verde; RL "Desfavorável (provisório)" x Orçado e "Favorável (provisório)" x Previsto).

## Backup e rollback
`backups/fase4-pagina-dre-pre-20261105-1440/` (arquivos do relatório antes da página + manifesto). Rollback: com o Desktop fechado, apagar a pasta `definition/pages/dre0pagina00000000a1` e restaurar `definition/pages/pages.json` do backup.
