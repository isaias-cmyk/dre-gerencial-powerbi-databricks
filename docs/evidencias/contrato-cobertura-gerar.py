"""Inspeção local de XLSX e matriz documental; não acessa nem altera Databricks/PBIP."""
import csv, hashlib, json, re, zipfile, posixpath
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter
from xml.etree import ElementTree as ET

root = Path(__file__).resolve().parents[2]
out = root / 'docs/evidencias/contrato-cobertura-20261102'
out.mkdir(exist_ok=True)
book = root / 'BaseDados.xlsx'
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
before = digest(book)
ns = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
rid = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
pattern = re.compile(r'fechamento|fechado|completude|manifesto|sem movimento|n[aã]o carregad|certific|pipeline|processad', re.I)
sheets, hits = [], []
with zipfile.ZipFile(book) as z:
    wb = ET.fromstring(z.read('xl/workbook.xml'))
    rels = {r.get('Id'): r.get('Target') for r in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
    shared = [''.join(e.itertext()) for e in ET.fromstring(z.read('xl/sharedStrings.xml'))]
    props = ET.fromstring(z.read('docProps/core.xml'))
    core = {e.tag.split('}')[-1]: e.text for e in props}
    date1904 = wb.find('m:workbookPr', ns)
    is1904 = date1904 is not None and date1904.get('date1904') in ('1', 'true')
    epoch = datetime(1904, 1, 1) if is1904 else datetime(1899, 12, 30)
    for sh in wb.find('m:sheets', ns):
        name = sh.get('name')
        target = rels[sh.get(rid)]
        path = target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/' + target)
        xml = ET.fromstring(z.read(path))
        rows = []
        for row in xml.findall('m:sheetData/m:row', ns):
            cells = {}
            for c in row.findall('m:c', ns):
                val = c.findtext('m:v', default='', namespaces=ns)
                if c.get('t') == 's':
                    val = shared[int(val)] if val else ''
                elif c.get('t') == 'inlineStr':
                    val = ''.join(c.find('m:is', ns).itertext())
                cells[re.sub(r'\d', '', c.get('r'))] = val
                if pattern.search(val):
                    hits.append({'aba': name, 'celula': c.get('r'), 'texto': val[:300]})
            if any(cells.values()):
                rows.append(cells)
        header = rows[0] if rows else {}
        months = Counter()
        invalid = 0
        compcol = next((k for k, v in header.items() if v == 'competencia_data'), None)
        if compcol:
            for row in rows[1:]:
                try:
                    dt = epoch + timedelta(days=float(row.get(compcol, '')))
                    months[dt.strftime('%Y-%m')] += 1
                except (ValueError, OverflowError):
                    invalid += 1
        sheets.append({'aba': name, 'visibilidade': sh.get('state', 'visible'),
                       'cabecalho': header, 'linhas_nao_vazias_sem_cabecalho': max(len(rows)-1, 0),
                       'competencias': dict(sorted(months.items())), 'datas_nao_interpretadas': invalid})
    special = [n for n in z.namelist() if any(t in n.lower() for t in ['custom', 'comment', 'signature', 'external', 'vba'])]
    binary_meta = {'arquivo': 'xl/metadata', 'tamanho_bytes': len(z.read('xl/metadata')),
                   'interpretado': False} if 'xl/metadata' in z.namelist() else None
facts = {'arquivo': 'BaseDados.xlsx', 'sha256': before, 'propriedades_core': core,
         'epoca_excel': str(epoch.date()), 'abas': sheets, 'ocorrencias_termos_controle': hits,
         'partes_especiais': special, 'metadata_binario': binary_meta,
         'limites': 'Copia local; identidade com arquivo ingerido nao certificada; ausencia de termos nao prova ausencia de controle externo.'}
(out/'inspecao-arquivo-produtor.json').write_text(json.dumps(facts, ensure_ascii=False, indent=2), encoding='utf-8')

src = root/'docs/evidencias/competencias-exportacoes-20261102/New_Query_2026_11_02_15_53_51 (3).csv'
with src.open(encoding='utf-8-sig', newline='') as f:
    observed = list(csv.DictReader(f))
lookup = {(r['cod_filial'], r['competencia'][:7]): int(r['qtd_lancamentos']) for r in observed}
assert len(lookup) == len(observed) == 87
matrix = []
for branch in ('01', '02', '03'):
    for year in (2021, 2022, 2023):
        for month in range(1, 13):
            key = (branch, f'{year}-{month:02d}')
            count = lookup.get(key)
            matrix.append({'filial': branch, 'competencia': key[1]+'-01', 'cenario': 'Realizado',
                           'observacao': 'DADOS_OBSERVADOS' if count is not None else 'SEM_LANCAMENTOS_OBSERVADOS',
                           'quantidade_exportada': count,
                           'carga_completa_certificada': 'DESCONHECIDA',
                           'processada_sem_movimento_certificada': 'DESCONHECIDA',
                           'nao_carregada_confirmada': 'DESCONHECIDA',
                           'fechamento_contabil_certificado': 'DESCONHECIDO',
                           'evidencia': 'E01' if count is not None else 'E02',
                           'origem_certificacao': 'NAO_RECEBIDA',
                           'pendencia': 'P1/P2/P3/P4' if count is not None else 'P1/P2/P3/P4/P5'})
with (out/'matriz-108.csv').open('w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=matrix[0].keys())
    writer.writeheader(); writer.writerows(matrix)
assert len(matrix) == 108 and sum(r['quantidade_exportada'] is None for r in matrix) == 21
assert sum(r['quantidade_exportada'] or 0 for r in matrix) == 3741
assert before == digest(book)
summary = {'pares': 108, 'com_lancamentos': 87, 'sem_lancamentos_observados': 21,
           'certificacoes_completude_recebidas': 0, 'certificacoes_sem_movimento_recebidas': 0,
           'declaracoes_nao_carregada_recebidas': 0, 'certificacoes_fechamento_recebidas': 0,
           'copia_excel_preservada_sha256': before, 'xlsx_abas': len(sheets),
           'origem_csv_sha256': digest(src), 'sql_remoto_executado': 0}
(out/'validacao.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
# Matriz no corpo do contrato, sem substituir as seções redigidas manualmente.
table = ['| Filial | Competência | Observação / qtd. exportada | Carga completa | Sem movimento certificado | Não carregada confirmada | Fechamento | Evidência | Certificador | Pendências |',
         '| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |']
for r in matrix:
    obs = f"Dados observados / {r['quantidade_exportada']}" if r['quantidade_exportada'] is not None else 'Sem lançamentos observados / ausente no CSV'
    table.append(f"| {r['filial']} | {r['competencia']} | {obs} | Desconhecida | Desconhecido | Desconhecida | Desconhecido | {r['evidencia']} | Não recebido | {r['pendencia']} |")
(out/'matriz-108.md').write_text('\n'.join(table)+'\n', encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False))
