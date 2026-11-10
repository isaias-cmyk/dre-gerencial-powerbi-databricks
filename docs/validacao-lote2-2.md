# Lote 2.2 — implementação e validação

Data: 02/11/2026. Responsável: Codex. **Lote 2.2 concluído tecnicamente: DAX ampliado aprovado e 1.155/1.155 conciliações SQL independentes aprovadas no grão acordado. Lote 2.3 liberado somente para planejamento, sem implementação iniciada.**

## Preparação, escopo e proteção

Lidos AGENTS.md, PLANS.md, plano do Lote 2.2, contratos, aceite/validação do Lote 2.1 e TMDL real das seis medidas. Lote 2.1 concluído tecnicamente confirmado. Desktop e mecanismo fechados, verificados por processos no host antes do backup e imediatamente antes da edição; [evidência](evidencias/lote2-2-20261102-163559/desktop-antes-edicao.json). Nenhuma aplicação foi encerrada pelo agente.

Plano confrontado com a solicitação: sem divergência funcional. Autorizadas as dez posições e três cenários, total 30; nomes exatos e contratos individuais registrados em contratos-medidas-dax.md antes da escrita TMDL. O plano anterior foi preservado como histórico, com adendo de escopo. Estratégia CALCULATE + KEEPFILTERS compatível com as bases; sem filtros substitutivos.

Git continua fora de repositório: status/rev-parse código 128. Não houve init, commit ou publicação. Diferenças preexistentes desde a baseline da rodada anterior: PLANS.md, model.tmdl, _Medidas.tmdl, cache e dois localSettings. Novos arquivos preexistentes, inclusive consultas salvas pelo Desktop, estão na baseline atual. Causas não presumidas; todo o estado de entrada foi preservado. O snapshot atual, não uma versão antiga, é a referência deste lote. [Preparação/diferenças](evidencias/lote2-2-20261102-163559/preparacao.json).

Backup atualizado: `backups/lote2-2-20261102-163559/`, 237 arquivos incluídos, cinco .pbi excluídos explicitamente; backups e .git excluídos. Snapshot/ZIP e restauração isolada conferidos por SHA-256 para todos os arquivos incluídos. ZIP SHA-256 `FA29E6155CB41F16A4495475BD71244A8440DB99049BE24D48D944C37BC5CCAC`. [Manifesto](../backups/lote2-2-20261102-163559/manifesto-sha256.json). Configurações/cache excluídos não foram editados; backup no mesmo disco não protege contra perda física.

## Medidas implementadas

Cada indicador abaixo tem as medidas `DRE | <Indicador> Realizado`, `DRE | <Indicador> Orçado` e `DRE | <Indicador> Previsto`:

| Posição | Indicador / pasta DRE |
| --- | --- |
| 1 | Receita Operacional Bruta |
| 2 | Deduções da Receita |
| 3 | Receita Operacional Líquida |
| 4 | Custos |
| 5 | Margem de Contribuição |
| 6 | Despesas Operacionais |
| 7 | Resultado Financeiro |
| 9 | Depreciação e Amortização |
| 10 | Outras Receitas e Despesas |
| 12 | Provisão para IR e CSLL |

Catálogo com os 30 nomes exatos, cenários, colunas, pastas e lineageTags: [JSON](evidencias/lote2-2-20261102-163559/catalogo-novas-medidas.json). Contratos individuais: [contratos-medidas-dax.md](contratos-medidas-dax.md), seção Lote 2.2.

Único arquivo de produção alterado: `DRE Moderno - Databricks.SemanticModel/definition/tables/_Medidas.tmdl`. Inseridos 30 blocos antes da coluna auxiliar, conservando os bytes originais restantes. As seis medidas, coluna, partição e identificadores existentes foram preservados. Nenhuma alteração em model.tmdl, tabelas anteriores, consultas M, conexões, credenciais, relações, PBIP/PBIR, páginas, visuais ou AGENTS.md.

Todas reutilizam uma base com interseção na posição fixa; preservam sinais ajustados, Filial/Calendário e BLANK. Posições/descrições incompatíveis retornam BLANK. Seleção múltipla que inclua a posição e total geral retornam somente a posição específica; não somam as posições. Bases mantêm BLANK em múltiplas posições. Posições 3 e 5 leem valores da view, sem recomposição. Margem de Contribuição é monetária. Sem ABS, COALESCE, tipolancamento, percentuais, desvios ou YTD nas medidas. Conta/dim_dre continuam sem propagação automática à view.

