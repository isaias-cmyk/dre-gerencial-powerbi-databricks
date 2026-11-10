# L2.3.1 — aceite técnico final, 03/11/2026

**Concluído tecnicamente no escopo da cobertura didática DIDATICA-1.0-20261103.** Persistência e conciliação SQL aprovadas; este aceite substitui os estados históricos de validação pendente abaixo. Não é homologação contábil real. L2.3.2 não iniciado.

## Persistência aprovada

O usuário confirmou explicitamente ter salvo, fechado e reaberto o mesmo PBIP antes da captura. A imagem mostra o projeto salvo e a configuração oculta/desconectada; a sequência de fechamento/reabertura é evidência declarada pelo usuário, não inferida da imagem.

Após essa confirmação, o agente executou cinco consultas de leitura na sessão reaberta: configuração, tabelas, medidas, partições e relacionamentos. Resultados em `docs/evidencias/lote2-3-1-diagnostico-20261103-125235/`: nove intervalos exatamente iguais aos anteriores, incluindo datas/versão/hash; 41 medidas Valid com as mesmas expressões (normalização apenas de whitespace); 16 tabelas, 16 partições Ready sem ErrorMessage e 18 relacionamentos preservados. Configuração oculta e sem relacionamento físico. Na comparação dos relacionamentos, foram desconsiderados somente IDs numéricos e o identificador do catálogo de sessão; nomes/colunas/cardinalidades/direções/estados permaneceram iguais.

Nenhuma medida, configuração, conexão ou página foi alterada pelo agente nesta homologação. A inspeção local foi somente leitura; os registros integridade.json das consultas não apontam alteração dos arquivos de produção.

## Conciliação independente aprovada

CSV SQL fornecido pelo usuário preservado integralmente, junto das duas capturas e manifesto SHA-256 conferido, em `docs/evidencias/lote2-3-1-homologacao-20261103/`. A captura do Databricks mostra a consulta de preflight correspondente ao roteiro e o resultado “No rows returned / 0 rows”: nenhuma duplicação de grão encontrada nessa execução.

Comparador existente executado efetivamente:

```powershell
python docs/testes/lote2-3-1/comparar-conciliacao.py docs/evidencias/lote2-3-1-homologacao-20261103/L231_SQL_comparabilidade.csv docs/evidencias/lote2-3-1-diagnostico-20261103-090110/09-matriz-comparabilidade.json docs/evidencias/lote2-3-1-homologacao-20261103/conciliacao-sql.json
```

| Critério | Resultado |
| --- | --- |
| Chaves esperadas / SQL / DAX | 1.755 / 1.755 / 1.755 |
| Casos aprovados / reprovados | **1.755 / 0** |
| Chaves ausentes/extras e duplicações | Zero |
| Divergência máxima | **R$ 0,00000010** (1E-7), inferior a R$ 0,01 |
| NULL/BLANK coincidentes | **600** |
| Contagem de pares de cobertura SQL × DAX | Coincidente em todas as chaves |
| Preflight de duplicações | Aprovado por captura da execução SQL com zero linhas |

Grão conciliado: grupo de filiais × recorte × posição DRE × cenário, cinco grupos, nove recortes, 13 posições e três cenários. Inclui posições 8/11 BLANK e períodos sem Realizado fornecido. Preserva a diferença entre zero monetário e ausência. Não se afirma nova conciliação de cada uma das 36 competências isoladamente; o aceite corresponde aos recortes preparados.

Proveniência: execução SQL pelo usuário no Databricks; comparador e conferência pós-reabertura pelo agente. A versão Delta/snapshot exato e o fuso da consulta SQL financeira não constam do CSV. Os valores coincidem integralmente no grão testado; não declarar identidade temporal de commits. Essa limitação de rastreabilidade fica registrada e não é convertida em certificação contábil. Para nova carga, hash ou atualização diferente, invalidar a extrapolação deste aceite e reconciliar novamente.

## Evidências e encerramento

[Artefato de aceite](evidencias/lote2-3-1-homologacao-20261103/aceite.json), [comparação SQL](evidencias/lote2-3-1-homologacao-20261103/conciliacao-sql.json) e [manifesto dos anexos](evidencias/lote2-3-1-homologacao-20261103/manifesto.json). Resultados locais anteriores permanecem válidos: 1.755 verificações DAX, 600 BLANK preservados, 1.620 verificações de regressão com diferença máxima R$ 0,00, guardas e sintéticos descritos no histórico. As novas consultas de metadados e a conciliação não são contadas como repetição dessa regressão.

