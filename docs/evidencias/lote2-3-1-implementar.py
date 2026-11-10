"""Implementação autorizada após fechamento/backup. Não abre nem grava serviço tabular."""
from pathlib import Path
from datetime import date
import json, uuid, hashlib, re

root=Path(__file__).resolve().parents[2]
prep=json.loads((root/'docs/evidencias/lote2-3-1-implementacao-atual.json').read_text())
backup=Path(prep['backup'])/'restauracao-teste'
ev=Path(prep['evidence'])
manifest=json.loads((root/'docs/cobertura-temporal-didatica.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(root/'BaseDados.xlsx')==manifest['sha256_arquivo']
folder=root/'DRE Moderno - Databricks.SemanticModel/definition'
measures=folder/'tables/_Medidas.tmdl'
old=measures.read_bytes()
assert old==(backup/measures.relative_to(root)).read_bytes()
assert len(re.findall(rb'(?m)^\s*measure ',old))==36
assert not (folder/'tables/_ConfigCobertura.tmdl').exists()
uid=lambda:str(uuid.uuid4())
cols=[('cod_filial','string'),('cenario','string'),('inicio_competencia','dateTime'),
      ('fim_competencia','dateTime'),('versao_contrato','string'),('hash_base','string'),('estado','string')]
text='table _ConfigCobertura\n\tisHidden\n\tlineageTag: '+uid()+'\n'
for name,typ in cols:
    text+=f'\n\tcolumn {name}\n\t\tdataType: {typ}\n\t\tisHidden\n\t\tlineageTag: {uid()}\n\t\tsummarizeBy: none\n\t\tsourceColumn: [{name}]\n'
    if typ=='dateTime': text+='\t\tformatString: yyyy-MM-dd\n'
text+='\n\tpartition _ConfigCobertura = calculated\n\t\tmode: import\n\t\tsource =\n\t\t\tDATATABLE (\n'
for name,typ in cols:
    text+=f'\t\t\t\t"{name}", '+('DATETIME' if typ=='dateTime' else 'STRING')+',\n'
text+='\t\t\t\t{\n'
rows=[]
for r in manifest['intervalos']:
    start=date.fromisoformat(r['inicio_competencia']); end=date.fromisoformat(r['fim_competencia'])
    rows.append(f'{{ "{r["cod_filial"]}", "{r["cenario"]}", "{start.isoformat()} 00:00:00", "{end.isoformat()} 00:00:00", "{manifest["versao"]}", "{manifest["sha256_arquivo"]}", "{r["estado"]}" }}')
text+=',\n'.join('\t\t\t\t\t'+r for r in rows)+'\n\t\t\t\t}\n\t\t\t)\n'

common='''VAR _Filiais = SELECTCOLUMNS ( VALUES ( 'dim_filial'[cod_filial] ), "__Filial", 'dim_filial'[cod_filial] )
VAR _Datas = VALUES ( 'dim_calendario'[data] )
VAR _Meses = SELECTCOLUMNS ( VALUES ( 'dim_calendario'[inicio_mes] ), "__Mes", 'dim_calendario'[inicio_mes] )
VAR _Cfg = ALL ( '_ConfigCobertura' )
VAR _Versao = CONCATENATEX ( DISTINCT ( '_ConfigCobertura'[versao_contrato] ), '_ConfigCobertura'[versao_contrato], ", " )
VAR _CfgInvalida =
    COUNTROWS ( _Cfg ) = 0
    || CALCULATE ( DISTINCTCOUNT ( '_ConfigCobertura'[versao_contrato] ), REMOVEFILTERS ( '_ConfigCobertura' ) ) <> 1
    || CALCULATE ( DISTINCTCOUNT ( '_ConfigCobertura'[hash_base] ), REMOVEFILTERS ( '_ConfigCobertura' ) ) <> 1
    || COUNTROWS ( FILTER ( _Cfg,
        ISBLANK ( '_ConfigCobertura'[inicio_competencia] ) || ISBLANK ( '_ConfigCobertura'[fim_competencia] )
        || '_ConfigCobertura'[inicio_competencia] > '_ConfigCobertura'[fim_competencia]
        || DAY ( '_ConfigCobertura'[inicio_competencia] ) <> 1 || DAY ( '_ConfigCobertura'[fim_competencia] ) <> 1
        || '_ConfigCobertura'[estado] <> "FORNECIDO_DIDATICO"
        || ISBLANK ( '_ConfigCobertura'[versao_contrato] ) || ISBLANK ( '_ConfigCobertura'[hash_base] ) ) ) > 0
VAR _MesParcial = COUNTROWS ( FILTER ( _Meses,
    VAR _M = [__Mes]
    RETURN COUNTROWS ( FILTER ( _Datas, 'dim_calendario'[data] >= _M && 'dim_calendario'[data] <= EOMONTH ( _M, 0 ) ) ) <> DAY ( EOMONTH ( _M, 0 ) ) ) ) > 0
VAR _SemConfiguracao = COUNTROWS ( FILTER ( _Filiais,
    VAR _F = [__Filial]
    RETURN COUNTROWS ( FILTER ( _Cfg, '_ConfigCobertura'[cod_filial] = _F && '_ConfigCobertura'[cenario] = "Realizado" ) ) = 0 ) ) > 0
VAR _Grade = ADDCOLUMNS ( CROSSJOIN ( _Filiais, _Meses ),
'''
for scen,alias in [('Realizado','R'),('Orcado','O'),('Previsto','P')]:
    common+=f'''    "__{alias}", VAR _F = [__Filial] VAR _M = [__Mes]
        RETURN COUNTROWS ( FILTER ( _Cfg, '_ConfigCobertura'[cod_filial] = _F && '_ConfigCobertura'[cenario] = "{scen}"
            && '_ConfigCobertura'[inicio_competencia] <= _M && '_ConfigCobertura'[fim_competencia] >= _M ) ){',' if alias!='P' else ' )'}
'''
common+='''VAR _Cortes = ADDCOLUMNS ( _Filiais, "__Corte",
    VAR _F = [__Filial] RETURN MAXX ( FILTER ( _Grade, [__Filial] = _F && [__R] = 1 ), [__Mes] ) )
VAR _SemCobertura = COUNTROWS ( FILTER ( _Cortes, ISBLANK ( [__Corte] ) ) ) > 0
VAR _Corte = MINX ( _Cortes, [__Corte] )
VAR _Pares = FILTER ( _Grade, NOT ISBLANK ( _Corte ) && [__Mes] <= _Corte )
VAR _Lacuna = COUNTROWS ( FILTER ( _Pares, [__R] <> 1 ) ) > 0
VAR _FaltaCfgO = COUNTROWS ( FILTER ( _Pares, [__O] <> 1 ) ) > 0
VAR _FaltaCfgP = COUNTROWS ( FILTER ( _Pares, [__P] <> 1 ) ) > 0
VAR _PosicaoValida = HASONEVALUE ( 'vw_dre_comparativo'[ordem_dre] )
    && NOT ISBLANK ( SELECTEDVALUE ( 'vw_dre_comparativo'[descricao_dre] ) )
    && NOT CONTAINSSTRING ( SELECTEDVALUE ( 'vw_dre_comparativo'[descricao_dre] ), "EBIT" )
VAR _ContextoInvalido = _CfgInvalida || _SemConfiguracao || _MesParcial || _Lacuna
    || COUNTROWS ( _Filiais ) = 0 || COUNTROWS ( _Meses ) = 0 || NOT _PosicaoValida
VAR _Mascara = SELECTCOLUMNS ( _Pares, "__F", [__Filial], "__M", [__Mes] )
'''
common+='VAR _Dados = ADDCOLUMNS ( _Pares,\n'
for name,alias in [('Realizado','R'),('Orçado','O'),('Previsto','P')]:
    common+=f'''    "__V{alias}", VAR _F = [__Filial] VAR _M = [__Mes]
        RETURN CALCULATE ( [DRE | {name}], KEEPFILTERS ( TREATAS ( {{ ( _F, _M ) }}, 'vw_dre_comparativo'[cod_filial], 'vw_dre_comparativo'[competencia] ) ) ){',' if alias!='P' else ' )'}
'''
common+='''VAR _FaltaR = COUNTROWS ( FILTER ( _Dados, ISBLANK ( [__VR] ) ) ) > 0
VAR _FaltaO = _FaltaCfgO || COUNTROWS ( FILTER ( _Dados, ISBLANK ( [__VO] ) ) ) > 0
VAR _FaltaP = _FaltaCfgP || COUNTROWS ( FILTER ( _Dados, ISBLANK ( [__VP] ) ) ) > 0
'''
expressions=[]
for name,alias in [('Realizado','R'),('Orçado','O'),('Previsto','P')]:
    guard=' || _Falta'+alias if alias!='R' else ''
    expressions.append((f'DRE | {name} Comparável',common+f'''RETURN
    IF ( _ContextoInvalido || _SemCobertura || COUNTROWS ( _Pares ) = 0 || _FaltaR{guard}, BLANK (),
        CALCULATE ( [DRE | {name}], KEEPFILTERS ( TREATAS ( _Mascara, 'vw_dre_comparativo'[cod_filial], 'vw_dre_comparativo'[competencia] ) ) ) )''','R$ #,##0.00;(R$ #,##0.00);R$ 0.00'))
expressions.append(('DRE | Pares Filial-Competência Comparáveis',common+'''RETURN
    IF ( _ContextoInvalido, BLANK (), IF ( _SemCobertura, 0, COUNTROWS ( _Pares ) + 0 ) )''','0'))
expressions.append(('DRE | Status Comparabilidade',common+'''RETURN
    "Cobertura didática | " & _Versao & " | " &
    SWITCH ( TRUE (),
        _CfgInvalida, "Configuração inválida",
        _SemConfiguracao, "Filial sem configuração",
        COUNTROWS ( _Filiais ) = 0 || COUNTROWS ( _Meses ) = 0, "Seleção vazia",
        _MesParcial, "Selecione meses completos",
        NOT _PosicaoValida, "Selecione uma posição DRE elegível; EBITDA/EBIT sem cálculo",
        _Lacuna, "Lacuna ou conflito de cobertura",
        _SemCobertura || COUNTROWS ( _Pares ) = 0, "Sem Realizado fornecido no período selecionado",
        _FaltaR, "Realizado ausente/incompleto na posição; cobertura não é movimento",
        _FaltaO && _FaltaP, "Orçado e Previsto incompletos no recorte",
        _FaltaO, "Orçado incompleto no recorte",
        _FaltaP, "Previsto incompleto no recorte",
        COUNTROWS ( _Pares ) < COUNTROWS ( _Filiais ) * COUNTROWS ( _Meses ), "Recorte comparável parcial; corte comum " & FORMAT ( _Corte, "yyyy-MM" ),
        "Período integralmente comparável; corte comum " & FORMAT ( _Corte, "yyyy-MM" ) )''',None))
new='\n'
for name,expr,fmt in expressions:
    new+=f'\n\t/// Cobertura DIDÁTICA configurável. Não certifica fechamento contábil; preserva BLANK, seleção e valores ajustados.\n\tmeasure \'{name}\' =\n'
    new+='\n'.join('\t\t\t'+line for line in expr.splitlines())+'\n'
    if fmt:new+='\t\tformatString: '+fmt+'\n'
    new+='\t\tdisplayFolder: DRE\\Comparabilidade\n\t\tlineageTag: '+uid()+'\n'
assert all('2023' not in expr for _,expr,_ in expressions)
assert all('tipolancamento' not in expr for _,expr,_ in expressions)
(folder/'tables/_ConfigCobertura.tmdl').write_text(text,encoding='utf-8',newline='\n')
# Inserir antes da coluna auxiliar; preservar integralmente cada bloco antigo.
oldtext=old.decode('utf-8-sig')
anchor='\tcolumn _Organizacao'
assert anchor in oldtext
updated=oldtext.replace(anchor,new+'\n'+anchor,1)
measures.write_bytes(updated.encode('utf-8'))
model=folder/'model.tmdl'; m=model.read_text(encoding='utf-8-sig')
assert 'ref table _ConfigCobertura' not in m
model.write_text(m.replace('ref table _Medidas','ref table _Medidas\nref table _ConfigCobertura',1),encoding='utf-8',newline='\n')
(ev/'expressoes-novas.json').write_text(json.dumps([{'nome':n,'expressao':e} for n,e,_ in expressions],ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'tabela':'_ConfigCobertura','intervalos':len(rows),'medidas':[x[0] for x in expressions],'backup':str(backup)},ensure_ascii=False))
