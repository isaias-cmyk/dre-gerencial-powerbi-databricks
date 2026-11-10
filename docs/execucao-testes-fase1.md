# Execução dos testes dinâmicos da Fase 1

**Estado final em 02/11/2026: Fase 1 concluída com aceite técnico; Fase 2 liberada, ainda não iniciada.** As 23 consultas DAX/INFO registradas são compatíveis com a conciliação SQL independente informada pelo usuário (16 linhas, diferenças consolidadas de R$ 0,00 nos três cenários e totais por filial coincidentes). O usuário aprovou a estratégia DRE e os limites de Conta. Ver [aceite final da auditoria](auditoria-modelo-semantico.md) e [registro de proveniência](evidencias/fase1-aceite-tecnico/aceite.json). Resultado Líquido, EBITDA e EBIT permanecem pendentes de homologação contábil.

As seções de preparação e instruções abaixo preservam o roteiro da auditoria, incluindo limitações anteriores à abertura do modelo. Esses bloqueios históricos foram encerrados pelo aceite técnico; os scripts continuam disponíveis para manutenção e novos testes quando necessários.

## O que foi possível executar nesta continuação

Foram recuperados os roteiros existentes e consultados os recursos de execução: Codex Document Control não encontrou sessões conectadas; consultas de processos não retornaram PBIDesktop nem msmdsrv; a pasta padrão AnalysisServicesWorkspaces estava vazia. Power BI Desktop e sua biblioteca AdomdClient existem em Program Files, mas instalação não equivale a um modelo carregado. CLI Databricks/DAX Studio/Tabular Editor não foram encontrados no PATH consultado. Nenhuma sessão autenticada da origem foi disponibilizada.

Assim, **zero consultas SQL e zero consultas DAX contra dados foram executadas nesta continuação**. Não houve tentativa de usar um endpoint inventado, abrir/atualizar automaticamente o projeto original ou extrair credenciais do Desktop. Isso preserva os arquivos de produção. Se o usuário carregar uma cópia isolada, os scripts abaixo poderão ser executados sem nova auditoria estática.

Executados localmente: geração do complemento, conferência dos roteiros por leitura, verificação de delimitadores, referências de colunas usadas e ausência de comandos de mutação, integridade por hashes e validação de links/documentação. Essas verificações não compilam DAX/SQL e não aprovam chaves, filtros ou números financeiros.

## Arquivos e reuso

Pasta do complemento: `docs/evidencias/fase1-dinamica/`.

- [SQL original](evidencias/fase1/roteiro-testes-nao-executados.sql): reutilizar para chaves, nulos, órfãos das 13 relações de negócio, coerência da filial da conta, calendário, grão e controles. Não foi reescrito nem modificado.
- [DAX original](evidencias/fase1/roteiro-testes-nao-executados.dax): preservado como histórico; as consultas específicas abaixo completam os recortes ausentes.
- [SQL complementar](evidencias/fase1-dinamica/complemento-databricks.sql): identificação de filiais/contas, linha 13 por filial/ano, matriz por período, vazios/colisões de chave, mapeamento de DRE, cobertura por cenário e referência da conta escolhida.
- [Registro de testes](evidencias/fase1-dinamica/registro-testes.csv): critérios, estado, obtido, divergência, evidência, executor e datas. Todos os grupos iniciam como NAO_EXECUTADO; campos de resultados ficam vazios.
- [Reuso e hashes dos roteiros](evidencias/fase1-dinamica/reuso.json), [estado de execução](evidencias/fase1-dinamica/estado-execucao.json) e [descoberta de ambiente](evidencias/fase1-dinamica/ambiente.json).

## Preparar a execução sem alterar produção

1. Com Desktop fechado, copiar o PBIP atual e suas pastas Report/SemanticModel para uma pasta de trabalho isolada, preservando caminhos relativos e excluindo .pbi. Não substituir os originais nem copiar credenciais. Usar a configuração/autenticação já existente e não editar host, warehouse ou consultas.
2. Abrir a cópia no Power BI Desktop. Registrar versão do aplicativo, caminho da cópia, horário da última atualização, eventual RLS/papel ativo e mensagens de atualização. Se a cópia não tiver dados, atualizar somente a cópia com a conexão existente; se pedir nova configuração/credencial, parar e registrar a dependência.
3. Usar a Exibição de Consulta DAX, colando **um arquivo por execução**. Executar EVALUATE, não criar medida/tabela calculada e não clicar em ações de atualizar o modelo com mudanças. O pacote não contém DEFINE MEASURE, ALTER ou CREATE.
4. Usar contexto sem RLS para o controle consolidado, se autorizado no ambiente; caso haja restrição, registrar o papel e não comparar total restrito ao controle integral.
5. Executar SQL no editor Databricks SQL com warehouse e acesso já existentes. Cada SELECT/WITH é independente; salvar cada saída com o ID indicado. Não criar tabelas/views temporárias para estes testes.
6. Origem e modelo precisam representar a mesma atualização. Se a origem mudar durante a coleta, reexecutar o par afetado; diferenças de atualização não são defeito de relacionamento demonstrado.
7. Exportar resultados CSV ou copiar as grades integralmente para arquivos de evidência. Em ambientes sem exportação, registrar capturas legíveis e contagens completas, sem tratar linhas truncadas como resultado integral. Salvar erro exato se um teste não compilar.

