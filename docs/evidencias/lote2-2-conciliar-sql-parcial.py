from pathlib import Path
from decimal import Decimal
import csv, json, collections, hashlib

r=Path(__file__).resolve().parents[2]
o=r/'docs/evidencias/lote2-2-sql-recebido-20261102'
sql=list(csv.DictReader((o/'resultado-sql.csv').open(encoding='utf-8-sig')))
dax=json.loads((r/'docs/evidencias/lote2-2-execucao-20261102-185954/02-filiais-periodos-conciliacao.json').read_text(encoding='utf-8-sig'))
d={tuple(str(x[k]).lower() for k in ['[GrupoFilial]','[Periodo]','[Posicao]','[Cenario]']):x['[Obtido]'] for x in dax}
seen=set(); rows=[]; maximum=Decimal(0); blanks=0
for x in sql:
    k=tuple(x[k].lower() for k in ['grupo_filial','periodo','posicao','cenario'])
    assert k not in seen and k in d
    seen.add(k)
    a=None if d[k] is None else Decimal(str(d[k]))
    b=None if x['valor'].lower() in ('null','') else Decimal(x['valor'])
    delta=None if a is None or b is None else abs(a-b)
    if delta is not None: maximum=max(maximum,delta)
    passed=(a is None)==(b is None) and (delta is None or delta<=Decimal('.01'))
    blanks+=a is None and b is None
    rows.append(dict(zip(['grupo_filial','periodo','posicao','cenario'],k),DAX=str(a),SQL=str(b),Diferenca=None if delta is None else str(delta),Aprovado=passed))
missing=[dict(zip(['grupo_filial','periodo','posicao','cenario'],k)) for k in sorted(d.keys()-seen)]
for name,data in [('comparacao-parcial',rows),('chaves-ausentes',missing),('divergencias',[x for x in rows if not x['Aprovado']])]:
    (o/(name+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    if data:
        with (o/(name+'.csv')).open('w',newline='',encoding='utf-8-sig') as f:
            w=csv.DictWriter(f,fieldnames=list(data[0])); w.writeheader(); w.writerows(data)
summary={'Esperados':1155,'Recebidos':len(sql),'Conciliados':sum(x['Aprovado'] for x in rows),'Divergencias':sum(not x['Aprovado'] for x in rows),'Ausentes':len(missing),'DiferencaMaxima':str(maximum),'BlankCoincidentes':blanks,'AusentesPorGrupoPeriodo':dict(collections.Counter(x['grupo_filial']+'/'+x['periodo'] for x in missing)),'ComparadorOriginal':'Executado; rejeitou cobertura 1000/1155','Proveniencia':'SQL fornecido pelo usuário, comparado com DAX previamente executado; nenhuma nova execução SQL pelo agente','OriginalSHA256':hashlib.sha256((o/'resultado-original.tsv').read_bytes()).hexdigest(),'AceiteCompleto':False,'Status':'BLOQUEADO_EXPORTACAO_SQL_INCOMPLETA','CompetenciaMensal':'Não comprovada individualmente; exportação agrupada por período','DataExecucaoSQL':'Não informada no anexo','ProducaoAlterada':False}
(o/'resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