- [x] Persistência após salvar, fechar e reabrir comprovada no escopo declarado e conferido.
- [x] Configuração materializada, oculta/desconectada e contrato/hash preservados.
- [x] 41 medidas válidas, intervalos e relacionamentos preservados.
- [x] Testes locais e regressão anteriores aprovados.
- [x] Preflight e conciliação SQL independente aprovados no grão definido.
- [x] **L2.3.1 concluído tecnicamente**, sem certificação de fechamento contábil real.
- [ ] L2.3.2 não iniciado; apto somente a planejamento e autorização específica do próximo sublote.

Pré-requisitos para L2.3.2: manter este aceite como baseline; confirmar escopo exclusivo M40–M43 e contratos de desvios em períodos equivalentes, percentual sobre ABS da referência, zero/BLANK e tolerância; antes de editar, Desktop fechado, backup novo/restaurável e preservação das 41 medidas/configuração existentes. Não ampliar para favorabilidade ou cumprimento. Resultado Líquido continua provisório; EBITDA e EBIT sem cálculo até homologação específica.

---

## Histórico anterior ao aceite final

Os estados de pendência abaixo foram superados pelo aceite acima no escopo demonstrado.

# L2.3.1 — implementação e validação, 03/11/2026

**Implementado, em validação; não concluído.** Abertura do PBIP, materialização, medidas e testes locais confirmados. Falta conciliação SQL independente deste sublote. Nenhum outro sublote iniciado. A convenção didática não certifica fechamento contábil real.

## Autorização, segurança e alterações

Solicitação anexada pelo usuário aprovou a tabela local e as cinco medidas; nome adotado **_ConfigCobertura**, substituindo o nome candidato _CoberturaTemporal do desenho. AGENTS.md, PLANS.md, planejamento, contrato didático e contratos de medidas consultados. Lotes 2.1 e 2.2 tecnicamente aceitos, conforme evidências anteriores; não são homologação contábil.

Desktop inicialmente aberto: usuário confirmou fechamento, seguido de verificação real dos processos no host. Git status/rev-parse retornou 128, diretório fora de repositório; nenhum init/commit. Backup `backups/lote2-3-1-implementacao-20261103-085405/snapshot.zip`, 412 arquivos, restauração de teste conferida por SHA-256. ZIP SHA-256 `f9743c8019f62695617c4b30302267ac6fb755566df4b1fadc9c0f7d7743c117`. Exclusões: backups, .git e .pbi; inclui fontes/documentação/Excel. [Preparação](evidencias/lote2-3-1-implementacao-20261103-085405/preparacao.json), [baseline](evidencias/lote2-3-1-implementacao-20261103-085405/baseline.json) e [integridade inicial](evidencias/lote2-3-1-implementacao-20261103-085405/integridade-estatica.json), nesta pasta de evidências. Os links relativos desta cópia são locais à pasta; no relatório consolidado usar o diretório de evidências citado abaixo.

Arquivos de produção afetados exclusivamente:

- `DRE Moderno - Databricks.SemanticModel/definition/tables/_ConfigCobertura.tmdl`: novo, tabela calculada local DATATABLE, oculta, sete colunas e nove linhas, sem relacionamento.
- `DRE Moderno - Databricks.SemanticModel/definition/model.tmdl`: acrescentado somente o registro lógico da nova tabela; normalização de quebras de linha, sem mudança de opções existentes.
- `DRE Moderno - Databricks.SemanticModel/definition/tables/_Medidas.tmdl`: acrescentadas cinco medidas e respectivas descrições/pasta/lineageTags novos. Os 36 blocos anteriores permanecem idênticos na comparação textual normalizada.

Fatos, dimensões de negócio, partições M, conexões, relacionamentos, páginas, AGENTS.md e Excel preservados por hashes. Arquivos preexistentes alterados fora de docs/documentação limitam-se a model.tmdl e _Medidas.tmdl; configuração é arquivo novo. Estado confirmado no parser e mecanismo: **16 tabelas, 18 relações, 41 medidas; configuração oculta e desconectada**.

## Configuração e contratos definitivos deste sublote

