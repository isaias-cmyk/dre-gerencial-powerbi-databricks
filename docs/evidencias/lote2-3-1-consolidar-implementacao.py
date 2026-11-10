from pathlib import Path
from collections import Counter
import json,hashlib,re
from decimal import Decimal
root=Path(__file__).resolve().parents[2]
prep=json.loads((root/'docs/evidencias/lote2-3-1-implementacao-atual.json').read_text())
ev=Path(prep['evidence']); base=root/'docs/evidencias'
def read(folder,name):return json.loads((base/folder/(name+'.json')).read_text(encoding='utf-8-sig'))
final='lote2-3-1-diagnostico-20261103-090110'
matrix=read(final,'09-matriz-comparabilidade')
reg=read('lote2-3-1-diagnostico-20261103-085903','14-regressao-36-medidas')
guards=read(final,'11-guardas-contexto')
config=read(final,'10-configuracao-materializacao')
zero=read('lote2-3-1-diagnostico-20261103-090240','12-sintetico-zero')[0]
blank=read('lote2-3-1-diagnostico-20261103-090240','13-sintetico-blank')[0]
parts=read('lote2-3-1-diagnostico-20261103-090326','18-estado-particoes')
rels=read('lote2-3-1-diagnostico-20261103-090326','19-estado-relacionamentos')
measures=read(final,'17-estado-medidas')
tables=read(final,'16-estado-tabelas')
assert len(config)==9 and len({(x['_ConfigCobertura[cod_filial]'],x['_ConfigCobertura[cenario]']) for x in config})==9
manifest=json.loads((root/'docs/cobertura-temporal-didatica.json').read_text())
for c in config:
    m=next(x for x in manifest['intervalos'] if x['cod_filial']==c['_ConfigCobertura[cod_filial]'] and x['cenario']==c['_ConfigCobertura[cenario]'])
    for key in ('inicio_competencia','fim_competencia'):
        assert c['_ConfigCobertura['+key+']'][:10]==m[key]
    assert c['_ConfigCobertura[versao_contrato]']==manifest['versao']
    assert c['_ConfigCobertura[hash_base]']==manifest['sha256_arquivo']
    assert c['_ConfigCobertura[estado]']==m['estado']
assert len(matrix)==1755 and all(x['[Aprovado]'] for x in matrix)
assert len(reg)==1620 and all(x['[Aprovado]'] for x in reg)
assert all(all(x.get(k) is None for k in ('[Realizado]','[Orcado]','[Previsto]','[Pares]')) for x in guards)
assert zero['[Realizado]']==0 and zero['[Orcado]']==-100 and zero['[Previsto]']==0 and zero['[Pares]']==1
assert all(blank[k] is None for k in ('[Realizado]','[Orcado]','[Previsto]')) and blank['[Pares]']==1
assert len(measures)==41 and all(x['[State]']=='Valid' for x in measures)
assert len(parts)==16 and all(x['State']==1 and x['ErrorMessage'] is None for x in parts)
assert len(rels)==18 and '_ConfigCobertura' not in json.dumps(rels)
expected={'Integral':29,'2021':12,'2022':12,'2023':5,'2023_JanMai':5,'2023_JunDez':0,'2023_Maio':1,'2023_Junho':0,'2023_JanMar':2}
for x in matrix:
    want=None if x['[Value]'] in (8,11) else expected[x['[Periodo]']] * (3 if x['[Grupo]']=='Consolidado' else 2 if x['[Grupo]']=='01+02' else 1)
    assert x['[Pares]']==want
lookup={(x['[Grupo]'],x['[Periodo]'],x['[Value]'],x['[Cenario]']):x['[Valor]'] for x in matrix}
additive=[]
for (group,period,pos,scen),value in lookup.items():
    if group not in ('Consolidado','01+02'):continue
    sub=[lookup[(b,period,pos,scen)] for b in (('01','02','03') if group=='Consolidado' else ('01','02'))]
    if all(v is None for v in sub):assert value is None
    else:
        assert value is not None and all(v is not None for v in sub)
        assert abs(Decimal(str(value))-sum(Decimal(str(v)) for v in sub))<=Decimal('0.01')
    additive.append((group,period,pos,scen))
