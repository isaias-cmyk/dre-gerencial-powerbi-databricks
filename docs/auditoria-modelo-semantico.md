# Auditoria do Modelo Semântico — Fase 1

Data: 02/11/2026, America/Sao_Paulo. Responsável: Codex.
**Estado atual: Fase 1 CONCLUÍDA com aceite técnico em 02/11/2026. Fase 2 LIBERADA, ainda NÃO INICIADA.** As 23 consultas DAX/INFO e os 80 casos filial/período registrados são compatíveis com a conciliação SQL independente informada pelo usuário (16 linhas; diferenças de R$ 0,00 nos três cenários e totais por filial coincidentes). A estratégia inicial DRE foi aprovada pelo usuário. Aceite final e proveniência na seção 14; seções de preparação/rodadas anteriores preservam seu estado histórico. Resultado Líquido, EBITDA e EBIT continuam pendentes de homologação contábil.

## 1. Escopo, baseline e método

As seções 1–9 descrevem a inspeção inicial; seções 12–13 registram a preparação e execução local. Afirmações históricas de teste não executado/bloqueio foram superadas pelo aceite técnico da seção 14, sem reescrever os logs de evidência.

AGENTS.md e PLANS.md foram lidos integralmente. A Fase 0 está concluída no plano; foram consultados arquitetura, validações, histórico, resultado, inventários de tabelas/relacionamentos/conexões e evidências de integridade da Fase 0.

O ZIP da Fase 0 mantém SHA-256 `7E550BB10CECEF3093F5EC3EE4EEEBA1F1CF2CC1088E21AD8BC82CA2637B58C2`. Os 36 arquivos de entrada, exceto PLANS.md atualizado após aquele snapshot, coincidem com os hashes da Fase 0. [Comparação registrada](evidencias/fase1/comparacao-fase0.json).

Foram inspecionados PBIP, definition.pbir, definition.pbism, report/page JSON e os TMDL reais: database, model, relationships, tabelas e cultura. Fontes de dados não foram substituídas por BaseDados.xlsx nem por conteúdo do cache.abf.

Nesta fase somente documentação, evidências e roteiros de consulta de auditoria foram criados/atualizados. Nenhuma consulta M, conexão Databricks, credencial, propriedade do modelo, relacionamento, medida ou página foi alterada. Roteiros SQL/DAX são arquivos de teste somente leitura e **não foram executados**; não são implementação de medidas.

Métodos:
- extração textual de declarações e propriedades TMDL, com linhas de referência;
- comparação dos endpoints e tipos das relações, IDs/lineageTags e referências de tabela/variation;
- análise de caminhos num grafo **condicional** de filtros;
- parsing sintático de JSON e comparação SHA-256.

O extrator não é um parser/compilador TMDL oficial. Foi corrigido durante a execução para delimitar cada declaração de coluna por linha; o resultado final foi confrontado com as oito definições reais, totalizando 56 colunas de negócio. As evidências finais correspondem à execução corrigida.

## 2. Inventário de tabelas, tipos e propriedades

Confirmadas quatro dimensões, três fatos e uma view, com 56 colunas importadas. Além delas há seis tabelas técnicas calculadas de data, totalizando 14 tabelas. Modelo em compatibilidade 1606, culture en-US e sourceQueryCulture pt-BR; todas as partições estão em Import.

As oito consultas M navegam diretamente pelo conector DatabricksMultiCloud.Catalogs em workspace.gold, sem etapas explícitas de ajuste de sinal, criação de chave ou substituição de NULL. O inventário estático não comprova as regras SQL internas da origem.

As oito tabelas de negócio:
- não declaram isHidden em suas tabelas/colunas;
- não declaram isKey ou isNullable nas colunas;
- não declaram displayFolder ou sortByColumn;
- apresentam sourceColumn correspondente ao nome importado e lineageTags;
- não contêm medidas explícitas.
Ausência de isKey não prova ausência de unicidade nos dados; ausência de isNullable não comprova ausência de NULL. O fato de um lado ser esperado como “um” não certifica unicidade.


### dim_calendario

Arquivo: [dim_calendario.tmdl](../DRE%20Moderno%20-%20Databricks.SemanticModel/definition/tables/dim_calendario.tmdl). Partição Import/M; tabela e colunas sem isHidden explícito.

| Coluna | Tipo TMDL | Agregação | Formato explícito | Linha |
| --- | --- | --- | --- | ---: |
| data | dateTime | none | Long Date | 4 |
| ano | int64 | sum | 0 | 20 |
| mes | int64 | sum | 0 | 29 |
| dia | int64 | sum | 0 | 38 |
| trimestre | int64 | sum | 0 | 47 |
| ano_mes | string | none | ausente | 56 |
| inicio_mes | dateTime | none | Long Date | 64 |
| numero_ano_mes | int64 | sum | 0 | 80 |

### dim_conta

Arquivo: [dim_conta.tmdl](../DRE%20Moderno%20-%20Databricks.SemanticModel/definition/tables/dim_conta.tmdl). Partição Import/M; tabela e colunas sem isHidden explícito.

| Coluna | Tipo TMDL | Agregação | Formato explícito | Linha |
| --- | --- | --- | --- | ---: |
| id_conta | string | none | ausente | 4 |
| ordem_conta | int64 | sum | 0 | 12 |
| descricaon1 | string | none | ausente | 21 |
| descricaon2 | string | none | ausente | 29 |
| detalharn2 | int64 | sum | 0 | 37 |
| mascaradre_id | string | none | ausente | 46 |
| tipolancamento | int64 | sum | 0 | 54 |
| cod_filial | string | none | ausente | 63 |

### dim_dre

Arquivo: [dim_dre.tmdl](../DRE%20Moderno%20-%20Databricks.SemanticModel/definition/tables/dim_dre.tmdl). Partição Import/M; tabela e colunas sem isHidden explícito.

| Coluna | Tipo TMDL | Agregação | Formato explícito | Linha |
| --- | --- | --- | --- | ---: |
| id_dre | string | none | ausente | 4 |
| ordem_dre | int64 | sum | 0 | 12 |
| descricao_dre | string | none | ausente | 21 |
| subtotal | int64 | sum | 0 | 29 |
| filial | string | none | ausente | 38 |
| cod_filial | string | none | ausente | 46 |

### dim_filial

Arquivo: [dim_filial.tmdl](../DRE%20Moderno%20-%20Databricks.SemanticModel/definition/tables/dim_filial.tmdl). Partição Import/M; tabela e colunas sem isHidden explícito.

| Coluna | Tipo TMDL | Agregação | Formato explícito | Linha |
| --- | --- | --- | --- | ---: |
| cod_filial | string | none | ausente | 4 |
| filial | string | none | ausente | 12 |

### fato_lancamentos

Arquivo: [fato_lancamentos.tmdl](../DRE%20Moderno%20-%20Databricks.SemanticModel/definition/tables/fato_lancamentos.tmdl). Partição Import/M; tabela e colunas sem isHidden explícito.

