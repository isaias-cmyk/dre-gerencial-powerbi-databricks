from pathlib import Path
from decimal import Decimal
import json, csv

root=Path(__file__).resolve().parents[2]
evidence=root/'docs/evidencias'
first=evidence/'lote2-2-execucao-20261102-185937'
matrixdir=evidence/'lote2-2-execucao-20261102-185954'
extra=evidence/'lote2-2-execucao-20261102-190116'
regcontextsdir=evidence/'lote2-2-execucao-20261102-190257'
out=evidence/'lote2-2-validacao-final-20261102'
out.mkdir(exist_ok=True)
def read(folder,name):
    return json.loads((folder/(name+'.json')).read_text(encoding='utf-8-sig'))
def dec(x): return Decimal(str(x))
def equal(a,b):
    return (a is None and b is None) if a is None or b is None else abs(dec(a)-dec(b))<=Decimal('.01')
failures=[]
groups=[]
def check(group,key,condition,detail=None):
    if not condition: failures.append({'Grupo':group,'Chave':key,'Detalhe':detail})

catalog=read(evidence/'lote2-2-20261102-163559','catalogo-novas-medidas')
names={m['Nome'] for m in catalog}
byname={m['Nome']:m for m in catalog}
matrix=read(matrixdir,'02-filiais-periodos-conciliacao')
new=[r for r in matrix if r['[Medida]'] in names]
rl=[r for r in matrix if r['[Medida]'] not in names]
check('Cobertura','Matriz',len(matrix)==1155 and len(new)==1050 and len(rl)==105)
keys={(r['[GrupoFilial]'],r['[Periodo]'],r['[Medida]']) for r in matrix}
check('Cobertura','Unicidade',len(keys)==1155)
differences=[]
for r in matrix:
    key={k:r[k] for k in ['[GrupoFilial]','[Periodo]','[Medida]','[Cenario]','[Posicao]']}
    a,b=r['[Obtido]'],r['[EsperadoView]']
    check('Matriz',key,equal(a,b) and r['[Aprovado]'] is True)
    check('Ausencia',key,r['[AusenciaAposMaio]'] is True)
    if a is not None and b is not None:
        differences.append(abs(dec(a)-dec(b)))
        check('Sinal',key,(dec(a)>0)-(dec(a)<0)==(dec(b)>0)-(dec(b)<0))
    if r['[Medida]'] in byname:
        m=byname[r['[Medida]']]
        check('Contrato',key,r['[Posicao]']==m['Posicao'] and r['[Cenario]']==m['Cenario'])
lookup={(r['[GrupoFilial]'],r['[Periodo]'],r['[Medida]']):r['[Obtido]'] for r in matrix}
aditividade=[]
for period in sorted({r['[Periodo]'] for r in matrix}):
    for name in sorted({r['[Medida]'] for r in matrix}):
        for group,branches in [('Consolidado',['01','02','03']),('01+02',['01','02'])]:
            a=lookup[group,period,name]
            vals=[lookup[b,period,name] for b in branches]
            total=None if all(v is None for v in vals) else sum(dec(v) for v in vals if v is not None)
            passed=equal(a,total)
            row={'GrupoFilial':group,'Periodo':period,'Medida':name,'Total':None if a is None else str(a),'SomaFiliais':None if total is None else str(total),'Diferenca':None if a is None or total is None else str(dec(a)-total),'Aprovado':passed}
            aditividade.append(row)
            check('Aditividade',row,passed)
for group in ['Consolidado','01','02','03','01+02']:
    for period in sorted({r['[Periodo]'] for r in new}):
        rows=[r for r in new if r['[GrupoFilial]']==group and r['[Periodo]']==period]
        groups.append({'GrupoFilial':group,'Periodo':period,'Executados':len(rows),'Aprovados':sum(equal(r['[Obtido]'],r['[EsperadoView]']) and r['[Aprovado]'] is True and r['[AusenciaAposMaio]'] is True for r in rows),'Blank':sum(r['[Obtido]'] is None for r in rows),'ZeroLegitimo':sum(r['[Obtido]'] is not None and dec(r['[Obtido]'])==0 for r in rows)})
