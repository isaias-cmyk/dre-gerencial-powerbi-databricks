-- COMPLEMENTO somente leitura aos roteiros originais. NÃO EXECUTADO.
-- Executar uma instrução por vez no Databricks SQL autenticado existente.
-- S00: catálogo real, sem inventar códigos de filial/conta.
SELECT cod_filial, filial FROM workspace.gold.dim_filial ORDER BY filial;
SELECT id_conta, descricaon1, descricaon2, detalharn2 FROM workspace.gold.dim_conta ORDER BY id_conta;
-- S01: células base de evidência para o modelo e a origem: linha 13 por filial/ano.
SELECT cod_filial, YEAR(competencia) AS ano, COUNT(*) AS linhas,
 SUM(realizado) AS realizado, SUM(orcado) AS orcado, SUM(previsto) AS previsto
FROM workspace.gold.vw_dre_comparativo WHERE ordem_dre=13
GROUP BY cod_filial,YEAR(competencia) ORDER BY cod_filial,ano;
-- S02: controle integral sem filtro temporal. NULL não deve ser aprovado como zero.
SELECT SUM(realizado) AS realizado,SUM(orcado) AS orcado,SUM(previsto) AS previsto,
 ROUND(SUM(realizado),2)-5038227.39 AS dif_realizado,
 ROUND(SUM(orcado),2)-6622493.82 AS dif_orcado,
 ROUND(SUM(previsto),2)-6157931.19 AS dif_previsto
FROM workspace.gold.vw_dre_comparativo WHERE ordem_dre=13;

-- S03-fato_lancamentos: matriz filial x período. Para view, valores financeiros somente linha 13.
WITH periodos AS (
 SELECT * FROM VALUES ('Integral',DATE '2021-01-01',DATE '2024-01-01'),
 ('2021',DATE '2021-01-01',DATE '2022-01-01'),('2022',DATE '2022-01-01',DATE '2023-01-01'),
 ('2023_JanMai',DATE '2023-01-01',DATE '2023-06-01'),('2023_JunDez',DATE '2023-06-01',DATE '2024-01-01') AS p(periodo,inicio,fim)),
 filiais AS (SELECT cod_filial,filial,FALSE AS consolidado FROM workspace.gold.dim_filial
 UNION ALL SELECT CAST(NULL AS STRING),'Consolidado',TRUE)
SELECT 'fato_lancamentos' AS tabela,b.cod_filial,b.filial,p.periodo,COUNT(f.competencia_data) AS linhas,SUM(f.valor) AS valor
 FROM filiais b CROSS JOIN periodos p LEFT JOIN workspace.gold.fato_lancamentos f
 ON (b.consolidado OR f.cod_filial=b.cod_filial) AND f.competencia_data>=p.inicio AND f.competencia_data<p.fim
 GROUP BY b.cod_filial,b.filial,p.periodo ORDER BY b.filial,p.periodo;

-- S03-fato_orcamento: matriz filial x período. Para view, valores financeiros somente linha 13.
WITH periodos AS (
 SELECT * FROM VALUES ('Integral',DATE '2021-01-01',DATE '2024-01-01'),
 ('2021',DATE '2021-01-01',DATE '2022-01-01'),('2022',DATE '2022-01-01',DATE '2023-01-01'),
 ('2023_JanMai',DATE '2023-01-01',DATE '2023-06-01'),('2023_JunDez',DATE '2023-06-01',DATE '2024-01-01') AS p(periodo,inicio,fim)),
 filiais AS (SELECT cod_filial,filial,FALSE AS consolidado FROM workspace.gold.dim_filial
 UNION ALL SELECT CAST(NULL AS STRING),'Consolidado',TRUE)
SELECT 'fato_orcamento' AS tabela,b.cod_filial,b.filial,p.periodo,COUNT(f.competencia_data) AS linhas,SUM(f.valor) AS valor
 FROM filiais b CROSS JOIN periodos p LEFT JOIN workspace.gold.fato_orcamento f
 ON (b.consolidado OR f.cod_filial=b.cod_filial) AND f.competencia_data>=p.inicio AND f.competencia_data<p.fim
 GROUP BY b.cod_filial,b.filial,p.periodo ORDER BY b.filial,p.periodo;

-- S03-fato_previsao: matriz filial x período. Para view, valores financeiros somente linha 13.
WITH periodos AS (
 SELECT * FROM VALUES ('Integral',DATE '2021-01-01',DATE '2024-01-01'),
 ('2021',DATE '2021-01-01',DATE '2022-01-01'),('2022',DATE '2022-01-01',DATE '2023-01-01'),
 ('2023_JanMai',DATE '2023-01-01',DATE '2023-06-01'),('2023_JunDez',DATE '2023-06-01',DATE '2024-01-01') AS p(periodo,inicio,fim)),
 filiais AS (SELECT cod_filial,filial,FALSE AS consolidado FROM workspace.gold.dim_filial
 UNION ALL SELECT CAST(NULL AS STRING),'Consolidado',TRUE)
SELECT 'fato_previsao' AS tabela,b.cod_filial,b.filial,p.periodo,COUNT(f.competencia_data) AS linhas,SUM(f.valor) AS valor
 FROM filiais b CROSS JOIN periodos p LEFT JOIN workspace.gold.fato_previsao f
 ON (b.consolidado OR f.cod_filial=b.cod_filial) AND f.competencia_data>=p.inicio AND f.competencia_data<p.fim
 GROUP BY b.cod_filial,b.filial,p.periodo ORDER BY b.filial,p.periodo;

