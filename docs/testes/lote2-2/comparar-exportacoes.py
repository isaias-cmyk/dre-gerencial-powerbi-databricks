"""Comparação de exports CSV reais: python comparar-exportacoes.py dax.csv sql.csv saida.json.
Não executa SQL nem DAX; exige 1.155 chaves únicas e preserva ausência versus zero.
"""
import csv, json, sys
from decimal import Decimal
from pathlib import Path

def load(path, aliases, value):
    text=Path(path).read_text(encoding='utf-8-sig')
    dialect=csv.Sniffer().sniff(text[:4096],delimiters=',;\t')
    result={}
    for original in csv.DictReader(text.splitlines(),dialect=dialect):
        row={k.strip('[]').lower():v.strip() for k,v in original.items()}
        key=tuple(row[k].lower() for k in aliases)
        if key in result: raise ValueError(f'Chave duplicada: {key}')
        raw=row[value]
        if raw.lower() in ('','null','blank','(blank)'):
            amount=None
        else:
            # Exportar sem agrupamento de milhar; separador decimal pode ser vírgula.
            if ',' in raw and '.' in raw: raise ValueError('Exportar valores sem separador de milhar.')
            amount=Decimal(raw.replace(',','.'))
        result[key]=amount
    if len(result)!=1155: raise ValueError(f'Esperadas 1155 chaves, obtidas {len(result)} em {path}')
    return result

if len(sys.argv)!=4: raise SystemExit(__doc__)
dax=load(sys.argv[1],['grupofilial','periodo','posicao','cenario'],'obtido')
sql=load(sys.argv[2],['grupo_filial','periodo','posicao','cenario'],'valor')
assert dax.keys()==sql.keys(), 'Conjuntos de chaves diferentes.'
diff=[]
for key,a in dax.items():
    b=sql[key]
    if (a is None)!=(b is None) or (a is not None and b is not None and abs(a-b)>Decimal('.01')):
        diff.append({'Chave':key,'DAX':str(a),'SQL':str(b)})
report={'Casos':len(dax),'Tolerancia':'0.01','Divergencias':diff,'Aprovado':not diff,
        'DAXOrigem':str(Path(sys.argv[1]).resolve()),'SQLOrigem':str(Path(sys.argv[2]).resolve())}
Path(sys.argv[3]).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'Casos':len(dax),'Divergencias':len(diff),'Aprovado':not diff}))
raise SystemExit(0 if not diff else 1)
