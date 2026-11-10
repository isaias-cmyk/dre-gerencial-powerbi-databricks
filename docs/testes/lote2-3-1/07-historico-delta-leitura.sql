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
