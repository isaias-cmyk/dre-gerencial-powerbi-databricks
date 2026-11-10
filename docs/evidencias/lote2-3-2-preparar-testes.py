"""Prepara consultas futuras/documentais; não executa DAX/SQL nem altera produção."""
from pathlib import Path
import ast,json,re
root=Path(__file__).resolve().parents[2]
out=root/'docs/testes/lote2-3-2'; out.mkdir(exist_ok=True)
# Reutilizar os contextos do gerador anterior sem importar/executar seu módulo.
tree=ast.parse((root/'docs/evidencias/lote2-3-1-gerar-testes.py').read_text(encoding='utf-8'))
vals={}
for node in tree.body:
    if isinstance(node,ast.Assign) and isinstance(node.value,ast.Constant):
        for t in node.targets:
            if isinstance(t,ast.Name):vals[t.id]=node.value.value
groups,periods,df,bf=[vals[k] for k in ('groups','periods','datefilter','branchfilter')]
months=[f'{y}-{m:02d}' for y in (2021,2022,2023) for m in range(1,13)]
monthly='DATATABLE ( "Periodo", STRING, { '+', '.join('{"M'+m+'"}' for m in months)+' } )'
monthly_df="FILTER ( ALL ( 'dim_calendario'[data] ), FORMAT ( 'dim_calendario'[data], \"yyyy-MM\" ) = RIGHT ( _Periodo, 7 ) )"
specs=[('M40','DRE | Desvio Realizado x Orçado (R$)','Orçado',False),
       ('M41','DRE | Desvio Realizado x Orçado (%)','Orçado',True),
       ('M42','DRE | Desvio Realizado x Previsto (R$)','Previsto',False),
       ('M43','DRE | Desvio Realizado x Previsto (%)','Previsto',True)]
def matrix(periods,dates):
    rows=[]
    for ident,name,scenario,pct in specs:
        ref='_O' if scenario=='Orçado' else '_P'
        formula=f'DIVIDE ( _R - {ref}, ABS ( {ref} ) )' if pct else f'_R - {ref}'
        guard=f'ISBLANK ( _R ) || ISBLANK ( {ref} )'+(f' || {ref} = 0' if pct else '')
        rows.append(f'''ROW ( "ID", "{ident}", "Medida", "{name}", "Unidade", "{'Razao' if pct else 'BRL'}",
 "Valor", [{name}], "Esperado", IF ( {guard}, BLANK (), {formula} ),
 "RealizadoComparavel", _R, "ReferenciaComparavel", {ref},
 "Pares", [DRE | Pares Filial-Competência Comparáveis], "StatusCobertura", [DRE | Status Comparabilidade] )''')
    return '''-- PLANEJADO/NAO EXECUTADO. Rodar SOMENTE após implementar M40–M43.
-- Não DEFINE MEASURE: não implementa medidas nem altera o modelo.
-- Esperado algébrico usa comparáveis do modelo; SQL é a conciliação financeira independente.
DEFINE VAR _Contextos = CROSSJOIN ( '''+groups+', '+periods+''', GENERATESERIES ( 1, 13 ) )
EVALUATE ADDCOLUMNS ( GENERATE ( _Contextos,
 VAR _Grupo=[Grupo] VAR _Periodo=[Periodo] VAR _Posicao=[Value]
 RETURN CALCULATETABLE (
 VAR _R=[DRE | Realizado Comparável] VAR _O=[DRE | Orçado Comparável] VAR _P=[DRE | Previsto Comparável]
 RETURN UNION ( '''+',\n'.join(rows)+' ),\n'+bf+',\n'+dates+''',
 TREATAS ( { _Posicao }, 'vw_dre_comparativo'[ordem_dre] ) ) ),
 "BlankDivergente", ISBLANK([Valor]) <> ISBLANK([Esperado]),
 "Diferenca", IF ( NOT ISBLANK([Valor]) && NOT ISBLANK([Esperado]), [Valor]-[Esperado] ),
 "Aprovado", IF ( ISBLANK([Valor]) || ISBLANK([Esperado]), ISBLANK([Valor]) && ISBLANK([Esperado]), ABS([Valor]-[Esperado]) <= IF([Unidade]="BRL",0.01,0.00000001) ) )
ORDER BY [Grupo],[Periodo],[Value],[ID]
'''
(out/'01-matriz-desvios-planejada.dax').write_text(matrix(periods,df),encoding='utf-8')
(out/'02-mensal-desvios-planejada.dax').write_text(matrix(monthly,monthly_df),encoding='utf-8')
cases=[('positivo',120,100,20,.2),('negativo',80,100,-20,-.2),('igual',100,100,0,0),
 ('referencia_negativa_desvio_negativo',-120,-100,-20,-.2),('referencia_negativa_desvio_positivo',-80,-100,20,.2),
 ('resultado_negativo_menos_negativo',-20,-100,80,.8),('realizado_zero',0,100,-100,-1),
 ('zero_com_referencia_negativa',0,-100,100,1),('referencia_zero',20,0,20,None),('ambos_zero',0,0,0,None),
 ('realizado_blank',None,100,None,None),('referencia_blank',100,None,None,None),('ambos_blank',None,None,None,None),
 ('mudanca_sinal_positiva',100,-100,200,2),('mudanca_sinal_negativa',-100,100,-200,-2)]