A execução de consultas na DAX Query View retorna dados sem criar objetos do modelo. [Documentação Microsoft](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view).

## Ordem de execução e critérios

### 1. Descoberta e metadados reais

Executar [01-descoberta.dax](evidencias/fase1-dinamica/01-descoberta.dax), [02-relacionamentos.dax](evidencias/fase1-dinamica/02-relacionamentos.dax) e [03-colunas.dax](evidencias/fase1-dinamica/03-colunas.dax).

- Confirmar os códigos reais correspondentes a São Paulo, Rio de Janeiro e Florianópolis. Os testes de matriz percorrem todas as filiais cadastradas e consolidado, sem inventar códigos ou assumir equivalência por texto. Se os nomes diferirem, registrar o mapa cidade → código; se faltar alguma cidade, o requisito não está atendido.
- Reconciliar os 18 nomes/IDs com o inventário existente: 13 relações de negócio e cinco técnicas; 12 ativas de negócio, uma inativa dim_conta.cod_filial → dim_filial.cod_filial; cinco técnicas ativas.
- Confirmar FromCardinality Many e ToCardinality One, direção OneDirection (To → From), estado de relação válido e tipos compatíveis. Esses são os valores esperados do desenho, **não valores efetivos já medidos**. Toda divergência exige explicação e nova avaliação, sem editar a relação.
- Confirmar ausência de BothDirections/Automatic não documentado, ciclos/caminhos alternativos e relações adicionais não inventariadas. Correlacionar as propriedades reais com os testes comportamentais; uma consulta que não gera erro não certifica ausência de ambiguidade em todo o modelo.
- INFO.VIEW pode exigir versão compatível. Se indisponível, usar [02b-metadados-fallback.dmv](evidencias/fase1-dinamica/02b-metadados-fallback.dmv) em DAX Studio/SSMS já conectado ou registrar as propriedades de cada relação na Model View do Desktop. Não executar DMV na DAX Query View.

