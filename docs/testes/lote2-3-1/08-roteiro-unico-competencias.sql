-- L2.3.1: ROTEIRO UNICO SOMENTE LEITURA, 02/11/2026.
-- Reutiliza 05, 07 e 06 nesta ordem. Nao executado pelo agente no Databricks.
-- Selecionar e executar CADA instrucao separadamente no SQL Editor.
-- Exportar resultados completos segundo docs/execucao-roteiro-unico-competencias.md.
-- Sem DDL/DML; SHOW CREATE apenas retorna texto, nao executar o texto retornado.
-- Erros/permissoes devem ser registrados; nao ignorar instrucoes com falha.
-- Grade fixa 2021-2023 e somente universo DIAGNOSTICO de 108 pares, nao corte definitivo.

-- A: seis resultados A01-A06, reaproveitados do roteiro 05.
-- INVESTIGAÇÃO SOMENTE LEITURA. Preparado; NÃO EXECUTADO pelo agente.
-- Executar as instruções individualmente no warehouse existente e exportar cada resultado.
-- Resultados de information_schema são limitados pelos privilégios do usuário.
-- Ausência no resultado não comprova inexistência de objetos sem permissão.

-- 1. Descobrir schemas realmente acessíveis, sem presumir nomes de Bronze/Silver.
SELECT catalog_name, schema_name
FROM workspace.information_schema.schemata
ORDER BY schema_name;

-- 2. Inventário de objetos candidatos a controle em todos os schemas acessíveis.
SELECT table_catalog, table_schema, table_name, table_type, comment
FROM workspace.information_schema.tables
WHERE LOWER(CONCAT_WS(' ',table_name,comment))
 RLIKE 'controle|control|manifest|carga|load|fech|clos|process|audit|cobertura|coverage|pipeline|batch'
ORDER BY table_schema, table_name;

-- 3. Campos candidatos e comentários, inclusive quando o nome da tabela não sugere controle.
SELECT table_schema, table_name, column_name, data_type, comment
FROM workspace.information_schema.columns
WHERE LOWER(CONCAT_WS(' ',column_name,comment))
 RLIKE 'compet|filial|cenario|status|fech|clos|process|carga|load|ingest|complet|cobertura|coverage|lote|batch'
ORDER BY table_schema, table_name, ordinal_position;

-- 4. Metadados e definição acessível das views gerenciais. Definição NULL pode ser restrição de acesso.
SELECT table_catalog, table_schema, table_name, view_definition
FROM workspace.information_schema.views
WHERE table_schema='gold'
 AND table_name IN ('vw_dre_comparativo','vw_dre_provisoria','vw_financeiro_comparativo');

-- 5. Exibe a definição da view como TEXTO, sem executá-la como DDL.
SHOW CREATE TABLE workspace.gold.vw_dre_comparativo;

-- 6. Campos e rastreabilidade da origem já conhecida.
SELECT cod_filial, _arquivo_origem, _aba_origem, _tabela_origem, _data_ingestao,
 MIN(competencia_data) AS primeira_competencia_com_linha,
 MAX(competencia_data) AS ultima_competencia_com_linha,
 COUNT(DISTINCT competencia_data) AS competencias_com_linha,
 COUNT(*) AS linhas
FROM workspace.gold.fato_lancamentos
GROUP BY cod_filial, _arquivo_origem, _aba_origem, _tabela_origem, _data_ingestao
ORDER BY cod_filial, primeira_competencia_com_linha;

-- Opcional, após confirmar que fato_lancamentos é tabela Delta e que há acesso:
-- DESCRIBE HISTORY workspace.gold.fato_lancamentos;
-- Commit Delta/ingestão prova operação na tabela, não fechamento de cada filial/mês.
-- Não executar SQL dinâmico montado a partir de comentários/definições retornados.
-- Se surgir um controle candidato, inspecionar seu schema/contrato antes de consultar campos presumidos.

-- B: sete resultados B01-B07, reaproveitados do roteiro 07.
-- SOMENTE LEITURA. Preparado em 02/11/2026; não executado remotamente.
-- Executar cada instrução separadamente. Preservar resultados completos e erros de permissão.
-- Reutilizar primeiro o roteiro 05 para schemas, candidatos, campos e rastreabilidade.

-- Inventário completo das camadas; não restringir a busca de controles a estas camadas (ver 05).
SELECT table_catalog, table_schema, table_name, table_type, comment
FROM workspace.information_schema.tables
WHERE LOWER(table_schema) IN ('bronze','silver','gold')
ORDER BY table_schema,table_name;

