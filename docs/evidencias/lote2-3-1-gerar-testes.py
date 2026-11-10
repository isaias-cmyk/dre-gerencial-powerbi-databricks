from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[2]
tests=root/'docs/testes/lote2-3-1'
groups='DATATABLE ( "Grupo", STRING, { {"01"}, {"02"}, {"03"}, {"Consolidado"}, {"01+02"} } )'
periods='DATATABLE ( "Periodo", STRING, { {"Integral"}, {"2021"}, {"2022"}, {"2023"}, {"2023_JanMai"}, {"2023_JunDez"}, {"2023_Maio"}, {"2023_Junho"}, {"2023_JanMar"} } )'
datefilter='''FILTER ( ALL ( 'dim_calendario'[data] ),
    SWITCH ( _Periodo,
        "Integral", TRUE (), "2021", YEAR ( 'dim_calendario'[data] ) = 2021,
        "2022", YEAR ( 'dim_calendario'[data] ) = 2022,
        "2023", YEAR ( 'dim_calendario'[data] ) = 2023,
        "2023_JanMai", YEAR ( 'dim_calendario'[data] ) = 2023 && MONTH ( 'dim_calendario'[data] ) <= 5,
        "2023_JunDez", YEAR ( 'dim_calendario'[data] ) = 2023 && MONTH ( 'dim_calendario'[data] ) >= 6,
        "2023_Maio", YEAR ( 'dim_calendario'[data] ) = 2023 && MONTH ( 'dim_calendario'[data] ) = 5,
        "2023_Junho", YEAR ( 'dim_calendario'[data] ) = 2023 && MONTH ( 'dim_calendario'[data] ) = 6,
        "2023_JanMar", YEAR ( 'dim_calendario'[data] ) = 2023 && MONTH ( 'dim_calendario'[data] ) IN { 1, 3 }, FALSE () ) )'''
branchfilter='''FILTER ( ALL ( 'dim_filial'[cod_filial] ), _Grupo = "Consolidado" || 'dim_filial'[cod_filial] = _Grupo || ( _Grupo = "01+02" && 'dim_filial'[cod_filial] IN { "01", "02" } ) )'''
positionfilter="TREATAS ( { _Posicao }, 'vw_dre_comparativo'[ordem_dre] )"
header='-- Teste somente leitura; datas constantes aqui representam o contrato de teste independente.\n'
test=header+f'''DEFINE
 VAR _Contextos = CROSSJOIN ( {groups}, {periods}, GENERATESERIES ( 1, 13 ) )
EVALUATE
GENERATE ( _Contextos,
 VAR _Grupo = [Grupo] VAR _Periodo = [Periodo] VAR _Posicao = [Value]
 RETURN CALCULATETABLE (
'''
rows=[]
for scen,col in [('Realizado','realizado'),('Orçado','orcado'),('Previsto','previsto')]:
    rows.append(f'''ROW ( "Cenario", "{scen}", "Valor", [DRE | {scen} Comparável],
    "Esperado", IF ( NOT ( _Posicao IN {{ 8, 11 }} ), CALCULATE ( SUM ( 'vw_dre_comparativo'[{col}] ), KEEPFILTERS ( 'vw_dre_comparativo'[competencia] <= DATE ( 2023, 5, 1 ) ) ) ),
    "Pares", [DRE | Pares Filial-Competência Comparáveis], "Status", [DRE | Status Comparabilidade] )''')