Configuração reproduz `docs/cobertura-temporal-didatica.json`, versão DIDATICA-1.0-20261103 e hash do Excel `27e02e7148984d74acdb5cf086a9ba637c55617152793f23509d3bad24bce04b`. Cenários internos Orcado/Previsto correspondem aos nomes públicos Orçado/Previsto. Competências inicial/final são datas tipadas do primeiro dia do mês, inclusivas. Não há 31/05/2023 nem outro corte fixo nas cinco expressões: somente na configuração versionada.

Nove chaves filial/cenário únicas, sem intervalos conflitantes, conferidas com o manifesto materializado. Nesta versão há **um intervalo por filial/cenário**. Expressões consultam todos os intervalos, exigindo exatamente uma cobertura por mês elegível; múltiplos intervalos e cortes divergentes futuros exigirão novo contrato, validação global de sobreposição e testes próprios antes de uso. Não preencher lacunas: contexto com mês selecionado anterior/igual ao corte sem cobertura válida é bloqueado.

Lógica comum: filiais da dimensão + meses/dias da seleção; guarda de mês completo; cobertura por configuração independente do indicador; última competência selecionada coberta por filial; menor corte entre todas as filiais; pares até esse corte sem incluir meses não selecionados. Filtros virtuais de tuplas são aplicados à view com KEEPFILTERS/TREATAS, preservando os filtros existentes. Conta e dim_dre continuam sem propagação automática à view; não se criou uma solução de detalhe por conta.

| Medida | Contrato implementado |
| --- | --- |
| DRE \| Realizado Comparável | Base Realizado na máscara comum; BLANK se faltar Realizado da posição em qualquer par requerido. Não altera a máscara nem transforma falta de indicador em zero |
| DRE \| Orçado Comparável | Mesma máscara, configuração de Orçado deve cobrir todos os pares; Realizado e referência presentes em todos eles, senão BLANK com diagnóstico |
| DRE \| Previsto Comparável | Mesmo contrato para Previsão; não reduz Realizado para esconder referência ausente |
| DRE \| Pares Filial-Competência Comparáveis | Cardinalidade da máscara configurada; independe do valor financeiro. Contexto/posição inválidos → BLANK; contexto válido sem Realizado fornecido → 0 diagnóstico |
| DRE \| Status Comparabilidade | Texto com natureza didática e versão; informa seleção inválida, meses parciais, configuração ausente/inválida, lacuna, posição inválida, ausência de dados/referência e recorte parcial/integral com corte comum |

Todas consultam explicitamente a configuração; sem novos helpers persistidos, desvios, favorabilidade ou cumprimento. Medidas numéricas conservam sinais e zero legítimo, sem tipolancamento/ABS/COALESCE. Somente o status usa FORMAT para exibir competência; medidas financeiras permanecem numéricas BRL. Posição única válida/descrição da própria view, proteção EBIT herdada; total entre posições BLANK, total entre filiais na mesma posição recalculado. M49 não certifica um mês nem declara fechamento.

Política conservadora de dados insuficientes: um par com indicador Realizado ausente torna as três referências comparáveis indisponíveis para essa posição, mantendo sua contagem de cobertura e status explicativo. Referência ausente bloqueia apenas o cenário afetado; Realizado continua válido se completo. Isso evita apresentar totais parciais como completos; não é alteração das 36 bases antigas.

Código efetivo: TMDL nos três arquivos acima; expressões novas registradas em `docs/evidencias/lote2-3-1-implementacao-20261103-085405/expressoes-novas.json`. Rotina de geração preservada em docs/evidencias/lote2-3-1-implementar.py; não rerodar sobre implementação existente (possui guardas de entrada). Rotina de testes gera a versão inicial dos testes; ajustes finais do SQL e sintéticos estão nos roteiros efetivamente executados/exportáveis, cujos hashes foram registrados. Não sobrescrevê-los rerodando o gerador indiscriminadamente.

## Testes executados e resultados

