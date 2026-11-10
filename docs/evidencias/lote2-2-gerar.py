from pathlib import Path
import json, uuid, re

root=Path(__file__).resolve().parents[2]
prep=json.loads((root/'docs/evidencias/lote2-2-atual.json').read_text(encoding='utf-8'))
ev=Path(prep['Evidence'])
items=[(1,'Receita Operacional Bruta'),(2,'Deduções da Receita'),(3,'Receita Operacional Líquida'),(4,'Custos'),(5,'Margem de Contribuição'),(6,'Despesas Operacionais'),(7,'Resultado Financeiro'),(9,'Depreciação e Amortização'),(10,'Outras Receitas e Despesas'),(12,'Provisão para IR e CSLL')]
scenarios=[('Realizado','realizado'),('Orçado','orcado'),('Previsto','previsto')]
catalog=[{'Nome':f'DRE | {label} {sc}','Posicao':pos,'Indicador':label,'Cenario':sc,'Coluna':col,'Base':f'DRE | {sc}','Pasta':f'DRE\\{label}','LineageTag':str(uuid.uuid4())} for pos,label in items for sc,col in scenarios]
contracts=root/'docs/contratos-medidas-dax.md'
with contracts.open('a',encoding='utf-8') as f:
    f.write('\n\n# Lote 2.2 — contratos autorizados antes da implementação\n\nEstado: escopo de 30 novas medidas confirmado pela solicitação do usuário. Compatível com docs/plano-lote2-2.md, sem divergência funcional. Nomes normalizados conforme a lista autorizada; Margem de Contribuição é monetária, sem percentual. Lote 2.1 e seus contratos permanecem preservados.\n\n')
    for m in catalog:
        f.write(f'''## {m['Nome']}

- **Posição:** ordem_dre = {m['Posicao']}; indicador {m['Indicador']}.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[{m['Coluna']}], via [{m['Base']}]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `{m['Pasta']}`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição {m['Posicao']} da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.

''')
plan=root/'docs/plano-lote2-2.md'
with plan.open('a',encoding='utf-8') as f:
    f.write('\n\n## Confronto com a solicitação de execução — 02/11/2026\n\nEscopo confirmado: as dez posições propostas foram autorizadas, com três cenários e 30 medidas. Sem divergência funcional. Nomes adotam os indicadores da solicitação, com prefixo DRE e sufixo Realizado/Orçado/Previsto, registrados individualmente nos contratos antes da escrita TMDL. A instrução para iniciar foi recebida. Plano anterior preservado como histórico; estado atual e checklist de execução em PLANS.md e docs/validacao-lote2-2.md.\n')
