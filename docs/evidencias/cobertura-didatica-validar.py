"""Validação documental e simulação de conjuntos; não implementa/valida DAX."""
from pathlib import Path
from datetime import date
import hashlib, json, csv

root = Path(__file__).resolve().parents[2]
out = root/'docs/evidencias/cobertura-didatica-20261103'
out.mkdir(exist_ok=True)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
expected = '27e02e7148984d74acdb5cf086a9ba637c55617152793f23509d3bad24bce04b'
assert sha(root/'BaseDados.xlsx') == expected
manifest = {
    'id': 'DRE-TREINAMENTO-COBERTURA', 'versao': 'DIDATICA-1.0-20261103',
    'data_convencao': '2026-11-03', 'origem': 'Declaracao explicita do usuario nesta conversa',
    'natureza': 'PREMISSA_DIDATICA', 'arquivo': 'BaseDados.xlsx',
    'versao_arquivo_local': 'TREINAMENTO-20261103-HASH-27e02e714898',
    'sha256_arquivo': expected, 'certificacao_tecnica_completude': None,
    'fechamento_contabil_real': None, 'universo_inicio': '2021-01-01',
    'universo_fim': '2023-12-01',
    'estado_realizado_fora_intervalo_no_universo': 'NAO_FORNECIDO_DIDATICO',
    'fora_universo': 'NAO_DEFINIDO', 'intervalos': []}
for branch in ('01', '02', '03'):
    for scenario in ('Realizado', 'Orcado', 'Previsto'):
        manifest['intervalos'].append({'cod_filial': branch, 'cenario': scenario,
            'inicio_competencia': '2021-01-01',
            'fim_competencia': '2023-05-01' if scenario == 'Realizado' else '2023-12-01',
            'estado': 'FORNECIDO_DIDATICO'})
target = root/'docs/cobertura-temporal-didatica.json'
target.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
months = [date(y,m,1).isoformat() for y in (2021,2022,2023) for m in range(1,13)]
coverage = {}
for r in manifest['intervalos']:
    key = r['cod_filial'],r['cenario']
    assert key not in coverage
    coverage[key] = {m for m in months if r['inicio_competencia'] <= m <= r['fim_competencia']}
    assert date.fromisoformat(r['inicio_competencia']).day == 1
    assert date.fromisoformat(r['fim_competencia']).day == 1
assert sum(len(coverage[(b,'Realizado')]) for b in ('01','02','03')) == 87
for scenario in ('Orcado','Previsto'):
    assert sum(len(coverage[(b,scenario)]) for b in ('01','02','03')) == 108
def pairs(branches, selected, conf=coverage):
    selected = set(selected)
    available = [conf.get((b,'Realizado'),set()) & selected for b in branches]
    if not available or any(not s for s in available):
        return set()
    cutoff = min(max(s) for s in available)
    allowed = {m for m in selected if m <= cutoff}
    if any(not allowed <= s for s in available):
        return set()  # lacuna interna bloqueia contexto; não é fórmula DAX
    return {(b,m) for b in branches for m in allowed}
allb = ('01','02','03')
cases = [('integral',allb,months,87),
         ('2021',allb,[m for m in months if m.startswith('2021')],36),
         ('2022',allb,[m for m in months if m.startswith('2022')],36),
         ('2023',allb,[m for m in months if m.startswith('2023')],15),
         ('jun_dez_2023',allb,[m for m in months if '2023-06' <= m],0),
         ('filial_01',('01',),months,29),
         ('filiais_01_02',('01','02'),months,58),
         ('descontinuo_jan_mar_2023',allb,['2023-01-01','2023-03-01'],6),
         ('filial_nao_configurada',('04',),months,0)]
results = []
for name,branches,selected,expected_count in cases:
    actual = len(pairs(branches,selected))
    assert actual == expected_count
    results.append({'caso':name,'pares_esperados':expected_count,'pares_obtidos':actual,'aprovado':True})
with (root/'docs/evidencias/contrato-cobertura-20261102/matriz-108.csv').open(encoding='utf-8-sig') as f:
    matrix = list(csv.DictReader(f))
for row in matrix:
    row['cobertura_didatica'] = ('FORNECIDO_DIDATICO' if row['competencia'] in coverage[(row['filial'],'Realizado')]
                                 else 'NAO_FORNECIDO_DIDATICO')
    row['origem_premissa'] = 'Usuario; DIDATICA-1.0-20261103'
with (out/'matriz-108-didatica.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer = csv.DictWriter(f,fieldnames=matrix[0].keys()); writer.writeheader(); writer.writerows(matrix)
baseline = json.loads((out/'baseline-protecao.json').read_text(encoding='utf-8-sig'))
changed = [r['arquivo'] for r in baseline if sha(root/r['arquivo']).upper()!=r['sha256'].upper()]
assert not changed
measures = (root/'DRE Moderno - Databricks.SemanticModel/definition/tables/_Medidas.tmdl').read_text(encoding='utf-8-sig')
count = sum(line.lstrip().startswith('measure ') for line in measures.splitlines())
assert count == 36
summary = {'manifesto':str(target.relative_to(root)), 'sha256_manifesto':sha(target),
           'hash_excel_confere':True,'intervalos':9,'pares_realizado':87,'pares_nao_fornecidos':21,
           'pares_orcado':108,'pares_previsto':108,'validacoes_conjuntos':results,
           'escopo':'Validacao documental/local de conjuntos; nao executa DAX, SQL, TMDL ou materializacao',
           'producao_arquivos_conferidos':len(baseline),'producao_arquivos_alterados':changed,
           'medidas_existentes':count,'medidas_novas':0,'tabela_configuracao_criada_no_modelo':False}
(out/'validacao.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
