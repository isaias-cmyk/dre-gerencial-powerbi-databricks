# L2.3.2 — Validação dos desvios M40–M43

Data: 03/11/2026 (Q01/Q02 em 04/11/2026). Estado: **implementado, validado em DAX e conciliado com SQL independente no Databricks (Q01 2.340/2.340; Q02 9.360/9.360). **Aceite técnico do usuário em 04/11/2026 13:16. Sublote concluído** (aceite técnico/didático; não é homologação contábil).

Plano e contratos: [plano-lote2-3-2.md](plano-lote2-3-2.md). Evidências: [evidencias/lote2-3-2-execucao-20261103/](evidencias/lote2-3-2-execucao-20261103/).

## 1. Execução

| Item | Registro |
| --- | --- |
| Forma de edição | MCP powerbi-modeling com Power BI Desktop aberto (decisão do usuário registrada em PLANS.md), servidor reiniciado em modo `--readwrite` |
| Backup prévio | `backups/lote2-3-2-pre-20261103-2125/`, 34 arquivos do PBIP + `manifesto.json` (SHA-256). Leitura de volta: 33/34 hashes idênticos; `visual.json` não relido por profundidade de pasta (tamanho 1.864 bytes confere). 34/34 idênticos ao commit `512c4cc` após normalização CRLF→LF |
| Baseline antes da escrita | Modelo ao vivo = `_Medidas.tmdl` em disco: 41 medidas, 16 tabelas, 18 relacionamentos |
| Criação | M40 e M42; depois M41 e M43 (ordem da seção 9). Expressões idênticas à seção 4 do plano; pasta `DRE\Desvios`; formatos `R$ #,##0.00;(R$ #,##0.00);R$ 0.00` e `0.00%;(0.00%);0.00%` |
| Resultado estrutural | 45 medidas, 16 tabelas, 18 relacionamentos, 16 partições |
| Salvamento | PBIP salvo pelo usuário às 22:17 (título do Desktop e data dos arquivos TMDL) |

## 2. Resultados

| ID | Teste | Resultado |
| --- | --- | --- |
| S01 | 15 sintéticos do contrato (roteiro 03) | 15/15 aprovados |
| S02 | 15 sintéticos com cópias privadas das quatro expressões em estrutura de medidas | 60/60 aprovados |
| — | Compilação prévia das quatro expressões apenas em consulta (DEFINE MEASURE) | Sem erro |
| G01 | Total entre posições, datas parciais (02–31/05/2023), posição/descrição conflitantes (roteiro 04) | 12/12 BLANK |
| D01 | 5 grupos × 9 recortes × 13 posições × 4 medidas (roteiro 01) | **2.340/2.340**; 0 BLANK divergente; diferença máxima 0; 800 BLANK esperados (40 por grupo/medida) |
| D02 | 5 grupos × 36 competências × 13 posições × 4 medidas (roteiro 02) | **9.360/9.360**; 0 BLANK divergente; diferença máxima 0 |
| G02 | Totais entre filiais (2022, 11 posições elegíveis) | Monetário consolidado = soma das filiais (resíduo < 1E-7); percentual = razão dos agregados, diferente da soma das razões; sinal preservado com referência negativa (ex.: Custos, R−O = +284.680,94, +0,70%) |
| R01 | Regressão das 41 | Expressões e lineageTags idênticos ao backup (modelo ao vivo e arquivo salvo); conciliação medida × view 528/528 (33 medidas × 16 contextos), máximo 3E-8; controles RL 5.038.227,39 / 6.622.493,82 / 6.157.931,19; Comparável 2023: 819.957,24 / 813.676,11 / 15 pares; Status "Recorte comparável parcial; corte comum 2023-05" |
| R02 | Persistência | `_Medidas.tmdl` salvo com 45 medidas; 41 antigas textualmente idênticas; `_ConfigCobertura.tmdl` e `relationships.tmdl` idênticos ao backup; `model.tmdl` difere apenas na anotação `PBI_ProTooling` (+`"MCP-PBIModeling"`), acrescentada pela ferramenta |
| V01 | Formatação | FORMAT com os formatos persistidos: negativos entre parênteses, razão 0,0070 → `0.70%`, sem multiplicação por 100. Modelo em cultura en-US (separadores `,`/`.`), limitação pré-existente |
| Q01 | SQL independente agregado (roteiro 05) | **2.340/2.340**; 800 NULL/BLANK coincidentes; 0 duplicadas, ausentes ou extras; dif. máx. BRL 1,5E-7, razão 2,2E-15. Preflight de grão: 0 duplicidades. Statement IDs em `sql_statement_ids.json` |
| Q02 | SQL independente mensal (roteiro 06) | **9.360/9.360**; 2.980 NULL/BLANK coincidentes; 0 duplicadas, ausentes ou extras; dif. máx. BRL 1,8E-9, razão 5,9E-16. 10 páginas SQL (`sql_statement_ids_mensal.json`) × 6 blocos DAX |

