# Investigação remota de competências — 02/11/2026

## Resultado e escopo

**Investigação remota não realizada: não foi obtido canal autenticado de consulta ao Databricks nesta sessão. O contrato de cobertura temporal permanece bloqueado.** Não há conclusão sobre a inexistência de controles no catálogo remoto. Nenhuma tabela, view, pipeline, medida, conexão, relacionamento ou página foi alterada; o L2.3.1 não foi implementado.

Preparação: lidos AGENTS.md, PLANS.md, docs/validacao-lote2-3-1.md e docs/proposta-controle-competencias.md. Reutilizados os roteiros 05 e 06 em docs/testes/lote2-3-1/. A investigação desta execução limita-se ao acesso remoto e à preparação documental; não foram repetidos testes do Power BI.

## Acesso e SQL efetivamente executado

| Verificação nesta sessão | Resultado observado |
| --- | --- |
| Inventário de ferramentas disponíveis | Nenhum conector Databricks/warehouse SQL identificado |
| Inicialização do navegador, `cua.getState()` | Falha anterior à navegação: `failed to write kernel assets`, erro de caminho inexistente, os error 3 |
| Document Control, listagem de sessões | Nenhuma sessão conectada |
| `Get-Command databricks -ErrorAction SilentlyContinue` | Nenhum comando retornado no ambiente consultado |
| Consultas SQL enviadas ao Databricks | **0** |
| Objetos inspecionados remotamente | **0** |
| Versões, operações e horários Delta coletados | **Nenhum** |

Esses resultados não demonstram indisponibilidade do serviço, credenciais inválidas ou ausência de autenticação em aplicativos externos. Não foram procurados tokens nem modificadas credenciais. Não há SQL executado remotamente a transcrever: todos os SQLs abaixo estão preparados para execução manual, sem resultados atribuídos a esta sessão.

## Roteiros e instruções exatas

No SQL Editor do Databricks, com o warehouse existente e um usuário com acesso de leitura, executar cada instrução separadamente. Não executar definições DDL retornadas como texto. Guardar erros de autorização; ausência de linhas no information_schema pode refletir permissões.

1. Executar **docs/testes/lote2-3-1/05-investigar-metadados-databricks.sql**: schemas acessíveis; objetos candidatos em todo o catálogo; campos candidatos; definições das views e rastreabilidade Gold. O `SHOW CREATE TABLE` apenas consulta a definição, sem executar o DDL retornado.
2. Executar **docs/testes/lote2-3-1/07-historico-delta-leitura.sql**, instrução a instrução: inventário completo Bronze/Silver/Gold, colunas, DETAIL e propriedades do Realizado Gold. Executar HISTORY somente após confirmar formato Delta. O gerador SELECT retorna instruções de leitura como texto; selecionar manualmente os objetos reais de Realizado e controles encontrados, inspecionar DETAIL/propriedades e, quando Delta, HISTORY em cada camada. Não presumir nomes de tabelas Bronze/Silver.
3. Para cada controle candidato encontrado pelo roteiro 05, inspecionar seu schema e documentação antes de construir SELECT sobre registros. Registrar o SQL exato e verificar filial, competência, cenário, status de carga, completude, fechamento, execução e contagens esperadas/processadas se existirem. Nenhuma consulta de registros com campos presumidos foi preparada como se o objeto existisse.
4. Executar **docs/testes/lote2-3-1/06-diagnostico-mensal-databricks.sql**. Produz a grade filial × mês do calendário, contagens de movimentos/valores presentes/zeros, presença na view, primeiro e último mês com movimento e lacunas intermediárias. A normalização mensal evita perder datas dentro do mês. COALESCE aplica-se somente às contagens, nunca a valores monetários. Executar também o complemento de linhas fora da grade no roteiro 07.
5. Relacionar a grade às execuções e aos certificados candidatos por chave explícita, incluindo meses sem movimento. Registrar separadamente mês sem linhas, mês certificado sem movimento e mês sem certificado. Não considerar orçamento/previsão como prova de carga do Realizado.

Exportar **todos** os resultados em CSV, sem truncamento, com nome do roteiro/instrução/objeto. Guardar SQL executado, identificador da consulta, data/hora e fuso da sessão, warehouse/runtime informado pelo ambiente, mensagens de erro e permissões conhecidas. Para HISTORY preservar todo o histórico retido e campos efetivamente retornados, especialmente versão, timestamp, operação, parâmetros, métricas, execução/job/notebook e userMetadata quando disponíveis. Não inventar campos ausentes. Um histórico retido pode não abranger a ingestão inicial.

