-- Somente leitura. NÃO EXECUTADO nesta entrega.
-- Grade real de três filiais e competências do calendário: contagens, não certificado de carga.
-- COALESCE abaixo é restrito a CONTAGENS diagnósticas, nunca a valores financeiros.
WITH meses AS (
 SELECT DISTINCT CAST(inicio_mes AS DATE) AS competencia
 FROM workspace.gold.dim_calendario
), filiais AS (
 SELECT cod_filial, filial FROM workspace.gold.dim_filial
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
SELECT d.cod_filial, d.filial, m.competencia,
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
