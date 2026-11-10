"""Completa os roteiros de F1 sem executar SQL/DAX nem alterar fontes de produção."""
from pathlib import Path
from datetime import datetime
import json, hashlib, csv

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/evidencias/fase1-dinamica'
OUT.mkdir(exist_ok=False)

def put(name, text):
    (OUT/name).write_text(text, encoding='utf-8')

def js(name, value):
    put(name,json.dumps(value,ensure_ascii=False,indent=2))

def h(p):
    return hashlib.sha256(p.read_bytes()).hexdigest().upper()

baseline=[]
for p in ROOT.rglob('*'):
    if p.is_file() and p.relative_to(ROOT).parts[0] not in ('docs','backups','.git'):
        baseline.append({'path':p.relative_to(ROOT).as_posix(),'sha256':h(p)})
js('baseline-protecao.json',baseline)
old=ROOT/'docs/evidencias/fase1'
js('reuso.json',[{'path':str((old/n).relative_to(ROOT)), 'sha256':h(old/n),'action':'Preservado; complementado sem duplicar a auditoria estática'} for n in ('roteiro-testes-nao-executados.sql','roteiro-testes-nao-executados.dax')])

header='// FASE 1. Consulta somente leitura, NÃO EXECUTADA neste ambiente. Não cria medidas.\n'
def dax(name, body): put(name,header+body.strip()+'\n')

dax('01-descoberta.dax',"""
EVALUATE
SELECTCOLUMNS('dim_filial', "Codigo", 'dim_filial'[cod_filial], "Filial", 'dim_filial'[filial])
ORDER BY [Filial]
""")
dax('02-relacionamentos.dax','EVALUATE INFO.VIEW.RELATIONSHIPS()')
dax('03-colunas.dax','EVALUATE INFO.VIEW.COLUMNS()')
put('02b-metadados-fallback.dmv',"""-- SOMENTE DAX Studio/SSMS em sessão já conectada; uma consulta por execução.
SELECT * FROM $SYSTEM.TMSCHEMA_RELATIONSHIPS;
SELECT * FROM $SYSTEM.TMSCHEMA_TABLES;
SELECT * FROM $SYSTEM.TMSCHEMA_COLUMNS;
-- Correlacionar TableID/ColumnID para ler endpoints e tipos. Não executar na DAX Query View.
""")

keys={'dim_filial':'cod_filial','dim_conta':'id_conta','dim_dre':'id_dre','dim_calendario':'data'}
rows=[]
for t,k in keys.items():
    blanks=f'ISBLANK(\'{t}\'[{k}])'
    if t!='dim_calendario': blanks+=f' || LEN(TRIM(\'{t}\'[{k}])) = 0'
    rows.append(f'''ROW("Teste", "Chave {t}.{k}",
 "Linhas", COUNTROWS(ALLNOBLANKROW('{t}')),
 "ChavesDistintas", COUNTROWS(DISTINCT(SELECTCOLUMNS(ALLNOBLANKROW('{t}'), "K", '{t}'[{k}]))),
 "ChavesAusentes", COUNTROWS(FILTER(ALLNOBLANKROW('{t}'), {blanks})))''')
dax('04-chaves-modelo.dax','EVALUATE\nUNION(\n'+',\n'.join(rows)+'\n)')
rels=json.loads((old/'relacionamentos.json').read_text(encoding='utf-8-sig'))
rows=[]
for r in rels:
    if r['technical']:continue
    ft,fc=r['from'].split('.'); tt,tc=r['to'].split('.')
    blanks=f'ISBLANK(\'{ft}\'[{fc}])'
    if r['fromType']=='string':blanks+=f' || LEN(TRIM(\'{ft}\'[{fc}])) = 0'
    rows.append(f'''ROW("Relacao", "{r['id']}",
 "NulosOuVazios", COUNTROWS(FILTER(ALLNOBLANKROW('{ft}'), {blanks})),
 "OrfaosNaoNulos", COUNTROWS(FILTER(ALLNOBLANKROW('{ft}'),
 NOT ISBLANK('{ft}'[{fc}]) && NOT ('{ft}'[{fc}] IN SELECTCOLUMNS(ALLNOBLANKROW('{tt}'), "K", '{tt}'[{tc}])))))''')
