-- Somente SELECT. NÃO EXECUTADO nesta entrega. Exportar resultado completo sem arredondar valores.
-- Usar a mesma atualização de dados do modelo Power BI; não comparar estados diferentes.
WITH periodos(periodo,inicio,fim) AS (VALUES
('Integral',DATE '2021-01-01',DATE '2024-01-01'),
('2021',DATE '2021-01-01',DATE '2022-01-01'),
('2022',DATE '2022-01-01',DATE '2023-01-01'),
('2023',DATE '2023-01-01',DATE '2024-01-01'),
('2023_JanMai',DATE '2023-01-01',DATE '2023-06-01'),
('2023_JunDez',DATE '2023-06-01',DATE '2024-01-01'),
('2023_Junho',DATE '2023-06-01',DATE '2023-07-01')),
grupos(grupo_filial) AS (VALUES ('Consolidado'),('01'),('02'),('03'),('01+02')),
posicoes(posicao) AS (VALUES (1),(2),(3),(4),(5),(6),(7),(9),(10),(12),(13)),
cenarios(cenario) AS (VALUES ('Realizado'),('Orçado'),('Previsto'))
SELECT g.grupo_filial,p.periodo,o.posicao,c.cenario,
 COUNT(v.ordem_dre) AS linhas_fonte,
 SUM(CASE c.cenario WHEN 'Realizado' THEN v.realizado WHEN 'Orçado' THEN v.orcado ELSE v.previsto END) AS valor,
 COUNT(CASE c.cenario WHEN 'Realizado' THEN v.realizado WHEN 'Orçado' THEN v.orcado ELSE v.previsto END) AS valores_presentes
FROM grupos g CROSS JOIN periodos p CROSS JOIN posicoes o CROSS JOIN cenarios c
LEFT JOIN workspace.gold.vw_dre_comparativo v
 ON v.ordem_dre=o.posicao AND v.competencia>=p.inicio AND v.competencia<p.fim
 AND (g.grupo_filial='Consolidado' OR v.cod_filial=g.grupo_filial OR (g.grupo_filial='01+02' AND v.cod_filial IN ('01','02')))
GROUP BY g.grupo_filial,p.periodo,o.posicao,c.cenario
ORDER BY g.grupo_filial,p.periodo,o.posicao,c.cenario;