test+=' UNION ( '+',\n'.join(rows)+' ),\n'+branchfilter+',\n'+datefilter+',\n'+positionfilter+' ) )\n'
# Uma segunda EVALUATE não é necessária: acrescentar veredito via ADDCOLUMNS.
test=test.replace('EVALUATE\nGENERATE','EVALUATE\nADDCOLUMNS ( GENERATE')
test+=''', "AmbosBlank", ISBLANK ( [Valor] ) && ISBLANK ( [Esperado] ),
 "BlankDivergente", ISBLANK ( [Valor] ) <> ISBLANK ( [Esperado] ),
 "Diferenca", IF ( NOT ISBLANK ( [Valor] ) && NOT ISBLANK ( [Esperado] ), [Valor] - [Esperado] ),
 "Aprovado", IF ( ISBLANK ( [Valor] ) || ISBLANK ( [Esperado] ), ISBLANK ( [Valor] ) && ISBLANK ( [Esperado] ), ABS ( [Valor] - [Esperado] ) <= 0.01 ) )
ORDER BY [Grupo], [Periodo], [Value], [Cenario]
'''
(tests/'09-matriz-comparabilidade.dax').write_text(test,encoding='utf-8')
integrity='''-- Consultas somente leitura; não atualizam nem salvam o modelo.
EVALUATE '_ConfigCobertura'
EVALUATE INFO.VIEW.MEASURES()
EVALUATE INFO.VIEW.RELATIONSHIPS()
EVALUATE INFO.VIEW.TABLES()
'''
(tests/'10-configuracao-materializacao.dax').write_text(integrity,encoding='utf-8')
guards='''EVALUATE
UNION (
 CALCULATETABLE ( ROW ( "Caso", "Datas parciais", "Realizado", [DRE | Realizado Comparável], "Orcado", [DRE | Orçado Comparável], "Previsto", [DRE | Previsto Comparável], "Pares", [DRE | Pares Filial-Competência Comparáveis], "Status", [DRE | Status Comparabilidade] ), DATESBETWEEN ( 'dim_calendario'[data], DATE(2023,5,2), DATE(2023,5,31) ), TREATAS ( {13}, 'vw_dre_comparativo'[ordem_dre] ) ),
 ROW ( "Caso", "Total entre posicoes", "Realizado", [DRE | Realizado Comparável], "Orcado", [DRE | Orçado Comparável], "Previsto", [DRE | Previsto Comparável], "Pares", [DRE | Pares Filial-Competência Comparáveis], "Status", [DRE | Status Comparabilidade] ),
 CALCULATETABLE ( ROW ( "Caso", "Posicao descricao conflitantes", "Realizado", [DRE | Realizado Comparável], "Orcado", [DRE | Orçado Comparável], "Previsto", [DRE | Previsto Comparável], "Pares", [DRE | Pares Filial-Competência Comparáveis], "Status", [DRE | Status Comparabilidade] ), TREATAS({1}, 'vw_dre_comparativo'[ordem_dre]), TREATAS({"descricao_inexistente_teste"}, 'vw_dre_comparativo'[descricao_dre]) ) )
'''
(tests/'11-guardas-contexto.dax').write_text(guards,encoding='utf-8')
for num,rval in [(12,'0'),(13,'BLANK ()')]:
    synthetic=f'''-- SINTETICO: DEFINE MEASURE substitui bases somente nesta consulta, sem persistencia.
DEFINE
 MEASURE '_Medidas'[DRE | Realizado] = {rval}
 MEASURE '_Medidas'[DRE | Orçado] = -100
 MEASURE '_Medidas'[DRE | Previsto] = 0
EVALUATE
CALCULATETABLE ( ROW ( "Caso", "Sintetico R={rval}", "Realizado", [DRE | Realizado Comparável], "Orcado", [DRE | Orçado Comparável], "Previsto", [DRE | Previsto Comparável], "Pares", [DRE | Pares Filial-Competência Comparáveis], "Status", [DRE | Status Comparabilidade] ),
 TREATAS({{ "01" }}, 'dim_filial'[cod_filial]),
 DATESBETWEEN('dim_calendario'[data],DATE(2023,5,1),DATE(2023,5,31)),
 TREATAS({{13}},'vw_dre_comparativo'[ordem_dre]) )
'''
    (tests/f'{num}-sintetico-{"zero" if num==12 else "blank"}.dax').write_text(synthetic,encoding='utf-8')