dax('05-integridade-modelo.dax','EVALUATE\nUNION(\n'+',\n'.join(rows)+'\n)')

periods='''VAR _Periodos = DATATABLE("Periodo", STRING, "InicioNumero", INTEGER, "FimNumero", INTEGER,
 { {"Integral",20210101,20240101}, {"2021",20210101,20220101},
   {"2022",20220101,20230101}, {"2023_JanMai",20230101,20230601}, {"2023_JunDez",20230601,20240101} })
VAR _Filiais = UNION(
 SELECTCOLUMNS(FILTER(ALLNOBLANKROW('dim_filial'), NOT ISBLANK('dim_filial'[cod_filial])),
 "Codigo",'dim_filial'[cod_filial],"Filial",'dim_filial'[filial],"Consolidado",FALSE()),
 ROW("Codigo",BLANK(),"Filial","Consolidado","Consolidado",TRUE()))
VAR _Casos = CROSSJOIN(_Filiais,_Periodos)'''
datevars='''VAR _Cod = [Codigo]
VAR _Todos = [Consolidado]
VAR _IniNum = [InicioNumero]
VAR _FimNum = [FimNumero]
VAR _Ini = DATE(INT(_IniNum/10000), MOD(INT(_IniNum/100),100), MOD(_IniNum,100))
VAR _Fim = DATE(INT(_FimNum/10000), MOD(INT(_FimNum/100),100), MOD(_FimNum,100))
VAR _Datas = FILTER(ALL('dim_calendario'), 'dim_calendario'[data]>=_Ini && 'dim_calendario'[data]<_Fim)
VAR _Filial = FILTER(ALL('dim_filial'), _Todos || 'dim_filial'[cod_filial]=_Cod)'''
facts=['fato_lancamentos','fato_orcamento','fato_previsao']
for t in facts+['vw_dre_comparativo']:
    dc='competencia' if t.startswith('vw_') else 'competencia_data'
    body=f'''EVALUATE
{periods}
RETURN GENERATE(_Casos,
 {datevars}
 VAR _ViaDimensoes = CALCULATETABLE('{t}', _Datas, _Filial)
 VAR _Direto = FILTER(ALL('{t}'), (_Todos || '{t}'[cod_filial]=_Cod)
    && '{t}'[{dc}]>=_Ini && '{t}'[{dc}]<_Fim)
 RETURN ROW("Tabela","{t}","LinhasViaDimensoes",COUNTROWS(_ViaDimensoes),
 "LinhasDiretas",COUNTROWS(_Direto),
 "Extras",COUNTROWS(EXCEPT(_ViaDimensoes,_Direto)),
 "Faltantes",COUNTROWS(EXCEPT(_Direto,_ViaDimensoes))))
ORDER BY [Filial],[Periodo]'''
    dax('06-filtros-'+t+'.dax',body)