| Verificação | Resultado comprovado |
| --- | --- |
| Parser TMDL | Sem erro; 16 tabelas, 18 relações, 41 medidas, configuração oculta/desconectada |
| Abertura/materialização | PBIP aberto no Desktop pelo agente; nove linhas reais de configuração retornadas; 16 partições Ready, sem ErrorMessage na rodada final |
| Medidas | 41 Valid no mecanismo, incluindo as cinco novas |
| Matriz principal | 45 combinações × 13 posições × três cenários = **1.755 verificações aprovadas**, zero divergências; máximo R$ 0,00 contra view importada; **600 BLANK** coincidentes |
| Cardinalidade da cobertura | Conferida em todas as 1.755 linhas; nas posições elegíveis: integral 29 meses por filial, 2021/2022 12, 2023/JanMai cinco, maio um, junho/JunDez zero, JanMar dois |
| Guardas | Três contextos aprovados: dias parciais, total entre posições e posição/descrição conflitantes; números e pares BLANK |
| Aditividade | **702 comparações derivadas da matriz**, incluindo BLANK, soma de 01/02/03 versus consolidado e 01+02, no mesmo recorte; zero falhas, tolerância R$ 0,01 |
| Regressão das 36 | **1.620 comparações aprovadas**, máximo R$ 0,00 contra view importada no período selecionado original, sem aplicar novo corte às bases |
| Zero/BLANK sintéticos | Duas consultas privadas: R=0/O=-100/P=0 preservados; R=BLANK mantém as três financeiras BLANK e contagem de um par. Expressões redefinidas identicamente em escopo de consulta, não casos reais da origem |
| Integridade | 36 medidas antigas idênticas; fontes/relacionamentos/páginas intactos; consultas de leitura sem mudanças nos arquivos de produção |
| SQL independente | **Não executado pelo agente; não aprovado.** Roteiro e comparador entregues |

Grupos: 01, 02, 03, consolidado e 01+02. Nove períodos: integral, 2021, 2022, 2023, Jan–Mai/2023, Jun–Dez/2023, maio/2023, junho/2023 e janeiro+março/2023 sem fevereiro. A matriz inclui posições 8/11, sempre BLANK. Casos derivados e contagens sobrepostas não representam execuções independentes adicionais.

Evidências finais:

- `docs/evidencias/lote2-3-1-implementacao-20261103-085405/resumo-validacao.json`: consolidação assertiva dos resultados e preservação.
- `docs/evidencias/lote2-3-1-diagnostico-20261103-090110/`: matriz, configuração, guardas e metadados finais.
- `docs/evidencias/lote2-3-1-diagnostico-20261103-085903/14-regressao-36-medidas.json`: regressão executada.
- `docs/evidencias/lote2-3-1-diagnostico-20261103-090240/`: sintéticos finais.
- `docs/evidencias/lote2-3-1-diagnostico-20261103-090326/`: partições Ready e relacionamentos.

Histórico preservado: a primeira expressão da configuração com DATE dentro de DATATABLE passou no parser, mas o mecanismo retornou erro de constante e impediu cinco consultas novas. A configuração foi preservada antes do ajuste; a instância de teste foi fechada normalmente e o fechamento conferido antes da edição. Literais ISO tipados DATETIME foram testados em consulta e materializados após reabrir o PBIP, mantendo os mesmos intervalos. A documentação oficial permite constantes de data em DATATABLE; prevalece a compatibilidade realmente verificada neste mecanismo. Não se declarou a primeira rodada aprovada.

Os dois primeiros sintéticos, sobrescrevendo somente bases na consulta, retornaram valores reais devido às dependências persistidas e **não demonstraram zero/BLANK**. Foram corrigidos apenas nos testes, redefinindo as cinco expressões em escopo da consulta; novos resultados acima comprovam os casos sintéticos. Nenhuma medida de produção foi alterada por causa desses testes.

## Conciliação e pendências de aceite

Guia: **docs/execucao-validacao-l2-3-1.md**. Executar as duas instruções de `docs/testes/lote2-3-1/15-conciliacao-databricks.sql`: preflight sem duplicações e exportação financeira com 1.755 linhas. Comparador `docs/testes/lote2-3-1/comparar-conciliacao.py` compara SQL à matriz DAX por grupo/período/posição/cenário, incluindo cardinalidade e NULL/BLANK, tolerância R$ 0,01. Confirmar mesma atualização antes do aceite. SQL usa a convenção explicitamente em CTE, não como prova de fechamento.

Estado: **L2.3.1 em validação, não concluído**. Falta conciliação SQL independente; salvar/reabrir pelo Desktop após materialização é recomendação adicional de persistência ainda não verificada. Não há testes financeiros de dados futuros ou nova configuração com lacunas/cortes distintos; essa ampliação deve ser validada quando o contrato mudar. Nenhuma liberação para L2.3.2.

## Atualização e recuperação

