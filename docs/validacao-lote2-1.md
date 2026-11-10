# Lote 2.1 — implementação e validação

Data: 02/11/2026. Responsável: Codex. Escopo: somente as seis medidas fundamentais da Fase 2. **Estado: concluído tecnicamente em 02/11/2026. Validação dinâmica e materialização comprovadas. Lote 2.2 planejado, não iniciado.**

## Preparação cumprida

- AGENTS.md, PLANS.md e auditoria da Fase 1 lidos integralmente; aceite técnico de F1 conferido.
- Desktop inicialmente aberto: aguardado fechamento pelo usuário e confirmados zero processos PBIDesktop/msmdsrv às 16:04. Nova verificação antes da escrita confirmou Desktop fechado. Nenhum processo foi encerrado pelo agente.
- Modelo real inspecionado e lido pelo TmdlSerializer instalado: 14 tabelas, 18 relações e zero medidas explícitas antes do lote.
- Git instalado, mas esta pasta não é repositório; status/rev-parse retornaram 128. Não há branch/commit ou alterações não commitadas determináveis. Nenhum init, commit ou publicação executado.
- Comparação com a baseline anterior identificou PLANS.md e dois localSettings.json diferentes antes do lote. Essas diferenças são de entrada e foram preservadas; configurações locais não foram editadas.
- Plano, arquivos, riscos e testes apresentados antes da implementação. [Contratos](contratos-medidas-dax.md) criados antes das medidas.

## Backup e recuperação

Backup: `backups/lote2-1-20261102-160536/`.

- 176 arquivos incluídos: fontes atuais e documentação/evidências preexistentes.
- Quatro arquivos em .pbi excluídos, incluindo cache/configurações locais; backups antigos e .git fora do inventário.
- `snapshot/`, `snapshot.zip`, `manifesto-sha256.json` e `restauracao-teste/` preservados.
- ZIP restaurado em pasta isolada; quantidade e hashes dos 176 arquivos conferidos individualmente.
- SHA-256 do ZIP: `B48E09E1E12CD51EF7C77A5B02448F0845EBF405C154FBCFEB94F86C9E46B78C`.

[Preparação](evidencias/lote2-1-20261102-160536/preparacao.json), [situação Git](evidencias/lote2-1-20261102-160536/git.json) e [manifesto](../backups/lote2-1-20261102-160536/manifesto-sha256.json).

Rollback, se houver erro de abertura/cálculo: fechar Desktop, preservar o estado atual, verificar hashes do backup e recuperar em cópia isolada o model.tmdl anterior. A nova _Medidas.tmdl não existia no snapshot; retirá-la da cópia de recuperação somente após conferir dependências e preservar trabalho posterior. Comparar o conjunto restaurado, abrir/validar a cópia e só então decidir substituição do projeto. Não restaurar configurações locais nem sobrescrever documentação/trabalho mais recente sem análise. Backup no mesmo disco não protege contra perda física do disco.

## Arquivos de produção alterados

| Arquivo | Alteração |
| --- | --- |
| SemanticModel/definition/tables/_Medidas.tmdl | Novo: tabela calculada local, uma coluna oculta de organização e seis medidas |
| SemanticModel/definition/model.tmdl | Apenas acrescentada a referência `ref table _Medidas` |

Oito consultas M, 18 relações, tabelas de negócio e técnicas anteriores, PBIP, PBIR, páginas, tema, conexões e credenciais foram preservados. A nova partição calculada usa DATATABLE constante, sem origem externa ou relação com outras tabelas.