baseline=json.loads((ev/'baseline.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
changed=[x['path'] for x in baseline if sha(root/x['path'])!=x['sha256']]
prod=[x for x in changed if not x.startswith('docs/') and x!='PLANS.md']
assert sorted(prod)==sorted(['DRE Moderno - Databricks.SemanticModel/definition/model.tmdl','DRE Moderno - Databricks.SemanticModel/definition/tables/_Medidas.tmdl'])
before=(Path(prep['backup'])/'restauracao-teste/DRE Moderno - Databricks.SemanticModel/definition/tables/_Medidas.tmdl').read_text(encoding='utf-8-sig')
after=(root/'DRE Moderno - Databricks.SemanticModel/definition/tables/_Medidas.tmdl').read_text(encoding='utf-8-sig')
def measureblocks(s):
    ans={}
    for m in re.finditer(r"(?m)^\tmeasure '([^']+)' =",s):
        e=re.search(r'(?m)^\t(?:measure |column |partition |///)',s[m.end():])
        ans[m[1]]=s[m.start():m.end()+e.start() if e else len(s)].strip()
    return ans
old=measureblocks(before); new=measureblocks(after)
assert len(old)==36 and all(new[k]==v for k,v in old.items())
summary={'estado':'IMPLEMENTADO_EM_VALIDACAO_SQL_PENDENTE',
 'backup':prep,'configuracao':{'linhas':9,'contrato_intervalos_hash_coincidentes':True,'oculta':next(x['[IsHidden]'] for x in tables if x['[Name]']=='_ConfigCobertura'),'sem_relacionamentos':True},
 'modelo':{'tabelas':16,'relacionamentos':18,'medidas_validas':41,'particoes_ready':16},
 'matriz':{'combinacoes':45,'posicoes':13,'cenarios':3,'casos':len(matrix),'aprovados':len(matrix),'falhas':0,'max_diferenca':max(abs(x['[Diferenca]'] or 0) for x in matrix),'blank_preservados':sum(x['[AmbosBlank]'] for x in matrix),'pares_verificados':len(matrix)},
 'regressao':{'medidas':36,'casos':len(reg),'aprovados':len(reg),'max_diferenca':max(abs(x['[Diferenca]'] or 0) for x in reg)},
 'aditividade':{'comparacoes_incluindo_blank':len(additive),'falhas':0,'limite':'Mesmas competencias comuns para filiais e consolidado; comparacoes derivadas da matriz, nao execucoes adicionais'},
 'guardas':{'casos':3,'aprovados':3},'sinteticos':{'casos':2,'aprovados':2,'escopo':'Cinco expressoes redefinidas identicamente em consulta, bases privadas zero/blank; sem persistencia'},
 'sql_independente':{'executado':False,'aprovado':False,'pendencia':'Exportar os dois resultados do roteiro 15 e executar comparador para o mesmo snapshot'},
 'historico_erros':{'config_inicial':'DATATABLE DATE rejeitado; corrigido para literal ISO DATETIME com Desktop fechado, sem mudar intervalos',
 'sintetico_inicial':'Override somente das bases nao afetou dependencias persistidas; resultado inicial nao serve como prova de zero/blank; corrigido com cinco expressoes em escopo de consulta'},
 'arquivos_producao_preexistentes_alterados':prod,'medidas_antigas_identicas':36,'novo_arquivo':'definition/tables/_ConfigCobertura.tmdl',
 'pendencias':['Conciliacao SQL independente','Save/reabertura e persistencia do cache apos materializacao ainda nao testadas','Testes de configuracao futura com lacunas/cortes diferentes: validacao sintética ampliada pendente; nao houve alteracao da configuracao homologada']}
(ev/'resumo-validacao.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k not in ('backup','historico_erros')},ensure_ascii=False))