## Testes estáticos executados

- Parser TmdlSerializer instalado desserializou snapshot de entrada e definição final sem erro: 15 tabelas, 18 relações, oito partições M e 6 → 36 medidas.
- Trinta nomes novos únicos; expressões e posições comparadas com o catálogo, com formato monetário, pasta, descrição e lineageTag.
- As seis medidas existentes comparadas propriedade a propriedade: nome, expressão, descrição, formato, pasta, lineageTag e visibilidade inalterados.
- Coluna auxiliar oculta e partição DATATABLE constante preservadas; nenhum relacionamento novo.
- 39 arquivos protegidos de entrada conferidos por hashes; nenhum alterado.
- 180 lineageTags únicos; 124 JSON analisados sintaticamente.
- Dez consultas DAX com delimitadores balanceados e sem DEFINE MEASURE; isso não representa compilação DAX.

Evidências: [parser/medidas](evidencias/lote2-2-20261102-163559/validacao-tmdl.json), [verificação estática](evidencias/lote2-2-20261102-163559/verificacao-estatica.json), [preservação dos bytes](evidencias/lote2-2-20261102-163559/preservacao-seis-medidas.json). Script de parser: [lote2-2-validar.ps1](evidencias/lote2-2-validar.ps1). Inventário final: [arquivos-alterados.json](evidencias/lote2-2-20261102-163559/arquivos-alterados.json).

## Execução pendente — Power BI Desktop

Após terminar as gravações, abrir o PBIP atualizado. Confirmar 36 medidas e _Medidas materializada/sem erro. Executar um arquivo DAX por vez na Exibição de Consulta DAX, sem criar medidas temporárias ou de produção. Usar contexto inicial sem filtros externos e registrar catálogo, versão, data/atualização e resultados completos. Não editar TMDL com Desktop aberto.

| Arquivo em docs/testes/lote2-2 | Esperado / critério |
| --- | --- |
| 01-metadados.dax | 36 linhas, seis antigas + 30 novas, todas Valid, sem duplicação; conferir metadados com catálogo |
| 02-filiais-periodos-conciliacao.dax | 1.155 linhas: 33 medidas (30 novas + três RL) × cinco grupos de filial × sete recortes; Aprovado TRUE em todas e AusenciaAposMaio TRUE nas linhas Realizado; NULL/BLANK distinguido de zero |
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
- [x] Consultas DAX persistidas executadas, complementadas e resultados/erro corrigido registrados nas rodadas de validação final abaixo.
- [x] Recebida exportação SQL independente completa e executado o comparador: 1.155/1.155 chaves aprovadas, sem ausência ou duplicação, dentro de R$ 0,01.
- [x] Metadados monetários, materialização e regressões conferidos no modelo carregado; sem nova inspeção visual de cartões/páginas, conforme limitação registrada.
- [x] Aceite técnico do Lote 2.2 registrado com evidências DAX/SQL no grão acordado; não constitui homologação contábil ou conciliação mensal individual.

**Histórico da implementação estática: DAX = 0; SQL = 0 naquela entrega.** A execução DAX posterior está registrada na seção final deste documento. Desktop estava fechado para edição e não foi aberto pelo agente. Parser e inspeção estática não compilam/avaliam DAX, não validam a origem atual nem materializam a nova versão. O aceite do Lote 2.1 não é teste das 30 medidas novas. Nenhuma aprovação dinâmica foi presumida.

Resultado Líquido permanece provisório; EBITDA/EBIT não calculados e pendentes de homologação contábil. Não iniciar Lote 2.3 ou páginas. Em caso de falha: registrar erro, fechar Desktop, preservar estado atual e recuperar somente _Medidas.tmdl da cópia verificada em pasta isolada; revalidar dependências e dados antes de substituir qualquer arquivo. Não restaurar caches/configurações ou sobrescrever trabalho posterior.

## Recepção para análise dos resultados — 02/11/2026