literal=lambda x:'BLANK ()' if x is None else str(x)
rows=',\n'.join('{ "'+n+'", '+', '.join(literal(x) for x in (r,x,d,p))+' }' for n,r,x,d,p in cases)
synthetic='''-- SINTETICO PLANEJADO, NÃO EXECUTADO. Verifica contrato algébrico; não valida medidas persistidas.
DEFINE VAR _Casos = DATATABLE ( "Caso", STRING, "R", DOUBLE, "X", DOUBLE, "DeltaEsperado", DOUBLE, "PercentualEsperado", DOUBLE,
 { '''+rows+''' } )
EVALUATE
ADDCOLUMNS ( ADDCOLUMNS ( _Casos,
 "DeltaCalculado", IF ( ISBLANK([R]) || ISBLANK([X]), BLANK(), [R]-[X] ),
 "PercentualCalculado", IF ( ISBLANK([R]) || ISBLANK([X]) || [X]=0, BLANK(), DIVIDE([R]-[X],ABS([X])) ) ),
 "DeltaAprovado", IF ( ISBLANK([DeltaCalculado]) || ISBLANK([DeltaEsperado]), ISBLANK([DeltaCalculado]) && ISBLANK([DeltaEsperado]), ABS([DeltaCalculado]-[DeltaEsperado])<=0.01 ),
 "PercentualAprovado", IF ( ISBLANK([PercentualCalculado]) || ISBLANK([PercentualEsperado]), ISBLANK([PercentualCalculado]) && ISBLANK([PercentualEsperado]), ABS([PercentualCalculado]-[PercentualEsperado])<=0.00000001 ) )
'''
(out/'03-sinteticos-contrato-planejados.dax').write_text(synthetic,encoding='utf-8')
guardrows=[]
for case,filters in [('Total entre posicoes',''),('Datas parciais',"DATESBETWEEN('dim_calendario'[data],DATE(2023,5,2),DATE(2023,5,31)), TREATAS({13},'vw_dre_comparativo'[ordem_dre])"),('Posicao descricao conflitantes',"TREATAS({1},'vw_dre_comparativo'[ordem_dre]), TREATAS({\"descricao_inexistente_teste\"},'vw_dre_comparativo'[descricao_dre])")]:
    row='ROW ( "Caso", "'+case+'", '+', '.join('"'+ident+'", ['+name+']' for ident,name,_,_ in specs)+' )'
    guardrows.append('CALCULATETABLE ( '+row+', '+filters+' )' if filters else row)
(out/'04-guardas-desvios-planejadas.dax').write_text('-- PLANEJADO. Após implementação: todos os quatro números devem ser BLANK.\nEVALUATE UNION ( '+',\n'.join(guardrows)+' )\n',encoding='utf-8')