contexts=read(first,'03-posicao-descricao-contextos')
for r in contexts:check('Contexto',r,r['[Aprovado]'] is True and equal(r['[Obtido]'],r['[Esperado]']))
wide=read(first,'04-matriz-totais')
for r in wide:
    for i,m in enumerate(catalog,7):
        expected=lookup['Consolidado','Integral',m['Nome']] if r['[TotalGeral]'] or r['vw_dre_comparativo[ordem_dre]']==m['Posicao'] else None
        check('MatrizTotal',{'Posicao':r['vw_dre_comparativo[ordem_dre]'],'Total':r['[TotalGeral]'],'Medida':m['Nome']},equal(r[f'[M{i:02}]'],expected))
regression=read(extra,'12-regressao-ampliada')
check('Cobertura','Regressao',len(regression)==210)
for r in regression:check('Regressao',r,r['[Aprovado]'] is True and equal(r['[Obtido]'],r['[Esperado]']))
prior=evidence/'lote2-1-encerramento-20261102-162739'
oldcontexts=read(prior,'05-contextos-e-totais')
currentcontexts=read(first,'08-regressao-bases')
for a,b in zip(oldcontexts,currentcontexts):
    check('RegressaoContextos',a['[Contexto]'],a.keys()==b.keys() and all(equal(v,b[k]) if isinstance(v,(int,float)) or v is None else v==b[k] for k,v in a.items()))
regcontexts=read(regcontextsdir,'16-regressao-contextos-ampliada')
check('Cobertura','RegressaoContextosAmpliados',len(regcontexts)==175)
for r in regcontexts:
    group,period,context=r['[GrupoFilial]'],r['[Periodo]'],r['[Contexto]']
    for scenario,basekey,rlkey in [('Realizado','[BaseR]','[RLR]'),('Orçado','[BaseO]','[RLO]'),('Previsto','[BaseP]','[RLP]')]:
        expectedrl=lookup[group,period,'DRE | Resultado Líquido '+scenario] if context in ('SemFiltro','Multiplas1e13','Unica13') else None
        expectedbase=lookup[group,period,'DRE | Receita Operacional Bruta '+scenario] if context=='Unica1' else expectedrl if context=='Unica13' else None
        check('RegressaoContextosAmpliados',{'GrupoFilial':group,'Periodo':period,'Contexto':context,'Cenario':scenario},equal(r[basekey],expectedbase) and equal(r[rlkey],expectedrl))
control=read(first,'07-regressao-controle')[0]
for scenario,expected in [('Realizado','5038227.39'),('Orcado','6622493.82'),('Previsto','6157931.19')]:
    for name in ['Base'+scenario,'RL'+scenario+'Provisorio']:
        check('Controle',name,equal(control['['+name+']'],Decimal(expected)))
six=read(extra,'13-seis-cenarios-consolidado')
check('Cobertura','SeisCenarios',len(six)==180 and len({r['[Caso]'] for r in six})==6)
for r in six:check('SeisCenarios',r,r['[Aprovado]'] is True and equal(r['[ValorMedida]'],r['[ValorDireto]']))
sixabsence=[r for r in six if r['[Caso]']=='Consolidado_JunDez2023' and r['[Cenario]']=='Realizado']
check('Ausencia','SeisCenarios',len(sixabsence)==10 and all(r['[ValorMedida]'] is None and r['[ValorDireto]'] is None and r['[Status]']=='OK_BLANK' for r in sixabsence))
ebit=read(extra,'14-ebitda-ebit-ampliado')
ebitkeys=['[BaseR]','[BaseO]','[BaseP]','[RLR]','[RLO]','[RLP]']+[f'[M{i:02}]' for i in range(7,37)]
check('Cobertura','EBIT',len(ebit)==70)
for r in ebit:
    check('EBIT',{'GrupoFilial':r['[GrupoFilial]'],'Periodo':r['[Periodo]'],'Posicao':r['vw_dre_comparativo[ordem_dre]']},r['[LinhasFonte]']>0 and all(r[k] is None for k in ebitkeys))