Se Excel mudar: novo hash/versão → revisar contrato/intervalos com usuário → Desktop fechado e backup novo → atualizar manifesto documental e somente a partição constante aprovada → validar nove chaves ou novo esquema aprovado, não sobreposição e meses → parser/materialização → matriz/regressão/SQL no mesmo snapshot. Nunca estender por MAX de movimento nem preencher BLANK. Relacionamentos continuam desnecessários. Fora do universo configurado, não presumir novos períodos de treinamento.

Para recuperação, fechar Desktop e restaurar os arquivos afetados do backup confirmado; remover a nova configuração somente após conferir caminho e restaurar a referência correspondente em model.tmdl. Não restaurar caches/credenciais nem sobrescrever alterações posteriores sem análise. Não houve restauração sobre produção nesta tarefa.

Limites residuais: convenção fictícia, sincronização manual JSON/TMDL e arquivo local versus snapshot importado; desempenho observado da matriz (~35 segundos para consulta de 1.755 linhas) não é meta de visual; ausência de declaração contábil real. Resultado Líquido segue provisório, EBITDA/EBIT sem cálculo.

---

## Histórico anterior à implementação

Os registros anteriores abaixo ficam preservados; seus bloqueios de investigação não substituem o estado vigente de implementação em validação descrito acima.


# L2.3.1 — investigação de comparabilidade temporal

Data: 02/11/2026. **Bloqueado antes da implementação por ausência de contrato temporal certificado. Zero medidas novas criadas; 36 existentes preservadas.** O usuário restringiu expressamente esta etapa à investigação somente leitura, sem criar controle, modificar medidas/tabelas/views/relações ou fixar maio/2023 como corte.

## Preparação e decisões

AGENTS.md, PLANS.md, plano Lote 2.3, contratos e evidências dos Lotes 2.1/2.2 consultados. Seus aceites técnicos permanecem válidos no escopo documentado. Inspeção das 36 medidas existentes e metadados no mecanismo confirmou inventário, referências às bases e proteções de posição/EBIT.

Recebidas políticas A–D: corte comum entre filiais; percentuais futuros com denominador absoluto quando negativo e BLANK para referência zero/ausente; sinais preservados e favorabilidade por natureza; neutralidade monetária R$ 0,01, sem faixa percentual implícita. A política temporal substitui a recomendação inicial por presença de Realizado da posição. A própria solicitação exige distinguir mês sem movimento de não carregado antes de implementar. Orientação posterior do usuário confirma que manifesto/controle ainda não foi identificado/homologado e manda suspender a implementação até definir esse contrato.

Desktop estava aberto. Somente consultas DAX/INFO de leitura foram executadas, sem atualização, SaveChanges, criação temporária de medidas ou edição externa de fontes. Não foi solicitado fechamento para edição porque a orientação vigente passou a ser somente leitura. Git conferido: diretório fora de repositório, status/rev-parse código 128; nenhum init/commit.

## Evidências executadas

| Consulta | Resultado |
| --- | --- |
| 01-diagnostico-cobertura.dax | 108 linhas: três filiais × 36 meses; diagnóstico de presença de movimentos/valores, não certificado de carga |
| 02-colunas-modelo.dax | 114 colunas retornadas; nenhum campo importado de status de carga completa/fechamento identificado |
| 03-medidas-existentes.dax | 36 medidas existentes, nenhuma das cinco novas |
| 04-rastreabilidade.dax | Nove grupos por filial/arquivo/aba/tabela/ingestão; metadados de origem e presença de linhas |

Quatro consultas executadas com sucesso, zero erros. Saídas CSV/JSON e sessão/hashes: [rodada 1](evidencias/lote2-3-1-diagnostico-20261102-193245/execucao.json), [rodada 2](evidencias/lote2-3-1-diagnostico-20261102-193347/execucao.json). [Resumo da investigação](evidencias/lote2-3-1-investigacao-20261102-193557/resumo-investigacao.json).

| Filial | Meses inspecionados | Meses com lançamentos | Linhas fato | Último mês com movimento | Corte homologado |
| --- | ---: | ---: | ---: | --- | --- |
| 01 — São Paulo | 36 | 29 | 1.247 | maio/2023 | Não determinado |
| 02 — Rio de Janeiro | 36 | 29 | 1.247 | maio/2023 | Não determinado |
| 03 — Florianópolis | 36 | 29 | 1.247 | maio/2023 | Não determinado |

