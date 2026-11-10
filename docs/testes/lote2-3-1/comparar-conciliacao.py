"""Comparador SQL independente x exportação DAX 09. Não consulta fontes nem altera modelo."""
import argparse, csv, json
from decimal import Decimal
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('sql_csv',type=Path)
p.add_argument('dax_json',type=Path,help='JSON de 09-matriz-comparabilidade, gerado pelo executor local')
p.add_argument('saida_json',type=Path)
a=p.parse_args()
def number(v):
    return None if v is None or str(v).strip().lower() in ('','null','blank','none') else Decimal(str(v))
def read_sql():
    with a.sql_csv.open(encoding='utf-8-sig',newline='') as f:
        return [( (r['grupo_filial'],r['periodo'],int(r['posicao']),r['cenario']),
                  (number(r['valor']),number(r['pares'])) ) for r in csv.DictReader(f)]
def read_dax():
    return [((r['[Grupo]'],r['[Periodo]'],int(r['[Value]']),r['[Cenario]']),
             (number(r['[Valor]']),number(r['[Pares]'])))
            for r in json.loads(a.dax_json.read_text(encoding='utf-8-sig'))]
def index(rows):
    result={}; dup=[]
    for k,v in rows:
        if k in result:dup.append(k)
        result[k]=v
    return result,dup
s,sd=index(read_sql()); d,dd=index(read_dax())
missing=sorted(d.keys()-s.keys()); extra=sorted(s.keys()-d.keys()); failures=[]
maxdiff=Decimal('0'); blanks=0
for key in sorted(s.keys() & d.keys()):
    sv,sp=s[key]; dv,dp=d[key]
    if sv is None and dv is None:blanks+=1
    if (sv is None)!=(dv is None): failures.append({'chave':key,'motivo':'NULL/BLANK divergente'})
    elif sv is not None:
        diff=abs(sv-dv); maxdiff=max(maxdiff,diff)
        if diff>Decimal('0.01'):failures.append({'chave':key,'motivo':'Diferenca monetaria','diferenca':str(diff)})
    if sp!=dp:failures.append({'chave':key,'motivo':'Cardinalidade de cobertura divergente','sql':str(sp),'dax':str(dp)})
result={'sql_chaves':len(s),'dax_chaves':len(d),'esperadas':1755,'duplicacoes_sql':sd,'duplicacoes_dax':dd,
        'ausentes_sql':missing,'extras_sql':extra,'divergencias':failures,'diferenca_maxima':str(maxdiff),
        'null_blank_coincidentes':blanks,'tolerancia':'0.01',
        'aprovado':len(s)==len(d)==1755 and not(sd or dd or missing or extra or failures),
        'limite':'Depende de preflight de grao sem duplicacoes e confirmacao do mesmo snapshot SQL/Power BI; nao certifica fechamento'}
a.saida_json.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
raise SystemExit(0 if result['aprovado'] else 1)