Para cada fonte preencher: objeto; SQL/ID; arquivo de resultado; versão/horário; granularidade; estados observados; contagens; vínculo com filial/mês/cenário; autoridade do certificado; classificação; limitações. Exportar eventuais candidatos sensíveis apenas no ambiente autorizado, sem credenciais.

## Classificação das evidências

| Fonte ou evidência | Classificação possível | Situação comprovada nesta execução |
| --- | --- | --- |
| Certificado com chave filial/mês/cenário, completude e autoridade/estado documentados | Comprovação explícita de carga e/ou fechamento, conforme contrato; carga completa e fechamento são declarações distintas | Não consultado remotamente; não homologado |
| Commit Delta, métricas de escrita, job, timestamp de ingestão | Evidência indireta de processamento | Histórico remoto não coletado |
| Contagens mensais, MIN/MAX de competência, linhas da view | Apenas presença de movimentos | Grade SQL remota não executada |
| last_altered, ausência de objetos sem privilégio, mês sem linhas sem manifesto | Evidência insuficiente para cobertura/fechamento | Nenhuma inferência de fechamento autorizada |

Os diagnósticos locais anteriores, descritos em docs/validacao-lote2-3-1.md, observaram 29 meses com movimentos por filial, Jan/2021–Mai/2023, e rastreabilidade por arquivo/aba/ingestão. São evidências históricas locais de movimento/processamento; **não são resultados da investigação remota** e não comprovam meses fechados, carga completa ou ausência de controles não importados.