O usuário solicitou análise de resultados DAX e SQL que fornecerá. Nesta solicitação ainda não foram apresentados resultados, exportações ou logs de execução do Lote 2.2. Os arquivos localizados em docs/testes/lote2-2 e docs/evidencias/lote2-2-20261102-163559 contêm roteiros, catálogo e validações estáticas; não comprovam execução dinâmica.

Permanece pendente receber as saídas completas das dez consultas DAX e da SQL de referência, incluindo eventuais erros e identificação/data da atualização consultada. A consulta DAX 02 e a SQL devem conter as 1.155 chaves para conciliação. As demais saídas comprovam metadados, posição/descrição, filtros, totais, aditividade, BLANK, EBITDA/EBIT, regressões e materialização; a conciliação de valores isolada não substitui esses testes.

Nenhum resultado financeiro novo foi validado nesta etapa e nenhuma execução foi atribuída ao usuário sem evidência recebida. Aceite definitivo permanece pendente; produção preservada e Lote 2.3 não iniciado. Após receber os dados, registrar proveniência, resultados efetivos por medida/critério, divergências e testes ausentes antes de decidir o aceite.

## Resultado recebido posteriormente — consolidado integral

Recebidas 30 linhas pelo usuário, compatíveis com a consulta `docs/teste-consolidado-lote2-2.dax`. Proveniência: saída colada pelo usuário, sem nova execução DAX ou SQL pelo agente. Contexto identificado nas linhas: **Consolidado, 01/01/2021 a 31/12/2023**. A data da execução, versão do Desktop e identificação da atualização não constam do anexo. O registro anterior de ausência de resultados permanece histórico e é superado por esta recepção somente no contexto comprovado.

Evidências preservadas: [original TSV](evidencias/lote2-2-consolidado-recebido-20261102/resultado-original.tsv), [CSV com cabeçalhos](evidencias/lote2-2-consolidado-recebido-20261102/resultado-com-cabecalho.csv) e [análise objetiva](evidencias/lote2-2-consolidado-recebido-20261102/analise.json). Análise reproduzível em [lote2-2-analisar-consolidado.py](evidencias/lote2-2-analisar-consolidado.py). O TSV original, sem cabeçalhos, foi interpretado na ordem das 15 colunas da consulta consolidada e preservado sem alterações.

- **Cobertura:** 30 nomes distintos, exatamente os do catálogo aprovado; dez indicadores × três cenários. Posições 1–7, 9, 10 e 12 e associação medida/cenário conferidas em todas as linhas.
- **Conciliação local:** 30/30 valores de medida iguais ao cálculo direto sobre a posição correspondente da view importada; todas as diferenças são zero, Aprovado TRUE e Status OK. Nenhuma divergência de valor ou sinal detectada nesse contexto.
- **Sinais observados:** posições 1, 3 e 5 positivas; 2, 4, 6, 7, 9, 10 e 12 negativas nos três cenários. Coincidem com o cálculo direto recebido; isso não estabelece uma regra universal de sinal para indicadores mistos nem homologa sua composição contábil.
- **Receita Líquida e Margem de Contribuição:** recalculadas na análise das linhas recebidas somente como verificações aritméticas. Receita Líquida = Bruta + Deduções e Margem = Líquida + Custos coerentes nos três cenários; maior resíduo absoluto R$ 0,00000009, abaixo de R$ 0,01. Nenhuma fórmula de produção alterada.
- **Limite de BLANK:** todas as 30 linhas têm valores presentes; não há caso BLANK recebido. Esta saída não comprova ausência após maio/2023, contexto vazio ou conflito de posição/descrição.
- **Limite dos totais/filtros:** comprova o valor consolidado de cada posição no recorte integral; não comprova filiais individuais, seleção múltipla, recortes anuais/mensais, soma das filiais, matriz com linhas conflitantes ou total geral.

**Aceite parcial:** comparação das 30 medidas com a view importada aprovada no consolidado integral apresentado. Não constitui conciliação SQL independente. Não foram recebidas evidências novas de Resultado Líquido, EBITDA/EBIT, metadados/estado ou materialização neste anexo. Controles integrais dos cenários têm disponibilidades distintas e não representam desempenho em períodos equivalentes.