Total: 87 pares filial/mês com linhas, 21 sem linhas (junho–dezembro/2023 nas três filiais). Nos meses entre janeiro/2021 e maio/2023 não há lacuna intermediária de lançamentos observada; isso não comprova fechamento/completude nem ausência de lacunas em outros estados/snapshots. Não há evidência de mês sem movimento **com processamento certificado** nos campos disponíveis. Não foram encontrados valores zero nas linhas da fato desse diagnóstico; não se afirma teste de zero real de origem ou de estorno homologado.

A view possui 13 posições em todos os 108 pares, incluindo os 21 sem lançamentos. Nos meses com movimento, 11 posições têm Realizado presente; nos meses posteriores, nenhum Realizado presente. A existência das 13 linhas não certifica processamento do Realizado; o BLANK de EBITDA/EBIT ou de qualquer posição não determina cobertura global. Não somar as 13 posições para diagnosticar valor financeiro.

Rastreabilidade observada: `_arquivo_origem = BaseDados.xlsx`, abas/tabelas fLancamento1/2/3_ano1/2/3 e horários de `_data_ingestao`. Cada grupo de 2021/2022 contém 516 linhas e 12 competências com linhas; cada grupo de 2023 contém 215 linhas e cinco competências com linhas. Esses campos indicam origem de registros presentes/ingestão do grupo, sem declarar explicitamente todos os meses esperados, sucesso/completude por mês, ausência confirmada de movimento ou fechamento. Nenhum desses horários foi convertido em competência de fechamento.

## Investigação SQL/local e limites de acesso

Foram localizados os roteiros de Fase 1 e SQL de comparação do Lote 2.2. Eles consultam dados/contagens/valores; não contêm contrato autoritativo de fechamento ou definição de produção da view. As partições M apenas navegam as tabelas existentes do Databricks. Não foram encontrados, nos arquivos locais examinados fora dos backups, notebooks/pipelines ou definição SQL de carga que certifiquem a competência sem movimento.

Não há conector Databricks entre as ferramentas disponíveis nesta rodada. Uma tentativa de inventário de navegador falhou na inicialização do runtime (erro de caminho), sem consultar a origem nem alterar credenciais. SQL remoto executado pelo agente nesta investigação: **zero**. Não foi possível verificar controles nas camadas Bronze/Silver/Gold remotas ou obter a definição real da view. Não confundir ausência no modelo importado com inexistência no Databricks; permissões também podem limitar information_schema.

Roteiros remotos preparados, **não executados**:

1. [05-investigar-metadados-databricks.sql](testes/lote2-3-1/05-investigar-metadados-databricks.sql): schemas acessíveis, candidatos a controle, campos/comentários, definição acessível das views, SHOW CREATE como leitura de texto e rastreabilidade. Histórico Delta opcional só após conferir formato/permissão.
2. [06-diagnostico-mensal-databricks.sql](testes/lote2-3-1/06-diagnostico-mensal-databricks.sql): grade mensal, contagens pré-agregadas das fatos e view, sem multiplicar fatos por posições. COALESCE restrito a contagens, não valores financeiros.

Execução exata: no Databricks SQL e warehouse já configurado, abrir 05 e executar cada instrução individualmente. Exportar saídas completas com cabeçalhos, data/hora e indicação de permissões/erros; não executar como DDL o texto de definição retornado. Depois executar 06 e exportar a grade esperada de 108 pares filial/mês. Se houver controle candidato, fornecer schema, contrato/autoridade e resultado que certifique estado por filial/competência/cenário, inclusive mês processado sem movimento. Não preencher ou criar objetos nesta etapa. A descoberta de um nome de tabela ou commit Delta não homologa cobertura por si só.

## Contratos e proposta de controle

Os cinco nomes do plano foram preservados e formalizados como contratos condicionais em [contratos-medidas-dax.md](contratos-medidas-dax.md):

- DRE | Realizado Comparável.
- DRE | Orçado Comparável.
- DRE | Previsto Comparável.
- DRE | Pares Filial-Competência Comparáveis.
- DRE | Status Comparabilidade.

Todos dependem do mesmo certificado temporal confiável e permanecem **não implementados**, inclusive o diagnóstico, sem stub constante. A data comum não será calculada a partir do indicador, soma da fato, presença de Orçado/Previsto ou limite fixo do conjunto atual.