# Contracts are saved before the sole production edit. Preserve original bytes verbatim.
target=root/'DRE Moderno - Databricks.SemanticModel/definition/tables/_Medidas.tmdl'
original=target.read_bytes()
text=original.decode('utf-8-sig')
assert len(re.findall(r'^\tmeasure ',text,re.M))==6
insert=original.index(b'\tcolumn _Organizacao')
nl='\r\n' if b'\r\n' in original else '\n'
blocks=[]
for m in catalog:
    blocks.append(f'''\t/// {m['Indicador']} {m['Cenario']}: posição {m['Posicao']} da view ajustada; preserva Filial/Calendário, sinais e BLANK. Filtro conflitante retorna BLANK.
\tmeasure '{m['Nome']}' =
\t\t\tCALCULATE (
\t\t\t\t[{m['Base']}],
\t\t\t\tKEEPFILTERS ( 'vw_dre_comparativo'[ordem_dre] = {m['Posicao']} )
\t\t\t)
\t\tformatString: R$ #,##0.00;(R$ #,##0.00);R$ 0.00
\t\tdisplayFolder: {m['Pasta']}
\t\tlineageTag: {m['LineageTag']}

''')
added=''.join(blocks).replace('\n',nl).encode('utf-8')
target.write_bytes(original[:insert]+added+original[insert:])
assert target.read_bytes().replace(added,b'',1)==original
(ev/'catalogo-novas-medidas.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2),encoding='utf-8')
(ev/'preservacao-seis-medidas.json').write_text(json.dumps({'OriginalBytesRecoveredRemovingOnlyInsertion':True,'OriginalMeasures':6,'AddedMeasures':30,'Total':36,'Strategy':'CALCULATE + KEEPFILTERS; sem divergência do plano'},ensure_ascii=False,indent=2),encoding='utf-8')
tests=root/'docs/testes/lote2-2'
tests.mkdir(parents=True,exist_ok=True)
def write(name,s): (tests/name).write_text('// Somente leitura; NÃO EXECUTADO neste lote. Executar nas medidas persistidas após reabrir o PBIP.\n'+s+'\n',encoding='utf-8')
write('01-metadados.dax','EVALUATE FILTER(INFO.VIEW.MEASURES(), [Table] = "_Medidas")')
periods=[('Integral',20210101,20240101),('2021',20210101,20220101),('2022',20220101,20230101),('2023',20230101,20240101),('2023_JanMai',20230101,20230601),('2023_JunDez',20230601,20240101),('2023_Junho',20230601,20230701)]
perioddax='DATATABLE("Periodo",STRING,"InicioNumero",INTEGER,"FimNumero",INTEGER,{'+','.join(f'{{"{p}",{i},{e}}}' for p,i,e in periods)+'})'
filialdax='DATATABLE("GrupoFilial",STRING,{{"Consolidado"},{"01"},{"02"},{"03"},{"01+02"}})'
prefix=f'''EVALUATE
VAR _Periodos = {perioddax}
VAR _Filiais = {filialdax}
RETURN GENERATE(CROSSJOIN(_Filiais,_Periodos),
VAR _Grupo = [GrupoFilial]
VAR _I = [InicioNumero]
VAR _F = [FimNumero]
VAR _Inicio = DATE(INT(_I/10000),MOD(INT(_I/100),100),MOD(_I,100))
VAR _Fim = DATE(INT(_F/10000),MOD(INT(_F/100),100),MOD(_F,100))
VAR _Datas = FILTER(ALL('dim_calendario'), 'dim_calendario'[data]>=_Inicio && 'dim_calendario'[data]<_Fim)
VAR _FiltroFilial = FILTER(ALL('dim_filial'), _Grupo="Consolidado" || 'dim_filial'[cod_filial]=_Grupo || (_Grupo="01+02" && 'dim_filial'[cod_filial] IN {{"01","02"}}))
RETURN UNION(
'''
allcatalog=catalog+[{'Nome':f'DRE | Resultado Líquido {sc}','Posicao':13,'Cenario':sc,'Coluna':col} for sc,col in scenarios]
rows=[]
for m in allcatalog:
    rows.append(f'''VAR _Obtido = CALCULATE([{m['Nome']}],_Datas,_FiltroFilial)
VAR _Fonte = FILTER(ALL('vw_dre_comparativo'), 'vw_dre_comparativo'[ordem_dre]={m['Posicao']} && 'vw_dre_comparativo'[competencia]>=_Inicio && 'vw_dre_comparativo'[competencia]<_Fim && (_Grupo="Consolidado" || 'vw_dre_comparativo'[cod_filial]=_Grupo || (_Grupo="01+02" && 'vw_dre_comparativo'[cod_filial] IN {{"01","02"}})))
VAR _Esperado = SUMX(_Fonte,'vw_dre_comparativo'[{m['Coluna']}])
RETURN ROW("Medida","{m['Nome']}","Posicao",{m['Posicao']},"Cenario","{m['Cenario']}","Obtido",_Obtido,"EsperadoView",_Esperado,"Diferenca",IF(NOT ISBLANK(_Obtido) && NOT ISBLANK(_Esperado),_Obtido-_Esperado),"Aprovado",IF(ISBLANK(_Esperado),ISBLANK(_Obtido),NOT ISBLANK(_Obtido) && ABS(_Obtido-_Esperado)<=0.01))''')
write('02-filiais-periodos-conciliacao.dax',prefix+',\n'.join(rows)+'))\nORDER BY [GrupoFilial],[Periodo],[Posicao],[Cenario]')
rows=[]
for m in catalog:
    pos=m['Posicao']; other=2 if pos==1 else 1
    filters=[('SemFiltro',''),('UnicaAlvo',f",KEEPFILTERS('vw_dre_comparativo'[ordem_dre]={pos})"),('UnicaConflitante',f",KEEPFILTERS('vw_dre_comparativo'[ordem_dre]={other})"),('MultiplasInclui',f",KEEPFILTERS('vw_dre_comparativo'[ordem_dre] IN {{{pos},13}})"),('MultiplasExclui',",KEEPFILTERS('vw_dre_comparativo'[ordem_dre] IN {8,11})"),('DescricaoAlvo',f",KEEPFILTERS(FILTER(ALL('vw_dre_comparativo'[descricao_dre]),'vw_dre_comparativo'[descricao_dre] IN SELECTCOLUMNS(FILTER(ALL('vw_dre_comparativo'),'vw_dre_comparativo'[ordem_dre]={pos}),\"Rotulo\",'vw_dre_comparativo'[descricao_dre])))"),('DescricaoConflitante',",KEEPFILTERS('vw_dre_comparativo'[descricao_dre]=\"= EBITDA\")"),('SemDados',",KEEPFILTERS('vw_dre_comparativo'[ordem_dre]=999999)")]
    for label,filt in filters:
        expected='BLANK()' if label in ('UnicaConflitante','MultiplasExclui','DescricaoConflitante','SemDados') else f"CALCULATE(SUM('vw_dre_comparativo'[{m['Coluna']}] ),'vw_dre_comparativo'[ordem_dre]={pos})"
        rows.append(f'''VAR _V=CALCULATE([{m['Nome']}]{filt}) VAR _E={expected}
RETURN ROW("Medida","{m['Nome']}","Contexto","{label}","Obtido",_V,"Esperado",_E,"Aprovado",IF(ISBLANK(_E),ISBLANK(_V),NOT ISBLANK(_V) && ABS(_V-_E)<=0.01))''')
write('03-posicao-descricao-contextos.dax','EVALUATE UNION(\n'+',\n'.join(rows)+')')
columns=',\n'.join(f'"M{i:02d}",[{m["Nome"]}]' for i,m in enumerate(catalog,7))
write('04-matriz-totais.dax',"EVALUATE SUMMARIZECOLUMNS(ROLLUPADDISSUBTOTAL('vw_dre_comparativo'[ordem_dre],\"TotalGeral\"),\"LinhasFonte\",COUNTROWS('vw_dre_comparativo'),\n"+columns+')')
rows=[]
for m in catalog:
    rows.append(f'''VAR _C=[{m['Nome']}] VAR _S=SUMX(VALUES('dim_filial'[cod_filial]),CALCULATE([{m['Nome']}]))
RETURN ROW("Medida","{m['Nome']}","Consolidado",_C,"SomaFiliais",_S,"Aprovado",IF(ISBLANK(_C),ISBLANK(_S),NOT ISBLANK(_S) && ABS(_C-_S)<=0.01))''')
write('05-aditividade-filiais.dax','EVALUATE UNION('+',\n'.join(rows)+')')
write('06-ebitda-ebit.dax',"EVALUATE CALCULATETABLE(SUMMARIZECOLUMNS('vw_dre_comparativo'[ordem_dre],'vw_dre_comparativo'[descricao_dre],\"LinhasFonte\",COUNTROWS('vw_dre_comparativo'),\n"+columns+"),KEEPFILTERS('vw_dre_comparativo'[ordem_dre] IN {8,11}))")
for n,src in [('07-regressao-controle.dax','02-controle-integral.dax'),('08-regressao-bases.dax','05-contextos-e-totais.dax'),('09-materializacao.dax','10-materializacao.dax')]:
    (tests/n).write_bytes((root/'docs/testes/lote2-1'/src).read_bytes())
# Independent SQL: same keys and cuts as query 02, no sign adjustment or NULL replacement.
sql='''-- Somente SELECT. NÃO EXECUTADO nesta entrega. Exportar resultado completo sem arredondar valores.
-- Usar a mesma atualização de dados do modelo Power BI; não comparar estados diferentes.
WITH periodos(periodo,inicio,fim) AS (VALUES
'''+',\n'.join(f"('{p}',DATE '{str(i)[:4]}-{str(i)[4:6]}-{str(i)[6:]}',DATE '{str(e)[:4]}-{str(e)[4:6]}-{str(e)[6:]}')" for p,i,e in periods)+'''),
grupos(grupo_filial) AS (VALUES ('Consolidado'),('01'),('02'),('03'),('01+02')),
posicoes(posicao) AS (VALUES (1),(2),(3),(4),(5),(6),(7),(9),(10),(12),(13)),
cenarios(cenario) AS (VALUES ('Realizado'),('Orçado'),('Previsto'))
SELECT g.grupo_filial,p.periodo,o.posicao,c.cenario,
 COUNT(v.ordem_dre) AS linhas_fonte,
 SUM(CASE c.cenario WHEN 'Realizado' THEN v.realizado WHEN 'Orçado' THEN v.orcado ELSE v.previsto END) AS valor,
 COUNT(CASE c.cenario WHEN 'Realizado' THEN v.realizado WHEN 'Orçado' THEN v.orcado ELSE v.previsto END) AS valores_presentes
FROM grupos g CROSS JOIN periodos p CROSS JOIN posicoes o CROSS JOIN cenarios c
LEFT JOIN workspace.gold.vw_dre_comparativo v
 ON v.ordem_dre=o.posicao AND v.competencia>=p.inicio AND v.competencia<p.fim
 AND (g.grupo_filial='Consolidado' OR v.cod_filial=g.grupo_filial OR (g.grupo_filial='01+02' AND v.cod_filial IN ('01','02')))
GROUP BY g.grupo_filial,p.periodo,o.posicao,c.cenario
ORDER BY g.grupo_filial,p.periodo,o.posicao,c.cenario;
'''
(tests/'10-referencia-databricks.sql').write_text(sql,encoding='utf-8')
print(f'Contratos salvos antes da edição; {len(catalog)} medidas inseridas e nove DAX + SQL preparados em {tests}')
