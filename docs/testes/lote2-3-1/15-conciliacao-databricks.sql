-- Primeiro resultado: preflight de grão; zero linhas esperado. Não conciliar se retornar duplicações.
SELECT cod_filial,competencia,ordem_dre,count(*) quantidade
FROM workspace.gold.vw_dre_comparativo
GROUP BY cod_filial,competencia,ordem_dre HAVING count(*)<>1;

-- SOMENTE SELECT; não executado pelo agente. Contrato didático DIDATICA-1.0-20261103.
-- Exportar CSV completo; comparar mesma atualização do modelo. Não certifica fechamento.
WITH cobertura(cod_filial,inicio,fim) AS (VALUES
 ('01',DATE '2021-01-01',DATE '2023-05-01'),
 ('02',DATE '2021-01-01',DATE '2023-05-01'),
 ('03',DATE '2021-01-01',DATE '2023-05-01')),
meses AS (SELECT explode(sequence(DATE '2021-01-01',DATE '2023-12-01',INTERVAL 1 MONTH)) competencia),
grupos(grupo_filial) AS (VALUES ('01'),('02'),('03'),('Consolidado'),('01+02')),
periodos(periodo) AS (VALUES ('Integral'),('2021'),('2022'),('2023'),('2023_JanMai'),('2023_JunDez'),('2023_Maio'),('2023_Junho'),('2023_JanMar')),
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
 WHEN '2023_JanMar' THEN year(m.competencia)=2023 AND month(m.competencia) IN (1,3) ELSE false END
), contagens AS (
 SELECT g.grupo_filial,p.periodo,count(a.cod_filial) esperados
 FROM grupos g CROSS JOIN periodos p LEFT JOIN pares a ON a.grupo_filial=g.grupo_filial AND a.periodo=p.periodo
 GROUP BY g.grupo_filial,p.periodo
), dados AS (
 SELECT a.*,v.ordem_dre,v.realizado,v.orcado,v.previsto
 FROM pares a LEFT JOIN workspace.gold.vw_dre_comparativo v
 ON v.cod_filial=a.cod_filial AND v.competencia=a.competencia
)
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
ORDER BY g.grupo_filial,p.periodo,o.posicao,s.cenario;
-- Esperadas 1.755 linhas. Verificar grão único da view antes de aceitar contagens/somas.
-- Intervalos das três filiais são iguais neste contrato. SQL não generaliza cortes distintos;
-- testes de configuração alterada/lacunas são sintéticos separados e não editam produção.