Permanecem pendentes os demais testes DAX e a SQL com comparação das 1.155 chaves, além da identificação de atualização compatível entre origem e modelo. Nenhum item de aceite integral foi encerrado apenas com essas 30 linhas. **Lote 2.2 não concluído; Lote 2.3 não iniciado.** Nesta análise apenas documentação, cópia de evidências e script de análise foram escritos; nenhum arquivo de produção foi modificado.


## Validação dinâmica final ampliada — 02/11/2026

O usuário confirmou os seis cenários originais e autorizou a ampliação. Executada a matriz de cinco seleções (01, 02, 03, consolidado, 01+02) × sete recortes (integral, 2021, 2022, 2023, Jan–Mai/2023, Jun–Dez/2023, junho/2023). Os seis cenários originais estão cobertos e também foram executados em lote pelo roteiro 13, reutilizando a expressão da consulta consolidada sem alterar seu arquivo original.

**Proveniência desta rodada:** execução real pelo agente via ADOMD local, no modelo já carregado. Não foi atualizada, salva ou modificada a produção. Identificação do catálogo, horários e hashes constam em sessao.json/integridade.json de cada rodada. Os resultados recebidos anteriormente continuam preservados como histórico, agora complementados pelas execuções locais.

| Validação | Resultado comprovado |
| --- | --- |
| 30 medidas novas × 35 combinações | 1.050 executadas, 1.050 aprovadas, zero reprovadas |
| Diferença medida × view importada | Máxima R$ 0,00; sinais preservados |
| BLANK nas medidas novas | 100 casos verificados; ausência não convertida em zero; zero valores legitimamente iguais a zero encontrados nessa matriz |
| Três RL adicionais | 105/105 aprovações; dez BLANK |
| Seis cenários originais | 180/180 aprovações; dez Realizado do consolidado Jun–Dez/2023 BLANK, não zero |
| Posição/descrição/conflito/ausência | 240/240 casos aprovados |
| Total e linhas de matriz | 420 células verificadas; sem repetição em posição conflitante |
| Soma de filiais por período | 462/462 aprovações: 231 consolidado = 01+02+03 e 231 seleção 01+02 = soma de 01 e 02; maior resíduo absoluto R$ 0,000000089 |
| Regressão das seis medidas antigas | 210/210 verificações financeiras nas 35 combinações; 175 contextos ampliados com 1.050 valores conferidos; cinco contextos integrais comparados com resultados de Lote 2.1 e seis controles integrais conferidos |
| EBITDA/EBIT | 70 contextos, 2.520 células BLANK nas 36 medidas; sem cálculo habilitado |
| Receita Líquida e Margem | 105/105 verificações de identidades coerentes |
| Metadados/estado | 36 medidas Valid; 15 partições Ready sem erro; _Medidas materializada com uma linha/auxiliar zero |
| SQL independente | Não executado; zero casos conciliados com Databricks SQL nesta rodada |

As contagens dos testes específicos se sobrepõem à matriz por propósito de regressão; não representam novos casos independentes a somar. Nenhuma combinação filial/período/indicador/cenário falhou na matriz principal. A lista de divergências atuais está vazia.

**Correção do teste:** a primeira execução do roteiro 02 falhou por UNION com quantidades diferentes de colunas. A coluna AusenciaAposMaio existia apenas nos blocos de Realizado; os blocos Orçado/Previsto foram uniformizados no script de teste, sem mudança de medidas. A reexecução devolveu as 1.155 linhas previstas e foi aprovada. Total da rodada: 16 tentativas, 15 execuções bem-sucedidas e uma falha histórica de script corrigida; não ocultar esse erro nem apresentá-lo como falha atual do modelo.

Evidências: [resumo](evidencias/lote2-2-validacao-final-20261102/resumo.json), [35 combinações](evidencias/lote2-2-validacao-final-20261102/grupos-filtros.csv), [aditividade](evidencias/lote2-2-validacao-final-20261102/aditividade.csv), [divergências](evidencias/lote2-2-validacao-final-20261102/divergencias.json). Saídas CSV/JSON e logs completos nas pastas lote2-2-execucao-20261102-185937, -185954, -190116 e -190257. Cada rodada contém evidência de ausência de mudança nos hashes dos arquivos de produção.