Proposta completa, sem DDL nem criação: [proposta-controle-competencias.md](proposta-controle-competencias.md), candidato `workspace.gold.controle_competencias`, grão filial × competência × cenário, estados de carga/completude/fechamento, confirmação de sem movimento, versão/snapshot e rastreabilidade de processamento/autoridade. Reutilizar controle remoto existente se ele atender ao contrato; criar/consumir novo objeto exigiria aprovação e tarefa própria. Estados elegíveis, fechamento versus dados abertos, lacunas internas, datas parciais e semântica de referência ausente ainda exigem definição.

## Backup, estrutura e preservação

Snapshot de leitura dos arquivos serializados e documentação: `backups/lote2-3-1-investigacao-20261102-193557/`, 372 arquivos incluídos, cinco .pbi excluídos; backups/.git excluídos. ZIP restaurado isoladamente e hashes dos arquivos incluídos conferidos. SHA-256 do ZIP: `FEC746534CB5ECFBA315E2045C02866E732BD5850A02B8BD3982779CD5C20D25`. [Preparação](evidencias/lote2-3-1-investigacao-20261102-193557/preparacao.json) e [manifesto](../backups/lote2-3-1-investigacao-20261102-193557/manifesto-sha256.json).

Como Desktop estava aberto, esse snapshot não inclui alterações possivelmente não salvas em memória/cache; não substitui fechamento e backup atualizado antes de qualquer futura edição. Nenhuma restauração foi aplicada ao projeto original, nem abertura/teste funcional da cópia alegado.

Parser TmdlSerializer executado na definição existente: 15 tabelas, 18 relações, 36 medidas, zero novas. [Parser](evidencias/lote2-3-1-investigacao-20261102-193557/parser-existente.json). É validação da estrutura preservada, não execução das cinco medidas ausentes. [Integridade da produção](evidencias/lote2-3-1-investigacao-20261102-193557/integridade-producao.json) e integridade antes/depois de cada rodada sem alterações. As 36 medidas existentes permanecem intactas; não se declara nova regressão financeira completa nesta rodada, apenas metadados/estrutura e diagnóstico executados.

## Estado e ações necessárias

- [x] Aceites de Lotes 2.1/2.2 e estrutura real conferidos.
- [x] Políticas A–D e mudança de corte documentadas sem alterar decisões anteriores silenciosamente.
- [x] Diagnóstico local executado; rastreabilidade e limites da evidência registrados.
- [x] Snapshot restaurável/hashes verificados e produção preservada.
- [x] Proposta de controle e SQL remoto somente leitura preparados.
- [ ] Investigar metadados/definição SQL remota e identificar ou aprovar fonte autoritativa de cobertura.
- [ ] Homologar estados elegíveis, completude, fechamento/abertura, competência sem movimento e demais guardas temporais.
- [ ] Definir disponibilização do controle no modelo, caso necessário, em escopo aprovado.
- [ ] Confirmar Desktop fechado, backup atualizado e implementar somente as cinco medidas após resolver as dependências.
- [ ] Executar materialização, testes DAX/SQL mensais/cortes e regressão financeira das 36 antes de concluir.

**L2.3.1 bloqueado antes da implementação; não concluído.** Não foi determinada data de corte homologada para filial alguma ou consolidado. Nenhuma medida nova, controle Databricks, tabela, consulta, relacionamento, conexão ou página alterada. Demais sublotes não iniciados. Resultado Líquido provisório; EBITDA/EBIT sem cálculo até homologação contábil.

## Complemento: exportações remotas recebidas em 02/11/2026

Dois CSVs do usuário foram analisados e preservados com hashes em docs/evidencias/competencias-exportacoes-20261102/. Inventário: 28 objetos Bronze/Silver/Gold; histórico: versão 0, commit 2026-11-02T14:30:42.000Z, 3.741 linhas gravadas, sem nome da tabela no arquivo. Detalhes, classificação e pendências em docs/investigacao-remota-competencias.md. O registro anterior de ausência de consultas remotas pelo agente permanece válido; agora há evidência remota parcial fornecida pelo usuário. Não existe certificado mensal comprovado nos anexos; contrato temporal e implementação permanecem bloqueados.

## Resultado da primeira rodada remota fornecida pelo usuário — 02/11/2026

A01/A02/A03/B02 e A04 adicional analisadas; B04 recebida contém histórico, não propriedades. 193 colunas em 28 objetos, sem certificado explícito mensal; três views baseadas em movimentos e sem controle de fechamento nas definições. Evidências, limitações, análise dos zeros/NULL da view e próximas ações registradas em docs/investigacao-remota-competencias.md, seção Primeira rodada recebida. Fontes preservadas em docs/evidencias/competencias-primeira-rodada-20261102/. Não se comprova ausência global de controle. L2.3.1 bloqueado; 87 pares com lançamentos/21 sem lançamentos observados, cobertura dos 21 não certificada. Nenhum novo teste DAX nem alteração de produção.