Exemplo de leitura: Resultado Líquido 2023 no recorte comparável (Jan–Mai, três filiais): R−O = +6.281,13 (+0,77%); R−P = +35.983,38. Resultado Líquido 2022 consolidado: R−O = −111.518,39 (−5,04%); R−P = +55.682,24 (+2,72%).

## 3. Desvios dos roteiros e limitações

- D01/D02 executados em blocos (por grupo/ano) e resumidos por medida, porque a ponte com o computador encerra chamadas após 60 s. Colunas Pares/Status retiradas da execução por desempenho; a lógica Valor × Esperado e os critérios de aprovação são os dos roteiros.
- D02: filtro `FORMAT(data,"yyyy-MM")` substituído por `DATESBETWEEN(primeiro dia, EOMONTH)` — mesmo conjunto de datas, execução viável.
- R01 usou comparação textual das expressões + conciliação 528/528, não os roteiros 09/14 do L2.3.1.
- R02 confirmado em arquivo após salvar; o ciclo fechar/reabrir o Desktop não foi executado.
- Q01/Q02 executados pelo MCP databricks-local (`execute_query`, somente leitura, ≤1.000 linhas por chamada). Nenhuma escrita no Databricks.
- Defeito nos roteiros 05/06: o CASE final resultava em DECIMAL(38,2) e arredondava as razões M41/M43 a 2 casas. Corrigido apenas na saída, com `CAST(... AS DOUBLE)`; a lógica dos CTEs não mudou. Roteiros 05/06 corrigidos em 04/11/2026 com o mesmo CAST.
- Saída serializada em uma chave `grupo|periodo|posicao|id|valor` (NULL como `N`) com coluna de preenchimento, para gravação em arquivo pela ponte; Q02 paginado com `ORDER BY k LIMIT 1000 OFFSET`.
- Q02: predicado de `pares` simplificado para `p.periodo = concat('M', date_format(m.competencia,'yyyy-MM'))` e colunas não usadas retiradas (lógica equivalente).
- Contraparte DAX do Q02 exportada em 6 blocos (ano × grupos de filiais) com o mesmo filtro `DATESBETWEEN` do D02.
- `comparar-desvios.py` parametrizado (`esperadas`, nome do JSON de saída); critérios e tolerâncias inalterados.
- Desempenho: matrizes mensais com várias filiais levaram 30–35 s por bloco de 24 meses (herdado das medidas Comparáveis). Avaliar nos visuais.
- Testes D01/D02 comparam com a álgebra das Comparáveis importadas; não são conciliação financeira independente.

## 4. Pendências para aceite

1. ~~Q01~~ e ~~Q02~~ concluídos (04/11/2026).
2. ~~Aceite técnico do L2.3.2~~ concedido pelo usuário em 04/11/2026.
3. Opcional: fechar/reabrir o Desktop e confirmar 45 medidas Valid (R02 completo).
4. ~~CAST DOUBLE nos roteiros 05/06~~ corrigido em 04/11/2026.
5. Commit Git das medidas e evidências (não feito).

Implementação não homologa fechamento real, Resultado Líquido, EBITDA ou EBIT. Sem favorabilidade ou cumprimento. L2.3.3 não iniciado.

## 5. Rollback

Com o Desktop fechado, restaurar somente `DRE Moderno - Databricks2.SemanticModel/definition/tables/_Medidas.tmdl` de `backups/lote2-3-2-pre-20261103-2125/` (41 medidas) ou o mesmo arquivo do commit `512c4cc`; reabrir e revalidar 41 medidas, nove intervalos e controles.
