# L2.3.3 — Validação de impacto, classificação e cumprimento (M44–M48)

Data: 04/11/2026. Estado: **implementado, validado e persistido em arquivo (PBIP salvo pelo usuário em 04/11/2026 17:05). **Aceite técnico do usuário em 04/11/2026 17:26. Sublote concluído** (técnico/didático; não é homologação contábil).

Contrato: [plano-lote2-3-3.md](plano-lote2-3-3.md). Evidências: [evidencias/lote2-3-3-execucao-20261104/](evidencias/lote2-3-3-execucao-20261104/).

## 1. Execução

| Item | Registro |
| --- | --- |
| Decisões | Usuário em 04/11/2026: impacto no lucro em todas as linhas com valor; RL classificado com "(provisório)"; neutro até R$ 0,01; cumprimento só posições 1/3 |
| Backup prévio | `backups/lote2-3-3-pre-20261104-1325/`: 38 arquivos do PBIP + `manifesto.json` (SHA-256). `_Medidas.tmdl`, `_ConfigCobertura.tmdl`, `relationships.tmdl`, `model.tmdl` e `cache.abf` relidos do disco com hash idêntico |
| Baseline | Modelo ao vivo com 45 medidas antes da escrita |
| Criação | MCP powerbi-modeling, Desktop aberto. M44/M45 e depois M46/M47/M48, pasta `DRE\Desempenho`, expressões da seção 3 do contrato. Compilação prévia em consulta sem erro |
| Resultado | 50 medidas, 16 tabelas, 18 relacionamentos |

## 2. Resultados

| ID | Teste | Resultado |
| --- | --- | --- |
| S01 | 20 sintéticos de classificação + 11 de cumprimento (receita/gasto, limites ±0,01, estorno, IR crédito, RL, EBITDA/EBIT, BLANK, O zero/negativo, R negativo, posição não elegível) | **31/31** |
| Q/D | 5 grupos × 45 recortes (9 agregados + 36 meses) × 13 posições × 5 medidas, Power BI × regras aplicadas aos R/O/P calculados no Databricks | **14.625/14.625** (2.925 agregadas + 11.700 mensais); 6.345 BLANK/NULL coincidentes; 0 duplicadas, ausentes ou extras; dif. máx. R$ 1,5E-7, razão 8,9E-16 |
| — | Sanidade: R−O e R−P do roteiro 07 × saídas SQL do L2.3.2 | 5.850/5.850 |
| G01 | Total entre posições, posições 1+3 juntas, datas parciais 02–31/05/2023, posição × descrição conflitantes, Jun–Dez/2023 | Todos BLANK |
| R01 | Controles: RL 5.038.227,39 / 6.622.493,82 / 6.157.931,19; Comparável RL 2023 819.957,24 / 813.676,11 / 15 pares; Status "corte comum 2023-05"; M40 RL 2022 −111.518,39 | Idênticos ao L2.3.1/L2.3.2 |
| R02 | Persistência em arquivo | `_Medidas.tmdl` salvo com **50 medidas**; **45/45 antigas textualmente idênticas** ao backup (inclui lineageTags); coluna `_Organizacao` e partição idênticas, apenas reposicionadas após as novas medidas; `_ConfigCobertura.tmdl`, `relationships.tmdl` e `model.tmdl` com hash idêntico ao backup |

Distribuição das classificações (M46+M47, todas as células): Favorável 1.884; Desfavorável 1.713; Favorável (provisório) 213; Desfavorável (provisório) 147; Em linha 3. M48 preenchido em 360 células (posições 1/3 com realizado).

Leitura (2022, consolidado, x Orçado): Receita Bruta −488.959,49 Desfavorável, cumprimento 99,43%; Custos +284.680,94 Favorável (gasto menor); Despesas −115.329,26 Desfavorável; Resultado Líquido −111.518,39 Desfavorável (provisório).

## 3. Desvios e limitações

- Classificação retorna BLANK sem dados, em vez dos rótulos "Sem dados comparáveis"/"Sem regra aprovada" sugeridos no plano-mãe: medidas de texto sempre preenchidas expandem matrizes com linhas vazias. O motivo continua em M50 `DRE | Status Comparabilidade`.
- A guarda de regime de sinais para gastos (seção 5 do plano-mãe) não foi implementada: pela decisão 1, impacto = desvio, válido também com estornos ou IR positivo.
- Lado SQL: roteiro 07 (novo) reutiliza os CTEs dos roteiros 05/06 e devolve R/O/P comparáveis; as regras são aplicadas no `comparar-desempenho.py`. Executado pelo `execute_query` do MCP databricks-local, somente leitura, em 3 páginas.
- Exportação DAX em 8 blocos (limite de 60 s da ponte); ~18–22 s por bloco.

## 4. Pendências para aceite

1. ~~R02~~ concluído em 04/11/2026.
2. ~~Aceite técnico~~ concedido em 04/11/2026.
3. ~~Commit Git~~ `0a9fd51`.

Aceite técnico/didático; não homologa fechamento, EBITDA, EBIT ou Resultado Líquido.

## 5. Rollback

Com o Desktop fechado, restaurar `DRE Moderno - Databricks2.SemanticModel/definition/tables/_Medidas.tmdl` de `backups/lote2-3-3-pre-20261104-1325/` (45 medidas). Reabrir e conferir 45 medidas e os controles R01.