source=(root/'docs/testes/lote2-3-1/15-conciliacao-databricks.sql').read_text(encoding='utf-8')
preflight=source[:source.index('-- SOMENTE SELECT')]
body=source[source.index('WITH cobertura'):source.index(';\n-- Esperadas')]
at=body.index('\nSELECT g.grupo_filial,p.periodo,o.posicao,s.cenario,')
base=body[:at]+', comparaveis AS (\n'+body[at:body.index('\nORDER BY',at)]+'''\n), referencias AS (
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
 CASE WHEN r IS NULL OR x IS NULL THEN NULL
 WHEN unidade='BRL' THEN r-x
 WHEN x=0 THEN NULL ELSE (r-x)/abs(x) END valor
FROM operandos ORDER BY grupo_filial,periodo,posicao,id;
'''
notice='-- PLANEJADO/NAO EXECUTADO. Apenas SELECT, contrato didático; não certifica fechamento.\n-- Reutiliza o SQL independente homologado de L2.3.1. Datas somente na CTE de configuração.\n'
(out/'05-desvios-databricks-planejados.sql').write_text(notice+'-- Segunda saída esperada: 2.340 linhas.\n'+preflight+base,encoding='utf-8')
# Mesma máscara e regras, com 36 competências individuais explicitamente selecionadas.
monthlysql=base.replace("periodos(periodo) AS (VALUES ('Integral'),('2021'),('2022'),('2023'),('2023_JanMai'),('2023_JunDez'),('2023_Maio'),('2023_Junho'),('2023_JanMar'))",'periodos(periodo) AS (VALUES '+','.join("('M"+m+"')" for m in months)+')')
monthlysql=monthlysql.replace('ELSE false END',"ELSE p.periodo=concat('M',date_format(m.competencia,'yyyy-MM')) END")
assert monthlysql!=base and 'M2021-01' in monthlysql and 'M2023-12' in monthlysql
(out/'06-mensal-databricks-planejado.sql').write_text(notice+'-- Segunda saída esperada: 9.360 linhas.\n'+preflight+monthlysql,encoding='utf-8')
sqlrows=',\n'.join("('"+n+"', "+', '.join('CAST(NULL AS DOUBLE)' if v is None else str(v) for v in (r,x,d,p))+')' for n,r,x,d,p in cases)
sqlsynthetic='''-- SINTETICO PLANEJADO/NAO EXECUTADO. Sem tabelas de produção, não é evidência financeira independente.
WITH casos(caso,r,x,delta_esperado,percentual_esperado) AS (VALUES
'''+sqlrows+'''), calculos AS (
 SELECT *,CASE WHEN r IS NULL OR x IS NULL THEN NULL ELSE r-x END delta_calculado,
 CASE WHEN r IS NULL OR x IS NULL OR x=0 THEN NULL ELSE (r-x)/abs(x) END percentual_calculado
 FROM casos
)
SELECT *, CASE WHEN delta_calculado IS NULL OR delta_esperado IS NULL THEN delta_calculado IS NULL AND delta_esperado IS NULL ELSE abs(delta_calculado-delta_esperado)<=0.01 END delta_aprovado,
 CASE WHEN percentual_calculado IS NULL OR percentual_esperado IS NULL THEN percentual_calculado IS NULL AND percentual_esperado IS NULL ELSE abs(percentual_calculado-percentual_esperado)<=0.00000001 END percentual_aprovado
FROM calculos ORDER BY caso;
'''
(out/'07-sinteticos-contrato-planejados.sql').write_text(sqlsynthetic,encoding='utf-8')
registry={'estado':'PLANEJADO_NAO_EXECUTADO','contextos_agregados':45,'posicoes':13,'medidas_novas_previstas':4,'casos_agregados_previstos':2340,'contextos_mensais':180,'casos_mensais_previstos':9360,'casos_sinteticos':15,'guardas':3,'regressao':'Reutilizar scripts 09/14/16/17/18/19 do L2.3.1 e comparar a baseline aceita; 41 expressões devem ficar idênticas','origens_reutilizadas':['docs/evidencias/lote2-3-1-gerar-testes.py','docs/testes/lote2-3-1/15-conciliacao-databricks.sql'],'consultas_executadas':0}
(root/'docs/evidencias/lote2-3-2-planejamento-20261103/testes-previstos.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(registry,ensure_ascii=False))
