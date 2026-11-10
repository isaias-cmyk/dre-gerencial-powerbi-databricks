# Contrato de cobertura temporal — DRE Moderno - Databricks

## Estado vigente — convenção didática em 03/11/2026

**Contrato DIDATICA-1.0-20261103 estabelecido por premissa expressa do usuário para base fictícia de treinamento. Validação documental/local concluída; desbloqueio do L2.3.1 recomendado exclusivamente nesse escopo. Implementação não iniciada.** Não há certificação técnica de completude nem fechamento contábil real. O desenho abaixo ainda não foi aplicado ao modelo.

Esta seção prevalece sobre as exigências de certificação real e o bloqueio descritos no histórico de 02/11, somente para este conjunto didático. A matriz de certificações técnicas continua válida como registro do que não foi comprovado; ganha uma dimensão independente de cobertura didática. Não se exige agora obter um fechamento real para uma base fictícia. Em eventual uso real, a convenção não substitui o manifesto de produção proposto anteriormente.

### Identidade e premissa aceita

- Origem: declaração explícita do usuário nesta conversa, em 03/11/2026; não atribuída ao autor do Excel ou ao operador Databricks.
- Arquivo: BaseDados.xlsx. Versão local documental atribuída pelo projeto: **TREINAMENTO-20261103-HASH-27e02e714898**, sem alegar versão original do produtor.
- SHA-256 conferido nesta execução: **27e02e7148984d74acdb5cf086a9ba637c55617152793f23509d3bad24bce04b**. Coincide com o arquivo inspecionado anteriormente.
- Configuração documental versionada: [cobertura-temporal-didatica.json](cobertura-temporal-didatica.json). É artefato em docs, sem conexão com o modelo neste momento.

| Cenário | Filiais | Cobertura didática inclusiva | Fora dessa cobertura no universo 2021–2023 |
| --- | --- | --- | --- |
| Realizado | 01, 02, 03 | Janeiro/2021 a maio/2023 | Junho–dezembro/2023: Realizado não fornecido |
| Orçado | 01, 02, 03 | Janeiro/2021 a dezembro/2023 | Não há mês adicional declarado nesse universo |
| Previsto | 01, 02, 03 | Janeiro/2021 a dezembro/2023 | Não há mês adicional declarado nesse universo |

São 87 pares cobertos didaticamente no Realizado e 21 pares declarados **NAO_FORNECIDO_DIDATICO**. Nenhum desses 21 foi declarado processado sem movimento. Cobertura significa que o cenário foi disponibilizado para o exercício; não depende da soma financeira, da existência de uma conta/posição ou de movimento não nulo. Uma posição BLANK não reduz o intervalo didático, mas seu valor permanece BLANK. Fora de 2021–2023 ou para filial não configurada, o estado é **NAO_DEFINIDO**, sem extrapolação.

### Arquitetura recomendada — desenho, não implementação

**Uma tabela local de configuração desconectada e oculta, candidata `_CoberturaTemporal`, sem relacionamento adicional**, consultada somente pelas cinco medidas novas. Reutilizar dim_filial, dim_calendario, vw_dre_comparativo e as três bases de _Medidas para filtros e valores financeiros. A configuração deve ser independente dos movimentos.

O manifesto documental tem nove intervalos (três cenários × três filiais), cada um com início/fim de competência, natureza didática, versão do contrato e hash do arquivo. Limites são primeiros dias de meses, inclusivos; maio/2023 é representado como competência 2023-05-01. A futura tabela poderá ser materializada localmente como tabela calculada constante tipada, a partir da configuração aprovada, sem consultar Databricks. As datas ficam **na configuração**, nunca como 31/05/2023 nem como outra constante de corte nas cinco medidas. Esta entrega não contém TMDL ou fórmula dessa tabela.

Não haverá leitura automática do JSON pelo Power BI: na implementação futura, a materialização local deverá reproduzir os nove intervalos e os identificadores documentais, com conferência entre manifesto e tabela. Esse procedimento evita dependência de caminho local/credencial e alterações Power Query; exige controle explícito de sincronização. Não editar manualmente somente um dos dois artefatos.