-- Colunas reais das camadas, incluindo rastreabilidade e contagens esperadas/processadas.
SELECT table_schema,table_name,column_name,data_type,comment
FROM workspace.information_schema.columns
WHERE LOWER(table_schema) IN ('bronze','silver','gold')
ORDER BY table_schema,table_name,ordinal_position;

-- Objeto conhecido: confirmar format=delta antes de executar HISTORY.
DESCRIBE DETAIL workspace.gold.fato_lancamentos;
SHOW TBLPROPERTIES workspace.gold.fato_lancamentos;

-- Executar SOMENTE se DETAIL confirmar Delta; guardar todo o histórico retido, sem LIMIT 1.
DESCRIBE HISTORY workspace.gold.fato_lancamentos;

-- Gerador de instruções de metadados, apenas TEXTO. Não executa SQL dinâmico.
-- Selecionar manualmente os objetos relevantes do Realizado/controle após conferir o inventário.
-- TABLE_TYPE exclui views. DETAIL ainda pode falhar para formatos/objetos não suportados.
SELECT table_schema,table_name,
 CONCAT('DESCRIBE DETAIL `',REPLACE(table_catalog,'`','``'),'`.`',
 REPLACE(table_schema,'`','``'),'`.`',REPLACE(table_name,'`','``'),'`;') AS sql_detail,
 CONCAT('SHOW TBLPROPERTIES `',REPLACE(table_catalog,'`','``'),'`.`',
 REPLACE(table_schema,'`','``'),'`.`',REPLACE(table_name,'`','``'),'`;') AS sql_properties,
 CONCAT('DESCRIBE HISTORY `',REPLACE(table_catalog,'`','``'),'`.`',
 REPLACE(table_schema,'`','``'),'`.`',REPLACE(table_name,'`','``'),'`;') AS sql_history_somente_delta
FROM workspace.information_schema.tables
WHERE LOWER(table_schema) IN ('bronze','silver','gold')
 AND table_type IN ('MANAGED','EXTERNAL')
ORDER BY table_schema,table_name;

-- Complemento de cobertura: não perder linhas ausentes da grade calendário x dimensão filial.
WITH meses AS (
 SELECT DISTINCT CAST(inicio_mes AS DATE) AS competencia FROM workspace.gold.dim_calendario
), filiais AS (
 SELECT DISTINCT cod_filial FROM workspace.gold.dim_filial
)
SELECT f.cod_filial,CAST(date_trunc('MONTH',f.competencia_data) AS DATE) AS competencia,
 COUNT(*) AS linhas_fora_da_grade
FROM workspace.gold.fato_lancamentos f
LEFT JOIN filiais d ON d.cod_filial=f.cod_filial
LEFT JOIN meses m ON m.competencia=CAST(date_trunc('MONTH',f.competencia_data) AS DATE)
WHERE d.cod_filial IS NULL OR m.competencia IS NULL
GROUP BY f.cod_filial,CAST(date_trunc('MONTH',f.competencia_data) AS DATE)
ORDER BY f.cod_filial,competencia;

-- Controles candidatos: consultar registros somente após inspecionar colunas reais e contrato.
-- Não há SELECT com campos inventados. Para cada objeto, documentar a consulta efetivamente
-- construída/executada, chave filial/mês/cenário, estados, contagens e autoridade responsável.
-- No histórico, registrar version/timestamp/operation e metadados efetivamente retornados:
-- operationParameters, operationMetrics, job, notebook, userMetadata quando disponíveis.
-- WRITE/commit e last_altered não certificam completude mensal ou fechamento financeiro.

