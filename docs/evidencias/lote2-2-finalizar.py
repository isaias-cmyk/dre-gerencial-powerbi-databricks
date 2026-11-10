from pathlib import Path
import json, hashlib, re

root=Path(__file__).resolve().parents[2]
prep=json.loads((root/'docs/evidencias/lote2-2-atual.json').read_text(encoding='utf-8'))
ev=Path(prep['Evidence'])
catalog=json.loads((ev/'catalogo-novas-medidas.json').read_text(encoding='utf-8'))
tests=root/'docs/testes/lote2-2'
syntax=[]
for p in tests.glob('*.dax'):
    s=re.sub(r'//[^\n]*','',p.read_text(encoding='utf-8-sig'))
    s=re.sub(r'"(?:""|[^"])*"', '""', s)
    s=re.sub(r"'(?:''|[^'])*'", "''", s)
    stack=[]
    for ch in s:
        if ch in '({[': stack.append(ch)
        elif ch in ')}]':
            assert stack and stack.pop()=={')':'(','}':'{',']':'['}[ch],p.name
    assert not stack,p.name
    assert 'DEFINE MEASURE' not in s.upper()
    syntax.append({'Arquivo':p.name,'Delimitadores':'OK','CompilacaoDAX':'NAO_EXECUTADA'})
lineages=[]
for p in (root/'DRE Moderno - Databricks.SemanticModel/definition').rglob('*.tmdl'):
    lineages.extend(re.findall(r'^\s*lineageTag:\s*(.+)$',p.read_text(encoding='utf-8-sig'),re.M))
assert len(lineages)==len(set(lineages)), 'LineageTag duplicado'
baseline=json.loads((ev/'baseline.json').read_text(encoding='utf-8'))
target='DRE Moderno - Databricks.SemanticModel/definition/tables/_Medidas.tmdl'
def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest().upper()
protected=[r for r in baseline if r['Path']!='PLANS.md' and not r['Path'].startswith('docs/') and r['Path']!=target]
assert all(sha(root/r['Path'])==r['SHA256'] for r in protected),'Arquivo protegido alterado'
json_count=0
for p in root.rglob('*.json'):
    if p.relative_to(root).parts[0] in ('backups','.git') or '.pbi' in p.parts: continue
    json.loads(p.read_text(encoding='utf-8-sig'));json_count+=1
