-- SINTETICO PLANEJADO/NAO EXECUTADO. Sem tabelas de produção, não é evidência financeira independente.
WITH casos(caso,r,x,delta_esperado,percentual_esperado) AS (VALUES
('positivo', 120, 100, 20, 0.2),
('negativo', 80, 100, -20, -0.2),
('igual', 100, 100, 0, 0),
('referencia_negativa_desvio_negativo', -120, -100, -20, -0.2),
('referencia_negativa_desvio_positivo', -80, -100, 20, 0.2),
('resultado_negativo_menos_negativo', -20, -100, 80, 0.8),
('realizado_zero', 0, 100, -100, -1),
('zero_com_referencia_negativa', 0, -100, 100, 1),
('referencia_zero', 20, 0, 20, CAST(NULL AS DOUBLE)),
('ambos_zero', 0, 0, 0, CAST(NULL AS DOUBLE)),
('realizado_blank', CAST(NULL AS DOUBLE), 100, CAST(NULL AS DOUBLE), CAST(NULL AS DOUBLE)),
('referencia_blank', 100, CAST(NULL AS DOUBLE), CAST(NULL AS DOUBLE), CAST(NULL AS DOUBLE)),
('ambos_blank', CAST(NULL AS DOUBLE), CAST(NULL AS DOUBLE), CAST(NULL AS DOUBLE), CAST(NULL AS DOUBLE)),
('mudanca_sinal_positiva', 100, -100, 200, 2),
('mudanca_sinal_negativa', -100, 100, -200, -2)), calculos AS (
 SELECT *,CASE WHEN r IS NULL OR x IS NULL THEN NULL ELSE r-x END delta_calculado,
 CASE WHEN r IS NULL OR x IS NULL OR x=0 THEN NULL ELSE (r-x)/abs(x) END percentual_calculado
 FROM casos
)
SELECT *, CASE WHEN delta_calculado IS NULL OR delta_esperado IS NULL THEN delta_calculado IS NULL AND delta_esperado IS NULL ELSE abs(delta_calculado-delta_esperado)<=0.01 END delta_aprovado,
 CASE WHEN percentual_calculado IS NULL OR percentual_esperado IS NULL THEN percentual_calculado IS NULL AND percentual_esperado IS NULL ELSE abs(percentual_calculado-percentual_esperado)<=0.00000001 END percentual_aprovado
FROM calculos ORDER BY caso;