-- C01: grade explicita 108 pares, adaptada do roteiro 06.
-- Somente leitura. NÃO EXECUTADO nesta entrega.
-- Grade real de três filiais e competências do calendário: contagens, não certificado de carga.
-- COALESCE abaixo é restrito a CONTAGENS diagnósticas, nunca a valores financeiros.
WITH meses AS (
 SELECT explode(sequence(DATE '2021-01-01',DATE '2023-12-01',INTERVAL 1 MONTH)) AS competencia
), filiais AS (
 SELECT cod_filial FROM VALUES ('01'),('02'),('03') AS esperado(cod_filial)
), f AS (
 SELECT cod_filial, CAST(date_trunc('MONTH',competencia_data) AS DATE) AS competencia,
 COUNT(*) AS lancamentos,
 COUNT(valor) AS valores_presentes,
 SUM(CASE WHEN valor=0 THEN 1 ELSE 0 END) AS valores_zero
 FROM workspace.gold.fato_lancamentos
 GROUP BY cod_filial, CAST(date_trunc('MONTH',competencia_data) AS DATE)
), v AS (
 SELECT cod_filial, CAST(date_trunc('MONTH',competencia) AS DATE) AS competencia,
 COUNT(*) AS linhas_view,
 COUNT(realizado) AS posicoes_realizado_presente,
 SUM(CASE WHEN realizado=0 THEN 1 ELSE 0 END) AS posicoes_realizado_zero
 FROM workspace.gold.vw_dre_comparativo
 GROUP BY cod_filial, CAST(date_trunc('MONTH',competencia) AS DATE)
), grade AS (
SELECT d.cod_filial, m.competencia,
 COALESCE(f.lancamentos,0) AS lancamentos,
 COALESCE(f.valores_presentes,0) AS valores_presentes,
 COALESCE(f.valores_zero,0) AS valores_zero,
 COALESCE(v.linhas_view,0) AS linhas_view,
 COALESCE(v.posicoes_realizado_presente,0) AS posicoes_realizado_presente,
 COALESCE(v.posicoes_realizado_zero,0) AS posicoes_realizado_zero,
 'NAO_INFERIDA_POR_MOVIMENTO' AS cobertura_homologada
FROM filiais d CROSS JOIN meses m
LEFT JOIN f ON f.cod_filial=d.cod_filial AND f.competencia=m.competencia
LEFT JOIN v ON v.cod_filial=d.cod_filial AND v.competencia=m.competencia
), limites AS (
 SELECT *,
 MIN(CASE WHEN lancamentos>0 THEN competencia END) OVER (PARTITION BY cod_filial) AS primeiro_mes_com_movimento,
 MAX(CASE WHEN lancamentos>0 THEN competencia END) OVER (PARTITION BY cod_filial) AS ultimo_mes_com_movimento
 FROM grade
)
SELECT *,
 CASE WHEN lancamentos>0 THEN 'COM_MOVIMENTO' ELSE 'SEM_MOVIMENTO_OBSERVADO' END AS presenca,
 CASE WHEN lancamentos=0 AND competencia BETWEEN primeiro_mes_com_movimento AND ultimo_mes_com_movimento
 THEN TRUE ELSE FALSE END AS lacuna_intermediaria,
 lancamentos-valores_presentes AS valores_nulos_a_investigar
FROM limites
ORDER BY cod_filial,competencia;
-- Normalização mensal usada somente para contagens. O calendário delimita o universo.
-- Ausências fora do calendário, filiais órfãs e datas NULL exigem a consulta complementar do roteiro 07.
-- Lacunas e valores NULL são sinais a investigar; não comprovam falha nem fechamento.

-- D01: conferir calendario e filiais esperados sem multiplicar linhas da grade C01.
WITH meses AS (
 SELECT explode(sequence(DATE '2021-01-01',DATE '2023-12-01',INTERVAL 1 MONTH)) AS competencia
), filiais AS (
 SELECT cod_filial FROM VALUES ('01'),('02'),('03') AS e(cod_filial)
), cal AS (
 SELECT CAST(inicio_mes AS DATE) competencia,COUNT(*) dias
 FROM workspace.gold.dim_calendario GROUP BY CAST(inicio_mes AS DATE)
), dim AS (
 SELECT cod_filial,COUNT(*) linhas FROM workspace.gold.dim_filial GROUP BY cod_filial
)
SELECT f.cod_filial,m.competencia,COALESCE(d.linhas,0) linhas_dim_filial,
 COALESCE(c.dias,0) dias_no_calendario,
 dayofmonth(last_day(m.competencia)) dias_esperados
FROM filiais f CROSS JOIN meses m
LEFT JOIN dim d ON d.cod_filial=f.cod_filial
LEFT JOIN cal c ON c.competencia=m.competencia
ORDER BY f.cod_filial,m.competencia;