[Guia de execução final](execucao-final-lote2-2.md) contém os seis cenários, scripts reutilizados/complementos e instruções exatas de Desktop/Databricks. A SQL existente em docs/testes/lote2-2/10-referencia-databricks.sql foi preservada e corresponde às mesmas 1.155 chaves da DAX 02. O CSV DAX para conciliação está em docs/evidencias/lote2-2-execucao-20261102-185954/02-filiais-periodos-conciliacao.csv. Falta executar o SELECT na origem e comparar a exportação real pelo comparador preparado, com estado de dados equivalente, NULL coincidente e tolerância R$ 0,01. Nenhum conector de execução Databricks estava disponível entre as ferramentas desta rodada; não foi presumida indisponibilidade do serviço ou de suas credenciais.

**Status: testes DAX ampliados aprovados; Lote 2.2 não concluído, aguardando a conciliação SQL independente.** Não confundir comparação medida × view importada com comparação contra a origem. As homologações contábeis permanecem pendentes. Nenhuma inspeção visual adicional de páginas/cartões ou teste de desempenho foi realizada. Resultado Líquido continua provisório; EBITDA/EBIT sem cálculo; Lote 2.3 não iniciado.


## SQL independente recebido — conciliação parcial e bloqueio de cobertura

Recebido anexo do usuário com cabeçalho grupo_filial, periodo, posicao, cenario, linhas_fonte, valor e valores_presentes. Proveniência: resultado SQL executado no Databricks e fornecido pelo usuário; nenhuma nova execução SQL pelo agente. Original preservado em [resultado-original.tsv](evidencias/lote2-2-sql-recebido-20261102/resultado-original.tsv), convertido sem alteração dos valores em [resultado-sql.csv](evidencias/lote2-2-sql-recebido-20261102/resultado-sql.csv). Data/hora da consulta e identificação da atualização da origem não foram informadas no anexo.

O comparador de exportações existente foi executado contra o CSV DAX da rodada -185954. Rejeitou a cobertura com código de saída 1: esperava 1.155 chaves, mas recebeu 1.000. Não gerou aprovação completa. O comparador original não foi alterado para relaxar esse critério. [Registro da rejeição](evidencias/lote2-2-sql-recebido-20261102/comparador-original-status.json).

Foi realizada comparação complementar das 1.000 chaves disponíveis, com a exportação JSON DAX da mesma rodada, usando Decimal e preservando NULL/BLANK. [Script reproduzível](evidencias/lote2-2-conciliar-sql-parcial.py), [resumo](evidencias/lote2-2-sql-recebido-20261102/resumo.json) e [comparações por chave](evidencias/lote2-2-sql-recebido-20261102/comparacao-parcial.csv).

- 1.000 chaves únicas recebidas, todas pertencentes ao conjunto DAX esperado.
- 1.000 conciliações aprovadas; zero divergências monetárias ou de ausência entre as linhas recebidas.
- Maior diferença absoluta: R$ 0,00000008, inferior à tolerância R$ 0,01; arredondada a centavos, R$ 0,00.
- 88 casos com NULL SQL e BLANK DAX coincidentes; ausência não convertida em zero.
- 155 chaves SQL ausentes, não consideradas aprovadas e não reconstruídas por inferência.

| Grupo / período sem cobertura completa | Chaves ausentes |
| --- | ---: |
| Consolidado / 2023 | 23 |
| Consolidado / 2023_JanMai | 33 |
| Consolidado / 2023_JunDez | 33 |
| Consolidado / 2023_Junho | 33 |
| Consolidado / Integral | 33 |

Lista exata de filial/grupo, período, posição e cenário faltantes: [chaves-ausentes.csv](evidencias/lote2-2-sql-recebido-20261102/chaves-ausentes.csv). O anexo termina no consolidado/2023/posição 4/Orçado; a quantidade exata de 1.000 linhas sugere um limite de cópia/exportação, mas a causa não foi comprovada. Exportar o resultado completo, sem limitar a 1.000 linhas, em vez de presumir os valores restantes. Pode ser fornecido o CSV integral de 1.155 linhas ou complemento identificável das 155 chaves; duplicações/conflitos devem ser conferidos antes de reunir arquivos.

