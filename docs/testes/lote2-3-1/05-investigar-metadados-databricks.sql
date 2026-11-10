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