Justificativa da tabela adicional: centraliza parâmetros sem repeti-los em cinco fórmulas, suporta filial/cenário/versão e preserva as 36 medidas e tabelas de origem. Colocar configuração em _Medidas alteraria seu papel/partição; adicionar colunas às dimensões misturaria premissa de cobertura com atributos de calendário/filial; descobrir MAX na fato/view confundiria cobertura com movimento. Essas alternativas não são recomendadas para este requisito. O novo objeto é pequeno e sem propagação física de filtros. **Nenhuma tabela foi criada; inclusão estrutural requer aprovação do desenho antes da edição futura.**

Se aplicado, o impacto esperado é de 15 para 16 tabelas, mantendo 18 relacionamentos, e de 36 para 41 medidas após adicionar apenas M37/M38/M39/M49/M50. Esses números são previsão, não estado implementado. Preservar todos os IDs existentes; criar IDs próprios somente para novos objetos aprovados. Nenhuma nova consulta M, conexão, alteração Databricks ou página necessária.

### Algoritmo contratual das cinco medidas futuras

1. Ler filiais selecionadas de dim_filial e datas selecionadas de dim_calendario, independentemente das linhas com valores na view. Filial sem configuração torna o contexto indisponível, sem ignorá-la no cálculo do corte. A seleção de posição não define cobertura.
2. Aplicar a guarda de meses completos: seleção parcial de dias retorna números BLANK e status “Selecione meses completos”. Isso conserva os limites do usuário, sem completar ou ratear datas. Filtros temporais/filiais devem partir das dimensões; filtros diretos adicionais na view devem continuar restringindo os resultados e precisam de teste de conflitos, sem remoção indiscriminada de filtros.
3. Expandir os intervalos configurados em competências virtuais e intersectar com os meses efetivamente selecionados. Para cada filial selecionada obter a última competência coberta nessa seleção; o corte comum é a menor dessas últimas competências. Sem cobertura em alguma filial, retornar contexto indisponível.
4. Construir os pares de todas as filiais selecionadas com os meses selecionados até o corte comum, limitados pela cobertura de cada filial. Se houver mês selecionado anterior/igual ao corte sem cobertura em alguma filial, bloquear por lacuna; não preencher intervalos nem incluir meses não selecionados. Neste conjunto os três intervalos Realizado são iguais.
5. Aplicar o mesmo conjunto de pares ao Realizado, Orçado e Previsto por filtro virtual, preservando os filtros existentes de posição/descrição e demais filtros. Reutilizar as bases para respeitar posição única e BLANK de EBITDA/EBIT. Para filtragem virtual entre tabelas sem relação, a documentação oficial descreve [TREATAS](https://learn.microsoft.com/en-us/dax/treatas-function-dax); interseção com filtros existentes deve respeitar [KEEPFILTERS](https://learn.microsoft.com/en-us/dax/keepfilters-function-dax). A escolha final e os contextos serão validados no mecanismo, sem supor equivalência entre a simulação local e DAX.
6. Validar cobertura e disponibilidade da referência em todos os pares antes de agregar Orçado/Previsto. Falta de uma referência bloqueia aquela comparação e gera diagnóstico; não diminuir o Realizado silenciosamente. BLANK do Realizado em uma posição continua BLANK, sem zero artificial e sem alterar a premissa global. Referência zero é valor presente.
7. M49 conta pares de cobertura, não linhas da fato nem pares com valor do indicador. Pode contar 87 mesmo que uma posição esteja BLANK. Sem pares, a contagem diagnóstica pode ser 0; números financeiros continuam BLANK. M50 deve explicitar “Cobertura didática”, contrato ativo e recorte integral/parcial/sem Realizado fornecido, além das guardas. Não usar texto “fechado”.

Nomes preservados: `DRE | Realizado Comparável`, `DRE | Orçado Comparável`, `DRE | Previsto Comparável`, `DRE | Pares Filial-Competência Comparáveis`, `DRE | Status Comparabilidade`. Não implementar desvios, classificação ou outros sublotes. As bases selecionadas antigas continuam disponíveis inclusive para Orçado/Previsto de junho–dezembro/2023.

### Validação técnica disponível e riscos residuais

Executada validação local do manifesto: hash do Excel, nove chaves filial/cenário, limites mensais e totais de 87 pares Realizado/108 Orçado/108 Previsto. Nove simulações de conjuntos aprovadas: integral, 2021, 2022, 2023, junho–dezembro/2023, filial única, duas filiais, seleção descontínua e filial sem configuração. Essas simulações verificam conjuntos e contagens, **não valores financeiros nem execução DAX**. [Evidência](evidencias/cobertura-didatica-20261103/validacao.json).

| Risco residual | Controle previsto |
| --- | --- |
| Confundir exercício com certificação real | Natureza PREMISSA_DIDATICA e ausência de fechamento real explícitas; nunca preencher certificado técnico com esta convenção |
| Arquivo novo e configuração antiga | Novo hash exige nova versão, revisão dos intervalos, evidências de vínculo com a carga e invalidação do aceite anterior até revisão |
| Desalinhamento entre arquivo local e modelo importado | A correspondência do hash local não prova identidade com o snapshot Databricks/Power BI; exigir verificação de atualização e conciliação mensal na implementação |
| Divergência JSON/tabela constante | Conferir versão/hash e cada intervalo após materialização; revisão obrigatória antes de testes |
| Meses cobertos com indicador ausente ou referência incompleta | Não derivar cobertura do valor; manter BLANK e diagnóstico por indicador/referência |
| Filtros parciais/conflitantes e totais | Testar meses completos, seleções descontínuas, filiais múltiplas, ausência de configuração, lacunas sintéticas e posições; preservar 36 medidas por regressão |

Quando novos dados forem disponibilizados: identificar e hashear o novo arquivo, revisar declaração didática e períodos de cada cenário, incrementar versão, preservar a anterior, atualizar configuração local em escopo autorizado e reexecutar testes de cobertura e conciliação. Não estender cobertura automaticamente por MAX de movimento ou pela data do sistema. Um intervalo futuro descontínuo exige intervalos separados e guarda de lacunas; não transformar automaticamente em um único intervalo contínuo.

### Decisão vigente

**A dependência de contrato foi resolvida para a finalidade didática declarada. Recomenda-se desbloquear exclusivamente a preparação e futura implementação do L2.3.1 após aprovação do desenho da tabela local**, Desktop fechado e backup atualizado/restaurável. Não marcar o sublote concluído. Nesta execução fica registrada a proposta concreta de desbloqueio; nenhuma edição de produção está autorizada por inferência a partir desta documentação.

Homologação didática da premissa: declaração do usuário. Validação documental/local: executada pelo agente. Aprovação do desenho estrutural e testes de materialização/DAX/SQL/regressão: **pendentes**. Homologação contábil real: não declarada. As exigências históricas de certificados reais ficam preservadas para eventual uso produtivo, sem bloquear artificialmente o exercício após a mudança explícita de escopo.

### Histórico anterior de investigação e certificações reais

As seções abaixo registram a proposta de 02/11 e os estados técnicos não comprovados. Seus textos de bloqueio e exigências de fechamento real não prevalecem sobre a convenção didática vigente acima. P1–P5 continuam pendências de certificação real e rastreabilidade, não requisitos automaticamente satisfeitos pela declaração didática.

Versão proposta 1.0, 02/11/2026. **Não homologado. L2.3.1 bloqueado antes da implementação.** Este documento é uma proposta final para revisão pelos responsáveis, não um certificado emitido. Nenhuma pessoa foi designada como certificador sem confirmação. Não cria tabela Databricks nem autoriza edição de produção.

## Escopo e conclusões comprovadas

A matriz contém **108 pares filial × competência do Realizado**: filiais 01, 02 e 03, de janeiro/2021 a dezembro/2023. São 87 pares com lançamentos observados até maio/2023 e 21 pares sem lançamentos observados entre junho e dezembro/2023. A cobertura dos 21 não foi certificada; também não há certificado de completude ou fechamento para os 87 apenas por terem movimentos. Realizado observado até maio/2023 não é corte definitivo certificado.

Orçamento e Previsão têm disponibilidade observada de janeiro/2021 a dezembro/2023 nas evidências anteriores; essa disponibilidade não certifica o Realizado. O manifesto lógico completo deve ter chave filial × competência × cenário; a matriz de 108 pares abaixo retrata somente o Realizado. A certificação dos outros cenários e de suas versões requer registros próprios, sem atribuir-lhes fechamento do Realizado.

As verificações A01/A02/A03/B02/B04 e a definição das views foram **reutilizadas como evidências anteriores**, sem repetir consultas ou investigação de metadados. B04 está concluída: propriedades técnicas Delta sem certificado mensal ou contábil. Não se afirma inexistência global de controle externo ou inacessível.

## Evidências ainda não avaliadas: investigação desta entrega

Foi inspecionada em leitura a cópia **BaseDados.xlsx na raiz do projeto**, que os registros anteriores explicitamente não haviam auditado. Leitura direta do pacote OOXML, sem executar macros, fórmulas ou conexões; o SHA-256 permaneceu inalterado. Resultados reproduzíveis em [inspecao-arquivo-produtor.json](evidencias/contrato-cobertura-20261102/inspecao-arquivo-produtor.json) e rotina em [contrato-cobertura-gerar.py](evidencias/contrato-cobertura-gerar.py).

- Treze abas visíveis: estrutura DRE, plano de contas, Orçamento, Previsão e nove abas de lançamentos por filial/ano.
- Cada aba de lançamentos de 2021 e 2022 contém 516 registros, 43 por mês; cada aba de 2023 contém 215 registros, 43 por mês de janeiro a maio. São 3.741 registros no conjunto das nove abas. O vínculo entre nomes de abas e filiais é coerente com a rastreabilidade anterior, mas a regra de mapeamento ainda precisa ser ratificada pelo produtor.
- As abas Orçamento e Previsão têm 4.644 registros cada, 129 por mês entre janeiro/2021 e dezembro/2023. São contagens observadas na cópia, não quantidades esperadas declaradas pelo produtor.
- As abas de fatos apresentam os campos competencia_data, planoContas_id e valor. Não há aba identificada como manifesto ou certificado mensal. Propriedades core estão vazias, sem autor/responsável certificado.
- Busca textual nas células por termos de manifesto, certificação, completude, processamento e fechamento não encontrou ocorrências. Não foram encontradas partes de comentários, assinatura digital ou VBA na lista do pacote. Existe uma parte binária xl/metadata de 528 bytes, não interpretada; não se atribui significado de certificação a ela. Ausência de termos não exclui documentação externa.
- Datas seriais foram interpretadas pela época Excel declarada/padrão do arquivo; zero datas de competência não interpretadas na inspeção. Não houve conciliação financeira linha a linha, nem validação de fórmulas recalculadas.

**Limitação essencial:** o nome BaseDados.xlsx e contagens coincidentes não provam que a cópia local seja exatamente o arquivo usado na ingestão. É necessário hash/versão do artefato efetivamente consumido e evidência do produtor. O arquivo mostra conteúdo disponível, não a totalidade esperada nem fechamento.

Busca dirigida no projeto, fora de backups/caches e artefatos gerados de testes, não localizou notebook de ingestão exportado (.ipynb/.dbc) nem declaração autoritativa do produtor. Os SQLs disponíveis são testes e definições já examinadas; scripts Python de auditoria não são pipelines de origem. O histórico anterior referencia notebookId 3921734519707848, mas seu código, revisão e logs de execução não foram fornecidos nem acessados nesta entrega. Não se reconsultou o histórico. Nenhuma evidência nova do produtor foi obtida por serviço remoto; nenhuma mensagem foi enviada a responsáveis. A existência e o conteúdo de notebooks remotos permanecem pendentes, não refutados pela busca local.

## Seis situações: definição e separação

As situações não formam uma classificação única mutuamente exclusiva: observação, carga e fechamento são dimensões independentes. Um mês pode ter dados observados e carga completa certificada e, ainda assim, fechamento desconhecido. Na matriz, “desconhecido” significa ausência de evidência suficiente, não declaração de falso.

| Situação | Evidência mínima exigida | Situação recebida |
| --- | --- | --- |
| 1. Competência com dados observados | Linhas identificadas por filial/mês em exportação rastreável | 87 pares; não certifica completude |
| 2. Carga completa certificada | Declaração do produtor sobre universo esperado + validação de processamento/completude e vínculo de versão | Nenhum certificado recebido |
| 3. Processada sem movimento certificado | Declaração explícita de zero registros esperados + processamento/validação concluídos para aquele par | Nenhum certificado recebido; não atribuir aos 21 pares |
| 4. Não carregada | Declaração explícita do produtor/execução de que a competência não foi carregada, com escopo e snapshot | Nenhuma declaração recebida; não derivar de ausência de linhas |
| 5. Fechamento contábil certificado | Ato autorizado da Controladoria, com filial/mês, data e versão, incluindo reabertura | Nenhum certificado recebido |
| 6. Situação desconhecida | Falta, conflito ou insuficiência de evidência em qualquer dimensão | Carga/completude e fechamento desconhecidos nos 108 pares |

Não deduzir fechamento de movimento, ausência de movimento, Orçamento/Previsão, número de registros, nome de aba, timestamp de ingestão ou propriedades Delta. Agregado financeiro zero pode refletir compensação de movimentos; não é mês sem movimento. NULL/BLANK monetário permanece NULL/BLANK, sem preenchimento automático.

## Manifesto proposto para homologação documental

Pode ser inicialmente um CSV acompanhado de termo de aprovação versionado, armazenado na documentação autorizada. Não implica criar workspace.gold.controle_competencias nesta execução. A proposta detalhada anterior permanece em [proposta-controle-competencias.md](proposta-controle-competencias.md); este contrato fixa o conteúdo a submeter à homologação, sem aprová-lo automaticamente.

| Grupo | Campos / regra proposta |
| --- | --- |
| Identidade | id_manifesto, versao_manifesto, cod_filial, competencia (primeiro dia do mês), cenario; uma chave atual por filial/mês/cenário e histórico preservado |
| Observação | dados_observados, quantidade_observada, fonte_observacao, data_snapshot; separar de quantidade esperada; ausência de linha na exportação não vira zero certificado |
| Declaração de origem | arquivo/aba e hash/versão efetivamente consumida, produtor autorizado, escopo de contas/filiais/meses, quantidade_esperada e regra de completude; NULL significa não declarado |
| Processamento | id_execucao, notebook/código/revisão, início/fim com fuso explícito, quantidade_lida/aceita/rejeitada/duplicada e destino/snapshot; justificar descartes e transformações antes de reconciliar contagens |
| Carga | estado_carga DESCONHECIDA/NAO_CARREGADA/EM_PROCESSAMENTO/PARCIAL/COMPLETA/FALHA/INVALIDADA; COMPLETA exige certificado, não apenas sucesso técnico |
| Completude | estado_completude DESCONHECIDA/VALIDADA/DIVERGENTE, validação e evidência; sem_movimento_certificado verdadeiro/falso/NULL; verdadeiro somente com declaração de zero esperado e processamento verificado |
| Fechamento | estado_fechamento DESCONHECIDO/ABERTO/FECHADO/REABERTO/NAO_APLICAVEL; autoridade, evidência, data de fechamento/reabertura e versão dos dados. NAO_APLICAVEL somente com regra aprovada por cenário |
| Homologação | responsável pelos dados, aprovador de completude, responsável contábil, papéis autorizados, data/fuso, versão aprovada, parecer e referência verificável da aprovação |
| Auditoria | versão anterior, motivo da alteração, vigência, certificado substituído/invalidado e referência a reprocessamento; não apagar estado desconhecido ou divergente para obter aceite |

Estado NAO_CARREGADA corresponde à situação 4 somente quando documentado. Mesmo uma cópia de origem completa não comprova que todos os seus registros foram aceitos na Gold. Igualdade de contagens não garante igualdade de conteúdo: validar chaves, rejeições, duplicações e regras de transformação e, quando necessário, reconciliação de conteúdo.

## Evidências por linha e pendências

| Código | Proveniência e alcance |
| --- | --- |
| E01 | CSV fornecido pelo usuário, 87 pares únicos: [exportação preservada](<evidencias/competencias-exportacoes-20261102/New_Query_2026_11_02_15_53_51 (3).csv>); contagens por filial/mês. SQL e snapshot exatos ainda não anexados. Corroborado no nível de contagens mensais pela cópia local E03; não há nova certificação |
| E02 | Complemento da grade esperada 01/02/03 × 36 meses menos E01: 21 pares sem linhas observadas; coerente com diagnóstico DAX anterior em docs/validacao-lote2-3-1.md. Não é declaração de não carga ou de processamento vazio |
| E03 | Inspeção nova de BaseDados.xlsx; SHA-256 27e02e7148984d74acdb5cf086a9ba637c55617152793f23509d3bad24bce04b; conteúdo observado sem autoria/manifesto homologado. Origem exata do arquivo ingerido ainda não certificada |
| E04 | Evidências anteriores de histórico Delta/identificação da fato Gold e B04 concluída: processamento técnico, sem certificado mensal. Não reexecutadas nesta entrega |
| P1 | Produtor identificar arquivo efetivamente entregue, hash/versão, filiais/meses esperados e regra de contas; ratificar mapeamento das abas |
| P2 | Engenheiro/operador fornecer notebook e revisão/execução pertinentes, logs de entrada/aceitos/rejeitados e vínculo com snapshot Gold; código sem logs não prova execução |
| P3 | Responsável pelos dados certificar completude de cada par e registrar conflitos/rejeições; contagem observada não é expectativa |
| P4 | Controladoria declarar estado contábil por par e autoridade de fechamento/reabertura; ausência de termo fica desconhecida |
| P5 | Para os 21 pares, declarar com evidência se não carregados, processados sem movimento, parciais ou desconhecidos; não escolher por inferência |

“Não recebido” na coluna certificador refere-se à certificação mensal, não ao usuário que enviou uma exportação. Origem da certificação permanece não recebida em todas as linhas. E04 é contextual à tabela inteira e não certifica uma linha da matriz. P1–P4 aplicam-se a todos os pares; P5 acrescenta o esclarecimento necessário dos meses sem movimento observado.

## Fluxo proposto de homologação pelo responsável pelos dados

1. **Nomeação:** o proprietário dos dados confirma formalmente quem pode declarar completude e quem pode declarar fechamento. Não preencher automaticamente nomes a partir de usuário do commit Delta ou autor do arquivo.
2. **Entrega do produtor:** anexar arquivo/hash/versão, escopo esperado por filial/mês/cenário e declarações explícitas para cada mês sem movimento. Para histórico, certificação retroativa exige evidência e justificativa; não basta assinar um MAX de data.
3. **Comprovação de processamento:** anexar notebook exportado, revisão e logs correspondentes; reconciliar origem → processamento → Gold para o mesmo snapshot. Explicar rejeições/duplicidades/conversões; evidenciar zero esperado quando aplicável.
4. **Preenchimento e revisão:** responsável pelos dados preenche os estados dos 108 pares, mantendo desconhecidos/divergentes onde não houver prova. Uma aprovação por intervalo só pode valer como lote se enumerar explicitamente as chaves e a versão/hash da matriz e declarar exceções.
5. **Ato contábil separado:** Controladoria certifica fechamento/abertura/reabertura nos pares aplicáveis. Homologação técnica não substitui esse ato e não homologa automaticamente Resultado Líquido, EBITDA ou EBIT.
6. **Aceite versionado:** registrar parecer, papéis, data/fuso e referências verificáveis; publicar somente em local autorizado, sem envio automático nesta tarefa. Guardar versão anterior e invalidações. Campos de assinatura ficam vazios até recebimento efetivo.
7. **Reavaliação do bloqueio:** avaliar se há cobertura suficiente no escopo certificado e política temporal aprovada. Não exigir que todos os meses estejam fechados para reconhecer um subconjunto certificado, mas não liberar comparação que atravesse mês desconhecido. A implementação continua sujeita a autorização própria e aos testes previstos.

Modelo do termo a preencher: “Na qualidade de [papel autorizado], aprovo/rejeito a versão [versão/hash] do manifesto [ID], para as chaves [lista/anexo], cenário [cenário], snapshot [versão]. Declaro [carga/completude OU fechamento] nos estados registrados, com exceções [lista] e evidências [referências]. Responsável [não preenchido], data/fuso [não preenchidos].” Esse texto é uma proposta, não uma declaração assinada ou emitida.

## Política temporal proposta e guardas

Preservar o corte comum entre todas as filiais selecionadas. Usar apenas meses certificados dentro da seleção, sem fixar maio/2023. Falta de certificado em uma filial não pode ser omitida pelo MIN. Lacunas internas precisam bloquear o contexto ou receber política explícita aprovada; não preencher meses não selecionados.

Recomendação conservadora ainda sujeita a aceite: carga COMPLETA + completude VALIDADA + snapshot coerente + fechamento FECHADO. Se forem admitidos dados abertos, formalizar política distinta de cobertura técnica com estado contábil visível; não chamá-los de fechados. Reabertura/invalidação retira elegibilidade até nova certificação. Certificação de mês sem movimento preserva a cobertura, mas não autoriza trocar BLANK financeiro por zero. Orçamento/Previsão precisam de cobertura e versão compatíveis no mesmo recorte.

Testes exigidos antes de liberar implementação: 108 chaves únicas e meses normalizados; certificados válidos e vinculados ao snapshot; distinção entre zero movimento certificado e não carga; exceções/reaberturas/lacunas; filiais com cortes distintos; referência ausente; seleções parciais/descontínuas; validação de dados observados sem convertê-los em certificados. Testes futuros do manifesto não foram executados nesta entrega, pois os certificados não foram recebidos.

## Estado atual e validação documental executada

Matriz gerada a partir da exportação preservada, sem modificar seus dados: 108 chaves únicas, 87 com registros e 21 ausentes; soma das contagens observadas 3.741. Nenhuma certificação de completude, mês sem movimento, não carga ou fechamento foi recebida. Valores desconhecidos permanecem desconhecidos. Matriz auxiliar: [matriz-108.csv](evidencias/contrato-cobertura-20261102/matriz-108.csv); [validação](evidencias/contrato-cobertura-20261102/validacao.json).

**L2.3.1 bloqueado; contrato não homologado.** Nenhuma nova consulta remota, nova investigação de metadados ou alteração de produção nesta entrega. As 36 medidas permanecem preservadas e as cinco de comparabilidade não foram implementadas. Demais sublotes não iniciados; Resultado Líquido provisório e EBITDA/EBIT pendentes de homologação contábil.

## Matriz das 108 combinações — cenário Realizado

Cada linha separa observação das quatro certificações/declarações não recebidas. As 21 linhas ausentes da exportação não têm quantidade financeira ou contagem esperada preenchida artificialmente. Evidências e pendências seguem os códigos definidos acima.

| Filial | Competência | Observação / qtd. exportada | Carga completa | Sem movimento certificado | Não carregada confirmada | Fechamento | Evidência | Certificador | Pendências | Cobertura didática vigente |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | 2021-01-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 01 | 2021-02-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 01 | 2021-03-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 01 | 2021-04-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 01 | 2021-05-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 01 | 2021-06-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 01 | 2021-07-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 01 | 2021-08-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 01 | 2021-09-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 01 | 2021-10-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 01 | 2021-11-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 01 | 2021-12-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 01 | 2022-01-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 01 | 2022-02-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 01 | 2022-03-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 01 | 2022-04-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 01 | 2022-05-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 01 | 2022-06-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 01 | 2022-07-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 01 | 2022-08-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 01 | 2022-09-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 01 | 2022-10-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 01 | 2022-11-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 01 | 2022-12-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 01 | 2023-01-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 01 | 2023-02-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 01 | 2023-03-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 01 | 2023-04-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 01 | 2023-05-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 01 | 2023-06-01 | Sem lançamentos observados / ausente no CSV | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E02 | Não recebido | P1/P2/P3/P4/P5 | NAO_FORNECIDO_DIDATICO |
| 01 | 2023-07-01 | Sem lançamentos observados / ausente no CSV | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E02 | Não recebido | P1/P2/P3/P4/P5 | NAO_FORNECIDO_DIDATICO |
| 01 | 2023-08-01 | Sem lançamentos observados / ausente no CSV | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E02 | Não recebido | P1/P2/P3/P4/P5 | NAO_FORNECIDO_DIDATICO |
| 01 | 2023-09-01 | Sem lançamentos observados / ausente no CSV | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E02 | Não recebido | P1/P2/P3/P4/P5 | NAO_FORNECIDO_DIDATICO |
| 01 | 2023-10-01 | Sem lançamentos observados / ausente no CSV | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E02 | Não recebido | P1/P2/P3/P4/P5 | NAO_FORNECIDO_DIDATICO |
| 01 | 2023-11-01 | Sem lançamentos observados / ausente no CSV | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E02 | Não recebido | P1/P2/P3/P4/P5 | NAO_FORNECIDO_DIDATICO |
| 01 | 2023-12-01 | Sem lançamentos observados / ausente no CSV | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E02 | Não recebido | P1/P2/P3/P4/P5 | NAO_FORNECIDO_DIDATICO |
| 02 | 2021-01-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 02 | 2021-02-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 02 | 2021-03-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 02 | 2021-04-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 02 | 2021-05-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 02 | 2021-06-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 02 | 2021-07-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 02 | 2021-08-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 02 | 2021-09-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 02 | 2021-10-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 02 | 2021-11-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 02 | 2021-12-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 02 | 2022-01-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 02 | 2022-02-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 02 | 2022-03-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 02 | 2022-04-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 02 | 2022-05-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 02 | 2022-06-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 02 | 2022-07-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 02 | 2022-08-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 02 | 2022-09-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 02 | 2022-10-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 02 | 2022-11-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 02 | 2022-12-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 02 | 2023-01-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 02 | 2023-02-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 02 | 2023-03-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 02 | 2023-04-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 02 | 2023-05-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 02 | 2023-06-01 | Sem lançamentos observados / ausente no CSV | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E02 | Não recebido | P1/P2/P3/P4/P5 | NAO_FORNECIDO_DIDATICO |
| 02 | 2023-07-01 | Sem lançamentos observados / ausente no CSV | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E02 | Não recebido | P1/P2/P3/P4/P5 | NAO_FORNECIDO_DIDATICO |
| 02 | 2023-08-01 | Sem lançamentos observados / ausente no CSV | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E02 | Não recebido | P1/P2/P3/P4/P5 | NAO_FORNECIDO_DIDATICO |
| 02 | 2023-09-01 | Sem lançamentos observados / ausente no CSV | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E02 | Não recebido | P1/P2/P3/P4/P5 | NAO_FORNECIDO_DIDATICO |
| 02 | 2023-10-01 | Sem lançamentos observados / ausente no CSV | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E02 | Não recebido | P1/P2/P3/P4/P5 | NAO_FORNECIDO_DIDATICO |
| 02 | 2023-11-01 | Sem lançamentos observados / ausente no CSV | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E02 | Não recebido | P1/P2/P3/P4/P5 | NAO_FORNECIDO_DIDATICO |
| 02 | 2023-12-01 | Sem lançamentos observados / ausente no CSV | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E02 | Não recebido | P1/P2/P3/P4/P5 | NAO_FORNECIDO_DIDATICO |
| 03 | 2021-01-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 03 | 2021-02-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 03 | 2021-03-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 03 | 2021-04-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 03 | 2021-05-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 03 | 2021-06-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 03 | 2021-07-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 03 | 2021-08-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 03 | 2021-09-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 03 | 2021-10-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 03 | 2021-11-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 03 | 2021-12-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 03 | 2022-01-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 03 | 2022-02-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 03 | 2022-03-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 03 | 2022-04-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 03 | 2022-05-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 03 | 2022-06-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 03 | 2022-07-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 03 | 2022-08-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 03 | 2022-09-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 03 | 2022-10-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 03 | 2022-11-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 03 | 2022-12-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 03 | 2023-01-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 03 | 2023-02-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 03 | 2023-03-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 03 | 2023-04-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 03 | 2023-05-01 | Dados observados / 43 | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E01 | Não recebido | P1/P2/P3/P4 | FORNECIDO_DIDATICO |
| 03 | 2023-06-01 | Sem lançamentos observados / ausente no CSV | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E02 | Não recebido | P1/P2/P3/P4/P5 | NAO_FORNECIDO_DIDATICO |
| 03 | 2023-07-01 | Sem lançamentos observados / ausente no CSV | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E02 | Não recebido | P1/P2/P3/P4/P5 | NAO_FORNECIDO_DIDATICO |
| 03 | 2023-08-01 | Sem lançamentos observados / ausente no CSV | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E02 | Não recebido | P1/P2/P3/P4/P5 | NAO_FORNECIDO_DIDATICO |
| 03 | 2023-09-01 | Sem lançamentos observados / ausente no CSV | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E02 | Não recebido | P1/P2/P3/P4/P5 | NAO_FORNECIDO_DIDATICO |
| 03 | 2023-10-01 | Sem lançamentos observados / ausente no CSV | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E02 | Não recebido | P1/P2/P3/P4/P5 | NAO_FORNECIDO_DIDATICO |
| 03 | 2023-11-01 | Sem lançamentos observados / ausente no CSV | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E02 | Não recebido | P1/P2/P3/P4/P5 | NAO_FORNECIDO_DIDATICO |
| 03 | 2023-12-01 | Sem lançamentos observados / ausente no CSV | Desconhecida | Desconhecido | Desconhecida | Desconhecido | E02 | Não recebido | P1/P2/P3/P4/P5 | NAO_FORNECIDO_DIDATICO |


## Aplicação do contrato no PBIP — 03/11/2026

A solicitação de implementação aprovou o desenho; nome efetivo da tabela local: **_ConfigCobertura**, substituindo _CoberturaTemporal apenas como nome candidato. Nove intervalos, oculta e sem relacionamentos, fonte local constante com datas DATETIME em literais ISO aceitos no mecanismo; datas não fixadas nas cinco medidas. A configuração já foi materializada e conferida com este manifesto/versão/hash; as 36 medidas antigas preservadas e cinco novas validadas localmente. L2.3.1 em validação, não concluído, aguardando SQL independente e aceite. Ver docs/validacao-lote2-3-1.md. A convenção permanece didática, sem fechamento contábil real.
