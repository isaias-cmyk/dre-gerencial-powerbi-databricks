from pathlib import Path
from decimal import Decimal
import csv, io, json, hashlib

root=Path(__file__).resolve().parents[2]
source=Path(r'C:\Users\<usuario>\.codex\attachments\d6ec939b-3a07-48e1-b8ca-2f2dd391b737\Texto colado.txt')
out=root/'docs/evidencias/lote2-2-consolidado-recebido-20261102'
out.mkdir(exist_ok=True)
raw=source.read_bytes()
(out/'resultado-original.tsv').write_bytes(raw)
fields=['Indicador','PosicaoDRE','OrdemCenario','Cenario','NomeMedida','ValorMedida','ValorDireto','FilialConsultada','DataInicial','DataFinal','Diferenca','MedidaBlank','DiretoBlank','Aprovado','Status']
rows=list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig')),fieldnames=fields,delimiter='\t'))
catalog=json.loads((root/'docs/evidencias/lote2-2-20261102-163559/catalogo-novas-medidas.json').read_text(encoding='utf-8'))
expected={m['Nome']:m for m in catalog}
assert len(rows)==30 and len({r['NomeMedida'] for r in rows})==30
assert {r['NomeMedida'] for r in rows}==expected.keys()
values={}
for r in rows:
    m=expected[r['NomeMedida']]
    assert r['Indicador']==m['Indicador'] and int(r['PosicaoDRE'])==m['Posicao'] and r['Cenario']==m['Cenario']
    assert r['OrdemCenario']=={'Realizado':'1','Orçado':'2','Previsto':'3'}[r['Cenario']]
    assert r['FilialConsultada']=='Consolidado'
    assert r['DataInicial']=='Fri, 01 Jan 2021 00:00:00' and r['DataFinal']=='Sun, 31 Dec 2023 00:00:00'
    a,b=Decimal(r['ValorMedida']),Decimal(r['ValorDireto'])
    assert a==b and Decimal(r['Diferenca'])==a-b==0
    assert r['Aprovado']=='true' and r['Status']=='OK'
    assert r['MedidaBlank']==r['DiretoBlank']=='false'
    values[(int(r['PosicaoDRE']),r['Cenario'])]=a
identities=[]
for c in ['Realizado','Orçado','Previsto']:
    for name,pos,parts in [('Receita Líquida',3,(1,2)),('Margem de Contribuição',5,(3,4))]:
        diff=values[pos,c]-sum(values[p,c] for p in parts)
        assert abs(diff)<=Decimal('.01')
        identities.append({'Indicador':name,'Cenario':c,'Diferenca':str(diff),'Aprovado':True})
with (out/'resultado-com-cabecalho.csv').open('w',newline='',encoding='utf-8-sig') as f:
    writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)
result={'Proveniencia':'Resultado de consulta DAX fornecido pelo usuário; análise local do anexo, sem nova execução DAX/SQL pelo agente',
        'FonteAnexo':str(source),'SHA256Original':hashlib.sha256(raw).hexdigest(),
        'ConsultaCompativel':'docs/teste-consolidado-lote2-2.dax','Contexto':'Consolidado, 01/01/2021 a 31/12/2023',
        'MedidasRecebidas':30,'MedidasUnicas':30,'NomesPosicoesCenariosConformes':True,
        'Aprovados':30,'DivergenciasValor':0,'DiferencaMaxima':'0','SinaisIguaisAoDireto':True,
        'PosicoesPositivasNesteContexto':[1,3,5],'PosicoesNegativasNesteContexto':[2,4,6,7,9,10,12],
        'CasosBlankRecebidos':0,'IdentidadesConsolidadas':identities,
        'SQLRecebido':False,'NovasExecucoesDAXPeloAgente':0,'NovasExecucoesSQLPeloAgente':0,
        'Aceite':'PARCIAL — consolidado integral aprovado; lote não concluído',
        'Pendencias':['Conciliação SQL independente','Filiais individuais e seleção múltipla','Recortes anuais e mensais','BLANK após maio/2023 e contextos vazios','Filtros conflitantes de posição/descrição','Totais de matriz e soma das filiais','Regressão das seis medidas e proteção EBITDA/EBIT','Metadados/estado/materialização/formatação no modelo carregado']}
(out/'analise.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
