-- PLANEJADO/NAO EXECUTADO. Apenas SELECT, contrato didático; não certifica fechamento.
-- Reutiliza o SQL independente homologado de L2.3.1. Datas somente na CTE de configuração.
-- Segunda saída esperada: 9.360 linhas.
-- Primeiro resultado: preflight de grão; zero linhas esperado. Não conciliar se retornar duplicações.
SELECT cod_filial,competencia,ordem_dre,count(*) quantidade
FROM workspace.gold.vw_dre_comparativo
GROUP BY cod_filial,competencia,ordem_dre HAVING count(*)<>1;

WITH cobertura(cod_filial,inicio,fim) AS (VALUES
 ('01',DATE '2021-01-01',DATE '2023-05-01'),
 ('02',DATE '2021-01-01',DATE '2023-05-01'),
 ('03',DATE '2021-01-01',DATE '2023-05-01')),
meses AS (SELECT explode(sequence(DATE '2021-01-01',DATE '2023-12-01',INTERVAL 1 MONTH)) competencia),
grupos(grupo_filial) AS (VALUES ('01'),('02'),('03'),('Consolidado'),('01+02')),
periodos(periodo) AS (VALUES ('M2021-01'),('M2021-02'),('M2021-03'),('M2021-04'),('M2021-05'),('M2021-06'),('M2021-07'),('M2021-08'),('M2021-09'),('M2021-10'),('M2021-11'),('M2021-12'),('M2022-01'),('M2022-02'),('M2022-03'),('M2022-04'),('M2022-05'),('M2022-06'),('M2022-07'),('M2022-08'),('M2022-09'),('M2022-10'),('M2022-11'),('M2022-12'),('M2023-01'),('M2023-02'),('M2023-03'),('M2023-04'),('M2023-05'),('M2023-06'),('M2023-07'),('M2023-08'),('M2023-09'),('M2023-10'),('M2023-11'),('M2023-12')),
posicoes(posicao) AS (SELECT explode(sequence(1,13))),
cenarios(cenario) AS (VALUES ('Realizado'),('Orçado'),('Previsto')),
pares AS (
 SELECT g.grupo_filial,p.periodo,c.cod_filial,m.competencia
 FROM grupos g CROSS JOIN periodos p CROSS JOIN cobertura c CROSS JOIN meses m
 WHERE (g.grupo_filial='Consolidado' OR g.grupo_filial=c.cod_filial OR (g.grupo_filial='01+02' AND c.cod_filial IN ('01','02')))
 AND m.competencia BETWEEN c.inicio AND c.fim
 AND CASE p.periodo
 WHEN 'Integral' THEN true WHEN '2021' THEN year(m.competencia)=2021 WHEN '2022' THEN year(m.competencia)=2022
 WHEN '2023' THEN year(m.competencia)=2023
 WHEN '2023_JanMai' THEN year(m.competencia)=2023 AND month(m.competencia)<=5
 WHEN '2023_JunDez' THEN year(m.competencia)=2023 AND month(m.competencia)>=6
 WHEN '2023_Maio' THEN year(m.competencia)=2023 AND month(m.competencia)=5
 WHEN '2023_Junho' THEN year(m.competencia)=2023 AND month(m.competencia)=6
 WHEN '2023_JanMar' THEN year(m.competencia)=2023 AND month(m.competencia) IN (1,3) ELSE p.periodo=concat('M',date_format(m.competencia,'yyyy-MM')) END
), contagens AS (
 SELECT g.grupo_filial,p.periodo,count(a.cod_filial) esperados
 FROM grupos g CROSS JOIN periodos p LEFT JOIN pares a ON a.grupo_filial=g.grupo_filial AND a.periodo=p.periodo
 GROUP BY g.grupo_filial,p.periodo
), dados AS (
 SELECT a.*,v.ordem_dre,v.realizado,v.orcado,v.previsto
 FROM pares a LEFT JOIN workspace.gold.vw_dre_comparativo v
 ON v.cod_filial=a.cod_filial AND v.competencia=a.competencia
), comparaveis AS (

SELECT g.grupo_filial,p.periodo,o.posicao,s.cenario,
 CASE WHEN o.posicao NOT IN (8,11) THEN c.esperados END pares,
 count(d.cod_filial) linhas_view,
 count(d.realizado) valores_realizado_presentes,
 count(CASE s.cenario WHEN 'Realizado' THEN d.realizado WHEN 'Orçado' THEN d.orcado ELSE d.previsto END) valores_cenario_presentes,
 CASE WHEN o.posicao NOT IN (8,11) AND c.esperados>0 AND count(d.cod_filial)=c.esperados
 AND count(d.realizado)=c.esperados
 AND count(CASE s.cenario WHEN 'Realizado' THEN d.realizado WHEN 'Orçado' THEN d.orcado ELSE d.previsto END)=c.esperados
 THEN sum(CASE s.cenario WHEN 'Realizado' THEN d.realizado WHEN 'Orçado' THEN d.orcado ELSE d.previsto END) END valor
FROM grupos g CROSS JOIN periodos p CROSS JOIN posicoes o CROSS JOIN cenarios s
JOIN contagens c ON c.grupo_filial=g.grupo_filial AND c.periodo=p.periodo
LEFT JOIN dados d ON d.grupo_filial=g.grupo_filial AND d.periodo=p.periodo AND d.ordem_dre=o.posicao
GROUP BY g.grupo_filial,p.periodo,o.posicao,s.cenario,c.esperados
), referencias AS (
 SELECT grupo_filial,periodo,posicao,
 max(CASE WHEN cenario='Realizado' THEN valor END) r,
 max(CASE WHEN cenario='Orçado' THEN valor END) o,
 max(CASE WHEN cenario='Previsto' THEN valor END) p,
 max(pares) pares
 FROM comparaveis GROUP BY grupo_filial,periodo,posicao
), medidas(id,medida,unidade) AS (VALUES
 ('M40','DRE | Desvio Realizado x Orçado (R$)','BRL'),
 ('M41','DRE | Desvio Realizado x Orçado (%)','Razao'),
 ('M42','DRE | Desvio Realizado x Previsto (R$)','BRL'),
 ('M43','DRE | Desvio Realizado x Previsto (%)','Razao')),
operandos AS (
 SELECT a.*,m.id,m.medida,m.unidade,
 CASE WHEN m.id IN ('M40','M41') THEN a.o ELSE a.p END x
 FROM referencias a CROSS JOIN medidas m
)
SELECT grupo_filial,periodo,posicao,id,medida,unidade,pares,r realizado_comparavel,x referencia_comparavel,
 -- Correcao 04/11/2026: CAST DOUBLE evita DECIMAL(38,2), que arredondava as razoes M41/M43 a 2 casas.
 CASE WHEN r IS NULL OR x IS NULL THEN NULL
 WHEN unidade='BRL' THEN CAST(r-x AS DOUBLE)
 WHEN x=0 THEN NULL ELSE CAST(r-x AS DOUBLE)/abs(CAST(x AS DOUBLE)) END valor
FROM operandos ORDER BY grupo_filial,periodo,posicao,id;