# Soma financeira EXCLUSIVAMENTE na linha 13. Integral aqui usa todos os registros, sem corte temporal.
dax('07-controle-integral.dax',"""
EVALUATE
VAR _R = CALCULATE(SUM('vw_dre_comparativo'[realizado]), 'vw_dre_comparativo'[ordem_dre]=13)
VAR _O = CALCULATE(SUM('vw_dre_comparativo'[orcado]), 'vw_dre_comparativo'[ordem_dre]=13)
VAR _P = CALCULATE(SUM('vw_dre_comparativo'[previsto]), 'vw_dre_comparativo'[ordem_dre]=13)
RETURN ROW("OrdemDRE",13,"Realizado",_R,"Orcado",_O,"Previsto",_P,
 "DifRealizado",IF(NOT ISBLANK(_R),ROUND(_R,2)-5038227.39),
 "DifOrcado",IF(NOT ISBLANK(_O),ROUND(_O,2)-6622493.82),
 "DifPrevisto",IF(NOT ISBLANK(_P),ROUND(_P,2)-6157931.19),
 "DadosPresentes",NOT ISBLANK(_R) && NOT ISBLANK(_O) && NOT ISBLANK(_P))
""")
dax('08-linha13-filial-periodo.dax',f'''EVALUATE
{periods}
RETURN GENERATE(_Casos,
 {datevars}
 VAR _V = CALCULATETABLE('vw_dre_comparativo',_Datas,_Filial,'vw_dre_comparativo'[ordem_dre]=13)
 RETURN ROW("Realizado",SUMX(_V,'vw_dre_comparativo'[realizado]),
 "Orcado",SUMX(_V,'vw_dre_comparativo'[orcado]),"Previsto",SUMX(_V,'vw_dre_comparativo'[previsto]),
 "Linhas",COUNTROWS(_V),"RealizadosNaoNulos",COUNTROWS(FILTER(_V,NOT ISBLANK('vw_dre_comparativo'[realizado])))))
ORDER BY [Filial],[Periodo]''')
dax('09-linha13-filial-ano.dax',"""
EVALUATE
CALCULATETABLE(
 SUMMARIZECOLUMNS('dim_filial'[cod_filial],'dim_filial'[filial],'dim_calendario'[ano],
 "Realizado",SUM('vw_dre_comparativo'[realizado]),
 "Orcado",SUM('vw_dre_comparativo'[orcado]),"Previsto",SUM('vw_dre_comparativo'[previsto]),
 "Linhas",COUNTROWS('vw_dre_comparativo')),
 'vw_dre_comparativo'[ordem_dre]=13)
ORDER BY 'dim_filial'[filial],'dim_calendario'[ano]
""")
dax('10-descobrir-conta.dax',"""
EVALUATE
ADDCOLUMNS(SELECTCOLUMNS(ALLNOBLANKROW('dim_conta'),
 "Conta",'dim_conta'[id_conta],"DescricaoN1",'dim_conta'[descricaon1],
 "DescricaoN2",'dim_conta'[descricaon2],"DetalharN2",'dim_conta'[detalharn2]),
 "Lancamentos",VAR _K=[Conta] RETURN COUNTROWS(FILTER(ALL('fato_lancamentos'),'fato_lancamentos'[planocontas_id]=_K)),
 "Orcamento",VAR _K=[Conta] RETURN COUNTROWS(FILTER(ALL('fato_orcamento'),'fato_orcamento'[planocontas_id]=_K)),
 "Previsao",VAR _K=[Conta] RETURN COUNTROWS(FILTER(ALL('fato_previsao'),'fato_previsao'[planocontas_id]=_K)))
ORDER BY [Conta]
""")
rows=[]
for t in facts:
    rows.append(f'''ROW("Tabela","{t}",
 "Total",COUNTROWS(ALL('{t}')),
 "ViaConta",CALCULATE(COUNTROWS('{t}'),TREATAS({{_Conta}},'dim_conta'[id_conta])),
 "Direto",COUNTROWS(FILTER(ALL('{t}'),'{t}'[planocontas_id]=_Conta)),
 "Extras",COUNTROWS(EXCEPT(CALCULATETABLE('{t}',TREATAS({{_Conta}},'dim_conta'[id_conta])),FILTER(ALL('{t}'),'{t}'[planocontas_id]=_Conta))),
 "Faltantes",COUNTROWS(EXCEPT(FILTER(ALL('{t}'),'{t}'[planocontas_id]=_Conta),CALCULATETABLE('{t}',TREATAS({{_Conta}},'dim_conta'[id_conta])))))''')
rows.append('''ROW("Tabela","vw_dre_comparativo",
 "Total",COUNTROWS(ALL('vw_dre_comparativo')),
 "ViaConta",CALCULATE(COUNTROWS('vw_dre_comparativo'),TREATAS({_Conta},'dim_conta'[id_conta])),
 "Direto",COUNTROWS(ALL('vw_dre_comparativo')),
 "Extras",COUNTROWS(EXCEPT(CALCULATETABLE('vw_dre_comparativo',TREATAS({_Conta},'dim_conta'[id_conta])),ALL('vw_dre_comparativo'))),
 "Faltantes",COUNTROWS(EXCEPT(ALL('vw_dre_comparativo'),CALCULATETABLE('vw_dre_comparativo',TREATAS({_Conta},'dim_conta'[id_conta])))))''')
