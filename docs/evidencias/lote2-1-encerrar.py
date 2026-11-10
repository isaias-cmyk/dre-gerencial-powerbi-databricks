from pathlib import Path
import json

root = Path(__file__).resolve().parents[2]
out = root / 'docs/evidencias/lote2-1-encerramento-20261102-162739'
def read(name):
    return json.loads((out / f'{name}.json').read_text(encoding='utf-8-sig'))

assert len(read('execucao')) == 11
assert all(r['State'] == 'EXECUTADO' for r in read('execucao'))
assert all(r['Unchanged'] for r in read('integridade'))
assert len(read('01-metadados')) == 6
assert all(r['[State]'] == 'Valid' for r in read('01-metadados'))
for name in ['02-controle-integral', '03-filial-periodo', '07-ebitda-ebit', '08-ausencia-realizado', '09-limites-conta-dre']:
    rows = read(name)
    assert rows
    for r in rows:
        assert all(v is True for k, v in r.items() if 'Aprovado' in k or 'Blank]' in k)
assert len(read('03-filial-periodo')) == 20
assert {r['vw_dre_comparativo[ordem_dre]'] for r in read('07-ebitda-ebit')} == {8, 11}
assert read('10-materializacao') == [{'[Linhas]': 1, '[Organizacao]': 0}]
partition = next(r for r in read('11-particoes') if r['[Name]'] == '_Medidas')
assert partition['[State]'] == 1 and partition['[ErrorMessage]'] is None
contexts = {r['[Contexto]']: r for r in read('05-contextos-e-totais')}
for c in ['SemFiltro', 'Multiplas1e13', 'SemDados']:
    assert all(contexts[c][k] is None for k in ['[BaseR]', '[BaseO]', '[BaseP]'])
for c in ['Unica1', 'SemDados']:
    assert all(contexts[c][k] is None for k in ['[RLR]', '[RLO]', '[RLP]'])
total = next(r for r in read('06-total-matriz') if r['[EhTotalGeral]'])
assert total['[PosicoesVisiveis]'] == 13
assert all(total[k] is None for k in ['[Realizado]', '[Orcado]', '[Previsto]'])
result = {'Estado': 'CONCLUIDO_TECNICAMENTE', 'ConsultasExecutadas': 11, 'FalhasExecucao': 0,
          'CasosFilialPeriodo': 20, 'VerificacoesCenarioAprovadas': 60,
          'Materializacao': {'Linhas': 1, 'Organizacao': 0, 'Estado': 'Ready', 'Erro': None,
                             'RefreshedTimeReportadoPeloMotor': partition['[RefreshedTime]']},
          'Cartao': {'Valor': 'R$ 5,04M', 'Proveniencia': 'Confirmacao expressa do usuario; sem captura pelo agente'},
          'SQL': 'Sem nova execucao; conciliacao F1 mantida como referencia',
          'ProducaoAlteradaNestaRodada': False, 'Lote22': 'PLANEJADO_NAO_INICIADO',
          'PendenciasContabeis': ['EBITDA', 'EBIT', 'Resultado Liquido provisorio']}
(out / 'aceite.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
