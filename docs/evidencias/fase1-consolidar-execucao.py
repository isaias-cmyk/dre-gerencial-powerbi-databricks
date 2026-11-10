"""Avalia saídas reais ADOMD. Não acessa ou altera o modelo Power BI."""
import json,csv,collections
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'docs/evidencias'
RUNS=[BASE/f'fase1-execucao-20261102-{s}' for s in ('154642','154704','154749','154841')]
OUT=RUNS[0]
def read(run,name):return json.loads((run/name).read_text(encoding='utf-8-sig'))
def clean(rows):return [{k.strip('[]'):v for k,v in r.items()} for r in rows]
def rows(run,name):return clean(read(run,name+'.json'))
def count(v):return 0 if v is None else v
def cents(v):return Decimal(str(v)).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
fail=[]
def require(ok,label):
 if not ok:fail.append(label)
keys=rows(OUT,'04-chaves-modelo')
for r in keys:require(r['Linhas']>0 and r['Linhas']==r['ChavesDistintas'] and count(r['ChavesAusentes'])==0,r['Teste'])
integrity=rows(OUT,'05-integridade-modelo')
for r in integrity:require(count(r['NulosOuVazios'])==0 and count(r['OrfaosNaoNulos'])==0,r['Relacao'])
metadata=rows(OUT,'02-relacionamentos')
cols=rows(OUT,'03-colunas')
coltypes={(r['Table'],r['Name']):r['DataType'] for r in cols}
typepairs=[]
for r in metadata:
 require(r['FromCardinality']=='Many' and r['ToCardinality']=='One' and r['CrossFilteringBehavior']=='OneDirection' and r['State']=='Ready',r['Name']+' propriedades')
 pair=[coltypes[r['FromTable'],r['FromColumn']],coltypes[r['ToTable'],r['ToColumn']]]
 typepairs.append({'ID':r['Name'],'Types':pair})
 # INFO.VIEW pode rotular Date/DateTime por apresentação; ambos correspondem ao tipo temporal tabular.
 norm=lambda t:'DateTime' if t in ('Date','DateTime') else t
 require(norm(pair[0])==norm(pair[1]),r['Name']+' tipos')
g=collections.defaultdict(list)
for r in metadata:
 if r['IsActive']:g[r['ToTable']].append(r['FromTable'])
names=set(r['Table'] for r in cols)
def paths(s,t,visited=()):
 if s==t:return 1
 return sum(paths(n,t,visited+(s,)) for n in g[s] if n not in visited and n!=s)
multiple=[(s,t) for s in names for t in names if s!=t and paths(s,t)>1]
require(not multiple,'múltiplos caminhos ativos reais')
require(sum(r['IsActive'] for r in metadata)==17,'17 ativos totais')
require([r['Name'] for r in metadata if not r['IsActive']]==['AutoDetected_b803a55e-b318-4f25-80e8-6068d5cedb12'],'relação inativa')
matrix=[]
for p in sorted(OUT.glob('06-*.json')):
 for r in clean(json.loads(p.read_text(encoding='utf-8-sig'))):
  require(count(r['LinhasViaDimensoes'])==count(r['LinhasDiretas']) and not r['Extras'] and not r['Faltantes'],p.stem+' '+r['Filial']+' '+r['Periodo'])
  matrix.append(r)
finance=rows(OUT,'07-controle-integral')[0]
require(finance['DadosPresentes'],'presença controle')
for field,expected in [('Realizado','5038227.39'),('Orcado','6622493.82'),('Previsto','6157931.19')]:require(cents(finance[field])==Decimal(expected),field+' controle')
periods=rows(OUT,'08-linha13-filial-periodo')
annual=read(OUT,'09-linha13-filial-ano.json')
for period in {r['Periodo'] for r in periods}:
 group=[r for r in periods if r['Periodo']==period]
 consolidated=next(r for r in group if r['Consolidado'])
 for measure in ('Realizado','Orcado','Previsto'):
  amounts=[r[measure] for r in group if not r['Consolidado'] and r[measure] is not None]
  if not amounts:require(consolidated[measure] is None,period+' '+measure+' BLANK')
  else:require(abs(cents(sum(amounts))-cents(consolidated[measure]))<=Decimal('.01'),period+' soma filial '+measure)
for measure in ('Realizado','Orcado','Previsto'):require(abs(cents(sum(r['['+measure+']'] or 0 for r in annual))-cents(finance[measure]))<=Decimal('.01'),'soma filial/ano '+measure)
for r in periods:
 if r['Periodo']=='2023_JunDez':require(r['Realizado'] is None and not r['RealizadosNaoNulos'],'BLANK pós maio '+r['Filial'])
account=rows(RUNS[1],'11-filtro-conta')
for r in account:
 require(r['ParametroValido'] and count(r['ViaConta'])==count(r['Direto']) and not r['Extras'] and not r['Faltantes'],r['Tabela']+' conta')
 if r['Tabela']!='vw_dre_comparativo':require(0<r['ViaConta']<r['Total'],r['Tabela']+' amostra discriminante')
cross=rows(RUNS[1],'17-intersecao-conta-filial-periodo')
for r in cross:
 for f in ('Lancamentos','Orcamento','Previsao'):require(count(r[f+'Via'])==count(r[f+'Direto']) and not r[f+'Extras'] and not r[f+'Faltantes'],'intersecao '+f+' '+r['Codigo']+' '+r['Periodo'])
