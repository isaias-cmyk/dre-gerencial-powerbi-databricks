-- FASE 1: roteiro somente leitura, preparado e NÃO EXECUTADO.
-- Não altera consultas M, conexões nem dados. Executar na origem autenticada e guardar resultados.
-- Unicidade global e NULL nas chaves candidatas; zero linhas no segundo SELECT é esperado.

SELECT 'dim_filial' AS objeto, COUNT(*) AS linhas, COUNT(DISTINCT cod_filial) AS chaves_distintas,
 SUM(CASE WHEN cod_filial IS NULL THEN 1 ELSE 0 END) AS chaves_nulas FROM workspace.gold.dim_filial;
SELECT cod_filial, COUNT(*) AS quantidade FROM workspace.gold.dim_filial
 GROUP BY cod_filial HAVING COUNT(*) > 1;

SELECT 'dim_conta' AS objeto, COUNT(*) AS linhas, COUNT(DISTINCT id_conta) AS chaves_distintas,
 SUM(CASE WHEN id_conta IS NULL THEN 1 ELSE 0 END) AS chaves_nulas FROM workspace.gold.dim_conta;
SELECT id_conta, COUNT(*) AS quantidade FROM workspace.gold.dim_conta
 GROUP BY id_conta HAVING COUNT(*) > 1;

SELECT 'dim_dre' AS objeto, COUNT(*) AS linhas, COUNT(DISTINCT id_dre) AS chaves_distintas,
 SUM(CASE WHEN id_dre IS NULL THEN 1 ELSE 0 END) AS chaves_nulas FROM workspace.gold.dim_dre;
SELECT id_dre, COUNT(*) AS quantidade FROM workspace.gold.dim_dre
 GROUP BY id_dre HAVING COUNT(*) > 1;

SELECT 'dim_calendario' AS objeto, COUNT(*) AS linhas, COUNT(DISTINCT data) AS chaves_distintas,
 SUM(CASE WHEN data IS NULL THEN 1 ELSE 0 END) AS chaves_nulas FROM workspace.gold.dim_calendario;
SELECT data, COUNT(*) AS quantidade FROM workspace.gold.dim_calendario
 GROUP BY data HAVING COUNT(*) > 1;

-- IDs de conta repetidos entre filiais e combinação conta/filial.
SELECT id_conta, COUNT(DISTINCT cod_filial) AS filiais FROM workspace.gold.dim_conta
 GROUP BY id_conta HAVING COUNT(DISTINCT cod_filial) > 1;
SELECT cod_filial, id_conta, COUNT(*) AS n FROM workspace.gold.dim_conta
 GROUP BY cod_filial, id_conta HAVING COUNT(*) > 1;
-- Chave candidata e ordem gerencial. Não assumir que ordem_dre é única globalmente.
SELECT cod_filial, ordem_dre, COUNT(*) AS n FROM workspace.gold.dim_dre
 GROUP BY cod_filial, ordem_dre HAVING COUNT(*) > 1;
SELECT cod_filial, COUNT(*) AS linhas, COUNT(DISTINCT ordem_dre) AS ordens,
 MIN(ordem_dre) AS menor, MAX(ordem_dre) AS maior FROM workspace.gold.dim_dre GROUP BY cod_filial;

-- Integridade AutoDetected_b803a55e-b318-4f25-80e8-6068d5cedb12: órfãos e chaves nulas em separado.
SELECT 'AutoDetected_b803a55e-b318-4f25-80e8-6068d5cedb12' AS relacionamento, COUNT(*) AS orfaos_nao_nulos
 FROM workspace.gold.dim_conta f LEFT ANTI JOIN workspace.gold.dim_filial d ON f.cod_filial = d.cod_filial
 WHERE f.cod_filial IS NOT NULL;
SELECT 'dim_conta.cod_filial' AS coluna, COUNT(*) AS nulos FROM workspace.gold.dim_conta WHERE cod_filial IS NULL;

-- Integridade AutoDetected_d9ec7926-13de-4e3a-beaf-9d5600fb340f: órfãos e chaves nulas em separado.
SELECT 'AutoDetected_d9ec7926-13de-4e3a-beaf-9d5600fb340f' AS relacionamento, COUNT(*) AS orfaos_nao_nulos
 FROM workspace.gold.dim_dre f LEFT ANTI JOIN workspace.gold.dim_filial d ON f.cod_filial = d.cod_filial
 WHERE f.cod_filial IS NOT NULL;
SELECT 'dim_dre.cod_filial' AS coluna, COUNT(*) AS nulos FROM workspace.gold.dim_dre WHERE cod_filial IS NULL;