DETAIL descreve propriedades físicas/metadados; HISTORY descreve operações na tabela. Operação WRITE concluída não certifica todas as competências. `information_schema.tables.last_altered` não é prova suficiente de atualização dos dados, menos ainda de fechamento. Referências oficiais: [DETAIL](https://docs.databricks.com/aws/en/delta/table-details), [HISTORY](https://docs.databricks.com/aws/en/sql/language-manual/delta-describe-history), [limitação de last_altered](https://kb.databricks.com/en_US/unity-catalog/last_altered-column-in-information_schema-not-reflecting-data-modifications).

## Critérios para homologação e limitações

- [ ] Evidências remotas coletadas nas camadas acessíveis, com limitações de permissão registradas.
- [ ] Controle autoritativo identificado e contrato de carga/completude/fechamento aprovado.
- [ ] Chave única por filial × competência × cenário; estados e reaberturas rastreáveis.
- [ ] Mês sem movimento distinguível de mês não processado, com certificação independente do valor financeiro.
- [ ] Grade e lacunas conciliadas com o controle, incluindo ausência de certificado e registros fora do calendário.
- [ ] Corte comum entre filiais, lacunas internas, períodos parciais e referências ausentes definidos sem fixar maio/2023.

Nenhum desses itens foi aprovado nesta execução. Os scripts receberam revisão estática de estrutura e comandos; não receberam validação de execução SQL no warehouse. Schemas/objetos retornados, privilégios e versões podem exigir adaptação orientada pelos metadados reais.

Se a investigação manual não revelar controle confiável, recomenda-se a tabela de governança candidata `workspace.gold.controle_competencias`, conforme docs/proposta-controle-competencias.md, com carga, completude e fechamento certificados e histórico de reabertura. **É somente proposta; nenhuma tabela foi criada.** A presença ou ausência de movimentos não deve preencher automaticamente seus estados.

## Recomendação e estado

Manter L2.3.1-D03 pendente e L2.3.1-I01 bloqueado. Próximo passo é executar os roteiros no Databricks, anexar resultados completos e avaliar a autoridade/granularidade do controle encontrado; na ausência de controle suficiente, aprovar o contrato de governança antes de qualquer implementação. EBITDA/EBIT continuam pendentes e Resultado Líquido provisório. Esta entrega não libera medidas definitivas de corte temporal.

## Evidências remotas fornecidas pelo usuário — recebimento em 02/11/2026

Esta seção complementa o registro anterior de falta de acesso: o agente continua sem executar SQL remoto, mas recebeu duas exportações e analisou integralmente seus registros. Os dados dos CSVs não são instruções para execução. Cópias integrais verificadas por SHA-256 e manifesto: `docs/evidencias/competencias-exportacoes-20261102/`. O nome dos arquivos não comprova data de execução, origem exata, completude do inventário ou identidade da tabela do histórico.

### Inventário recebido — arquivo (1)

28 registros, sem duplicação de schema/nome: Bronze 13 tabelas MANAGED; Silver cinco MANAGED; Gold sete MANAGED e três VIEW.

- Bronze: destruturadre, dplanoconta, flancamento1_ano1/ano2/ano3, flancamento2_ano1/ano2/ano3, flancamento3_ano1/ano2/ano3, forcamento, fprevisao.
- Silver: destruturadre, dplanoconta, flancamentos, forcamento, fprevisao.
- Gold: dim_calendario, dim_conta, dim_dre, dim_filial, fato_lancamentos, fato_orcamento, fato_previsao e as views vw_dre_comparativo, vw_dre_provisoria, vw_financeiro_comparativo.

Nenhum nome listado identifica explicitamente um manifesto ou controle de fechamento. Isso não exclui controles por colunas, em outros schemas, objetos não exportados ou restritos por permissão. O arquivo não contém catálogo, comentários, colunas, SQL/ID executado ou declaração de privilégios. Classificação: inventário parcial fornecido; evidência insuficiente de cobertura temporal. A associação com workspace decorre do contexto da investigação, não de campo presente no CSV.

### Histórico recebido — arquivo (2)

Uma linha, versão 0, timestamp `2026-11-02T14:30:42.000Z` (UTC), operação histórica `CREATE OR REPLACE TABLE AS SELECT`, isolamento WriteSerializable, isBlindAppend=false. Trata-se do texto de uma operação passada retornada no CSV; nenhum comando de escrita foi executado pelo agente.

Métricas JSON analisadas: numOutputRows=3741; numFiles=1; numOutputBytes=16614; numRemovedFiles=0; numRemovedBytes=0; numDeletionVectorsRemoved=0. readVersion, job e userMetadata estão representados por null; há identificadores de notebook/consulta/cluster. Engine informado: Databricks-Runtime/19.12.x-aarch64-photon-scala2.13. Identidade pessoal permanece apenas no anexo original, sem reprodução neste resumo.

**Tabela de origem do histórico não identificada no arquivo.** Os 3.741 registros coincidem numericamente com a contagem local anterior do Realizado, mas a coincidência não prova identidade de objeto, versão importada ou completude. Uma linha exportada não comprova que todo o histórico retido foi fornecido. Classificação: evidência indireta de processamento de uma tabela ainda não vinculada nominalmente; não certifica filial, competência, carga completa ou fechamento. O horário é do commit exportado, não do fechamento financeiro nem necessariamente da consulta.

### Pendências e decisão após os anexos

1. Fornecer SQL/ID da consulta e nome totalmente qualificado da tabela do histórico, preferencialmente junto do DESCRIBE DETAIL correspondente. Não atribuir o histórico à Gold sem essa identificação.
2. Executar/exportar a busca de colunas e controles do roteiro 05, incluindo estados, contagens esperadas/processadas e documentação da autoridade de fechamento.
3. Inspecionar DETAIL/propriedades/HISTORY das tabelas reais identificadas em cada camada. Os nomes acima permitem direcionar a inspeção, mas ainda não foram consultados pelo agente.
4. Executar a grade mensal do roteiro 06 e o complemento fora da grade do 07; confrontar cada par com evidência de processamento/completude, inclusive mês sem movimento.

Nenhum certificado mensal confiável foi demonstrado pelos anexos. Não foi comprovada inexistência global de controle. **L2.3.1-D03 permanece parcialmente investigado e pendente; contrato temporal não homologado e implementação bloqueada.** Proposta de governança preservada, sem criação de tabela. Não foram repetidos testes DAX nem alterados arquivos de produção.

## Continuação: origem do histórico confirmada e terceiro CSV — 02/11/2026

O usuário confirmou expressamente que o histórico Delta recebido pertence a `workspace.gold.fato_lancamentos`, com 3.741 linhas de saída. A pendência de identificação nominal foi resolvida por essa confirmação; o CSV original continua sem nome da tabela e não se alega nova consulta remota de verificação. Commit versão 0 em 2026-11-02T14:30:42.000Z continua sendo evidência de carga técnica, sem certificação mensal ou fechamento.

Terceiro CSV analisado integralmente: `New_Query_2026_11_02_15_53_51 (3).csv`, colunas cod_filial, competencia, qtd_lancamentos, valor_total. São 87 chaves distintas, sem duplicação, três filiais com 29 meses consecutivos cada entre Jan/2021 e Mai/2023; 1.247 lançamentos por filial, total 3.741. Não há lacuna intermediária nas competências presentes. Frente ao universo de 108 pares, faltam 21 chaves (Jun–Dez/2023 nas três filiais). São chaves ausentes da exportação, não meses certificados sem movimento. Nenhuma linha tem contagem zero. O SQL e a identidade temporal do snapshot não constam no CSV; não atribuir automaticamente à Gold sem a consulta de origem. O valor_total não foi usado como certificado de cobertura, nem reinterpretado como valor ajustado de DRE ou homologação financeira.

Cópia preservada com hash conferido e resumo: `docs/evidencias/competencias-exportacoes-20261102/recepcao-3.json`. A análise de continuidade mensal e revisão estática do novo roteiro estão em `revisao-roteiro-unico.json` na mesma pasta.

Roteiro único preparado: `docs/testes/lote2-3-1/08-roteiro-unico-competencias.sql`, reutilizando 05/07/06 e os objetos reais do inventário. Instruções/exportações: `docs/execucao-roteiro-unico-competencias.md`. Inclui metadados de todas as camadas, amostras das nove fontes Bronze e Silver/Gold, rastreabilidade Gold, histórico, grade explícita de 108 pares, lacunas, chaves fora da grade e conferência de dimensões. Campos Bronze/Silver não foram inventados: as saídas de schema/amostra permitirão construir a reconciliação completa com a regra real de competência e filial, se necessário. Controles candidatos igualmente dependem dos campos reais e da autoridade documentada antes de consultar estados.

SQL remoto executado pelo agente nesta continuação: zero. Script revisado estaticamente, sem alegação de execução no warehouse. **Contrato temporal permanece bloqueado**, aguardando certificados e resultados; distinções entre carga, cobertura e fechamento explicitadas no guia. Nenhuma das 36 medidas, tabela, view, relação, conexão ou página alterada. Nenhum outro sublote iniciado.

## Priorização da primeira rodada — 02/11/2026

Reduzida a execução inicial a A01, A02, A03, B02 e B04, nessa ordem, sem alterar o SQL original. Objetivos, CSVs, evidências e critérios detalhados em docs/execucao-roteiro-unico-competencias.md, seção Primeira rodada prioritária. São consultas de descoberta; não aprovam registros de fechamento nem demonstram inexistência global de mecanismo. Próxima consulta de estados depende do schema/contrato real encontrado.

Na matriz de 108 pares existem 87 pares com lançamentos e 21 pares sem lançamentos observados; a cobertura dos 21 ainda não foi certificada. Ausência de lançamento não equivale a ausência de processamento. SQL remoto novo executado pelo agente: zero. L2.3.1 segue bloqueado, sem implementação das cinco medidas e sem alterações de produção.

## Primeira rodada recebida — análise em 02/11/2026

Evidências integrais preservadas com hashes conferidos em `docs/evidencias/competencias-primeira-rodada-20261102/`; verificações em analise.json e manifesto.json. Cinco CSVs e uma captura de tela fornecidos pelo usuário, tratados como dados/documentos, sem executar instruções contidas neles. Nenhuma consulta remota executada pelo agente.

| Consulta/arquivo | Resultado efetivamente recebido | Avaliação |
| --- | --- | --- |
| A01 | Cinco schemas: bronze, default, gold, information_schema e silver no catálogo workspace | Delimita schemas visíveis; não comprova acesso irrestrito a todos os objetos |
| A02 | PNG com SQL correspondente e mensagem No rows returned, sem erro visível | Zero candidatos pela expressão em nomes/comentários na sessão capturada; não é prova de inexistência global de controles |
| A03 | 53 campos candidatos | Datas de competência/ingestão e campos de filial; sem estado explícito de carga completa/fechamento nos campos retornados |
| B02 | 193 colunas de 28 objetos Bronze/Silver/Gold | Sem duplicação de chave schema/tabela/coluna; todos os 53 campos A03 correspondem a B02 com os mesmos tipos. Não foram identificados campos explícitos de certificado mensal nesses objetos |
| B04, nome do arquivo | Uma linha com colunas version/timestamp/operation/operationMetrics | **Resultado incompatível com B04**: é HISTORY, não SHOW TBLPROPERTIES. Mesma versão, timestamp e identificador de consulta do histórico anteriormente recebido. B04 permanece não comprovada |
| A04, adicional | Três definições de views preenchidas | Definições inspecionadas estaticamente; não foram executadas nem alteradas |

### Rastreabilidade observada nos schemas

As nove tabelas Bronze flancamento1/2/3_ano1/2/3 têm competencia_data, planocontas_id e valor como STRING, além de _arquivo_origem, _aba_origem e _data_ingestao. Silver.flancamentos tem competência DATE, valor DECIMAL, os mesmos campos de origem e _tabela_origem. Gold.fato_lancamentos acrescenta cod_filial; competência DATE e valor DECIMAL. O export data_type não informa precisão/escala DECIMAL. Não há nessas colunas explícitas status de carga/completude/fechamento, contagem esperada/processada, responsável de fechamento ou confirmação de mês sem movimento. O tipo STRING das datas Bronze exige verificar formato/conversão antes de reconciliar competências; nenhuma regra foi inventada nesta rodada.

Rastreabilidade é evidência indireta de ingestão dos registros existentes. Não certifica períodos vazios nem completude de cada mês. A ausência desses campos em B02 refuta a hipótese de um certificado explícito nessas colunas visíveis; não exclui outro objeto, pipeline, manifesto externo ou fonte com permissão diferente. default é visível em A01, mas B02 é restrito às três camadas; A02/A03 são buscas por padrões e também têm limites de descoberta.

### Definição real das views: implicações para cobertura

A04 mostra que vw_dre_comparativo une Realizado/Orçamento/Previsão, ajusta o sinal com tipolancamento, agrega movimentos analíticos por filial/mês/posição e calcula subtotais; posições 8 e 11 são explicitamente NULL. Não há consulta a manifesto ou estado de carga/fechamento nas três definições fornecidas.

A estrutura agregada pode apresentar um par filial/mês por haver Orçamento ou Previsão mesmo sem Realizado; isso explica por que a presença da linha da view não certifica processamento do Realizado. A definição não constrói por si só o calendário completo: os pares vêm dos movimentos dos cenários. Dentro de um cenário/mês existente, SUM(CASE ... ELSE 0 END) pode produzir zero para uma posição analítica ausente; a ausência do cenário Realizado inteiro continua NULL no pivot. Essas duas situações não equivalem a certificado de mês sem movimento. Este achado é de inspeção SQL, não um novo teste dinâmico de valores/BLANK.

vw_financeiro_comparativo também aplica tipolancamento e calcula desvios com referência não nula/não zero e ABS no denominador; vw_dre_provisoria parte do Realizado e preserva NULL nas posições 8/11. Não reaplicar sinais no Power BI nem somar as 13 linhas. A revisão não homologa Resultado Líquido ou EBITDA/EBIT contabilmente.

### Decisão e próxima ação dirigida

**Nenhum controle confiável de cobertura ou fechamento foi demonstrado nas evidências recebidas. L2.3.1 permanece bloqueado.** Há evidência de ingestão técnica; cobertura temporal completa e fechamento contábil continuam não certificados. São dimensões distintas de evidência.

Na matriz de 108 pares, há 87 pares com lançamentos e 21 sem lançamentos observados; **a cobertura desses 21 ainda não foi certificada**. Não se infere ausência de processamento e tampouco se considera os 87 completos/fechados apenas por haver movimento.

Prioridade imediata: executar a B04 original `SHOW TBLPROPERTIES workspace.gold.fato_lancamentos;` e exportar o resultado de propriedades, sem renomear o histórico como propriedades. Depois, para diagnóstico dos pares e da linhagem, reutilizar C01 e A06 do roteiro 08; essas consultas não homologam fechamento. Para desbloqueio, é necessária documentação/manifesto autoritativo ou controle externo que declare cobertura mensal, completude, meses sem movimento e autoridade de fechamento. Se não existir, seguir a proposta de governança em docs/proposta-controle-competencias.md mediante aprovação própria, sem criar objeto nesta investigação. Repetir históricos ou amostras de movimentos isoladamente não resolve essa dependência.

Não se marcou D03 concluída. Nenhum SQL original ou arquivo de produção alterado; 36 medidas preservadas; cinco novas não implementadas; outros sublotes não iniciados.

## B04 corrigida recebida — 02/11/2026

Novo B04_propriedades_gold.csv analisado integralmente: estrutura key/value, 20 propriedades, sem chaves duplicadas. Cópia independente preservada em docs/evidencias/competencias-b04-corrigida-20261102/, hash da cópia conferido com o original e resumo em analise.json. O anexo anterior com nome B04 contendo HISTORY foi preservado como histórico, sem sobrescrita.

As propriedades recebidas são técnicas: clusterByAuto, clusteringColumns, checkpoint v2, deletion vectors, row tracking, recursos/protocolos Delta, versões mínimas de leitor/escritor, compressão zstd, formato parquet e identificador Unity Catalog. Não há estado de carga/completude/fechamento, referência explícita a manifesto mensal, contagens esperadas por filial/competência ou autoridade contábil entre as 20 propriedades exportadas. A existência de row tracking não certifica cobertura mensal nem fechamento.

io.unitycatalog.tableId = 544e577c-d871-46b2-8d08-5281ab2e7862 coincide com a propriedade registrada em operationParameters.properties do histórico Delta anterior, já atribuído pelo usuário a workspace.gold.fato_lancamentos. Isso reforça a vinculação técnica entre as exportações, sem comprovar completude temporal. A correspondência de IDs foi efetivamente calculada localmente, não é nova consulta ao Databricks.

**B04 recebida e analisada; a pendência de arquivo incorreto foi resolvida.** A primeira rodada prioritária A01/A02/A03/B02/B04 está analisada no escopo dos anexos fornecidos (A02 como captura), com A04 adicional. Nenhum certificado confiável de cobertura/fechamento foi demonstrado. Não se declara inexistência global de controle externo ou restrito por permissão.

**Contrato temporal não homologado; L2.3.1 permanece bloqueado.** Há 87 pares com lançamentos e 21 sem lançamentos observados na matriz de 108; a cobertura dos 21 segue não certificada. Não inferir ausência de processamento. Próximo passo decisivo é obter manifesto/contrato ou evidência autoritativa do produtor/Controladoria, inclusive meses sem movimento, ou aprovar a governança proposta em tarefa própria. C01/A06 continuam úteis ao diagnóstico, mas não substituem certificado. Nenhum script novo, tabela ou medida criada; nenhuma alteração de produção e zero SQL remoto executado pelo agente.

## Proposta final de manifesto — 02/11/2026

Contrato produzido em docs/contrato-cobertura-temporal.md, com matriz integral de 108 pares Realizado: 87 com lançamentos e 21 sem lançamentos observados. Todos os estados de completude, processamento sem movimento certificado, não carga confirmada e fechamento permanecem desconhecidos; nenhum certificado atribuído.

Somente evidência antes não auditada foi investigada: cópia local BaseDados.xlsx, em leitura OOXML. Treze abas, nove de lançamentos totalizando 3.741 registros, 29 meses por filial e 43 registros por mês. Orçamento/Previsão: 4.644 registros e 36 meses por aba. Sem manifesto/autoria certificado identificado; ausência de termos não exclui controle externo. Hash do arquivo preservado; identidade com arquivo ingerido ainda depende do produtor. Parte binária xl/metadata não interpretada, limitação registrada. Não foram localizados notebooks de ingestão exportados nem termo autoritativo do produtor nos arquivos do projeto consultados; notebook remoto do histórico não acessado. Não se repetiu B04 nem qualquer consulta de metadados.

Evidências novas: docs/evidencias/contrato-cobertura-20261102/inspecao-arquivo-produtor.json, matriz-108.csv e validacao.json. Proposta define papéis ainda não nomeados, requisitos de declaração e vínculo de snapshot, homologação técnica separada da contábil, reabertura e preenchimento dos 21 pares sem inferir processamento. Contrato não homologado; L2.3.1 continua bloqueado, cinco medidas não implementadas, produção preservada e demais sublotes não iniciados.

## Atualização vigente — premissa didática, 03/11/2026

A declaração do usuário de base fictícia e períodos disponibilizados fundamenta o contrato DIDATICA-1.0-20261103, vinculado ao hash conferido de BaseDados.xlsx. Não há certificação real nova. Cobertura didática: Realizado Jan/2021–Mai/2023 nas três filiais; Jun–Dez/2023 não fornecido; Orçado/Previsto Jan/2021–Dez/2023. Os bloqueios históricos por ausência de fechamento real deixam de impedir por si sós o treinamento. Desbloqueio do L2.3.1 recomendado após aprovação do desenho estrutural e segurança de edição; nenhuma implementação nesta entrega. Detalhes em docs/contrato-cobertura-temporal.md e PLANS.md. Matriz técnica desconhecida preservada separadamente da convenção; validacao.json em docs/evidencias/cobertura-didatica-20261103/ comprova apenas verificação local/documental e conjuntos, não DAX/SQL.