dax('11-filtro-conta.dax','''EVALUATE
VAR _Conta = "__ID_CONTA_ANALITICA__"
VAR _Valida = CONTAINS(ALLNOBLANKROW('dim_conta'),'dim_conta'[id_conta],_Conta)
RETURN ADDCOLUMNS(UNION(
'''+',\n'.join(rows)+'''),"ParametroValido",_Valida)
// Substituir somente o parâmetro pela conta analítica confirmada no teste 10.
// ParametroValido FALSE impede aceite; números vazios/zero não aprovam o teste.
''')
dax('12-filtro-dre.dax',"""
EVALUATE
VAR _UmaLinha = TOPN(1,FILTER(ALLNOBLANKROW('dim_dre'), 'dim_dre'[ordem_dre]=1),'dim_dre'[id_dre],ASC)
VAR _IDs = SELECTCOLUMNS(_UmaLinha,"K",'dim_dre'[id_dre])
VAR _ComDRE = CALCULATETABLE('vw_dre_comparativo',TREATAS(_IDs,'dim_dre'[id_dre]))
VAR _SemDRE = ALL('vw_dre_comparativo')
RETURN ROW("LinhasSelecionadasDimDRE",COUNTROWS(_UmaLinha),
 "LinhasViewAntes",COUNTROWS(_SemDRE),"LinhasViewDepois",COUNTROWS(_ComDRE),
 "Extras",COUNTROWS(EXCEPT(_ComDRE,_SemDRE)),"Faltantes",COUNTROWS(EXCEPT(_SemDRE,_ComDRE)),
 "LinhasViewPosicao1Direta",COUNTROWS(FILTER(_SemDRE,'vw_dre_comparativo'[ordem_dre]=1)))
// É necessário haver posição 1 e outras posições na view para a prova ser discriminante.
""")
dax('13-relacao-inativa.dax',"""
EVALUATE
GENERATE(SELECTCOLUMNS(ALLNOBLANKROW('dim_filial'),"Codigo",'dim_filial'[cod_filial],"Filial",'dim_filial'[filial]),
 VAR _Cod=[Codigo]
 VAR _ViaFilial=CALCULATETABLE('dim_conta',TREATAS({_Cod},'dim_filial'[cod_filial]))
 VAR _Todas=ALL('dim_conta')
 RETURN ROW("ContasTotal",COUNTROWS(_Todas),"ContasViaFilial",COUNTROWS(_ViaFilial),
 "ContasDaFilialDiretas",COUNTROWS(FILTER(_Todas,'dim_conta'[cod_filial]=_Cod)),
 "Extras",COUNTROWS(EXCEPT(_ViaFilial,_Todas)),"Faltantes",COUNTROWS(EXCEPT(_Todas,_ViaFilial))))
// Relação deve permanecer inativa em 02-relacionamentos. Nenhum USERELATIONSHIP é aplicado.
""")

