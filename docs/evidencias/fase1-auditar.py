"""Auditoria estática de arquivos TMDL deste projeto. Não compila TMDL nem executa SQL/DAX."""
import collections
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/evidencias/fase1'
OUT.mkdir(exist_ok=True)
MODEL = ROOT / 'DRE Moderno - Databricks.SemanticModel/definition'

def write(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def prop(body, name, indent=2):
    m = re.search(r'^' + '\t' * indent + re.escape(name) + r': (.+)$', body, re.M)
    return m.group(1).strip() if m else None

files = sorted(p for p in ROOT.rglob('*') if p.is_file() and p.relative_to(ROOT).parts[0] not in ('backups', 'docs', '.git'))
baseline = [{'path': p.relative_to(ROOT).as_posix(), 'bytes': p.stat().st_size, 'sha256': sha(p)} for p in files]
write('baseline-entrada.json', baseline)
f0 = json.loads((ROOT / 'docs/evidencias/fase0-20261102-145703/inventario-arquivos.json').read_text(encoding='utf-8-sig'))
comparison = []
for entry in f0:
    if entry['Path'] == 'PLANS.md':
        continue
    p = ROOT / entry['Path']
    comparison.append({'path': entry['Path'], 'exists': p.exists(), 'same_as_f0': p.exists() and sha(p) == entry['SHA256']})
write('comparacao-fase0.json', comparison)
tables = []
columns = {}
for file in sorted((MODEL / 'tables').glob('*.tmdl')):
    raw = file.read_text(encoding='utf-8-sig')
    name = re.search(r'^table (.+)$', raw, re.M).group(1).strip()
    col_list = []
    for m in re.finditer(r'^\tcolumn ([^\n]+)\n(.*?)(?=^\t\S|\Z)', raw, re.M | re.S):
        declaration, body = m.groups()
        col_name = declaration.split(' = ', 1)[0].strip("'")
        c = {'name': col_name, 'line': raw[:m.start()].count('\n')+1, 'dataType': prop(body, 'dataType'),
             'sourceColumn': prop(body, 'sourceColumn'), 'summarizeBy': prop(body, 'summarizeBy'),
             'formatString': prop(body, 'formatString'), 'sortByColumn': prop(body, 'sortByColumn'),
             'dataCategory': prop(body, 'dataCategory'), 'displayFolder': prop(body, 'displayFolder'),
             'isHiddenExplicit': bool(re.search(r'^\t\tisHidden(?:\s|$)', body, re.M)),
             'isKeyExplicit': bool(re.search(r'^\t\tisKey(?:\s|$)', body, re.M)),
             'isNullable': prop(body, 'isNullable'), 'lineageTag': prop(body, 'lineageTag')}
        col_list.append(c)
        columns[f'{name}.{col_name}'] = c
    tables.append({'name': name, 'path': file.relative_to(ROOT).as_posix(), 'technical': name.startswith(('LocalDateTable_', 'DateTableTemplate_')),
                   'isHiddenExplicit': bool(re.search(r'^\tisHidden(?:\s|$)', raw, re.M)),
                   'tableDataCategory': prop(raw, 'dataCategory', 1),
                   'columns': col_list, 'partitionMode': re.findall(r'^\t\tmode: (.+)$', raw, re.M),
                   'lineageTag': prop(raw, 'lineageTag', 1),
                   'measureDeclarations': re.findall(r'^\tmeasure (.+)$', raw, re.M),
                   'hierarchies': re.findall(r'^\thierarchy (.+)$', raw, re.M),
                   'variationRelationships': re.findall(r'^\t\t\trelationship: (.+)$', raw, re.M),
                   'MHasSignOrNullTransformation': bool(re.search(r'Table\.(TransformColumns|AddColumn|ReplaceValue)|Value\.NativeQuery|COALESCE', raw, re.I))})
write('tabelas-colunas.json', tables)
rels = []
raw = (MODEL / 'relationships.tmdl').read_text(encoding='utf-8-sig')
for m in re.finditer(r'^relationship (\S+)\n(.*?)(?=^relationship |\Z)', raw, re.M | re.S):
    rid, body = m.groups()
    props = dict(re.findall(r'^\t(\w+): (.+)$', body, re.M))
    fc, tc = props['fromColumn'], props['toColumn']
    rels.append({'id': rid, 'line': raw[:m.start()].count('\n')+1, 'from': fc, 'to': tc,
                 'technical': 'LocalDateTable_' in tc, 'properties': props,
                 'activeExplicit': props.get('isActive'), 'activeAssumedForGraph': props.get('isActive') != 'false',
                 'cardinalityDeclared': [props.get('fromCardinality'), props.get('toCardinality')],
                 'directionDeclared': props.get('crossFilteringBehavior'),
                 'fromExists': fc in columns, 'toExists': tc in columns,
                 'fromType': columns.get(fc, {}).get('dataType'), 'toType': columns.get(tc, {}).get('dataType'),
                 'typesMatch': fc in columns and tc in columns and columns[fc]['dataType'] == columns[tc]['dataType']})
write('relacionamentos.json', rels)

# Grapho CONDICIONAL: isActive omitido tratado ativo; oneDirection To -> From.
# Não representa prova dos valores efetivos no mecanismo.
def graph(include_inactive=False):
    g = collections.defaultdict(list)
    for r in rels:
        if r['activeAssumedForGraph'] or include_inactive:
            g[r['to'].split('.')[0]].append((r['from'].split('.')[0], r['id']))
    return g

def paths(g, source, target, visited=()):
    if source == target:
        return [[]]
    result = []
    for nxt, rid in g[source]:
        if nxt not in visited and nxt != source:
            for tail in paths(g, nxt, target, visited + (source,)):
                result.append([rid] + tail)
    return result

names = [t['name'] for t in tables]
g = graph()
reachability = [{'source': s, 'target': t, 'paths': paths(g, s, t)} for s in names for t in names if s != t]
write('caminhos-condicionais.json', {'assumptions': 'Relações omitindo isActive tratadas ativas; direção única To -> From em todas. Sem runtime.', 'paths': reachability})
multiple = [p for p in reachability if len(p['paths']) > 1]
g_all = graph(True)
inactive_multiple = [{'source': 'dim_filial', 'target': t, 'paths': paths(g_all, 'dim_filial', t)} for t in ('fato_lancamentos', 'fato_orcamento', 'fato_previsao')]
duplicates = [v for v in collections.Counter((r['from'],r['to']) for r in rels).items() if v[1] > 1]
duplicate_ids = [k for k,v in collections.Counter(r['id'] for r in rels).items() if v > 1]
lineages = []
for p in MODEL.rglob('*.tmdl'):
    lineages.extend(re.findall(r'^\s*lineageTag: (\S+)', p.read_text(encoding='utf-8-sig'), re.M))
duplicate_lineages = [k for k,v in collections.Counter(lineages).items() if v > 1]
model_raw = (MODEL / 'model.tmdl').read_text(encoding='utf-8-sig')
refs = re.findall(r'^ref table (.+)$', model_raw, re.M)
json_results = []
for p in files:
    if '.pbi' not in p.parts and (p.suffix in ('.json','.pbip','.pbir','.pbism') or p.name == '.platform'):
        obj = json.loads(p.read_text(encoding='utf-8-sig'))
        json_results.append({'path':p.relative_to(ROOT).as_posix(), 'parse':'OK', 'schema':obj.get('$schema')})
write('json-sintaxe.json', json_results)
ref_checks = [{'table':t['name'], 'relationship':r, 'exists':any(x['id']==r for x in rels)} for t in tables for r in t['variationRelationships']]
write('referencias-variations.json', ref_checks)
summary = {'timestamp': datetime.now().astimezone().isoformat(), 'scope':'Fase 1: somente leitura de fontes e auditoria estática',
           'tableCount': len(tables), 'businessTableCount':sum(not t['technical'] for t in tables),
           'businessColumnCount':sum(len(t['columns']) for t in tables if not t['technical']),
           'relationshipCount':len(rels), 'businessRelationships':sum(not r['technical'] for r in rels),
           'businessActiveAssumed':sum(not r['technical'] and r['activeAssumedForGraph'] for r in rels),
           'explicitInactive':sum(r['activeExplicit']=='false' for r in rels),
           'endpointErrors':[r['id'] for r in rels if not r['fromExists'] or not r['toExists']],
           'typeMismatch':[r['id'] for r in rels if not r['typesMatch']],
           'duplicateRelationshipPairs':duplicates, 'duplicateRelationshipIds':duplicate_ids, 'duplicateLineageTags':duplicate_lineages,
           'missingTableRefs':sorted(set(refs)-set(names)), 'tablesWithoutModelRef':sorted(set(names)-set(refs)),
           'variationReferenceErrors':[r for r in ref_checks if not r['exists']],
           'multipleActivePathsConditional':multiple, 'pathsIfInactiveActivated':inactive_multiple,
           'measureCount':sum(len(t['measureDeclarations']) for t in tables),
           'JSONParseCount':len(json_results), 'sameAsF0':sum(x['same_as_f0'] for x in comparison), 'comparedF0':len(comparison),
           'rowDataTests':'Não executados; sem sessão tabular/Databricks autenticada disponível',
           'phase1Status':'Bloqueado: chaves/integridade/filtros não comprovados; contrato de linha DRE e de detalhe por conta pendente',
           'phase2Status':'Não iniciada'}
write('resultado.json', summary)
print(json.dumps(summary, ensure_ascii=False, indent=2))