| Coluna | Tipo TMDL | Agregação | Formato explícito | Linha |
| --- | --- | --- | --- | ---: |
| competencia_data | dateTime | none | Long Date | 4 |
| planocontas_id | string | none | ausente | 15 |
| valor | double | sum | ausente | 23 |
| _arquivo_origem | string | none | ausente | 33 |
| _aba_origem | string | none | ausente | 41 |
| _data_ingestao | dateTime | none | General Date | 49 |
| _tabela_origem | string | none | ausente | 63 |
| cod_filial | string | none | ausente | 71 |

### fato_orcamento

Arquivo: [fato_orcamento.tmdl](../DRE%20Moderno%20-%20Databricks.SemanticModel/definition/tables/fato_orcamento.tmdl). Partição Import/M; tabela e colunas sem isHidden explícito.

| Coluna | Tipo TMDL | Agregação | Formato explícito | Linha |
| --- | --- | --- | --- | ---: |
| competencia_data | dateTime | none | Long Date | 4 |
| planocontas_id | string | none | ausente | 15 |
| valor | double | sum | ausente | 23 |
| _arquivo_origem | string | none | ausente | 33 |
| _aba_origem | string | none | ausente | 41 |
| _data_ingestao | dateTime | none | General Date | 49 |
| cod_filial | string | none | ausente | 63 |

### fato_previsao

Arquivo: [fato_previsao.tmdl](../DRE%20Moderno%20-%20Databricks.SemanticModel/definition/tables/fato_previsao.tmdl). Partição Import/M; tabela e colunas sem isHidden explícito.

| Coluna | Tipo TMDL | Agregação | Formato explícito | Linha |
| --- | --- | --- | --- | ---: |
| competencia_data | dateTime | none | Long Date | 4 |
| planocontas_id | string | none | ausente | 15 |
| valor | double | sum | ausente | 23 |
| _arquivo_origem | string | none | ausente | 33 |
| _aba_origem | string | none | ausente | 41 |
| _data_ingestao | dateTime | none | General Date | 49 |
| cod_filial | string | none | ausente | 63 |

### vw_dre_comparativo

Arquivo: [vw_dre_comparativo.tmdl](../DRE%20Moderno%20-%20Databricks.SemanticModel/definition/tables/vw_dre_comparativo.tmdl). Partição Import/M; tabela e colunas sem isHidden explícito.

| Coluna | Tipo TMDL | Agregação | Formato explícito | Linha |
| --- | --- | --- | --- | ---: |
| cod_filial | string | none | ausente | 4 |
| filial | string | none | ausente | 12 |
| competencia | dateTime | none | Long Date | 20 |
| ano | int64 | sum | 0 | 31 |
| ordem_dre | int64 | sum | 0 | 40 |
| descricao_dre | string | none | ausente | 49 |
| subtotal | int64 | sum | 0 | 57 |
| realizado | double | sum | ausente | 66 |
| orcado | double | sum | ausente | 76 |
| previsto | double | sum | ausente | 86 |


### Chaves candidatas e contratos a comprovar

| Objeto | Chave/grão candidato | Situação e teste necessário |
| --- | --- | --- |
| dim_filial | cod_filial | Endpoint de dimensão; testar NULL, vazio, duplicados e correspondência dos nomes |
| dim_conta | id_conta | Endpoint de dimensão; comprovar unicidade global, inclusive entre filiais |
| dim_dre | id_dre; alternativa (cod_filial, ordem_dre) | Não há relação pelo id_dre; ambas as hipóteses exigem teste; ordem_dre isolada não pode ser presumida única entre filiais |
| dim_calendario | data, um registro por dia | Testar unicidade, NULL, continuidade, anos completos e horário consistente |
| Três fatos | Grão de lançamento/orçamento/previsão ainda não comprovado | Não há ID de transação explícito; repetição de filial/conta/competência pode ser legítima, não eliminar como duplicado automaticamente |
| vw_dre_comparativo | (cod_filial, competencia, ordem_dre) | Grão esperado para DRE; verificar duplicação, 13 posições e coerência de descrição/subtotal |

As relações por conta usam **apenas id_conta**, sem cod_filial. Se esse ID repetir por filial, a cardinalidade esperada não será sustentável; testar também se a filial da conta coincide com a filial da fato. Uma conta “global” com múltiplas filiais precisa de contrato explícito antes de escolher chave composta ou dimensão compartilhada.

### Datas técnicas

Existem uma DateTableTemplate e cinco LocalDateTable, todas com isHidden, sete colunas e hierarquia de data. Os nomes completos constam de [tabelas-colunas.json](evidencias/fase1/tabelas-colunas.json).

Dim_calendario não declara dataCategory de tabela Time, isKey em data ou hierarquia própria. A anotação UnderlyingDateTimeDataType = Date **não comprova** marcação como tabela de datas nem garante horário zero nos valores. Existem variations automáticas de data em data, inicio_mes e _data_ingestao.

A inteligência temporal automática está habilitada no modelo. A referência oficial descreve requisitos de unicidade, continuidade e consistência de horário para marcar uma tabela de datas; a escolha entre inteligência temporal clássica e baseada em calendário deve ser decidida antes de configurar propriedades. [Microsoft: tabelas de datas](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-date-tables).

## 3. Inventário completo dos relacionamentos

**18 relações: 13 de negócio (12 ativas inferidas e uma inativa explícita), mais cinco técnicas de data ativas inferidas.**

“From” e “To” são endpoints serializados; **não são a seta do filtro**. Em todas as 18 relações, fromCardinality, toCardinality e crossFilteringBehavior estão omitidos. Para avaliar o desenho, adota-se como hipótese a cardinalidade *:1 e direção única To → From; **não foram lidos valores efetivos via TOM/DMV nem validada unicidade**. A cardinalidade efetiva e a direção permanecem pendentes em cada linha.