# Referência SQL de mesma granularidade das consultas 06/08; resultados vazios aparecem como COUNT 0, SUM NULL.
sql="""-- COMPLEMENTO somente leitura aos roteiros originais. NÃO EXECUTADO.
-- Executar uma instrução por vez no Databricks SQL autenticado existente.
-- S00: catálogo real, sem inventar códigos de filial/conta.
SELECT cod_filial, filial FROM workspace.gold.dim_filial ORDER BY filial;
SELECT id_conta, descricaon1, descricaon2, detalharn2 FROM workspace.gold.dim_conta ORDER BY id_conta;
-- S01: células base de evidência para o modelo e a origem: linha 13 por filial/ano.
SELECT cod_filial, YEAR(competencia) AS ano, COUNT(*) AS linhas,
 SUM(realizado) AS realizado, SUM(orcado) AS orcado, SUM(previsto) AS previsto
FROM workspace.gold.vw_dre_comparativo WHERE ordem_dre=13
GROUP BY cod_filial,YEAR(competencia) ORDER BY cod_filial,ano;
-- S02: controle integral sem filtro temporal. NULL não deve ser aprovado como zero.
SELECT SUM(realizado) AS realizado,SUM(orcado) AS orcado,SUM(previsto) AS previsto,
 ROUND(SUM(realizado),2)-5038227.39 AS dif_realizado,
 ROUND(SUM(orcado),2)-6622493.82 AS dif_orcado,
 ROUND(SUM(previsto),2)-6157931.19 AS dif_previsto
FROM workspace.gold.vw_dre_comparativo WHERE ordem_dre=13;
"""
for t in facts+['vw_dre_comparativo']:
    date='competencia' if t.startswith('vw_') else 'competencia_data'
    aggregates='SUM(f.realizado) AS realizado,SUM(f.orcado) AS orcado,SUM(f.previsto) AS previsto,COUNT(f.realizado) AS realizados_nao_nulos' if t.startswith('vw_') else 'SUM(f.valor) AS valor'
    rowfilter=' AND f.ordem_dre=13' if t.startswith('vw_') else ''
    sql+=f"""
-- S03-{t}: matriz filial x período. Para view, valores financeiros somente linha 13.
WITH periodos AS (
 SELECT * FROM VALUES ('Integral',DATE '2021-01-01',DATE '2024-01-01'),
 ('2021',DATE '2021-01-01',DATE '2022-01-01'),('2022',DATE '2022-01-01',DATE '2023-01-01'),
 ('2023_JanMai',DATE '2023-01-01',DATE '2023-06-01'),('2023_JunDez',DATE '2023-06-01',DATE '2024-01-01') AS p(periodo,inicio,fim)),
 filiais AS (SELECT cod_filial,filial,FALSE AS consolidado FROM workspace.gold.dim_filial
 UNION ALL SELECT CAST(NULL AS STRING),'Consolidado',TRUE)
SELECT '{t}' AS tabela,b.cod_filial,b.filial,p.periodo,COUNT(f.{date}) AS linhas,{aggregates}
 FROM filiais b CROSS JOIN periodos p LEFT JOIN workspace.gold.{t} f
 ON (b.consolidado OR f.cod_filial=b.cod_filial) AND f.{date}>=p.inicio AND f.{date}<p.fim{rowfilter}
 GROUP BY b.cod_filial,b.filial,p.periodo ORDER BY b.filial,p.periodo;
"""
    if t.startswith('vw_'):
        sql+="""
-- S04: contagens de TODAS as linhas da view para comparar com 06-filtros-vw (não é soma financeira).
SELECT cod_filial,competencia,COUNT(*) AS linhas FROM workspace.gold.vw_dre_comparativo
GROUP BY cod_filial,competencia ORDER BY cod_filial,competencia;
"""
for t,k in keys.items():
    if t!='dim_calendario':
        sql+=f"\n-- S05-{t}: vazios e colisões após normalização; não alterar os dados.\nSELECT COUNT(*) AS chaves_vazias FROM workspace.gold.{t} WHERE {k} IS NOT NULL AND TRIM({k})='';\nSELECT UPPER(TRIM({k})) AS chave_normalizada, COUNT(*) AS n FROM workspace.gold.{t}\nGROUP BY UPPER(TRIM({k})) HAVING COUNT(*)>1;\n"
sql+="""
-- S06: compatibilidade gerencial: sem NULL de chave de posição, descrição estável por ordem e por filial.
SELECT COUNT(*) AS posicoes_nulas FROM workspace.gold.vw_dre_comparativo WHERE ordem_dre IS NULL;
SELECT ordem_dre,COUNT(DISTINCT descricao_dre) AS descricoes,COUNT(DISTINCT subtotal) AS flags
FROM workspace.gold.vw_dre_comparativo GROUP BY ordem_dre;
SELECT descricao_dre,COUNT(DISTINCT ordem_dre) AS ordens FROM workspace.gold.vw_dre_comparativo
GROUP BY descricao_dre HAVING COUNT(DISTINCT ordem_dre)>1;
-- S07: cobertura exata da linha 13 por cenário/filial (min/max só contam valores não NULL).
SELECT cod_filial,
MIN(CASE WHEN realizado IS NOT NULL THEN competencia END) AS inicio_realizado,
MAX(CASE WHEN realizado IS NOT NULL THEN competencia END) AS fim_realizado,
MIN(CASE WHEN orcado IS NOT NULL THEN competencia END) AS inicio_orcado,
MAX(CASE WHEN orcado IS NOT NULL THEN competencia END) AS fim_orcado,
MIN(CASE WHEN previsto IS NOT NULL THEN competencia END) AS inicio_previsto,
MAX(CASE WHEN previsto IS NOT NULL THEN competencia END) AS fim_previsto,
COUNT(DISTINCT CASE WHEN realizado IS NOT NULL THEN competencia END) AS meses_realizado,
COUNT(DISTINCT CASE WHEN orcado IS NOT NULL THEN competencia END) AS meses_orcado,
COUNT(DISTINCT CASE WHEN previsto IS NOT NULL THEN competencia END) AS meses_previsto
FROM workspace.gold.vw_dre_comparativo WHERE ordem_dre=13 GROUP BY cod_filial;
-- S08: conta escolhida. Substituir o parâmetro na cópia da consulta antes de executar.
"""
for t in facts:
    sql+=f"SELECT '{t}' AS tabela,COUNT(*) AS linhas,SUM(valor) AS valor FROM workspace.gold.{t} WHERE planocontas_id='__ID_CONTA_ANALITICA__';\n"