[INFO.VIEW.RELATIONSHIPS](https://learn.microsoft.com/en-us/dax/info-view-relationships-function-dax) retorna cardinalidades, direção, estado e endpoints do modelo em execução.

### 2. Chaves e integridade

Executar SQL original e [04-chaves-modelo.dax](evidencias/fase1-dinamica/04-chaves-modelo.dax), [05-integridade-modelo.dax](evidencias/fase1-dinamica/05-integridade-modelo.dax), [14-calendario-modelo.dax](evidencias/fase1-dinamica/14-calendario-modelo.dax) e [16-grao-view.dax](evidencias/fase1-dinamica/16-grao-view.dax).

Aceite objetivo:

- Cada dimensão tem linhas > 0, contagem de chaves distintas igual à contagem física de linhas, zero chaves NULL/BLANK/vazias e zero duplicados. DAX usa ALLNOBLANKROW nas dimensões para não confundir a linha sintética de relacionamento com NULL físico; SQL confirma a origem.
- Zero órfãos e chaves ausentes nas três ligações conta–fato, quatro ligações filial–fatos/view e quatro ligações competência–calendário; conferir também os vínculos de dim_conta/dim_dre a filial.
- Calendário: zero NULL/duplicados, dias distintos = intervalo inclusivo em dias, zero horários diferentes de meia-noite e metadados ano/mês/inicio_mes coerentes. Horário não-zero exige investigar comparações exatas de competência, sem corrigir consultas nesta fase.
- id_conta deve ser globalmente único; colisões entre filiais ou diferenças de filial entre conta e fato precisam de investigação antes do aceite. A chave composta não deve ser implementada aqui.
- View: zero duplicados em (cod_filial, competencia, ordem_dre), posições e chaves não nulas, mapeamento consistente de ordem/descrição/subtotal. Retorno vazio de 16 significa ausência de duplicados somente se a view tiver dados.
- O complemento SQL testa vazios e colisões após UPPER/TRIM como diagnóstico de texto. O comportamento de collation da origem pode diferir do modelo; divergências devem ser explicadas usando os resultados DAX, sem normalizar produção automaticamente.

COUNTROWS pode retornar BLANK para conjunto vazio. **Somente nas contagens técnicas**, documentar BLANK como conjunto vazio/zero; isso não autoriza converter valores financeiros BLANK para zero. Uma tabela sem dados não aprova integridade por vacuidade.

### 3. Propagação de filial e período

Executar os quatro arquivos:

- [06 — lançamentos](evidencias/fase1-dinamica/06-filtros-fato_lancamentos.dax).
- [06 — orçamento](evidencias/fase1-dinamica/06-filtros-fato_orcamento.dax).
- [06 — previsão](evidencias/fase1-dinamica/06-filtros-fato_previsao.dax).
- [06 — view comparativa](evidencias/fase1-dinamica/06-filtros-vw_dre_comparativo.dax).

Cada arquivo testa filial individual e consolidado nos períodos 2021, 2022, janeiro–maio/2023 e junho–dezembro/2023, mais o intervalo 2021–2023. Com três filiais: 20 casos por tabela, 80 casos nos quatro arquivos; se houver mais filiais, a quantidade cresce e deve ser registrada. O caso Integral dessa matriz é limitado a 2021–2023; o controle 07 abaixo é sem qualquer filtro temporal e identifica diferenças fora do contrato.

Aceite em cada caso: LinhasViaDimensoes = LinhasDiretas, Extras = Faltantes = 0. Comparar também as contagens com o SQL na mesma seleção. Os testes usam EXCEPT nos dois sentidos e contagens; não dependem apenas de totais monetários coincidentes. RLS e duplicatas físicas precisam ser tratados nos testes de metadados/integridade anteriores.

S03 SQL fornece contagens das fatos e valores da view **somente da linha 13**. Para comparar contagens da view inteira usadas em 06, agregar S04 pelas mesmas filiais/datas; não comparar contagem de uma posição com a de todas as posições. Nunca somar valores financeiros das 13 linhas.

### 4. Conta analítica e interseções

Executar [10-descobrir-conta.dax](evidencias/fase1-dinamica/10-descobrir-conta.dax). Escolher e registrar uma conta realmente analítica com base na descrição e contrato contábil; detalharn2 não é usado como flag sem homologação. Preferir conta com registros nas três fatos e quantidade menor que o total em cada fato. Se não houver uma conta discriminante comum, documentar o caso e usar uma conta adicional para cada fato; não aprovar os três testes com um conjunto vazio.

Substituir **somente na cópia da consulta** `__ID_CONTA_ANALITICA__` pelo ID real nos arquivos [11-filtro-conta.dax](evidencias/fase1-dinamica/11-filtro-conta.dax), [17-interseção](evidencias/fase1-dinamica/17-intersecao-conta-filial-periodo.dax) e S08 SQL. IDs com aspas devem ser escapados conforme DAX/SQL.

Aceite:

- ParametroValido = TRUE; cada fato tem seleção via Conta igual ao filtro direto por planocontas_id, Extras = Faltantes = 0 e ao menos uma amostra não vazia e discriminante por fato. Confirmar contagens SQL.
- A view permanece com o mesmo conjunto e contagem antes/depois de selecionar Conta. Não deve receber filtro artificial de conta no teste. A falta desse filtro é **limitação esperada**, não defeito a resolver com bidirecionalidade.
- Arquivo 17 testa Conta + Filial + Período nas três fatos; mesmas igualdades e conjuntos são exigidos, incluindo interseções legitimamente vazias. Testes vazios isolados não bastam para comprovar propagação.

### 5. Estrutura DRE e relação inativa

Executar [12-filtro-dre.dax](evidencias/fase1-dinamica/12-filtro-dre.dax): seleciona uma linha existente de ordem 1 por id_dre. Exigir exatamente uma linha selecionada (chave única), posição 1 presente e outras posições existentes. A view deve permanecer com contagens e conjuntos idênticos antes/depois. Não se somam valores de todas as linhas para provar isolamento.

Executar [13-relacao-inativa.dax](evidencias/fase1-dinamica/13-relacao-inativa.dax): a seleção de Filial deve manter a lista completa de Conta quando não houver outro caminho ativo. Comparar à seleção direta de contas da filial para provar que a amostra distingue os cenários. Exigir ainda IsActive = FALSE na relação real; não usar USERELATIONSHIP nem ativar a relação para estes testes.

### 6. Conciliação financeira exclusivamente da linha 13

Executar [07-controle-integral.dax](evidencias/fase1-dinamica/07-controle-integral.dax), [08-filial/período](evidencias/fase1-dinamica/08-linha13-filial-periodo.dax), [09-filial/ano](evidencias/fase1-dinamica/09-linha13-filial-ano.dax), [15-cobertura](evidencias/fase1-dinamica/15-cobertura-cenarios.dax) e os SQL originais/S01/S02/S03/S07.

| Cenário | Total esperado sem filtro de período |
| --- | ---: |
| Realizado | R$ 5.038.227,39 |
| Orçamento | R$ 6.622.493,82 |
| Previsão | R$ 6.157.931,19 |

Aceite: DadosPresentes = TRUE; diferença absoluta de cada cenário após arredondar a centavos ≤ R$ 0,01. Toda diferença não zero deve ser explicada; tolerância não serve para ocultar divergências de regra. NULL/BLANK não é zero aprovado. Exportar os valores obtidos e diferenças, sem preencher o registro com os esperados como se fossem medições.

Por filial/ano, não há valores de controle previamente homologados. Usar a SQL como referência observada; comparar cada célula origem/modelo e registrar ambas. Somar filiais deve reconciliar o consolidado do mesmo cenário/recorte; somar anos deve reconciliar o integral, depois de conferir ausência de registros fora de 2021–2023.

Cobertura esperada por filial, se o contrato informado estiver completo: 29 competências realizadas de janeiro/2021 a maio/2023, 36 de orçamento e 36 de previsão de janeiro/2021 a dezembro/2023. Confirmar sem lacunas. Em junho–dezembro/2023, contagem de realizados preenchidos = 0 e soma financeira de realizado permanece BLANK/NULL. Uma linha com realizado = 0 é presença de dado, não ausência.

Para desempenho em 2023, comparar janeiro–maio com janeiro–maio dos outros cenários; junho–dezembro é projeção sem realizado, não uma comparação de cumprimento. Nenhum valor de EBITDA/EBIT é calculado ou homologado neste pacote.

## Estratégia DRE aprovada para implementação inicial

**Abordagem 1 aprovada pelo usuário — campos ordem_dre e descricao_dre da própria vw_dre_comparativo nos visuais gerenciais.** Para o desenho atual, reduz dependências, evita novas relações e elimina a necessidade de transmitir a linha de uma dimensão sem ligação. É compatível com PBIP/PBIR e tende a ter manutenção mais simples. Não usar dim_dre como filtro da view sem implementação específica. Detalhar contas com dim_conta e as três fatos; preservar os relacionamentos. Nenhuma mudança visual ou medida foi implementada nesta tarefa.

Condições antes de adotar: comprovar grão, consistência ordem/descrição entre filiais, ordenação e regras de subtotal. As medidas futuras precisam respeitar posição e tratar totais; usar campos da view não torna segura uma soma irrestrita das 13 posições. Usar Filial e Calendário comuns como filtros; Conta não afeta essa view e deve ter interação/limitação explicitada.

Abordagem 2 (dimensão com chave gerencial) fica como evolução se houver demanda por dimensão compartilhada entre múltiplos objetos e chave única comprovada. Implica mudança estrutural e revisão de impacto; não é necessária para os testes atuais.

Abordagem 3 (filtro virtual/TREATAS) é alternativa se for obrigatório usar dim_dre como eixo. Deve transportar posição e, quando necessário, pares (cod_filial, ordem_dre) sem quebrar os filtros existentes; exige testes de multi-seleção, totais e desempenho. Nenhuma medida definitiva foi criada. [Microsoft: TREATAS](https://learn.microsoft.com/en-us/dax/treatas-function-dax).

## Evidências, aprovação e Fase 2

Preencher registro-testes.csv com estado EXECUTADO_APROVADO, EXECUTADO_REPROVADO ou NAO_EXECUTADO, saída/erro, divergência, executor e datas. Manter os resultados reais em arquivos próprios; não sobrescrever as evidências históricas da inspeção.

A Fase 1 só pode ser aprovada com chaves/integridade aprovadas, relações efetivas e filtros comprovados, controles da linha 13 conciliados e limitações DRE/Conta aceitas no escopo. Uma falha ou teste obrigatório sem execução mantém o bloqueio.

**Estado final:** Fase 1 concluída com aceite técnico; Fase 2 liberada e não iniciada. Os resultados DAX foram executados/registrados pelo agente nas rodadas anteriores; a execução SQL independente e a coincidência por filial foram confirmadas pelo usuário nesta conversa de aceite, sem reexecução pelo agente ou reconstrução de sua grade de 16 linhas. A estratégia aprovada está registrada para a implementação inicial.

Resultado Líquido ainda depende de homologação contábil; a conciliação da linha 13 não homologa seu conceito contábil. EBITDA/EBIT continuam sem cálculo até homologação. Antes de F2, cumprir os pré-requisitos operacionais e de contrato de medidas do PLANS.md; os novos cálculos exigirão validação incremental própria.