## B04 correta analisada — 02/11/2026

Recebidas 20 propriedades key/value, todas técnicas, sem certificado de cobertura/fechamento. ID Unity Catalog correspondente ao histórico Delta previamente recebido, conferido localmente. Pendência de B04 incorreta resolvida; evidências em docs/evidencias/competencias-b04-corrigida-20261102/ e detalhamento em docs/investigacao-remota-competencias.md. Contrato temporal permanece não homologado; 21 dos 108 pares sem lançamentos observados ainda sem cobertura certificada. Nenhuma medida ou objeto de produção alterado.

## Homologação didática do contrato — 03/11/2026

Premissa expressa do usuário registrada no contrato DIDATICA-1.0-20261103 e validada documentalmente contra hash do Excel e conjuntos esperados. Realizado coberto didaticamente Jan/2021–Mai/2023; Jun–Dez/2023 não fornecido, sem atribuir processamento vazio; referências Jan/2021–Dez/2023. Não há fechamento real nem teste novo DAX/SQL. Evidência local: docs/evidencias/cobertura-didatica-20261103/validacao.json. Recomenda-se desbloqueio limitado do L2.3.1 após aprovar a tabela local de configuração proposta e cumprir segurança, sem iniciar implementação nesta tarefa. Medidas existentes 36, novas zero; controles contábeis provisórios preservados.



## Homologação final solicitada — aguardando evidências, 03/11/2026

O usuário ratificou os resultados locais já aprovados e informou que fornecerá evidências de persistência e conciliação SQL. Nesta mensagem não vieram novos arquivos, saídas SQL nem confirmação de salvar/fechar/reabrir. Não foram localizadas novas evidências dessas duas pendências na pasta docs do projeto. Não se executou novo teste dinâmico nesta etapa nem se reutilizou a abertura inicial como prova de persistência posterior.

| Critério de aceite final | Resultado nesta recepção |
| --- | --- |
| Persistência após salvar, fechar e reabrir o PBIP | Aguardando evidência; não aprovada nem reprovada |
| SQL independente, preflight e mesma atualização | Aguardando resultados; comparador não executado nesta recepção |
| Casos SQL novos aprovados/reprovados | Zero aprovados, zero reprovados; nenhum caso recebido/comparado, não significa aprovação |
| Divergência máxima SQL | Não apurada |
| Resultados locais anteriores | Mantidos: 1.755 verificações DAX aprovadas/600 BLANK; 1.620 de regressão aprovadas, diferença máxima R$ 0,00 |

Para persistência, fornecer confirmação explícita da sequência salvar → fechar → reabrir e evidências após a reabertura: configuração com nove intervalos/hash/versão correspondentes, oculta/desconectada, 41 medidas válidas e consultas de controle preservadas. A confirmação declarada pelo usuário deve ser identificada como tal, separada das saídas técnicas eventualmente consultadas.

Para SQL, fornecer L231_SQL_preflight.csv (zero linhas esperado; resultado vazio pode ser comprovado por captura identificável) e L231_SQL_comparabilidade.csv completo (1.755 linhas), com SQL/ID e referência de atualização compatível com o modelo. Usar o comparador existente sem alterar medidas/configuração e preservar ausência versus zero. Divergência ou evidência incompleta mantém a validação pendente.

**L2.3.1 em validação, não concluído.** Persistência e SQL tornaram-se critérios explícitos obrigatórios de encerramento nesta solicitação; a recomendação anterior de persistência não equivale ao seu aceite. Nenhuma das 41 medidas ou configuração temporal alterada pelo agente nesta etapa. Ausência de fechamento contábil real não é falha deste contrato didático; tampouco há certificação contábil. L2.3.2 não iniciado.

Pré-requisitos de L2.3.2: aprovação documentada das duas pendências e encerramento técnico de L2.3.1; autorização específica do próximo sublote e confirmação dos contratos M40–M43 (desvios monetários/percentuais, denominador absoluto, zero/BLANK e mesmo recorte); antes de editar, Desktop fechado e backup novo/restaurável, preservando as 41 medidas atuais. Sem ampliar para favorabilidade ou cumprimento.