A documentação define OneDirection como propagação de To para From; relações inativas não participam automaticamente dos filtros. Isso embasa a leitura condicional abaixo, não uma afirmação de teste de dados aprovado. [Microsoft: Relationships/TMSL](https://learn.microsoft.com/en-us/analysis-services/tmsl/relationships-object-tmsl).

Arquivo de origem: SemanticModel/definition/relationships.tmdl. Colunas de origem/destino existem e os tipos TMDL coincidem em todas as 18 relações.

| ID | From | To | Estado | Tipos From / To | joinOnDateBehavior explícito | Linha |
| --- | --- | --- | --- | --- | --- | ---: |
| dd5b6732-5fba-479d-b6f3-1936a8f1746b | dim_calendario.data | LocalDateTable_e416fc4a-500e-46eb-9219-3a8485e17504.Date | Ativo inferido | dateTime / dateTime | datePartOnly | 1 |
| 75b003b4-6187-4899-b2ad-e655b31b0fc9 | dim_calendario.inicio_mes | LocalDateTable_34e06e8e-8415-4982-a1d6-5bcb8aaf396d.Date | Ativo inferido | dateTime / dateTime | datePartOnly | 6 |
| 6c4b7869-5380-4800-881d-7b8930dd3d29 | fato_lancamentos._data_ingestao | LocalDateTable_9a63cac9-7363-4efb-a94e-52482a9f2a3b.Date | Ativo inferido | dateTime / dateTime | datePartOnly | 11 |
| f3198452-0cec-4397-9362-2a2c270304a4 | fato_orcamento._data_ingestao | LocalDateTable_48e7e8a8-fb4a-47d3-a465-3cfdcdc24531.Date | Ativo inferido | dateTime / dateTime | datePartOnly | 16 |
| 98d30182-d70a-4d7b-bde5-8ef769824638 | fato_previsao._data_ingestao | LocalDateTable_c5792a6d-2512-4297-9fab-d41d92d805c3.Date | Ativo inferido | dateTime / dateTime | datePartOnly | 21 |
| AutoDetected_b803a55e-b318-4f25-80e8-6068d5cedb12 | dim_conta.cod_filial | dim_filial.cod_filial | Inativo explícito | string / string | omitido | 26 |
| AutoDetected_d9ec7926-13de-4e3a-beaf-9d5600fb340f | dim_dre.cod_filial | dim_filial.cod_filial | Ativo inferido | string / string | omitido | 31 |
| AutoDetected_b9db6563-6b6a-4ed9-9873-033469b2f0ab | fato_lancamentos.cod_filial | dim_filial.cod_filial | Ativo inferido | string / string | omitido | 35 |
| AutoDetected_cf6c4540-68ae-4da2-acca-5a3bf495a442 | fato_orcamento.cod_filial | dim_filial.cod_filial | Ativo inferido | string / string | omitido | 39 |
| AutoDetected_2a7e773f-8348-4485-ac6c-69dd9df5dab8 | fato_previsao.cod_filial | dim_filial.cod_filial | Ativo inferido | string / string | omitido | 43 |
| AutoDetected_2ce0342d-62e0-4df8-a023-363036b47efe | vw_dre_comparativo.cod_filial | dim_filial.cod_filial | Ativo inferido | string / string | omitido | 47 |
| 13c78bc6-b976-df8e-f003-91414e803c01 | fato_lancamentos.competencia_data | dim_calendario.data | Ativo inferido | dateTime / dateTime | omitido | 51 |
| ddacb715-ec23-2d3c-a337-1083a97c680d | fato_orcamento.competencia_data | dim_calendario.data | Ativo inferido | dateTime / dateTime | omitido | 55 |
| 4f0276cf-4e80-7bc6-b833-a091883c1e68 | fato_previsao.competencia_data | dim_calendario.data | Ativo inferido | dateTime / dateTime | omitido | 59 |
| eefc7d39-b405-b354-72e6-c555cb0036a4 | vw_dre_comparativo.competencia | dim_calendario.data | Ativo inferido | dateTime / dateTime | omitido | 63 |
| dd8569c8-c610-4c02-d15c-c2afbea55cd5 | fato_lancamentos.planocontas_id | dim_conta.id_conta | Ativo inferido | string / string | omitido | 67 |
| 66e23276-0813-1463-b459-e591093be04e | fato_orcamento.planocontas_id | dim_conta.id_conta | Ativo inferido | string / string | omitido | 71 |
| 855510f8-a1e3-1f4c-4426-15e7304a95d0 | fato_previsao.planocontas_id | dim_conta.id_conta | Ativo inferido | string / string | omitido | 75 |

As primeiras cinco relações são técnicas. As 13 restantes são de negócio. A relação inativa é AutoDetected_b803a55e-b318-4f25-80e8-6068d5cedb12, entre dim_conta.cod_filial e dim_filial.cod_filial. **Recomenda-se preservá-la inativa enquanto o contrato não for revisto.**

Não foram encontrados pares de endpoints duplicados nem IDs de relacionamento repetidos. Há potencial redundância **de caminhos** se a relação inativa for ativada: Filial → Conta → cada fato passa a coexistir com Filial → cada fato. O grafo simulado encontra dois caminhos para cada uma das três fatos. Isso é risco de ambiguidade futura, não uma ambiguidade ativa já comprovada no mecanismo.

As cinco relações técnicas não são duplicatas exatas das relações de competência: três usam ingestão, não competência; duas adicionam calendários alternativos para o calendário principal. Têm risco de uso indevido e complexidade, mas não devem ser apagadas automaticamente.

## 4. Diagrama lógico textual e auditoria de filtros

Setas representam propagação **esperada sob direção única**, sujeita a conferência no mecanismo:

```text
dim_filial[cod_filial]
  ├──> fato_lancamentos[cod_filial]
  ├──> fato_orcamento[cod_filial]
  ├──> fato_previsao[cod_filial]
  ├──> vw_dre_comparativo[cod_filial]
  └──> dim_dre[cod_filial]

dim_calendario[data]
  ├──> fato_lancamentos[competencia_data]
  ├──> fato_orcamento[competencia_data]
  ├──> fato_previsao[competencia_data]
  └──> vw_dre_comparativo[competencia]

dim_conta[id_conta]
  ├──> fato_lancamentos[planocontas_id]
  ├──> fato_orcamento[planocontas_id]
  └──> fato_previsao[planocontas_id]

dim_filial[cod_filial] -X-> dim_conta[cod_filial] (inativa)
dim_dre: sem saída ativa prevista para as fatos ou a view
dim_conta: sem caminho ativo previsto para a view

LocalDateTable_e416... [Date] --> dim_calendario[data] --> fatos e view
LocalDateTable_34e0... [Date] --> dim_calendario[inicio_mes] --> fatos e view
LocalDateTable_9a63... [Date] --> fato_lancamentos[_data_ingestao]
LocalDateTable_48e7... [Date] --> fato_orcamento[_data_ingestao]
LocalDateTable_c579... [Date] --> fato_previsao[_data_ingestao]
DateTableTemplate: sem relação serializada
```

### Ano e mês

dim_calendario.ano/mes/ano_mes filtram as linhas de data da própria dimensão; o caminho esperado alcança as três fatos e a view por competência. Não há ligação por ano ou mes isoladamente e ela não deve ser criada para corrigir problemas de dados.

Usar mes sem ano agrupa o mesmo mês de vários anos. Usar vw_dre_comparativo.ano filtra a view e, na hipótese unidirecional, não retorna ao calendário nem alcança as três fatos. Por isso, filtros globais devem vir do calendário comum.

As relações de competência omitem datePartOnly; a anotação de data e formato Long Date não remove horas dos valores. Horários ou datas mensais inconsistentes podem gerar órfãos silenciosos. Testar igualdade exata, início de competência mensal e cobertura do calendário, sem alterar consultas para “corrigir” antes do diagnóstico.

### Filial

O caminho esperado de dim_filial alcança fatos, view e dim_dre diretamente. Como a relação com dim_conta é inativa, a lista de contas pode não se reduzir pela filial selecionada. Uma lista não reduzida não significa que o filtro combinado falhou: nas fatos, filial e conta devem se intersectar.

Filial textual em dim_dre ou na view não substitui dim_filial como filtro global. Sob direção única, selecionar esses campos não retorna filtro à dimensão Filial. Confirmar os códigos/nomes reais nos dados antes de padronizar São Paulo, Rio de Janeiro e Florianópolis.

### Conta

**Confirmado por inspeção:** há três relações de dim_conta.id_conta para planocontas_id das três fatos, com endpoints e tipos string compatíveis. **Comportamento esperado:** Conta filtra as três fatos. **Ainda não comprovado:** contagens/valores resultantes no mecanismo.

**A view não possui planocontas_id, id_conta ou relacionamento com dim_conta. Não existe caminho ativo previsto de Conta até vw_dre_comparativo.** Não apresentar indicadores da view como detalhados por conta nem tentar resolver com filtros bidirecionais. A interseção Conta + Filial nas fatos deve ser testada com SQL e DAX no mesmo recorte.

### Posição da DRE

dim_filial filtra dim_dre, mas dim_dre não filtra automaticamente a view na direção esperada. Usar descricao_dre de dim_dre como linha de matriz, somando a view sem aplicar posição, pode repetir o mesmo total em todas as linhas.

**As medidas futuras devem selecionar a posição correta da DRE**, usando ordem_dre e contexto de filial compatíveis, e definir o comportamento de totais. Alternativas para avaliação:
1. Usar campos de linha da própria view, ordenados após validar unicidade de descrição/ordem.
2. Manter dim_dre e aplicar contexto de linha explicitamente em medidas futuras.
3. Propor relação por chave de DRE compatível, apenas se unicidade e cobertura forem comprovadas; a view atual não possui id_dre.
Nenhuma alternativa foi implementada ou homologada; evitar relação muitos-para-muitos por ordem_dre repetida entre filiais.

### Ambiguidade e integridade

O grafo condicional atual não apresenta múltiplos caminhos ativos entre um mesmo par de tabelas. Esse resultado não certifica ausência de ambiguidade no mecanismo, nem valida direção efetiva, RLS ou comportamento de DAX.

Chaves ausentes/duplicadas, órfãos e divergência de filial entre conta/fato não são detectáveis pelas declarações. Não declarar integridade referencial aprovada. Os roteiros preparados verificam cada uma dessas condições.

## 5. Auditoria financeira

Fatos disponibilizam valor double; a view disponibiliza realizado, orcado e previsto double com summarizeBy sum. Não há medida financeira explícita nem filtro permanente de ordem_dre no modelo. A página atual não tem visual.json; não foi executada uma visualização de controle.

O contrato do projeto define os valores da view como ajustados. As consultas M apenas importam a view, sem reaplicar tipolancamento; isso não comprova que a regra SQL da origem foi executada corretamente nem esclarece se valor bruto das fatos já foi ajustado. **Não reaplicar natureza aos valores ajustados e não usar fatos brutas como equivalentes reconciliados da view.**

Os valores da view são aditivos apenas nos eixos compatíveis com a linha selecionada. Somar as 13 posições mistura linhas analíticas e subtotais, duplicando componentes. Também não se deve somar o mesmo indicador calculado nas fatos ao seu subtotal já presente na view.

| Controle integral da linha 13 | Valor informado | Resultado desta auditoria |
| --- | ---: | --- |
| Realizado | R$ 5.038.227,39 | Não revalidado por consulta |
| Orçamento | R$ 6.622.493,82 | Não revalidado por consulta |
| Previsão | R$ 6.157.931,19 | Não revalidado por consulta |

Os roteiros delimitam ordem_dre = 13 para o teste de conciliação. Isso não substitui a homologação das demais posições. Comparar fontes e modelo carregado com mesma atualização, filtro de filial e período; registrar esperado, obtido e diferença após arredondamento a centavos.

Realizado janeiro/2021–maio/2023; Orçamento/Previsão janeiro/2021–dezembro/2023 são coberturas informadas, ainda sem consulta nesta fase. Os controles integrais têm períodos diferentes; comparação de desempenho deve usar competências equivalentes. NULL/BLANK após maio não vira zero por conveniência.

O modelo declara returnErrorValuesAsNull. Investigar erros de origem/atualização antes de interpretar todo NULL como ausência legítima. Trata-se de risco, não evidência de erro ocorrido.

**EBITDA e EBIT continuam pendentes de homologação contábil, sem cálculo ou aproximação.** A favorabilidade de gastos deve considerar natureza/magnitude, sem inferir “favorável” de um desvio numericamente positivo.

## 6. Problemas, riscos e correções recomendadas

| ID / gravidade | Constatação ou hipótese | Impacto | Ação proposta, sem implementação |
| --- | --- | --- | --- |
| A01 Alta | Sem caminho ativo previsto Conta → view | Filtro de conta pode deixar indicadores DRE invariáveis | Informar limitação e restringir interação; detalhe exige fonte ajustada reconciliada por conta, com contrato aprovado |
| A02 Alta | Dim_dre sem caminho de linha para view/fatos | Total repetido por posição; seleção de DRE não propagada | Decidir abordagem das três alternativas acima, testar cada posição/filial e totais antes da F2 |
| A03 Alta | Unicidade de id_conta/cod_filial/data e grão DRE não testados | Cardinalidade inadequada, órfãos ou junções duplicadoras | Executar roteiro de chaves, NULL e integridade; se id_conta não for global, propor chave composta ou contrato global com impacto documentado |
| A04 Alta | Relação Filial–Conta inativa; ativação simulada cria caminhos alternativos | Ambiguidade e filtros imprevistos | Manter inativa; não ativar para reduzir lista de contas sem desenho e teste |
| A05 Alta | Valores da view com sum e 13 linhas não aditivas | Dupla contagem de subtotais | Medidas futuras devem aplicar posição e comportamento de total; nenhuma medida criada nesta fase |
| A06 Alta | Cardinalidade/direção efetivas e propagação sem consulta | Grafo esperado pode diferir da execução | Ler TOM/DMV ou propriedades Desktop e executar recortes comparados com SQL |
| A07 Média | Calendário sem marcação explícita; cinco calendários locais | Inteligência temporal inconsistente, filtro de ingestão confundido com competência | Validar calendário e estratégia temporal; só então propor marcação/hierarquia e migração de referências |
| A08 Média | Colunas de ano/mês/ordem/flags com sum | Agregações sem sentido e ordenação imprópria | Propor Não resumir e sortByColumn após comprovar relação rótulo/ordem |
| A09 Média | Campos técnicos visíveis e números double sem formato monetário explícito | Uso incorreto de metadados, ruído no painel e diferenças de apresentação | Ocultar metadados/FKs após revisar dependências; avaliar formato BRL e precisão sem conversão automática |
| A10 Alta | Contrato SQL de ajustes/sinais e cobertura não consultado | DAX pode reaplicar natureza ou converter ausência em zero | Validar regras da view, períodos e ausência; preservar conexões e consultas existentes |
| A11 Média | returnErrorValuesAsNull declarado | NULL pode exigir análise de erro de atualização | Conferir logs/erros de origem; distinguir erro de ausência legítima |
| A12 Alta | EBITDA/EBIT não homologados | Indicador contábil incorreto | Manter sem cálculo até decisão contábil; não bloqueia inventário, bloqueia esses indicadores |

Não há defeito de referência de coluna ou incompatibilidade de tipo serializado nos relacionamentos encontrados. A03/A06 são **pendências de validação**, não declarações de duplicação ou dados corrompidos já observados.

## 7. Organização proposta, sem alterações

- Manter nomes físicos, IDs e lineageTags; preferir rótulos de exibição documentados antes de renomear qualquer coluna/tabela.
- Propor ocultação de _arquivo_origem, _aba_origem, _data_ingestao e _tabela_origem; revisar FKs, cod_filial duplicado e colunas auxiliares antes de ocultar.
- Propor Não resumir para ano, mes, dia, trimestre, numero_ano_mes, ordem_conta, detalharn2, tipolancamento, ordem_dre e subtotal.
- Propor ordenação ano_mes por numero_ano_mes e descrição DRE por ordem_dre apenas depois de testar que cada rótulo possui uma ordem válida; mes numérico já ordena numericamente.
- Propor hierarquia Ano → Mês em dim_calendario, após decidir estratégia temporal e preservar referências automáticas.
- Reservar pastas de medidas futuras: Resultados, Comparações, Margens, Temporal, Participação e Controle. Escolher tabela hospedeira na F2, sem criar tabela de medidas agora.
- Usar dimensões comuns para filtros globais; documentar quando métricas de view não respondem a conta.
- Preservar tabelas técnicas existentes até avaliar todas as variations e referências; não remover automaticamente.

Toda implementação organizacional fica fora desta execução e requer aprovação do responsável, conforme solicitado pelo usuário.

## 8. Evidências e testes executados

| Teste | Resultado final | Evidência |
| --- | --- | --- |
| Fase 0 concluída e fontes comparadas | 36/36 hashes iguais, excluindo plano já atualizado | comparacao-fase0.json |
| Inventário de declarações | 14 tabelas, oito de negócio, 56 colunas de negócio, zero medidas | tabelas-colunas.json |
| Referências model → tabelas | Nenhuma referência ausente, nenhuma tabela sem ref | resultado.json |
| Endpoints de relacionamento | 36/36 endpoints existentes; tipos coincidem nos 18 pares | relacionamentos.json |
| IDs e lineageTags | Sem IDs de relações ou lineageTags repetidos detectados | resultado.json e script |
| Relações redundantes exatas | Nenhum par From/To repetido | resultado.json |
| Variations | Cinco referências a relacionamentos existentes | referencias-variations.json |
| Grafo condicional | Sem múltiplos caminhos atuais; ativação da inativa gera dois caminhos por fato | caminhos-condicionais.json e resultado.json |
| JSON | 11 arquivos de projeto analisados sintaticamente sem erro | json-sintaxe.json |
| Integridade ao terminar | Comparação final das fontes com baseline, incluindo conexões M | integridade-final.json |

Diretório de evidências: [fase1](evidencias/fase1/resultado.json). Script: [fase1-auditar.py](evidencias/fase1-auditar.py). O script não altera arquivos de projeto; grava somente evidências. [Baseline](evidencias/fase1/baseline-entrada.json).

As evidências históricas da Fase 0 foram preservadas. Resultado de descoberta de recursos: [ambiente.json](evidencias/fase1/ambiente.json). Não foram encontradas sessões Codex Document Control conectadas; PBIDesktop/msmdsrv não retornaram processos; CLI Databricks, DAX Studio e Tabular Editor não foram encontrados no PATH consultado. Isso não prova inexistência de outras instalações, mas não disponibilizou uma sessão autenticada para testes.

Nenhuma credencial foi lida para estabelecer nova conexão, nenhuma configuração foi modificada, e o projeto não foi aberto automaticamente para atualização.

## 9. Testes pendentes e ações para desbloquear

Os roteiros estão preparados com nomes reais, sem resultados inventados:
- [SQL somente leitura — não executado](evidencias/fase1/roteiro-testes-nao-executados.sql): unicidade/NULL, duplicados entre filiais, 13 posições, órfãos de todas as relações de negócio, coerência da filial da conta, calendário, grão da view, disponibilidade e controles da linha 13.
- [DAX/DMV somente leitura — não executado](evidencias/fase1/roteiro-testes-nao-executados.dax): controles da linha 13, contagens por calendário/filial/conta e leitura de metadados. Não cria medidas.

Para desbloquear:
1. Disponibilizar sessão de leitura do modelo carregado no Desktop e acesso autenticado à origem existente, ou executar os roteiros e fornecer as saídas. Registrar data de atualização/cenário e códigos reais de filial/conta.
2. Ler cardinalidade, direção e estado efetivos das 18 relações por TOM/DMV ou propriedades Desktop; correlacionar IDs.
3. Executar consultas de unicidade/NULL e órfãos, incluindo conta por filial e datas com horário; investigar qualquer resultado incompatível sem corrigir automaticamente.
4. Testar calendário: seleção de um ano, mês com ano, mês sem ano, meses não contíguos, intervalo e ausência após maio/2023. Comparar cada fato e view à SQL com exatamente os mesmos filtros.
5. Testar filial única, múltiplas e nenhuma seleção; conta única/múltiplas, Conta + Filial e Conta + Calendário. Usar contas com dados conhecidos; vazio ou valores coincidentemente iguais não comprovam propagação. Confirmar que a view permanece sem contrato de detalhe por conta.
6. Aprovar a abordagem de posição DRE e o contrato de detalhe ajustado por conta; não introduzir medidas ou mudar relações nesta auditoria sem nova decisão de escopo.
7. Comparar controles da linha 13 no modelo e na origem, por filial e consolidado, preservando o período integral de cada cenário. Não somar 13 linhas e não habilitar EBITDA/EBIT.
8. Registrar evidências e reavaliar os critérios de aceite antes de liberar a Fase 2.

## 10. Checklist de aceite técnico da Fase 1 — estado final

- [x] AGENTS.md e PLANS.md lidos; Fase 0 confirmada e evidências consultadas.
- [x] Oito tabelas de negócio e seis técnicas inventariadas; colunas e tipos serializados registrados.
- [x] Inventário completo dos 18 relacionamentos, IDs, endpoints e estados serializados.
- [x] Compatibilidade de tipos dos endpoints e referências estáticas verificadas.
- [x] Diagrama textual e caminhos esperados de ano, mês, filial e conta documentados.
- [x] Limitação da view agregada e risco de dimensão DRE sem propagação identificados.
- [x] Propostas de organização e correção documentadas, sem implementação.
- [x] Riscos de subtotal, sinal, NULL, período e EBITDA/EBIT registrados.
- [x] Cardinalidade e direção efetivas lidas do mecanismo nas consultas registradas.
- [x] Unicidade de chaves, NULL e integridade dos dados importados testados.
- [x] Calendário, horários, granularidade mensal e cobertura temporal comprovados no modelo.
- [x] Propagação de filtros executada no modelo e conciliação independente SQL × DAX informada pelo usuário, sem divergência declarada nos controles e totais por filial.
- [x] Ausência de caminhos ativos ambíguos no grafo efetivo e nos recortes dinâmicos testados.
- [x] Abordagem DRE 1 e limite do detalhamento por conta aprovados explicitamente pelo usuário.
- [x] Controles da linha 13 revalidados por DAX e compatíveis com o resultado SQL informado, com diferenças de R$ 0,00 nos três cenários.
- [x] Resultado Líquido, EBITDA e EBIT identificados como pendentes de homologação contábil; aceite limitado ao escopo técnico.

**Conclusão final: Fase 1 concluída com aceite técnico.** A confirmação SQL e o aceite do usuário encerram os bloqueios históricos; ver seção 14. Fase 2 liberada para execução, não iniciada. Não se declara homologação contábil de indicadores nem aprovação de medidas/páginas ainda não implementadas.

## 11. Referências oficiais consultadas

Consultadas em 02/11/2026 para interpretar propriedades e requisitos, sem alterar o modelo:
- [Microsoft: relacionamentos no Power BI](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-relationships-understand).
- [Microsoft: Relationships object / TMSL](https://learn.microsoft.com/en-us/analysis-services/tmsl/relationships-object-tmsl).
- [Microsoft: SingleColumnRelationship / TOM](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.singlecolumnrelationship).
- [Microsoft: tabelas de datas](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-date-tables).

## 12. Continuação para conclusão da Fase 1 — 02/11/2026

Esta continuação reutilizou os roteiros anteriores; não executou novamente a auditoria estática. Foi criado o [guia de execução dos testes](execucao-testes-fase1.md), com ordem de execução, resultados esperados, critérios de aceite e instruções para o Power BI Desktop e Databricks SQL.

### Recursos efetivamente disponíveis

Nova consulta ao Codex Document Control não encontrou sessão conectada. A consulta de processos retornou zero PBIDesktop/msmdsrv, e a pasta padrão AnalysisServicesWorkspaces estava vazia. Foi confirmada instalação do Power BI Desktop e AdomdClient, mas não existe modelo carregado/sessão autenticada acessível nesta descoberta. Não foram alteradas credenciais, conexões ou configurações para criar uma sessão. [Evidência de ambiente](evidencias/fase1-dinamica/ambiente.json).

**Consultas de dados executadas nesta continuação: SQL = 0; DAX = 0.** Portanto, continuam sem medição: unicidade/NULL, órfãos, relações efetivas, filtros e valores da linha 13. Não há contagens de divergências de dados obtidas; o registro mantém esses campos vazios em vez de inventar zeros.

### Artefatos preparados e testes locais executados

- Roteiros SQL/DAX originais preservados por hash e reutilizados: [reuso.json](evidencias/fase1-dinamica/reuso.json).
- Vinte arquivos DAX independentes, incluindo descoberta de filiais, metadados reais, chaves/integridade no modelo importado, calendário/grão da view, conta analítica, relação inativa, isolamento de dim_dre e conciliação da linha 13. Índice e links no guia.
- Quatro arquivos de matriz filial/período com seleção pelas dimensões versus seleção direta e comparação de conjuntos nos dois sentidos. Com três filiais, cobrem 80 casos incluindo consolidado e intervalo integral; os quatro recortes exigidos estão incluídos. Um arquivo adicional testa Conta + Filial + Período nas três fatos.
- SQL original reutilizado para integridade, complementado por [complemento-databricks.sql](evidencias/fase1-dinamica/complemento-databricks.sql), com referências da linha 13 por filial/ano e período, cobertura, vazios e seleção da conta.
- Fallback DMV para leitura de metadados em sessão tabular e instrução de conferência no Desktop caso INFO.VIEW não esteja disponível.
- [Registro de testes](evidencias/fase1-dinamica/registro-testes.csv) com 13 grupos, critérios objetivos, estado NAO_EXECUTADO e campos de resultados/evidências ainda vazios.
- Executadas geração dos artefatos, conferências locais de delimitadores e integridade dos arquivos. [Verificação local](evidencias/fase1-dinamica/verificacao-local.json). Essas verificações não equivalem a compilação DAX/SQL ou teste de dados; uma correção de parênteses foi aplicada ao complemento antes da verificação final.

### Recomendação DRE definida nesta continuação

Recomenda-se **abordagem 1: ordem_dre e descricao_dre da própria view** como eixo dos visuais gerenciais. É a solução mais simples para o modelo atual, sem nova relação física nem filtro virtual por linha, com menor manutenção e compatibilidade com PBIP/PBIR. A adoção exige comprovar consistência do grão/descrições e tratar o total das medidas futuras por posição; não torna a soma de 13 posições válida.

Dimensão com chave gerencial apropriada fica como evolução para compartilhamento entre objetos. TREATAS fica como alternativa caso o uso de dim_dre seja obrigatório; deve preservar o par filial/posição e seleções existentes quando necessário. Nenhuma dessas mudanças foi implementada. A recomendação ainda depende do aceite do responsável e dos testes de dados.

Conta continua sem detalhe sustentado na view agregada. O pacote verifica o isolamento em vez de tentar ativar caminhos indiretos. Os visuais futuros de DRE deverão declarar esse limite; análises por conta dependem das fatos e de regra ajustada conciliada, fora da implementação desta fase.

### Status de aceite e próximas ações concretas

- [x] Testes recuperados e complementados sem nova auditoria estática.
- [x] Guia com instruções, esperados, critérios e registro de evidências produzido.
- [x] Abordagem DRE recomendada e alternativas justificadas, sem implementação.
- [ ] Executar SQL de integridade e exportar resultados na origem existente.
- [ ] Executar DAX/DMV no modelo carregado e exportar propriedades efetivas/contagens.
- [ ] Comprovar os filtros de São Paulo, Rio de Janeiro, Florianópolis e consolidado nos quatro períodos, além de Conta e dim_dre.
- [ ] Conciliar exclusivamente a linha 13, integral e por filial/ano/período. Totais R$ 5.038.227,39 / R$ 6.622.493,82 / R$ 6.157.931,19 permanecem esperados, não revalidados.
- [ ] Registrar divergências reais, resolver bloqueios e obter aceite da estratégia e limites.

Não foram encontrados novos problemas de dados por teste dinâmico, pois tais testes não foram executados. Riscos anteriores de propagação DRE/Conta e subtotal permanecem; EBITDA/EBIT seguem pendentes. **Fase 1 não aprovada; projeto não liberado para Fase 2.** A ação seguinte é executar o pacote existente no Desktop/origem e preencher o registro, sem solicitar nova auditoria estática.

## 13. Execução real após abertura no Power BI — 02/11/2026

O usuário abriu o projeto no Power BI Desktop e autorizou nova tentativa dos testes. Foi encontrada a porta local 57446 e catálogo a46c4f87-54c4-4283-8269-dcf609511152; antes da execução, uma consulta de metadados conferiu as oito tabelas esperadas. A conexão ADOMD local exigiu execução fora do isolamento da ferramenta; foi usada exclusivamente para leitura. Não houve abertura automática, atualização, alteração de credenciais ou modificação do modelo.

### Evidências e escopo efetivo

Foram executadas **23 consultas DAX/INFO, sem erro**: as vinte do pacote anterior, mais contrato DRE, metadados das partições e mês/seleção múltipla. As duas consultas parametrizadas foram executadas com conta existente 01.02.04, ICMS. Não houve consulta SQL independente ao Databricks.

- [Execução principal: 18 consultas](evidencias/fase1-execucao-20261102-154642/execucao.json).
- [Conta e interseções: duas consultas](evidencias/fase1-execucao-20261102-154704/execucao.json).
- [Contrato DRE e partições: duas consultas](evidencias/fase1-execucao-20261102-154749/execucao.json).
- [Ano/mês e múltiplas filiais: uma consulta](evidencias/fase1-execucao-20261102-154841/execucao.json).
- [Consolidação avaliada automaticamente](evidencias/fase1-execucao-20261102-154642/consolidacao.json), [registro medido](evidencias/fase1-execucao-20261102-154642/registro-testes-executados.csv), [script de execução](evidencias/fase1-executar-local.ps1) e [avaliador](evidencias/fase1-consolidar-execucao.py).

Cada execução contém consulta identificada por nome/hash, instante, catálogo, saída JSON e CSV quando há linhas, além da comparação de hashes dos arquivos de entrada. Os quatro registros de integridade não apresentam arquivo alterado pelo executor. Uma resposta JSON vazia do teste de duplicados é resultado executado, não teste omitido.

Os dados testados são os **dados importados carregados**, não uma nova leitura da origem. As oito partições retornam State = 1 e ErrorMessage ausente; RefreshedTime bruto entre 2026-11-02T17:15:59.553333 e 2026-11-02T17:16:01.69. O rowset não fornece fuso nesses valores; foram preservados sem conversão e não são horários desta auditoria. Nenhum refresh foi disparado.

### Integridade e relacionamentos: resultados obtidos

| Dimensão | Linhas | Chaves distintas | Chaves ausentes detectadas |
| --- | ---: | ---: | ---: |
| dim_filial | 3 | 3 | 0 |
| dim_conta | 129 | 129 | 0 |
| dim_dre | 39 | 39 | 0 |
| dim_calendario | 1.095 | 1.095 | 0 |

Os 13 testes de integridade de negócio retornaram conjuntos vazios para chaves ausentes e órfãos, incluindo três ligações de conta às fatos, quatro de filial às fatos/view, quatro de competência ao calendário e duas ligações de dimensões à filial. A interpretação de BLANK em COUNTROWS vazio como zero foi aplicada **somente às contagens técnicas**; as saídas originais preservam null. Valores financeiros não foram preenchidos com zero.

Metadados efetivos: **18 relações, todas Many → One e OneDirection, estado Ready**. Doze relações de negócio ativas, Filial–Conta inativa e cinco técnicas ativas. Tipos dos endpoints foram conferidos nos metadados carregados; Date e DateTime são tratados como temporais tabulares, preservando os rótulos originais no resultado. As 112 colunas retornadas incluem 14 RowNumber internos do mecanismo, além das 98 colunas serializadas; isso não corresponde a novas tabelas/colunas de negócio criadas pelo agente.

O grafo construído a partir dos estados e direções reais não apresenta múltiplos caminhos ativos. Os testes de propagação não apontaram ambiguidade nos recortes executados. Isso não constitui homologação de RLS não testada nem de futuras alterações de relações.

Calendário contínuo de 01/01/2021 a 31/12/2023, com 1.095 dias; zero horários divergentes ou metadados ano/mês/inicio_mes incoerentes detectados. A marcação de calendário para inteligência temporal futura continua como recomendação organizacional, sem alteração nesta fase.

### Filtros e contrato gerencial: resultados obtidos

- Filiais reais: 01 São Paulo, 02 Rio de Janeiro, 03 Florianópolis.
- **80 casos filial/período aprovados** nas três fatos e view: contagem via dimensões igual à seleção direta e diferenças de conjuntos vazias nos dois sentidos. Incluem consolidado, 2021, 2022, janeiro–maio/2023, junho–dezembro/2023 e intervalo integral do contrato.
- Mais quatro casos de ano 2021, meses janeiro/março e seleção simultânea São Paulo/Florianópolis aprovados, comprovando filtro explícito por ano/mês e múltiplas filiais.
- Conta ICMS 01.02.04: selecionou 29 de 3.741 linhas de lançamentos, 36 de 4.644 linhas de orçamento e 36 de 4.644 linhas de previsão. Mesmos conjuntos da seleção direta. A view manteve **1.404 linhas**, comprovando sua ausência de filtro automático por conta.
- Conta + Filial + Período: **36 comparações de fatos aprovadas**, sendo 12 cenários em três fatos. Para essa conta de São Paulo, seleções de Rio/Florianópolis retornaram interseção vazia corretamente; não foram confundidas com aprovação de uma amostra global vazia.
- Dim_dre: selecionar um id de posição 1 manteve as 1.404 linhas da view; filtrar posição 1 diretamente na view alcança 108 linhas. A ausência de propagação automática está agora comprovada dinamicamente.
- Filial–Conta inativa: cada filial manteve 129 contas via dimensão Filial, enquanto o filtro direto de cod_filial retorna 43. Estado inativo e comportamento confirmados, sem ativar a relação.
- View sem duplicados no grão filial/competência/posição; cada grupo tem 13 posições; descrição e flag estáveis por ordem; nenhum par filial/ordem sem dimensão. Zero divergências de filial entre conta e fatos nos dez testes de contrato.

Esses resultados sustentam tecnicamente a **recomendação da abordagem 1**, campos ordem_dre/descricao_dre da própria view, com filtros comuns de Filial/Calendário e limite de Conta explícito. Não foi implementada nem tratada como aceite do responsável.

### Linha 13: conciliação no Power BI executada

| Cenário | Obtido no modelo, arredondado | Esperado | Diferença a centavos |
| --- | ---: | ---: | ---: |
| Realizado | R$ 5.038.227,39 | R$ 5.038.227,39 | R$ 0,00 |
| Orçamento | R$ 6.622.493,82 | R$ 6.622.493,82 | R$ 0,00 |
| Previsão | R$ 6.157.931,19 | R$ 6.157.931,19 | R$ 0,00 |

Os valores brutos double são preservados na evidência, com diferenças residuais de ponto flutuante abaixo do centavo. **Os controles foram revalidados no modelo carregado**, exclusivamente por ordem_dre = 13. Não houve soma financeira das 13 posições.

| Filial | Ano | Realizado | Orçamento | Previsão |
| --- | ---: | ---: | ---: | ---: |
| São Paulo | 2021 | 925.383,76 | 902.718,45 | 916.069,98 |
| São Paulo | 2022 | 943.357,75 | 935.094,60 | 877.195,90 |
| São Paulo | 2023 | 254.694,46 | 836.283,06 | 827.562,65 |
| Rio de Janeiro | 2021 | 639.921,00 | 687.763,50 | 619.321,73 |
| Rio de Janeiro | 2022 | 614.411,55 | 701.356,21 | 629.528,62 |
| Rio de Janeiro | 2023 | 352.637,77 | 753.250,10 | 675.855,67 |
| Florianópolis | 2021 | 552.761,33 | 633.711,51 | 540.873,63 |
| Florianópolis | 2022 | 542.434,76 | 575.271,64 | 537.797,30 |
| Florianópolis | 2023 | 212.625,01 | 597.044,75 | 533.725,71 |

Valores em reais. Somas por filial/ano e por período reconciliam os consolidados carregados. **2023 realizado é janeiro–maio, enquanto orçamento/previsão acima são anuais completos**; esta tabela é inventário de conciliação, não comparação equivalente de desempenho. Os recortes equivalentes de janeiro–maio estão registrados na saída 08-linha13-filial-periodo.

Cada filial possui 29 competências de realizado e 36 de orçamento/previsão. Em junho–dezembro/2023, realizado é BLANK e a contagem de valores realizados preenchidos é vazia, sem zero fabricado. EBITDA/EBIT continuam sem homologação.

### Checklist e pendências ao final da rodada local — histórico

Os dois itens então pendentes foram encerrados pelo aceite final da seção 14.

- [x] Testar chaves, NULL e integridade nas tabelas importadas carregadas.
- [x] Ler cardinalidade, direção, estados e tipos efetivos no mecanismo.
- [x] Testar filial, período, ano/mês, seleção múltipla e conta nas três fatos.
- [x] Confirmar ausência de filtro automático Conta/DRE na view e comportamento da relação inativa.
- [x] Testar grão/mapeamento DRE e coerência de filial da conta.
- [x] Revalidar controles da linha 13 no Power BI, com recortes filial/ano e BLANK pós-maio.
- [x] Documentar abordagem 1 como recomendação compatível com os resultados.
- [ ] Comparar independentemente com consultas Databricks SQL da mesma atualização. Esta execução não autentica nem altera a conexão da origem; os roteiros estão prontos, mas não executados contra ela.
- [ ] Registrar aceite do responsável da abordagem 1 e da limitação de conta para a view. Recomendar não equivale a aprovar em nome do responsável.

**Conclusão da rodada local (histórica):** testes locais aprovados; naquele momento ainda faltavam SQL independente e aceite da estratégia. Ambos foram posteriormente confirmados pelo usuário e registrados na seção 14. Nenhuma correção de produção foi necessária ou aplicada.

## 14. Aceite técnico final da Fase 1 e liberação da Fase 2

Em 02/11/2026, o usuário informou expressamente a execução da conciliação independente Databricks SQL × DAX Power BI, com consulta SQL de 16 linhas, diferenças consolidadas de R$ 0,00 e totais por filial coincidentes. Na mesma instrução, aprovou a estratégia DRE inicial e solicitou o encerramento técnico da Fase 1.

### Compatibilidade e proveniência das evidências

- Evidência executada anteriormente pelo agente: 23 consultas DAX/INFO, sem falhas, 80 casos filial/período aprovados, chaves e integridade verificadas e relações efetivas confirmadas. A [consolidação original](evidencias/fase1-execucao-20261102-154642/consolidacao.json) foi relida e seus indicadores/totais comparados à declaração do usuário, com compatibilidade confirmada.
- Evidência SQL e coincidência por filial: **fornecidas pelo usuário nesta conversa de aceite**. Não houve reexecução SQL pelo agente nesta tarefa; a mensagem contém o resumo da consulta de 16 linhas, sem a grade bruta anexa. O registro não inventa/reconstrói essas 16 linhas nem atribui sua execução ao agente.
- Aceite e decisão de arquitetura: instrução explícita do usuário nesta conversa. A declaração foi incorporada como evidência de execução externa e aceite, encerrando as duas dependências restantes.
- [Registro de aceite técnico](evidencias/fase1-aceite-tecnico/aceite.json), com proveniência, dados declarados, referência/hash da consolidação DAX e pendências contábeis. Logs anteriores que mostram zero consultas SQL representam o escopo daquelas rodadas e foram preservados.

| Cenário — linha 13 integral | Power BI registrado, arredondado | Databricks informado pelo usuário | Diferença consolidada informada |
| --- | ---: | ---: | ---: |
| Realizado | R$ 5.038.227,39 | R$ 5.038.227,39 | R$ 0,00 |
| Orçamento | R$ 6.622.493,82 | R$ 6.622.493,82 | R$ 0,00 |
| Previsão | R$ 6.157.931,19 | R$ 6.157.931,19 | R$ 0,00 |

Totais por filial coincidentes conforme a confirmação do usuário; os resultados DAX por filial/ano permanecem nas evidências da seção 13. Não se infere a composição das 16 linhas SQL nem uma nova homologação contábil a partir dessa quantidade.

### Estratégia DRE aprovada para implementação inicial

1. Usar vw_dre_comparativo[ordem_dre] e [descricao_dre] nos visuais gerenciais, com ordenação e subtotal tratados explicitamente.
2. Não usar dim_dre como filtro automático da view sem implementação específica e validação própria.
3. Usar dim_conta e fato_lancamentos/fato_orcamento/fato_previsao para detalhamento por conta. O aceite não cria uma regra de sinal ajustado para fatos brutas: documentar e conciliar essa regra antes de implementar medidas desse detalhamento.
4. Não somar indiscriminadamente as 13 linhas, não reaplicar tipolancamento aos valores já ajustados e preservar BLANK/NULL como ausência quando aplicável.
5. Preservar os relacionamentos existentes e respeitar períodos equivalentes nas comparações.

### Separação entre aceite técnico e homologação contábil

**Resultado Líquido ainda depende de homologação contábil.** A coincidência numérica da linha 13 comprova conciliação técnica, mas não homologa a classificação, composição ou fórmula contábil do Resultado Líquido. Qualquer referência futura deve identificar essa pendência.

**EBITDA e EBIT continuam sem cálculo até homologação contábil.** Essas pendências permanecem registradas e não impedem a execução das demais atividades de F2 no escopo aprovado. Também não se aprovam antecipadamente as novas medidas, páginas, análise de favorabilidade ou RLS que ainda precisam de seus próprios testes.

### Decisão final e pré-requisitos de início

- [x] Fase 1 — Concluída com aceite técnico, evidências compatíveis e estratégia inicial aprovada.
- [x] Fase 2 — Liberada para execução.
- [ ] Fase 2 — Iniciada. Nenhuma medida ou página foi criada/modificada nesta tarefa.

Antes de implementar F2: apresentar o lote e os arquivos afetados; fechar Desktop para edição e conferir backup atualizado; definir tabela hospedeira e contratos de medida por posição/fonte/sinal/contexto/total/BLANK; preservar a estratégia aprovada e os limites de Conta; definir recortes equivalentes e favorabilidade; preparar validação incremental e documentação das fórmulas/resultados. A lista operacional completa está no PLANS.md.

Nesta tarefa foram feitas apenas conferência das evidências e atualização documental. Modelo semântico, relacionamentos, consultas, medidas, páginas, conexões, credenciais e AGENTS.md permaneceram sem alterações pelo agente.
