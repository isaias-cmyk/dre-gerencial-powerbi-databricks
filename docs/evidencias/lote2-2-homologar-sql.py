from pathlib import Path
from decimal import Decimal
import csv, json, hashlib, shutil

r=Path(__file__).resolve().parents[2]
out=r/'docs/evidencias/lote2-2-sql-completo-20261102'
out.mkdir(exist_ok=True)
src=Path(r'C:\Users\<usuario>\Downloads\New_Query_2026_11_02_15_53_51.csv')
dest=out/src.name
shutil.copy2(src,dest)
sql=list(csv.DictReader(dest.open(encoding='utf-8-sig')))
dax=json.loads((r/'docs/evidencias/lote2-2-execucao-20261102-185954/02-filiais-periodos-conciliacao.json').read_text(encoding='utf-8-sig'))
keynames=['grupo_filial','periodo','posicao','cenario']
expected={tuple(str(x[k]) for k in ['[GrupoFilial]','[Periodo]','[Posicao]','[Cenario]']):x for x in dax}
seen=set(); comparisons=[]; blanks=0; maximum=Decimal(0)
for x in sql:
    key=tuple(x[k] for k in keynames)
    assert key not in seen and key in expected
    seen.add(key)
    d=expected[key]['[Obtido]']
    a=None if d is None else Decimal(str(d))
    b=None if x['valor'].lower() in ('','null') else Decimal(x['valor'])
    assert (a is None)==(b is None), key
    if a is None:
        blanks+=1; delta=None
    else:
        delta=abs(a-b); maximum=max(maximum,delta)
        assert delta<=Decimal('.01'),key
        assert (a>0)-(a<0)==(b>0)-(b<0),key
    branches=3 if x['grupo_filial']=='Consolidado' else 2 if x['grupo_filial']=='01+02' else 1
    months={'Integral':36,'2021':12,'2022':12,'2023':12,'2023_JanMai':5,'2023_JunDez':7,'2023_Junho':1}[x['periodo']]
    present=months if x['cenario']!='Realizado' else {'Integral':29,'2021':12,'2022':12,'2023':5,'2023_JanMai':5,'2023_JunDez':0,'2023_Junho':0}[x['periodo']]
    assert int(x['linhas_fonte'])==branches*months,key
    assert int(x['valores_presentes'])==branches*present,key
    comparisons.append(dict(zip(keynames,key),DAX=None if a is None else str(a),SQL=None if b is None else str(b),DiferencaAbsoluta=None if delta is None else str(delta),Aprovado=True))
assert len(sql)==1155 and seen==expected.keys()
with (out/'comparacao-completa.csv').open('w',newline='',encoding='utf-8-sig') as f:
    writer=csv.DictWriter(f,fieldnames=list(comparisons[0]));writer.writeheader();writer.writerows(comparisons)
prior=list(csv.DictReader((r/'docs/evidencias/lote2-2-sql-recebido-20261102/resultado-sql.csv').open(encoding='utf-8-sig')))
lookup={tuple(x[k] for k in keynames):x for x in sql}
assert all(x==lookup[tuple(x[k] for k in keynames)] for x in prior)
result={'Estado':'CONCLUIDO_TECNICAMENTE','SQLProveniencia':'Exportação Databricks fornecida pelo usuário; sem nova execução SQL pelo agente','OrigemCSV':str(src),'ArquivoPreservado':str(dest),'SHA256':hashlib.sha256(dest.read_bytes()).hexdigest(),'CasosEsperados':1155,'CasosRecebidos':1155,'Aprovados':1155,'Reprovados':0,'Ausentes':0,'Duplicados':0,'DiferencaMaxima':str(maximum),'Tolerancia':'0.01','NULL_BLANK_Coincidentes':blanks,'SinaisPreservados':True,'ContagensFonteEPresencaConformes':True,'Primeiras1000CoincidemComAnexoAnterior':True,'Grao':'grupo_filial × periodo (recorte agregado) × posicao × cenario','CompetenciasMensaisIndividuais':'Não conciliadas individualmente; contagens de competências presentes conferidas por recorte','DataHoraExecucaoSQL':'Não comprovada pelo conteúdo; nome do arquivo não é prova de horário','Lote23':'LIBERADO_SOMENTE_PLANEJAMENTO_NAO_INICIADO','PendenciasContabeis':['Resultado Líquido provisório','EBITDA','EBIT'],'ProducaoAlterada':False}
(out/'aceite.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