-- D02: resumo independente de valores monetarios: NULL, datas e filiais inesperadas.
SELECT COUNT(*) linhas,
 SUM(CASE WHEN cod_filial IS NULL THEN 1 ELSE 0 END) filial_nula,
 SUM(CASE WHEN competencia_data IS NULL THEN 1 ELSE 0 END) competencia_nula,
 SUM(CASE WHEN cod_filial NOT IN ('01','02','03') THEN 1 ELSE 0 END) filial_fora_universo,
 SUM(CASE WHEN competencia_data < DATE '2021-01-01' OR competencia_data >= DATE '2024-01-01' THEN 1 ELSE 0 END) data_fora_universo,
 COUNT(valor) valores_presentes,
 MIN(_data_ingestao) primeira_ingestao,MAX(_data_ingestao) ultima_ingestao
FROM workspace.gold.fato_lancamentos;

-- E: schema detalhado e amostra por objeto REAL do inventario recebido.
-- Amostras LIMIT 5 nao certificam completude. Servem para ler campos reais de rastreabilidade.
-- Nao ha nomes presumidos de colunas Bronze/Silver nem conversao de valores financeiros.
-- E01_schema.csv e E01_amostra.csv : workspace.silver.flancamentos
DESCRIBE TABLE EXTENDED workspace.silver.flancamentos;
SELECT * FROM workspace.silver.flancamentos LIMIT 5;

-- E02_schema.csv e E02_amostra.csv : workspace.gold.fato_lancamentos
DESCRIBE TABLE EXTENDED workspace.gold.fato_lancamentos;
SELECT * FROM workspace.gold.fato_lancamentos LIMIT 5;

-- E03_schema.csv e E03_amostra.csv : workspace.bronze.flancamento1_ano1
DESCRIBE TABLE EXTENDED workspace.bronze.flancamento1_ano1;
SELECT * FROM workspace.bronze.flancamento1_ano1 LIMIT 5;

-- E04_schema.csv e E04_amostra.csv : workspace.bronze.flancamento1_ano2
DESCRIBE TABLE EXTENDED workspace.bronze.flancamento1_ano2;
SELECT * FROM workspace.bronze.flancamento1_ano2 LIMIT 5;

-- E05_schema.csv e E05_amostra.csv : workspace.bronze.flancamento1_ano3
DESCRIBE TABLE EXTENDED workspace.bronze.flancamento1_ano3;
SELECT * FROM workspace.bronze.flancamento1_ano3 LIMIT 5;

-- E06_schema.csv e E06_amostra.csv : workspace.bronze.flancamento2_ano1
DESCRIBE TABLE EXTENDED workspace.bronze.flancamento2_ano1;
SELECT * FROM workspace.bronze.flancamento2_ano1 LIMIT 5;

-- E07_schema.csv e E07_amostra.csv : workspace.bronze.flancamento2_ano2
DESCRIBE TABLE EXTENDED workspace.bronze.flancamento2_ano2;
SELECT * FROM workspace.bronze.flancamento2_ano2 LIMIT 5;

-- E08_schema.csv e E08_amostra.csv : workspace.bronze.flancamento2_ano3
DESCRIBE TABLE EXTENDED workspace.bronze.flancamento2_ano3;
SELECT * FROM workspace.bronze.flancamento2_ano3 LIMIT 5;

-- E09_schema.csv e E09_amostra.csv : workspace.bronze.flancamento3_ano1
DESCRIBE TABLE EXTENDED workspace.bronze.flancamento3_ano1;
SELECT * FROM workspace.bronze.flancamento3_ano1 LIMIT 5;

-- E10_schema.csv e E10_amostra.csv : workspace.bronze.flancamento3_ano2
DESCRIBE TABLE EXTENDED workspace.bronze.flancamento3_ano2;
SELECT * FROM workspace.bronze.flancamento3_ano2 LIMIT 5;

-- E11_schema.csv e E11_amostra.csv : workspace.bronze.flancamento3_ano3
DESCRIBE TABLE EXTENDED workspace.bronze.flancamento3_ano3;
SELECT * FROM workspace.bronze.flancamento3_ano3 LIMIT 5;

-- FIM. Controles candidatos: consultar somente apos conhecer schema e autoridade.
-- A02/A03/B02 podem revelar controles em campos/comentarios, nao apenas nomes de tabela.
-- Nao assumir que tempo de ingestao, numero de linhas, commit ou presenca de valor prova carga completa.
-- Cobertura necessita certificado por filial/mes, inclusive zero movimento; fechamento necessita autoridade contabil.
-- Se surgir controle candidato, fornecer schema e contrato para preparar o SELECT exato, sem inventar campos.