Documentação e testes: docs/contratos-medidas-dax.md, docs/validacao-lote2-1.md, docs/testes/lote2-1/*.dax, docs/evidencias/lote2-1-validar.ps1, docs/evidencias/lote2-1-20261102-160536/*, PLANS.md e adendos em docs/validacoes.md e docs/alteracoes.md. O relatório completo de arquivos está em [arquivos-alterados.json](evidencias/lote2-1-20261102-160536/arquivos-alterados.json).

## Medidas e contratos implementados

- `DRE | Realizado`, `DRE | Orçado`, `DRE | Previsto`: retornam valor ajustado da posição única visível; sem descrição válida, múltiplas posições ou rótulo EBIT/EBITDA, retornam BLANK.
- `DRE | Resultado Líquido Realizado`, `DRE | Resultado Líquido Orçado`, `DRE | Resultado Líquido Previsto`: interseção KEEPFILTERS com posição 13; conflito de posição retorna BLANK. Descrições e pasta identificam provisoriedade/homologação contábil pendente.
- Filtros de dim_filial/dim_calendario preservados. dim_conta e dim_dre continuam sem filtro automático da view.
- Sem COALESCE, reaplicação de tipolancamento, margens, desvios, YTD ou cálculo de EBITDA/EBIT.
- Detalhes individuais: [contratos-medidas-dax.md](contratos-medidas-dax.md).

## Verificações estáticas executadas

| Verificação | Resultado |
| --- | --- |
| Parser TMDL Microsoft.PowerBI.Tabular | Definição completa desserializada sem erro antes e depois |
| Tabelas/relações | 14 → 15 tabelas; 18 → 18 relações |
| Medidas | Exatamente seis nomes solicitados, sem duplicação |
| Organização | Coluna auxiliar oculta; tabela visível com pastas de medidas; partição calculada local |
| Partições M | Oito antes e depois; arquivos de origem inalterados |
| Model.tmdl | Remover apenas a nova linha de referência reproduz o conteúdo anterior |
| Integridade de arquivos | Hashes preservados para os arquivos protegidos de produção |
| LineageTags | Únicos; identificadores existentes preservados |
| Referências das medidas | Colunas reais da view e medidas base previstas |
| Contratos de contexto | HASONEVALUE/BLANK e supressão de EBIT presentes nas bases; KEEPFILTERS 13 nas específicas |
| Metadados provisórios | Descrições e pasta das três medidas de Resultado Líquido explícitas |
| JSON preexistente | Parsing sintático executado sem erro; relatório não alterado |
| Nove consultas de teste | Delimitadores conferidos; nenhuma execução ou compilação DAX alegada |

Evidências: [parser](evidencias/lote2-1-20261102-160536/tmdl-parser.json), [validação estrutural](evidencias/lote2-1-20261102-160536/validacao-tmdl.json), [verificação estática](evidencias/lote2-1-20261102-160536/verificacao-estatica.json). Script reproduzível: [lote2-1-validar.ps1](evidencias/lote2-1-validar.ps1).

**Limite:** TmdlSerializer valida a estrutura TMDL, mas não compila/avalia as expressões DAX nem materializa a partição calculada. As medidas persistidas precisam ser carregadas e executadas no Desktop. As evidências de F1 continuam válidas como referência, não como prova de execução das medidas novas.

## Roteiro de execução — preservado para reprodução

Reabrir o PBIP atualizado depois de todas as gravações. Se houver pedido de atualização/cálculo para materializar a tabela local, usar o fluxo existente sem alterar consultas ou credenciais. Caso apareça erro, registrar a mensagem antes de salvar qualquer correção. Os arquivos não devem ser editados externamente enquanto o Desktop estiver aberto.

Na Exibição de Consulta DAX, executar um arquivo por vez. Não aplicar DEFINE MEASURE nem criar medidas pelo editor; os testes devem resolver os seis nomes já persistidos em _Medidas. Salvar as saídas/erros com a data do modelo e do teste.

| Consulta | Critério objetivo |
| --- | --- |
| [01 — metadados](testes/lote2-1/01-metadados.dax) | Seis medidas em _Medidas; pastas, formato e descrições provisórias corretos; sem erro de expressão |
| [02 — controle integral](testes/lote2-1/02-controle-integral.dax) | AprovadoR/O/P = TRUE; três bases em posição 13 e três específicas coincidem com R$ 5.038.227,39 / R$ 6.622.493,82 / R$ 6.157.931,19 |
| [03 — filial/período](testes/lote2-1/03-filial-periodo.dax) | Vinte casos (três filiais + consolidado × cinco recortes); AprovadoR/O/P = TRUE em cada um; comparação preserva a distinção BLANK/zero |
| [04 — posições](testes/lote2-1/04-posicoes.dax) | Treze linhas reais; bases correspondem à posição e fonte, salvo supressão de EBITDA/EBIT; específicas somente na posição 13 |
| [05 — contextos](testes/lote2-1/05-contextos-e-totais.dax) | SemFiltro e Multiplas1e13: bases BLANK e específicas da linha 13; Unica13: seis medidas da linha 13; Unica1: bases da posição 1 e específicas BLANK; SemDados: seis BLANK |
| [06 — matriz](testes/lote2-1/06-total-matriz.dax) | Bases BLANK no total geral multirregistro de posições; totais aditivos de posição única válidos; específicas no total somente linha 13 |
| [07 — EBITDA/EBIT](testes/lote2-1/07-ebitda-ebit.dax) | Identificar ambas as posições pelos rótulos reais; todas as seis verificações Blank = TRUE; resultado vazio não aprova identificação |
| [08 — ausência](testes/lote2-1/08-ausencia-realizado.dax) | AprovadoAusencia = TRUE para junho–dezembro/2023; orçamento/previsão continuam disponíveis |
| [09 — limites Conta/DRE](testes/lote2-1/09-limites-conta-dre.dax) | AprovadoLimites = TRUE; não atribuir a essas medidas detalhamento por conta ou filtro automático de dim_dre |

Conferir o formato monetário numérico na cultura de exibição efetiva. Comparar os recortes de 03 com os resultados de F1/SQL aceitos, usando o mesmo estado dos dados. Não comparar realizado parcial de 2023 com orçamento anual como desempenho equivalente. Não aprovar o lote se o modelo abriu sem erro, mas as consultas não foram executadas.

## Encerramento — evidências dinâmicas e aceite

Em 02/11/2026 às 16:27 (America/Sao_Paulo), foram executadas pelo agente 11 consultas DAX/INFO via ADOMD, exclusivamente em leitura no catálogo local do Desktop Store aberto. Não houve refresh, SaveChanges, alteração de medidas ou escrita em arquivos Power BI. As nove consultas preparadas foram reutilizadas; acrescentadas somente as consultas 10 (dados da tabela auxiliar) e 11 (partições).

Evidências brutas CSV/JSON e identificação da sessão: [pasta da execução](evidencias/lote2-1-encerramento-20261102-162739). [Log](evidencias/lote2-1-encerramento-20261102-162739/execucao.json), [aceite consolidado](evidencias/lote2-1-encerramento-20261102-162739/aceite.json), [integridade antes/depois](evidencias/lote2-1-encerramento-20261102-162739/integridade.json). Executor reproduzível: [PowerShell](evidencias/lote2-1-executar-local.ps1); verificações de resultados: [Python](evidencias/lote2-1-encerrar.py). O executor desta rodada seleciona o workspace Desktop Store; em outra instalação, conferir o caminho do workspace antes de executar.

| Critério | Resultado e evidência |
| --- | --- |
| Seis medidas persistidas | Consulta 01: seis medidas numéricas, todas Valid; nomes, pastas e descrições provisórias conferidos |
| Linha 13 integral | Consulta 02: bases e específicas R$ 5.038.227,39 / R$ 6.622.493,82 / R$ 6.157.931,19; três aprovações TRUE; diferença R$ 0,00 após arredondar a centavos |
| Filial/período | Consulta 03: 20 casos (três filiais e consolidado × cinco recortes); 60 verificações de cenário TRUE; comparação com a posição 13 da view importada |
| Posições únicas | Consulta 04: 13 posições reais, 108 registros de origem por posição; bases retornam valores, exceto indicadores protegidos; específicas somente em 13 |
| Múltiplas/vazio/conflito | Consulta 05: bases BLANK sem posição única; seis BLANK sem dados; Resultado Líquido BLANK para posição 1, preservando interseção |
| Total de matriz | Consulta 06: 13 posições e total; bases BLANK no total multirregistro; específicas somente linha 13 |
| EBITDA/EBIT | Consulta 07: posições 8 (= EBITDA) e 11 (= EBIT), ambas identificadas; 12 verificações BLANK TRUE |
| Ausência de realizado | Consulta 08: junho–dezembro/2023 BLANK nas duas medidas de realizado; Orçado R$ 1.372.901,80 e Previsto R$ 1.253.170,17 disponíveis |
| Limite de Conta/DRE | Consulta 09: Conta e dim_dre não alteram automaticamente o Resultado Líquido da view; AprovadoLimites TRUE |
| Materialização | Consulta 10: COUNTROWS(_Medidas) = 1 e MAX(_Organizacao) = 0; consulta 11: partição calculada State = 1 (Ready), ErrorMessage = NULL |
| Apresentação | Usuário confirmou cartão R$ 5,04M; evidência declarada pelo usuário, sem inspeção/captura visual pelo agente |
| Preservação | Nenhuma diferença de hash nos arquivos de entrada protegidos durante as consultas |

A partição local informa RefreshedTime `2026-11-02T19:18:44.82` (timestamp devolvido pelo mecanismo, preservado sem reinterpretar fuso). O enum ObjectState da biblioteca Microsoft.PowerBI.Tabular instalada confirma 1 = Ready. **Não há pendência de atualização ou materialização de _Medidas no estado consultado.** Reconhecimento de medidas isoladamente não seria prova suficiente; nesta rodada os dados da própria tabela foram consultados com sucesso.

O usuário também confirmou expressamente os três controles, retorno em posição única, BLANK em múltiplas posições, EBITDA/EBIT e junho/2023. Os resultados locais são compatíveis com essa declaração. No modelo carregado, o formato monetário aparece em FormatStringDefinition como expressão constante, com FormatString nulo; a apresentação monetária foi confirmada pelo usuário. Não foi alterado o formato de produção.

## Critérios de aceite

- [x] Estrutura TMDL validada e seis medidas reconhecidas/executáveis.
- [x] Tabela auxiliar materializada, Ready e sem erro.
- [x] Controles integrais conciliados a centavos e filiais/períodos testados.
- [x] Posição única, múltiplas posições, conflitos, vazio e total de matriz coerentes com os contratos.
- [x] EBITDA/EBIT protegidos e realizado ausente preservado como BLANK.
- [x] Limites de Conta/DRE e provisoriedade do Resultado Líquido explícitos.
- [x] Apresentação do cartão confirmada pelo usuário; evidências e proveniência registradas.
- [x] Arquivos de produção preservados nesta tarefa.

**Lote 2.1 concluído tecnicamente.** Fase 2 permanece em andamento. Lote 2.2 apenas planejado em [plano-lote2-2.md](plano-lote2-2.md), sem implementação.

## Limitações e riscos remanescentes

Testes executados sobre o modelo importado disponível; nenhuma nova consulta Databricks SQL nesta rodada. A conciliação SQL independente aceita em F1 permanece referência histórica, não nova execução. Não foram homologadas páginas futuras nem realizados testes de desempenho ou RLS. A validação visual do cartão tem proveniência no usuário.

Resultado Líquido permanece provisório e dependente de homologação contábil; EBITDA/EBIT seguem sem cálculo. Proteção por rótulo requer regressão se as descrições da origem mudarem. Cultura de exibição e formato do cartão devem ser preservados e novamente conferidos nos visuais futuros. Controles integrais abrangem períodos diferentes por cenário; não os usar como comparação de desempenho equivalente.