-- Integridade AutoDetected_b9db6563-6b6a-4ed9-9873-033469b2f0ab: órfãos e chaves nulas em separado.
SELECT 'AutoDetected_b9db6563-6b6a-4ed9-9873-033469b2f0ab' AS relacionamento, COUNT(*) AS orfaos_nao_nulos
 FROM workspace.gold.fato_lancamentos f LEFT ANTI JOIN workspace.gold.dim_filial d ON f.cod_filial = d.cod_filial
 WHERE f.cod_filial IS NOT NULL;
SELECT 'fato_lancamentos.cod_filial' AS coluna, COUNT(*) AS nulos FROM workspace.gold.fato_lancamentos WHERE cod_filial IS NULL;

-- Integridade AutoDetected_cf6c4540-68ae-4da2-acca-5a3bf495a442: órfãos e chaves nulas em separado.
SELECT 'AutoDetected_cf6c4540-68ae-4da2-acca-5a3bf495a442' AS relacionamento, COUNT(*) AS orfaos_nao_nulos
 FROM workspace.gold.fato_orcamento f LEFT ANTI JOIN workspace.gold.dim_filial d ON f.cod_filial = d.cod_filial
 WHERE f.cod_filial IS NOT NULL;
SELECT 'fato_orcamento.cod_filial' AS coluna, COUNT(*) AS nulos FROM workspace.gold.fato_orcamento WHERE cod_filial IS NULL;

-- Integridade AutoDetected_2a7e773f-8348-4485-ac6c-69dd9df5dab8: órfãos e chaves nulas em separado.
SELECT 'AutoDetected_2a7e773f-8348-4485-ac6c-69dd9df5dab8' AS relacionamento, COUNT(*) AS orfaos_nao_nulos
 FROM workspace.gold.fato_previsao f LEFT ANTI JOIN workspace.gold.dim_filial d ON f.cod_filial = d.cod_filial
 WHERE f.cod_filial IS NOT NULL;
SELECT 'fato_previsao.cod_filial' AS coluna, COUNT(*) AS nulos FROM workspace.gold.fato_previsao WHERE cod_filial IS NULL;

-- Integridade AutoDetected_2ce0342d-62e0-4df8-a023-363036b47efe: órfãos e chaves nulas em separado.
SELECT 'AutoDetected_2ce0342d-62e0-4df8-a023-363036b47efe' AS relacionamento, COUNT(*) AS orfaos_nao_nulos
 FROM workspace.gold.vw_dre_comparativo f LEFT ANTI JOIN workspace.gold.dim_filial d ON f.cod_filial = d.cod_filial
 WHERE f.cod_filial IS NOT NULL;
SELECT 'vw_dre_comparativo.cod_filial' AS coluna, COUNT(*) AS nulos FROM workspace.gold.vw_dre_comparativo WHERE cod_filial IS NULL;

-- Integridade 13c78bc6-b976-df8e-f003-91414e803c01: órfãos e chaves nulas em separado.
SELECT '13c78bc6-b976-df8e-f003-91414e803c01' AS relacionamento, COUNT(*) AS orfaos_nao_nulos
 FROM workspace.gold.fato_lancamentos f LEFT ANTI JOIN workspace.gold.dim_calendario d ON f.competencia_data = d.data
 WHERE f.competencia_data IS NOT NULL;
SELECT 'fato_lancamentos.competencia_data' AS coluna, COUNT(*) AS nulos FROM workspace.gold.fato_lancamentos WHERE competencia_data IS NULL;

-- Integridade ddacb715-ec23-2d3c-a337-1083a97c680d: órfãos e chaves nulas em separado.
SELECT 'ddacb715-ec23-2d3c-a337-1083a97c680d' AS relacionamento, COUNT(*) AS orfaos_nao_nulos
 FROM workspace.gold.fato_orcamento f LEFT ANTI JOIN workspace.gold.dim_calendario d ON f.competencia_data = d.data
 WHERE f.competencia_data IS NOT NULL;
SELECT 'fato_orcamento.competencia_data' AS coluna, COUNT(*) AS nulos FROM workspace.gold.fato_orcamento WHERE competencia_data IS NULL;

-- Integridade 4f0276cf-4e80-7bc6-b833-a091883c1e68: órfãos e chaves nulas em separado.
SELECT '4f0276cf-4e80-7bc6-b833-a091883c1e68' AS relacionamento, COUNT(*) AS orfaos_nao_nulos
 FROM workspace.gold.fato_previsao f LEFT ANTI JOIN workspace.gold.dim_calendario d ON f.competencia_data = d.data
 WHERE f.competencia_data IS NOT NULL;
SELECT 'fato_previsao.competencia_data' AS coluna, COUNT(*) AS nulos FROM workspace.gold.fato_previsao WHERE competencia_data IS NULL;