identities=read(first,'11-receita-liquida-margem')
for r in identities:check('Identidades',r,r['[IdentidadesCoerentes]'] is True)
metadata=read(first,'01-metadados')
check('Metadados','36medidas',len(metadata)==36 and len({r['[Name]'] for r in metadata})==36 and all(r['[State]']=='Valid' for r in metadata))
for m in catalog:
    row=next(r for r in metadata if r['[Name]']==m['Nome'])
    check('Metadados',m['Nome'],row['[LineageTag]']==m['LineageTag'] and row['[DisplayFolder]']==m['Pasta'])
partitions=read(extra,'15-estado-particoes')
check('Estado','Particoes',len(partitions)==15 and all(r['[Estado]']==1 and r['[Erro]'] is None for r in partitions))
check('Materializacao','_Medidas',read(first,'09-materializacao')==[{'[Linhas]':1,'[Organizacao]':0}])
for folder in [first,matrixdir,extra,regcontextsdir]:check('Integridade',folder.name,all(r['Unchanged'] for r in read(folder,'integridade')))
for name,rows in [('aditividade',aditividade),('grupos-filtros',groups),('divergencias',failures)]:
    (out/(name+'.json')).write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    if rows:
        with (out/(name+'.csv')).open('w',newline='',encoding='utf-8-sig') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
summary={'MatrizPrincipal':{'Combinacoes':35,'MedidasLote22':30,'Executados':1050,'Aprovados':sum(g['Aprovados'] for g in groups),'Reprovados':1050-sum(g['Aprovados'] for g in groups),'DivergenciaMaxima':str(max(differences)),'CasosBlank':sum(g['Blank'] for g in groups),'ZerosLegitimosEncontrados':sum(g['ZeroLegitimo'] for g in groups)},
 'ResultadoLiquidoAdicional':{'Casos':105,'Aprovados':sum(r['[Aprovado]'] is True for r in rl)},
 'SeisCenariosConfirmados':{'Casos':180,'Aprovados':sum(r['[Aprovado]'] is True for r in six),'RealizadoJunDezBlank':len(sixabsence)},
 'ContextosPosicaoDescricao':{'Casos':240,'Aprovados':sum(r['[Aprovado]'] is True for r in contexts)},
 'TotaisMatriz':{'CelulasVerificadas':420},
 'Aditividade':{'Casos':len(aditividade),'Aprovados':sum(r['Aprovado'] for r in aditividade),'MaxDiferenca':str(max(abs(dec(r['Diferenca'])) for r in aditividade if r['Diferenca'] is not None))},
 'Regressao':{'Medidas':6,'Combinacoes':35,'Casos':210,'Aprovados':sum(r['[Aprovado]'] is True for r in regression),'ContextosComparadosComLote21':5,'ControlesIntegrais':6,'ContextosAmpliados':175,'ValoresVerificadosContextosAmpliados':1050},
 'EBITDA_EBIT':{'Contextos':70,'CelulasBlank':2520,'Estado':'SEM_VALORES'},
 'IdentidadesReceitaMargem':{'Casos':105,'Aprovados':sum(r['[IdentidadesCoerentes]'] is True for r in identities)},
 'Metadados':{'MedidasValidas':36,'ParticoesReady':15,'MedidasMaterializada':True},
 'ErrosExecucao':{'Tentativas':16,'ExecucoesSucesso':15,'FalhasHistoricasScriptTeste':1,'FalhaCorrigida':'UNION com número de colunas desigual no roteiro 02; coluna de ausência uniformizada e reexecutada com sucesso'},
 'FalhasValidacaoAtuais':len(failures),'SQL':{'Executado':False,'CasosConciliados':0,'Estado':'PENDENTE — sem conector de execução Databricks disponível; SELECT e comparador preparados'},
 'ProducaoAlterada':False,'AceiteLote22':'PENDENTE_SQL_INDEPENDENTE','Lote23':'NAO_INICIADO'}
(out/'resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