-- S03-vw_dre_comparativo: matriz filial x período. Para view, valores financeiros somente linha 13.
WITH periodos AS (
 SELECT * FROM VALUES ('Integral',DATE '2021-01-01',DATE '2024-01-01'),
 ('2021',DATE '2021-01-01',DATE '2022-01-01'),('2022',DATE '2022-01-01',DATE '2023-01-01'),
 ('2023_JanMai',DATE '2023-01-01',DATE '2023-06-01'),('2023_JunDez',DATE '2023-06-01',DATE '2024-01-01') AS p(periodo,inicio,fim)),
 filiais AS (SELECT cod_filial,filial,FALSE AS consolidado FROM workspace.gold.dim_filial
 UNION ALL SELECT CAST(NULL AS STRING),'Consolidado',TRUE)
SELECT 'vw_dre_comparativo' AS tabela,b.cod_filial,b.filial,p.periodo,COUNT(f.competencia) AS linhas,SUM(f.realizado) AS realizado,SUM(f.orcado) AS orcado,SUM(f.previsto) AS previsto,COUNT(f.realizado) AS realizados_nao_nulos
 FROM filiais b CROSS JOIN periodos p LEFT JOIN workspace.gold.vw_dre_comparativo f
 ON (b.consolidado OR f.cod_filial=b.cod_filial) AND f.competencia>=p.inicio AND f.competencia<p.fim AND f.ordem_dre=13
 GROUP BY b.cod_filial,b.filial,p.periodo ORDER BY b.filial,p.periodo;

-- S04: contagens de TODAS as linhas da view para comparar com 06-filtros-vw (não é soma financeira).
SELECT cod_filial,competencia,COUNT(*) AS linhas FROM workspace.gold.vw_dre_comparativo
GROUP BY cod_filial,competencia ORDER BY cod_filial,competencia;

-- S05-dim_filial: vazios e colisões após normalização; não alterar os dados.
SELECT COUNT(*) AS chaves_vazias FROM workspace.gold.dim_filial WHERE cod_filial IS NOT NULL AND TRIM(cod_filial)='';
SELECT UPPER(TRIM(cod_filial)) AS chave_normalizada, COUNT(*) AS n FROM workspace.gold.dim_filial
GROUP BY UPPER(TRIM(cod_filial)) HAVING COUNT(*)>1;

-- S05-dim_conta: vazios e colisões após normalização; não alterar os dados.
SELECT COUNT(*) AS chaves_vazias FROM workspace.gold.dim_conta WHERE id_conta IS NOT NULL AND TRIM(id_conta)='';
SELECT UPPER(TRIM(id_conta)) AS chave_normalizada, COUNT(*) AS n FROM workspace.gold.dim_conta
GROUP BY UPPER(TRIM(id_conta)) HAVING COUNT(*)>1;

-- S05-dim_dre: vazios e colisões após normalização; não alterar os dados.
SELECT COUNT(*) AS chaves_vazias FROM workspace.gold.dim_dre WHERE id_dre IS NOT NULL AND TRIM(id_dre)='';
SELECT UPPER(TRIM(id_dre)) AS chave_normalizada, COUNT(*) AS n FROM workspace.gold.dim_dre
GROUP BY UPPER(TRIM(id_dre)) HAVING COUNT(*)>1;

-- S06: compatibilidade gerencial: sem NULL de chave de posição, descrição estável por ordem e por filial.
SELECT COUNT(*) AS posicoes_nulas FROM workspace.gold.vw_dre_comparativo WHERE ordem_dre IS NULL;
SELECT ordem_dre,COUNT(DISTINCT descricao_dre) AS descricoes,COUNT(DISTINCT subtotal) AS flags
FROM workspace.gold.vw_dre_comparativo GROUP BY ordem_dre;
SELECT descricao_dre,COUNT(DISTINCT ordem_dre) AS ordens FROM workspace.gold.vw_dre_comparativo
GROUP BY descricao_dre HAVING COUNT(DISTINCT ordem_dre)>1;
-- S07: cobertura exata da linha 13 por cenário/filial (min/max só contam valores não NULL).
SELECT cod_filial,
MIN(CASE WHEN realizado IS NOT NULL THEN competencia END) AS inicio_realizado,
MAX(CASE WHEN realizado IS NOT NULL THEN competencia END) AS fim_realizado,
MIN(CASE WHEN orcado IS NOT NULL THEN competencia END) AS inicio_orcado,
MAX(CASE WHEN orcado IS NOT NULL THEN competencia END) AS fim_orcado,
MIN(CASE WHEN previsto IS NOT NULL THEN competencia END) AS inicio_previsto,
MAX(CASE WHEN previsto IS NOT NULL THEN competencia END) AS fim_previsto,
COUNT(DISTINCT CASE WHEN realizado IS NOT NULL THEN competencia END) AS meses_realizado,
COUNT(DISTINCT CASE WHEN orcado IS NOT NULL THEN competencia END) AS meses_orcado,
COUNT(DISTINCT CASE WHEN previsto IS NOT NULL THEN competencia END) AS meses_previsto
FROM workspace.gold.vw_dre_comparativo WHERE ordem_dre=13 GROUP BY cod_filial;
-- S08: conta escolhida. Substituir o parâmetro na cópia da consulta antes de executar.
SELECT 'fato_lancamentos' AS tabela,COUNT(*) AS linhas,SUM(valor) AS valor FROM workspace.gold.fato_lancamentos WHERE planocontas_id='__ID_CONTA_ANALITICA__';
SELECT 'fato_orcamento' AS tabela,COUNT(*) AS linhas,SUM(valor) AS valor FROM workspace.gold.fato_orcamento WHERE planocontas_id='__ID_CONTA_ANALITICA__';
SELECT 'fato_previsao' AS tabela,COUNT(*) AS linhas,SUM(valor) AS valor FROM workspace.gold.fato_previsao WHERE planocontas_id='__ID_CONTA_ANALITICA__';