-- Integridade eefc7d39-b405-b354-72e6-c555cb0036a4: órfãos e chaves nulas em separado.
SELECT 'eefc7d39-b405-b354-72e6-c555cb0036a4' AS relacionamento, COUNT(*) AS orfaos_nao_nulos
 FROM workspace.gold.vw_dre_comparativo f LEFT ANTI JOIN workspace.gold.dim_calendario d ON f.competencia = d.data
 WHERE f.competencia IS NOT NULL;
SELECT 'vw_dre_comparativo.competencia' AS coluna, COUNT(*) AS nulos FROM workspace.gold.vw_dre_comparativo WHERE competencia IS NULL;

-- Integridade dd8569c8-c610-4c02-d15c-c2afbea55cd5: órfãos e chaves nulas em separado.
SELECT 'dd8569c8-c610-4c02-d15c-c2afbea55cd5' AS relacionamento, COUNT(*) AS orfaos_nao_nulos
 FROM workspace.gold.fato_lancamentos f LEFT ANTI JOIN workspace.gold.dim_conta d ON f.planocontas_id = d.id_conta
 WHERE f.planocontas_id IS NOT NULL;
SELECT 'fato_lancamentos.planocontas_id' AS coluna, COUNT(*) AS nulos FROM workspace.gold.fato_lancamentos WHERE planocontas_id IS NULL;

-- Integridade 66e23276-0813-1463-b459-e591093be04e: órfãos e chaves nulas em separado.
SELECT '66e23276-0813-1463-b459-e591093be04e' AS relacionamento, COUNT(*) AS orfaos_nao_nulos
 FROM workspace.gold.fato_orcamento f LEFT ANTI JOIN workspace.gold.dim_conta d ON f.planocontas_id = d.id_conta
 WHERE f.planocontas_id IS NOT NULL;
SELECT 'fato_orcamento.planocontas_id' AS coluna, COUNT(*) AS nulos FROM workspace.gold.fato_orcamento WHERE planocontas_id IS NULL;

-- Integridade 855510f8-a1e3-1f4c-4426-15e7304a95d0: órfãos e chaves nulas em separado.
SELECT '855510f8-a1e3-1f4c-4426-15e7304a95d0' AS relacionamento, COUNT(*) AS orfaos_nao_nulos
 FROM workspace.gold.fato_previsao f LEFT ANTI JOIN workspace.gold.dim_conta d ON f.planocontas_id = d.id_conta
 WHERE f.planocontas_id IS NOT NULL;
SELECT 'fato_previsao.planocontas_id' AS coluna, COUNT(*) AS nulos FROM workspace.gold.fato_previsao WHERE planocontas_id IS NULL;

-- Coerência de filial da conta versus filial do lançamento; requer chave conta validada antes.
SELECT COUNT(*) AS divergencias FROM workspace.gold.fato_lancamentos f JOIN workspace.gold.dim_conta d
 ON f.planocontas_id = d.id_conta WHERE NOT (f.cod_filial <=> d.cod_filial);
SELECT cod_filial, MIN(competencia_data) AS inicio, MAX(competencia_data) AS fim,
 COUNT(DISTINCT competencia_data) AS competencias, COUNT(*) AS linhas,
 SUM(CASE WHEN valor IS NULL THEN 1 ELSE 0 END) AS valores_nulos,
 SUM(CASE WHEN competencia_data != date_trunc('MONTH', competencia_data) THEN 1 ELSE 0 END) AS fora_inicio_mes,
 SUM(CASE WHEN competencia_data != date_trunc('DAY', competencia_data) THEN 1 ELSE 0 END) AS com_hora
 FROM workspace.gold.fato_lancamentos GROUP BY cod_filial;

-- Coerência de filial da conta versus filial do lançamento; requer chave conta validada antes.
SELECT COUNT(*) AS divergencias FROM workspace.gold.fato_orcamento f JOIN workspace.gold.dim_conta d
 ON f.planocontas_id = d.id_conta WHERE NOT (f.cod_filial <=> d.cod_filial);
SELECT cod_filial, MIN(competencia_data) AS inicio, MAX(competencia_data) AS fim,
 COUNT(DISTINCT competencia_data) AS competencias, COUNT(*) AS linhas,
 SUM(CASE WHEN valor IS NULL THEN 1 ELSE 0 END) AS valores_nulos,
 SUM(CASE WHEN competencia_data != date_trunc('MONTH', competencia_data) THEN 1 ELSE 0 END) AS fora_inicio_mes,
 SUM(CASE WHEN competencia_data != date_trunc('DAY', competencia_data) THEN 1 ELSE 0 END) AS com_hora
 FROM workspace.gold.fato_orcamento GROUP BY cod_filial;