O grão conciliado é grupo de filial × recorte temporal × posição × cenário. Não contém competência mensal individual; portanto esta comparação não comprova cada mês separadamente. Se esse critério mensal for exigido para o aceite final, fornecer exportações SQL/DAX no grão mensal correspondente. Não declarar essa cobertura a partir dos recortes agregados.

**Lote 2.2 bloqueado para aceite por exportação SQL incompleta.** Não há divergência financeira detectada nas 1.000 linhas disponíveis; falta cobertura para concluir a homologação. A validação DAX anterior permanece aprovada. Lote 2.3 não liberado nem iniciado. Resultado Líquido provisório e EBITDA/EBIT pendentes de homologação contábil. Nesta etapa somente evidências, script de comparação e documentação foram escritos; arquivos de produção preservados.


## Homologação técnica final — CSV SQL completo recebido em 02/11/2026

Recebido `C:\Users\<usuario>\Downloads\New_Query_2026_11_02_15_53_51.csv`: 1.155 registros, sem incluir cabeçalho. Proveniência: exportação da consulta independente Databricks fornecida pelo usuário; nenhuma nova consulta à origem executada pelo agente. O arquivo foi preservado integralmente em [cópia da evidência](evidencias/lote2-2-sql-completo-20261102/New_Query_2026_11_02_15_53_51.csv), com SHA-256 em [aceite.json](evidencias/lote2-2-sql-completo-20261102/aceite.json). O nome do arquivo não comprova horário da execução; essa limitação foi preservada.

O comparador original foi executado, sem relaxar os critérios, contra o CSV DAX da rodada -185954: saída código 0, Casos = 1.155, Divergencias = 0, Aprovado = TRUE. [Resultado do comparador](evidencias/lote2-2-validacao-final-20261102/conciliacao-sql-completa.json). Conferência complementar com Decimal, contagens e sinais: [script](evidencias/lote2-2-homologar-sql.py), [comparação por chave](evidencias/lote2-2-sql-completo-20261102/comparacao-completa.csv).

| Critério | Resultado comprovado |
| --- | --- |
| Cobertura de chaves | 1.155 esperadas e recebidas; conjuntos SQL/DAX iguais, sem duplicações ou ausências |
| Aprovações / reprovações | 1.155 / 0 |
| Diferença monetária máxima | R$ 0,00000010 (R$ 0,00 a centavos), abaixo de R$ 0,01 |
| NULL SQL × BLANK DAX | 110 casos coincidentes; preservados sem conversão em zero |
| Sinais financeiros | Coincidentes entre valores SQL e DAX nos casos com valor |
| Contagem de linhas e valores presentes | Coerentes com filiais e competências disponíveis em todos os recortes/cenários |
| Anexo anterior de 1.000 linhas | Todas as linhas coincidem com a exportação completa; 155 chaves faltantes agora cobertas |

**Grão de aceite:** grupo_filial × periodo (recorte agregado) × posicao × cenario. Cinco seleções de filial, sete períodos, 11 posições (dez indicadores do lote e Resultado Líquido para regressão) e três cenários. Esse é exatamente o grão do roteiro de referência e da exportação DAX comparada. As contagens de competências foram verificadas por recorte; os valores de cada mês individual não foram exportados/conciliados separadamente. Não declarar homologação mensal individual a partir deste aceite. Os valores disponíveis de todos os recortes conciliam, sem divergência que indique atualização incompatível; a identidade temporal exata de atualizações não é comprovada somente pelo conteúdo agregado ou nome do CSV.

Com as evidências DAX já aprovadas (1.050 medidas novas, 100 BLANK, filiais, contextos, totais, regressões e supressão de EBITDA/EBIT), a pendência da conciliação SQL no escopo acordado está resolvida. Os registros anteriores de bloqueio por exportação incompleta são históricos e ficam superados por esta exportação completa e comparação real.

**Lote 2.2 concluído tecnicamente em 02/11/2026. Lote 2.3 liberado exclusivamente para planejamento, não iniciado.** Fase 2 permanece em andamento. Nenhum arquivo de produção, conexão, consulta M, medida, relação ou página foi alterado nesta homologação. Resultado Líquido continua provisório; EBITDA/EBIT permanecem sem cálculo e sem homologação contábil. O aceite não cobre páginas futuras, desempenho, RLS ou detalhe mensal/por conta não testado.