evidence={'TMDL':'APROVADO (ver validacao-tmdl.json)','ProtectedFiles':len(protected),'ProtectedUnchanged':True,'UniqueLineageTags':len(lineages),'JSONParsed':json_count,'DAXFiles':syntax,'DynamicExecutions':0,'SQLExecutions':0}
(ev/'verificacao-estatica.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
report=f'''# Lote 2.2 — implementação e validação

Data: 02/11/2026. Responsável: Codex. **Implementação estática aprovada; lote não concluído. Validação dinâmica e conciliação Databricks SQL pendentes. Lote 2.3 não iniciado.**

## Preparação, escopo e proteção

Lidos AGENTS.md, PLANS.md, plano do Lote 2.2, contratos, aceite/validação do Lote 2.1 e TMDL real das seis medidas. Lote 2.1 concluído tecnicamente confirmado. Desktop e mecanismo fechados, verificados por processos no host antes do backup e imediatamente antes da edição; [evidência](evidencias/{prep['Tag']}/desktop-antes-edicao.json). Nenhuma aplicação foi encerrada pelo agente.

Plano confrontado com a solicitação: sem divergência funcional. Autorizadas as dez posições e três cenários, total 30; nomes exatos e contratos individuais registrados em contratos-medidas-dax.md antes da escrita TMDL. O plano anterior foi preservado como histórico, com adendo de escopo. Estratégia CALCULATE + KEEPFILTERS compatível com as bases; sem filtros substitutivos.

Git continua fora de repositório: status/rev-parse código 128. Não houve init, commit ou publicação. Diferenças preexistentes desde a baseline da rodada anterior: PLANS.md, model.tmdl, _Medidas.tmdl, cache e dois localSettings. Novos arquivos preexistentes, inclusive consultas salvas pelo Desktop, estão na baseline atual. Causas não presumidas; todo o estado de entrada foi preservado. O snapshot atual, não uma versão antiga, é a referência deste lote. [Preparação/diferenças](evidencias/{prep['Tag']}/preparacao.json).

Backup atualizado: `backups/{prep['Tag']}/`, {prep['Included']} arquivos incluídos, cinco .pbi excluídos explicitamente; backups e .git excluídos. Snapshot/ZIP e restauração isolada conferidos por SHA-256 para todos os arquivos incluídos. ZIP SHA-256 `{prep['ZIP_SHA256']}`. [Manifesto](../backups/{prep['Tag']}/manifesto-sha256.json). Configurações/cache excluídos não foram editados; backup no mesmo disco não protege contra perda física.

## Medidas implementadas

Cada indicador abaixo tem as medidas `DRE | <Indicador> Realizado`, `DRE | <Indicador> Orçado` e `DRE | <Indicador> Previsto`:

| Posição | Indicador / pasta DRE |
| --- | --- |
'''
for pos,label in [(m['Posicao'],m['Indicador']) for m in catalog[::3]]:
    report+=f'| {pos} | {label} |\n'
report+=f'''
Catálogo com os 30 nomes exatos, cenários, colunas, pastas e lineageTags: [JSON](evidencias/{prep['Tag']}/catalogo-novas-medidas.json). Contratos individuais: [contratos-medidas-dax.md](contratos-medidas-dax.md), seção Lote 2.2.

Único arquivo de produção alterado: `DRE Moderno - Databricks.SemanticModel/definition/tables/_Medidas.tmdl`. Inseridos 30 blocos antes da coluna auxiliar, conservando os bytes originais restantes. As seis medidas, coluna, partição e identificadores existentes foram preservados. Nenhuma alteração em model.tmdl, tabelas anteriores, consultas M, conexões, credenciais, relações, PBIP/PBIR, páginas, visuais ou AGENTS.md.

Todas reutilizam uma base com interseção na posição fixa; preservam sinais ajustados, Filial/Calendário e BLANK. Posições/descrições incompatíveis retornam BLANK. Seleção múltipla que inclua a posição e total geral retornam somente a posição específica; não somam as posições. Bases mantêm BLANK em múltiplas posições. Posições 3 e 5 leem valores da view, sem recomposição. Margem de Contribuição é monetária. Sem ABS, COALESCE, tipolancamento, percentuais, desvios ou YTD nas medidas. Conta/dim_dre continuam sem propagação automática à view.

## Testes estáticos executados

- Parser TmdlSerializer instalado desserializou snapshot de entrada e definição final sem erro: 15 tabelas, 18 relações, oito partições M e 6 → 36 medidas.
- Trinta nomes novos únicos; expressões e posições comparadas com o catálogo, com formato monetário, pasta, descrição e lineageTag.
- As seis medidas existentes comparadas propriedade a propriedade: nome, expressão, descrição, formato, pasta, lineageTag e visibilidade inalterados.
- Coluna auxiliar oculta e partição DATATABLE constante preservadas; nenhum relacionamento novo.
- {len(protected)} arquivos protegidos de entrada conferidos por hashes; nenhum alterado.
- {len(lineages)} lineageTags únicos; {json_count} JSON analisados sintaticamente.
- Dez consultas DAX com delimitadores balanceados e sem DEFINE MEASURE; isso não representa compilação DAX.

Evidências: [parser/medidas](evidencias/{prep['Tag']}/validacao-tmdl.json), [verificação estática](evidencias/{prep['Tag']}/verificacao-estatica.json), [preservação dos bytes](evidencias/{prep['Tag']}/preservacao-seis-medidas.json). Script de parser: [lote2-2-validar.ps1](evidencias/lote2-2-validar.ps1). Inventário final: [arquivos-alterados.json](evidencias/{prep['Tag']}/arquivos-alterados.json).

## Execução pendente — Power BI Desktop

Após terminar as gravações, abrir o PBIP atualizado. Confirmar 36 medidas e _Medidas materializada/sem erro. Executar um arquivo DAX por vez na Exibição de Consulta DAX, sem criar medidas temporárias ou de produção. Usar contexto inicial sem filtros externos e registrar catálogo, versão, data/atualização e resultados completos. Não editar TMDL com Desktop aberto.

| Arquivo em docs/testes/lote2-2 | Esperado / critério |
| --- | --- |
| 01-metadados.dax | 36 linhas, seis antigas + 30 novas, todas Valid, sem duplicação; conferir metadados com catálogo |
| 02-filiais-periodos-conciliacao.dax | 1.155 linhas: 33 medidas (30 novas + três RL) × cinco grupos de filial × sete recortes; Aprovado TRUE em todas; NULL/BLANK distinguido de zero |
| 03-posicao-descricao-contextos.dax | 240 casos: 30 medidas × oito contextos de posição/descrição; Aprovado TRUE em todos |
| 04-matriz-totais.dax | 14 linhas com total: cada medida somente na posição correspondente e total dessa posição; M07–M36 seguem a ordem do catálogo; linhas conflitantes BLANK |
| 05-aditividade-filiais.dax | 30 casos; soma das três filiais = consolidado, Aprovado TRUE |
| 06-ebitda-ebit.dax | Duas posições 8 e 11 presentes por LinhasFonte; três bases e 30 específicas BLANK; nenhuma medida nova EBITDA/EBIT |
| 07-regressao-controle.dax | Bases em 13 e RL coincidem com R$ 5.038.227,39 / R$ 6.622.493,82 / R$ 6.157.931,19; três aprovações TRUE |
| 08-regressao-bases.dax | Cinco contextos de Lote 2.1 inalterados, incluindo BLANK múltiplas/vazio e interseção do RL |
| 09-materializacao.dax | Uma linha na tabela auxiliar e valor zero; conferir também ausência de erros no Desktop |
| 11-receita-liquida-margem.dax | 105 casos; identidades Receita Líquida = Bruta + Deduções e Margem = Líquida + Custos coerentes a R$ 0,01, preservando ausência; divergência exige investigação, não recalcular produção |

Grupos: consolidado, 01 São Paulo, 02 Rio de Janeiro, 03 Florianópolis e seleção 01+02. Recortes: integral, 2021, 2022, 2023, janeiro–maio/2023, junho–dezembro/2023 e junho/2023. Em 2023 integral, Realizado é parcial; testar filtros não autoriza interpretar como desempenho equivalente ao orçamento anual. Para comparação, usar corte comum janeiro–maio. Após maio/2023, medidas Realizado devem ser BLANK e Orçado/Previsto disponíveis conforme fonte.

## Execução pendente — SQL e conciliação independente

Executar [10-referencia-databricks.sql](testes/lote2-2/10-referencia-databricks.sql) no warehouse existente com acesso já configurado. Somente SELECT; sem alteração de origem ou autenticação. Retorna 1.155 chaves (grupo_filial, periodo, posicao, cenario), valores, contagens de registros e valores presentes. Usa as mesmas posições/recortes da consulta DAX 02, preserva SUM(NULL) e não arredonda nem altera sinais. Confirmar estado de atualização equivalente ao modelo; divergência de atualização exige conciliar novamente no mesmo estado.

Exportar DAX 02 e SQL completos em CSV UTF-8, sem agrupamento de milhar ou formato monetário, preservando campos vazios/NULL. Comparar pelo script [comparar-exportacoes.py](testes/lote2-2/comparar-exportacoes.py): `python comparar-exportacoes.py dax.csv sql.csv resultado.json`. O script exige 1.155 chaves únicas em cada arquivo, conjuntos iguais, ausência coincidente e diferença absoluta máxima R$ 0,01; falha não pode ser aprovada sem investigação. Identidades e sinais devem ser conferidos nos testes, sem impor que indicadores mistos sejam sempre positivos/negativos. O comparador não foi executado sobre dados reais nesta rodada.

## Aceite e pendências

- [x] Backup restaurável e verificado; instruções e escopo confrontados.
- [x] Contratos das 30 medidas documentados antes da implementação.
- [x] Parser TMDL aprovado; 36 medidas sem duplicidade e seis antigas preservadas.
- [x] Fontes, relações e demais arquivos de produção preservados.
- [x] Roteiros DAX/SQL e critérios objetivos preparados.
- [ ] Compilar/executar dez consultas DAX nas medidas persistidas e registrar resultados/erros.
- [ ] Executar SQL e conciliar as 1.155 chaves com tolerância máxima R$ 0,01.
- [ ] Registrar apresentação monetária, materialização e regressões no modelo reaberto.
- [ ] Aceite definitivo do Lote 2.2 após todas as evidências dinâmicas.

**Execuções dinâmicas nesta entrega: DAX = 0; SQL = 0.** Desktop estava fechado para edição e não foi aberto pelo agente. Parser e inspeção estática não compilam/avaliam DAX, não validam a origem atual nem materializam a nova versão. O aceite do Lote 2.1 não é teste das 30 medidas novas. Nenhuma aprovação dinâmica foi presumida.

Resultado Líquido permanece provisório; EBITDA/EBIT não calculados e pendentes de homologação contábil. Não iniciar Lote 2.3 ou páginas. Em caso de falha: registrar erro, fechar Desktop, preservar estado atual e recuperar somente _Medidas.tmdl da cópia verificada em pasta isolada; revalidar dependências e dados antes de substituir qualquer arquivo. Não restaurar caches/configurações ou sobrescrever trabalho posterior.
'''
(root/'docs/validacao-lote2-2.md').write_text(report,encoding='utf-8')
p=root/'PLANS.md'
s=p.read_text(encoding='utf-8-sig')
s=s.replace('Lote 2.2 e Fases 3 a 10 não iniciados.', 'Lote 2.2 implementado estaticamente e pendente de testes dinâmicos/SQL; Lote 2.3 e Fases 3 a 10 não iniciados.')
s=s.replace('Fase 2 iniciada exclusivamente no Lote 2.1:', 'Fase 2 em andamento, com Lote 2.1 aceito e Lote 2.2 em validação:')
s=s.replace('Lote 2.2 planejado, não iniciado', 'Lote 2.2 implementado estaticamente, pendente de DAX/SQL')
s=s.replace('Lote 2.2 planejado e não iniciado', 'Lote 2.2 implementado estaticamente, pendente de DAX/SQL')
s=s.replace('- [ ] Lote 2.2, demais medidas, design system, páginas e homologação ainda não iniciados.', '- [ ] Lote 2.2 implementado estaticamente, não concluído; Lote 2.3, design system, páginas e homologação não iniciados.')
start=s.index('### Lote 2.2 — Receitas, Custos e Resultados Gerenciais')
end=s.index('## FASE 3',start)
s=s[:start]+f'''### Lote 2.2 — Receitas, Custos e Resultados Gerenciais

**Implementação estática aprovada; não concluído.** Trinta medidas novas em _Medidas, posições 1–7, 9, 10 e 12 × três cenários. Trinta e seis no total; seis antigas preservadas. [Validação e instruções](docs/validacao-lote2-2.md), [plano histórico e confronto](docs/plano-lote2-2.md), [contratos](docs/contratos-medidas-dax.md).

- [x] L2.2-P01: instrução recebida; documentos lidos e escopo compatível com plano aprovado.
- [x] L2.2-P02: Desktop/mecanismo fechados; Git fora de repositório; alterações de entrada preservadas.
- [x] L2.2-P03: backup {prep['Tag']}, {prep['Included']} arquivos incluídos; restauração SHA-256 verificada.
- [x] L2.2-C01: contratos individuais registrados antes da escrita TMDL; nomes, posições, sinais, filtros, totais, BLANK e formato definidos.
- [x] L2.2-I01: 30 medidas implementadas reutilizando bases e KEEPFILTERS; sem alterar produção fora de _Medidas.tmdl.
- [x] L2.2-V01a: parser e inspeção estática aprovados; 15 tabelas, 18 relações, oito partições M e 36 medidas. Hashes protegidos e seis medidas anteriores preservados.
- [x] L2.2-T01: dez DAX e uma SQL preparados; comparador de exportações disponível.
- [ ] L2.2-V01b: reabrir no Desktop e comprovar medidas válidas, formato e materialização.
- [ ] L2.2-V02: executar SQL e comparar as 1.155 chaves com DAX, ausência coincidente e tolerância máxima R$ 0,01.
- [ ] L2.2-V03: executar testes de contextos, filiais/períodos, sinais, receitas/custos, totais e regressões.
- [ ] L2.2-A01: aceite definitivo somente com evidências dinâmicas e SQL registradas.

Nesta rodada DAX = 0 e SQL = 0; pendentes porque o modelo estava fechado para edição, sem nova sessão de execução. Não confundir parser com execução. Resultado Líquido provisório mantido; EBITDA/EBIT sem medidas novas. Lote 2.3 e páginas não iniciados.

'''+s[end:]
p.write_text(s,encoding='utf-8')
for name in ['validacoes','alteracoes']:
    with (root/f'docs/{name}.md').open('a',encoding='utf-8') as f:
        f.write(f'\n\n## Lote 2.2 — 02/11/2026\n\nImplementadas 30 medidas de posições autorizadas na tabela _Medidas, preservando as seis existentes. Backup {prep["Tag"]}, {prep["Included"]} arquivos restaurados e hashes verificados. Parser TMDL aprovado: 36 medidas, 15 tabelas, 18 relações e oito partições M. Único arquivo de produção alterado: _Medidas.tmdl. Contratos e dez consultas DAX/uma SQL documentados. DAX/SQL não executados; lote não concluído até evidência dinâmica e conciliação independente. Ver docs/validacao-lote2-2.md. Lote 2.3 não iniciado; pendências contábeis mantidas.\n')
changed=[]
for row in baseline:
    p=root/row['Path']
    now=sha(p) if p.exists() else None
    if now!=row['SHA256']: changed.append({'Path':row['Path'],'State':'ALTERADO' if now else 'AUSENTE','Before':row['SHA256'],'After':now})
known={r['Path'] for r in baseline}
for p in root.rglob('*'):
    if p.is_file() and p.relative_to(root).parts[0] not in ('backups','.git'):
        rel=p.relative_to(root).as_posix()
        if rel not in known and not rel.startswith(f'docs/evidencias/{prep["Tag"]}/'):
            changed.append({'Path':rel,'State':'NOVO','After':sha(p)})
(ev/'arquivos-alterados.json').write_text(json.dumps(changed,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'Status':'IMPLEMENTADO_ESTATICAMENTE_NAO_CONCLUIDO','ChangedExisting':[r['Path'] for r in changed if r['State']=='ALTERADO'],'Static':evidence},ensure_ascii=False,indent=2))