# Regressão das 36 medidas persistidas: referência direta sobre a view, SEM corte comparável novo.
prep=json.loads((root/'docs/evidencias/lote2-3-1-implementacao-atual.json').read_text())
old=(Path(prep['backup'])/'restauracao-teste/DRE Moderno - Databricks.SemanticModel/definition/tables/_Medidas.tmdl').read_text(encoding='utf-8-sig')
names=re.findall(r"(?m)^\s*measure '([^']+)'",old)
mapping={'Receita Operacional Bruta':1,'Deduções da Receita':2,'Receita Operacional Líquida':3,'Custos':4,'Margem de Contribuição':5,'Despesas Operacionais':6,'Resultado Financeiro':7,'Depreciação e Amortização':9,'Outras Receitas e Despesas':10,'Provisão para IR e CSLL':12,'Resultado Líquido':13}
rows=[]
for name in names:
    pos=next((p for family,p in mapping.items() if family in name),13)
    col='realizado' if name.endswith('Realizado') else 'orcado' if name.endswith('Orçado') else 'previsto'
    rows.append(f'''CALCULATETABLE ( ROW ( "Medida", "{name}", "Valor", [{name}], "Esperado", SUM ( 'vw_dre_comparativo'[{col}] ) ), TREATAS ( {{ {pos} }}, 'vw_dre_comparativo'[ordem_dre] ) )''')
reg=header+f'''DEFINE VAR _Contextos = CROSSJOIN ( {groups}, {periods} )
EVALUATE ADDCOLUMNS ( GENERATE ( _Contextos,
 VAR _Grupo=[Grupo] VAR _Periodo=[Periodo]
 RETURN CALCULATETABLE ( UNION ( '''+',\n'.join(rows)+' ),\n'+branchfilter+',\n'+datefilter+''' ) ),
 "Aprovado", IF ( ISBLANK([Valor]) || ISBLANK([Esperado]), ISBLANK([Valor]) && ISBLANK([Esperado]), ABS([Valor]-[Esperado]) <= 0.01 ),
 "Diferenca", IF ( NOT ISBLANK([Valor]) && NOT ISBLANK([Esperado]), [Valor]-[Esperado] ) )
ORDER BY [Grupo],[Periodo],[Medida]
'''
(tests/'14-regressao-36-medidas.dax').write_text(reg,encoding='utf-8')

# SQL financeiro independente: configuração em CTE explícita do contrato, sem ler tabela Power BI.
sql='''-- SOMENTE SELECT; não executado pelo agente. Contrato didático DIDATICA-1.0-20261103.
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
), dados AS (
 SELECT a.*,v.ordem_dre,v.realizado,v.orcado,v.previsto
 FROM pares a LEFT JOIN workspace.gold.vw_dre_comparativo v
 ON v.cod_filial=a.cod_filial AND v.competencia=a.competencia
)
SELECT g.grupo_filial,p.periodo,o.posicao,s.cenario,
 count(d.cod_filial) pares,
 count(d.realizado) valores_realizado_presentes,
 count(CASE s.cenario WHEN 'Realizado' THEN d.realizado WHEN 'Orçado' THEN d.orcado ELSE d.previsto END) valores_cenario_presentes,
 CASE WHEN o.posicao NOT IN (8,11) AND count(d.cod_filial)>0
 AND count(d.realizado)=count(d.cod_filial)
 AND count(CASE s.cenario WHEN 'Realizado' THEN d.realizado WHEN 'Orçado' THEN d.orcado ELSE d.previsto END)=count(d.cod_filial)
 THEN sum(CASE s.cenario WHEN 'Realizado' THEN d.realizado WHEN 'Orçado' THEN d.orcado ELSE d.previsto END) END valor
FROM grupos g CROSS JOIN periodos p CROSS JOIN posicoes o CROSS JOIN cenarios s
LEFT JOIN dados d ON d.grupo_filial=g.grupo_filial AND d.periodo=p.periodo AND d.ordem_dre=o.posicao
GROUP BY g.grupo_filial,p.periodo,o.posicao,s.cenario
ORDER BY g.grupo_filial,p.periodo,o.posicao,s.cenario;
-- Esperadas 1.755 linhas. Verificar grão único da view antes de aceitar contagens/somas.
-- Intervalos das três filiais são iguais neste contrato. SQL não generaliza cortes distintos;
-- testes de configuração alterada/lacunas são sintéticos separados e não editam produção.
'''
(tests/'15-conciliacao-databricks.sql').write_text(sql,encoding='utf-8')
print('Criados 09–15; matriz 1755 verificações, regressão 1620; ainda não executados.')