put('complemento-databricks.sql',sql)

tests=[
 ('INT01','Chaves das quatro dimensões','SQL original + 04','Linhas > 0; chaves distintas=linhas; ausentes=0; duplicados=0'),
 ('INT02','Conta nas três fatos','SQL original + 05','Órfãos não nulos=0; chaves ausentes=0'),
 ('INT03','Filial nas três fatos e view','SQL original + 05','Órfãos não nulos=0; chaves ausentes=0'),
 ('INT04','Competência vs calendário','SQL original + 05','Órfãos não nulos=0; chaves ausentes=0; horário consistente'),
 ('REL01','Cardinalidade/direção/estado reais','02 + 03 ou DMV','18 IDs reconciliados; negócio 12 ativos/1 inativo; *:1 e OneDirection confirmados ou divergência analisada'),
 ('FIL01','Filial x período nas quatro tabelas','06-* + SQL S03/S04','Extras=Faltantes=0; contagens iguais; cobertura de cada cidade e Consolidado x quatro períodos'),
 ('FIL02','Conta nas três fatos e isolamento da view','10 + 11 + SQL S08','Parâmetro válido; amostra discriminante; fatos via dimensão=seleção direta; view inalterada'),
 ('FIL03','Dim_dre não filtra view','12','Uma linha selecionada; view com várias posições; contagens e conjuntos antes/depois iguais'),
 ('FIL04','Relação inativa Filial–Conta','13 + 02','Estado inativo; lista de contas inalterada pela filial; comparação direta discriminante'),
 ('FIN01','Linha 13 integral','07 + SQL S02','Dados presentes; valores esperados; diferenças arredondadas <= R$ 0,01'),
 ('FIN02','Linha 13 por filial/ano e período','08 + 09 + SQL S01/S03','Origem=modelo em cada célula; soma das filiais reconcilia consolidado; sem soma das 13 posições'),
 ('FIN03','Período realizado e BLANK após maio/2023','08 + SQL S07','29 competências realizado/36 orçamento/previsão por filial se contrato completo; realizado JunDez ausente, não zero fabricado'),
 ('DRE01','Estratégia gerencial','Guia de execução','Abordagem 1 recomendada; ordens/descrições/grão válidos; detalhe por conta explicitamente fora da view')]
with (OUT/'registro-testes.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f);w.writerow(['ID','Teste','Roteiro','Criterio','Estado','Obtido','Divergencia','Evidencia','Executor','DataAtualizacaoModelo','DataExecucao'])
    for id,title,script,criteria in tests:w.writerow([id,title,script,criteria,'NAO_EXECUTADO','','','','','',''])
js('estado-execucao.json',{'data':datetime.now().astimezone().isoformat(),'dynamicSQLExecuted':0,'dynamicDAXExecuted':0,'phase1':'Bloqueada','phase2':'Não liberada; não iniciada','resultsTemplateContainsMeasurements':False,'reason':'Nenhuma sessão autenticada/modelo carregado disponível na descoberta de ambiente'})
print(json.dumps({'out':str(OUT),'daxFiles':len(list(OUT.glob('*.dax'))),'testGroups':len(tests),'SQLDAXExecuted':False},ensure_ascii=False))
