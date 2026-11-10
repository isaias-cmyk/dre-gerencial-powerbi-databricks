# L2.3.1 — implementação e validação, 03/11/2026

**Implementado, em validação; não concluído.** Abertura do PBIP, materialização, medidas e testes locais confirmados. Falta conciliação SQL independente deste sublote. Nenhum outro sublote iniciado. A convenção didática não certifica fechamento contábil real.

## Autorização, segurança e alterações

Solicitação anexada pelo usuário aprovou a tabela local e as cinco medidas; nome adotado **_ConfigCobertura**, substituindo o nome candidato _CoberturaTemporal do desenho. AGENTS.md, PLANS.md, planejamento, contrato didático e contratos de medidas consultados. Lotes 2.1 e 2.2 tecnicamente aceitos, conforme evidências anteriores; não são homologação contábil.

Desktop inicialmente aberto: usuário confirmou fechamento, seguido de verificação real dos processos no host. Git status/rev-parse retornou 128, diretório fora de repositório; nenhum init/commit. Backup `backups/lote2-3-1-implementacao-20261103-085405/snapshot.zip`, 412 arquivos, restauração de teste conferida por SHA-256. ZIP SHA-256 `f9743c8019f62695617c4b30302267ac6fb755566df4b1fadc9c0f7d7743c117`. Exclusões: backups, .git e .pbi; inclui fontes/documentação/Excel. [Preparação](preparacao.json), [baseline](baseline.json) e [integridade inicial](integridade-estatica.json), nesta pasta de evidências. Os links relativos desta cópia são locais à pasta; no relatório consolidado usar o diretório de evidências citado abaixo.

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