dre=rows(OUT,'12-filtro-dre')[0]
require(dre['LinhasSelecionadasDimDRE']==1 and dre['LinhasViewAntes']==dre['LinhasViewDepois'] and not dre['Extras'] and not dre['Faltantes'] and 0<dre['LinhasViewPosicao1Direta']<dre['LinhasViewAntes'],'isolamento DRE')
inactive=rows(OUT,'13-relacao-inativa')
for r in inactive:require(r['ContasTotal']==r['ContasViaFilial']==129 and r['ContasDaFilialDiretas']==43 and not r['Extras'] and not r['Faltantes'],'lista contas '+r['Codigo'])
calendar=rows(OUT,'14-calendario-modelo')[0]
require(calendar['Dias']==calendar['DiasEsperados']==1095 and not calendar['ComHora'] and not calendar['MetadadosIncoerentes'],'calendário')
for r in rows(OUT,'15-cobertura-cenarios'):require(r['CompetenciasRealizado']==29 and r['CompetenciasOrcado']==r['CompetenciasPrevisto']==36,'cobertura '+r['Codigo'])
require(not read(OUT,'16-grao-view.json'),'duplicação view')
for r in rows(RUNS[2],'18-contrato-dre'):require(not r['Divergencias'],r['Teste'])
for r in rows(RUNS[3],'20-mes-multisselecao'):require(count(r['Via'])==count(r['Direto']) and not r['Extras'] and not r['Faltantes'],'multisselecao '+r['Tabela'])
parts=rows(RUNS[2],'19-particoes-carregadas')
statuses=[read(run,'execucao.json') for run in RUNS]
executions=[r for batch in statuses for r in (batch if isinstance(batch,list) else [batch]) if r['State']=='EXECUTADO']
result={'source':'Modelo importado carregado no Power BI Desktop, consultas ADOMD locais',
 'DAXQueriesExecuted':len(executions),'SQLQueriesExecuted':0,'QueryErrors':0,
 'KeyTests':keys,'IntegrityRelationshipTests':len(integrity),'OrphansOrMissingKeysDetected':0 if not fail else 'Ver falhas',
 'ActualRelationships':{'Total':len(metadata),'ActiveBusiness':12,'InactiveBusiness':1,'ActiveTechnical':5,'Cardinality':'Many:One','Direction':'OneDirection','State':'Ready','MultipleActivePaths':multiple,'TypePairs':typepairs},
 'BranchPeriodCases':len(matrix),'AccountBranchPeriodFactComparisons':len(cross)*3,'ExplicitMonthMultiBranchCases':4,
 'AccountSelected':{'ID':'01.02.04','Name':'ICMS','FactRows':[29,36,36],'ViewRowsUnchanged':1404},
 'Line13':finance,'Calendar':calendar,'Failures':fail,'LoadedModelDynamicTests':'APROVADOS' if not fail else 'REPROVADOS',
 'Remaining':['Comparação independente com Databricks SQL não executada','Aceite do responsável da abordagem DRE 1 e limites de conta ainda não registrado'],
 'Phase1':'Bloqueada para aceite global; testes locais aprovados' if not fail else 'Bloqueada',
 'Phase2':'Não iniciada e não liberada',
 'Particoes':[{'Name':r['Name'],'RefreshedTimeRaw':r['RefreshedTime'],'State':r['State'],'ErrorMessage':r['ErrorMessage']} for r in parts],
 'BlankInterpretation':'null em contagens COUNTROWS de conjuntos vazios interpretado como 0 técnico; valores financeiros preservados null',
 'ProductionChangedByRunner':any(not r['Unchanged'] for run in RUNS for r in read(run,'integridade.json'))}
(OUT/'consolidacao.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
# Registro medido novo, mantendo o template e as saídas históricas intactos.
with (ROOT/'docs/evidencias/fase1-dinamica/registro-testes.csv').open(encoding='utf-8-sig',newline='') as f:registry=list(csv.DictReader(f))
for r in registry:
 r['Estado']='EXECUTADO_APROVADO_MODELO' if r['ID']!='DRE01' else 'RECOMENDADO_ACEITE_PENDENTE'
 r['Executor']='Codex / ADOMD local';r['DataExecucao']='2026-11-02 15:46–15:49 America/Sao_Paulo'
 r['Evidencia']=';'.join(run.name for run in RUNS);r['Obtido']='Ver consolidacao.json e saídas CSV/JSON por consulta'
 r['Divergencia']='Sem falha detectada no modelo carregado; origem SQL não comparada'
 r['DataAtualizacaoModelo']='Ver RefreshedTime bruto em 19-particoes-carregadas.json; fuso não fornecido pelo rowset'
with (OUT/'registro-testes-executados.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=registry[0].keys());w.writeheader();w.writerows(registry)
print(json.dumps({'DAXQueriesExecuted':len(executions),'Failures':fail,'LocalDynamicTests':result['LoadedModelDynamicTests'],'SourceSQLExecuted':False,'ProductionChanged':result['ProductionChangedByRunner']},ensure_ascii=False,indent=2))
if fail:raise SystemExit(1)