-- Coerência de filial da conta versus filial do lançamento; requer chave conta validada antes.
SELECT COUNT(*) AS divergencias FROM workspace.gold.fato_previsao f JOIN workspace.gold.dim_conta d
 ON f.planocontas_id = d.id_conta WHERE NOT (f.cod_filial <=> d.cod_filial);
SELECT cod_filial, MIN(competencia_data) AS inicio, MAX(competencia_data) AS fim,
 COUNT(DISTINCT competencia_data) AS competencias, COUNT(*) AS linhas,
 SUM(CASE WHEN valor IS NULL THEN 1 ELSE 0 END) AS valores_nulos,
 SUM(CASE WHEN competencia_data != date_trunc('MONTH', competencia_data) THEN 1 ELSE 0 END) AS fora_inicio_mes,
 SUM(CASE WHEN competencia_data != date_trunc('DAY', competencia_data) THEN 1 ELSE 0 END) AS com_hora
 FROM workspace.gold.fato_previsao GROUP BY cod_filial;

-- Calendário: continuidade diária, hora e cobertura. Duplicados/NULL já testados acima.
SELECT MIN(data) AS inicio, MAX(data) AS fim, COUNT(DISTINCT CAST(data AS DATE)) AS dias,
 DATEDIFF(MAX(data), MIN(data)) + 1 AS dias_esperados,
 SUM(CASE WHEN data != date_trunc('DAY', data) THEN 1 ELSE 0 END) AS com_hora
 FROM workspace.gold.dim_calendario;
-- Ordenação ano_mes: uma única chave por rótulo.
SELECT ano_mes, COUNT(DISTINCT numero_ano_mes) AS chaves FROM workspace.gold.dim_calendario
 GROUP BY ano_mes HAVING COUNT(DISTINCT numero_ano_mes) != 1;
-- Grão da view e coerência da descrição/subtotal para cada ordem.
SELECT cod_filial, competencia, ordem_dre, COUNT(*) AS n FROM workspace.gold.vw_dre_comparativo
 GROUP BY cod_filial, competencia, ordem_dre HAVING COUNT(*) > 1;
SELECT ordem_dre, COUNT(DISTINCT descricao_dre) AS descricoes, COUNT(DISTINCT subtotal) AS marcacoes
 FROM workspace.gold.vw_dre_comparativo GROUP BY ordem_dre;
SELECT cod_filial, competencia, COUNT(DISTINCT ordem_dre) AS ordens
 FROM workspace.gold.vw_dre_comparativo GROUP BY cod_filial, competencia
 HAVING COUNT(DISTINCT ordem_dre) != 13;
-- Posição da DRE contra dimensão por filial/ordem; validar unicidade antes de qualquer join de valores.
SELECT v.cod_filial, v.ordem_dre, COUNT(*) AS n FROM workspace.gold.vw_dre_comparativo v
 LEFT ANTI JOIN workspace.gold.dim_dre d ON v.cod_filial=d.cod_filial AND v.ordem_dre=d.ordem_dre
 GROUP BY v.cod_filial, v.ordem_dre;
-- Disponibilidade de cada cenário e NULL por competência/filial na linha 13.
SELECT cod_filial, competencia, COUNT(*) AS linhas,
 COUNT(realizado) AS realizado_preenchido, COUNT(orcado) AS orcado_preenchido, COUNT(previsto) AS previsto_preenchido
 FROM workspace.gold.vw_dre_comparativo WHERE ordem_dre=13 GROUP BY cod_filial, competencia ORDER BY cod_filial, competencia;
-- Controles integrais: não usar este recorte para comparar cenários como períodos equivalentes.
SELECT SUM(realizado) AS realizado, SUM(orcado) AS orcado, SUM(previsto) AS previsto
 FROM workspace.gold.vw_dre_comparativo WHERE ordem_dre = 13;
-- Mesmo controle por filial; somar filiais deve reconciliar o consolidado.
SELECT cod_filial, SUM(realizado) AS realizado, SUM(orcado) AS orcado, SUM(previsto) AS previsto
 FROM workspace.gold.vw_dre_comparativo WHERE ordem_dre = 13 GROUP BY cod_filial;
-- Comparação equivalente 2023, condicionado à comprovação da cobertura janeiro-maio por filial.
SELECT cod_filial, SUM(realizado) AS realizado, SUM(orcado) AS orcado, SUM(previsto) AS previsto
 FROM workspace.gold.vw_dre_comparativo WHERE ordem_dre=13
 AND competencia >= DATE '2023-01-01' AND competencia < DATE '2023-06-01' GROUP BY cod_filial;

