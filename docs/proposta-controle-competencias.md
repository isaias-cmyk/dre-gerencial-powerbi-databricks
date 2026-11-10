# Proposta de controle de competências — dependência de L2.3.1

Data: 02/11/2026. **Somente proposta; nenhum objeto Databricks ou Power BI criado.** Fundamentada na orientação expressa do usuário: investigar em leitura e não implementar comparabilidade antes de um contrato temporal confiável.

## Problema e evidências

O modelo contém movimento e rastreabilidade das linhas, sem campo importado que distinga mês sem movimento, carga ausente, carga parcial, competência processada e competência fechada. A grade futura da DRE contém 13 posições por mês mesmo sem Realizado. Orçamento/Previsão não certificam carga do Realizado. Última linha, soma positiva, valor não BLANK de um indicador, arquivo anual ou horário de ingestão não são certificados de cobertura.

Não se afirma inexistência de controle no Databricks inteiro: Bronze/Silver e metadados remotos ainda precisam ser consultados com os roteiros de leitura preparados. Se existir controle confiável, preferir reutilizá-lo mediante contrato; não duplicá-lo automaticamente.

## Objeto lógico candidato

Nome proposto: `workspace.gold.controle_competencias`. Grão atual: **cod_filial × competencia mensal × cenario**, com uma linha atual por chave e histórico auditável das transições. O nome é uma proposta, não objeto existente nem autorização para DDL. Competência deve ser data do primeiro dia do mês; horário de processamento é timestamp separado, com fuso contratual explícito.

| Campo proposto | Significado / regra |
| --- | --- |
| cod_filial | Chave existente de dim_filial; obrigatório e íntegro |
| competencia | Mês de referência, obrigatório, primeiro dia; não data da ingestão |
| cenario | Realizado, Orçado ou Previsto, com domínio/de-para explícito |
| status_carga | NAO_PROCESSADA, EM_PROCESSAMENTO, CONCLUIDA, FALHA ou INVALIDADA; conclusão só após critérios documentados |
| status_completude | NAO_VERIFICADA, VALIDADA ou DIVERGENTE; distinguir sucesso técnico de completude dos dados |
| status_fechamento | NAO_FECHADO, FECHADO, REABERTO ou NAO_APLICAVEL; autoridade e regra por cenário definidas |
| sem_movimento_confirmado | Booleano com evidência de competência processada e vazia; NULL quando não avaliado. Não derivar de COUNT(*) = 0 isoladamente |
| data_hora_processamento | Fim da execução certificada, com fuso explícito; não reutilizar um timestamp genérico das linhas |
| data_hora_fechamento | Evento de fechamento autorizado; NULL se não houve fechamento |
| id_execucao | Identificador auditável do job/lote que certificou a competência |
| versao_dados | Versão/snapshot da origem relacionada ao certificado; deve ser conciliável com a atualização importada |
| origem_evidencia | Referência ao manifesto de origem/contrato/arquivo e período declarado, sem credenciais |
| quantidade_esperada | Contagem declarada pelo produtor ou regra de completude, podendo ser zero quando confirmado; NULL não substituído por zero |
| quantidade_processada | Contagem verificada no lote/snapshot, incluindo zero legítimo |
| validacao_completude | Identificador/resultado da validação que explica por que a carga é completa |
| responsavel_fechamento | Identificação do responsável/sistema autorizado a fechar ou reabrir a competência |
| atualizado_em / versao_controle | Atualização e versão do registro, para recuperação/histórico e invalidação de certificados anteriores |

Campos/estados finais devem ser aprovados antes de criar objetos. Se fechamento não for aplicável a Orçado/Previsto, NAO_APLICAVEL não pode ser interpretado como FECHADO do Realizado. A disponibilidade de referência e sua versão são verificadas separadamente.

## Regra candidata de elegibilidade e corte

Recomendação conservadora para aprovação: cobertura válida do Realizado requer carga CONCLUIDA, completude VALIDADA, versão coerente e fechamento FECHADO. Se a Controladoria quiser comparar dados processados ainda abertos, isso precisa ser uma política distinta, visível e explicitamente autorizada; não equivale a fechamento. A atual Política A determina corte comum, mas não homologa quais estados de carga/fechamento tornam a cobertura válida.

Uma única filial: última competência **certificada como válida dentro dos meses selecionados**. Múltiplas: considerar todas as filiais selecionadas, inclusive as sem linhas de movimento, e usar corte comum que não ultrapasse o último mês certificado de cada uma. Se alguma filial não tiver cobertura válida no período, não ignorá-la no MIN nem inventar uma data: comparação indisponível e diagnóstico por filial.

Uma data mínima dos últimos meses é insuficiente se houver lacuna intermediária. Proposta conservadora: detectar mês selecionado anterior/igual ao corte sem cobertura válida em alguma filial e bloquear o contexto, até definir como lidar com lacunas. Seleções descontínuas não devem incluir meses não selecionados. Não preencher implicitamente intervalos entre MIN e MAX. A mesma seleção válida de competências/filiais será aplicada às três bases financeiras.

Mês certificado sem movimento não some da cobertura; pode participar do corte com contagem zero. O valor financeiro do indicador continua segundo o contrato da view: BLANK permanece BLANK e zero explícito permanece zero. O controle não autoriza completar valores monetários, recalcular sinais ou transformar ausência de uma posição em zero. Se o contrato dos indicadores não distinguir ausência de referência e ausência de movimento, documentar e bloquear a comparação afetada separadamente da cobertura global.

Os 13 registros gerenciais futuros, uma posição BLANK ou um agregado que se anule não devem mudar o certificado global. A disponibilidade de referências Orçado/Previsto e sua versão precisam cobrir os meses certificados usados na comparação, sem esconder referência ausente por redução do Realizado.

## Como produzir evidência confiável

1. Descobrir controles existentes e analisar a definição SQL real da view, permissões e pipelines, sem alterá-los nesta investigação.
2. Identificar o produtor de cada cenário e seu manifesto de períodos esperados por filial, inclusive períodos sem movimento. Um arquivo anual só certifica meses expressamente declarados e verificados, não os doze por inferência do nome.
3. Definir critérios de completude, tratamento de rejeições, reprocessamento, estornos, cargas parciais e fechamento autorizado. Registrar estados de erro, sem excluir competências problemáticas do cadastro esperado.
4. Projetar armazenamento/histórico e testes; somente após aprovação implementar o controle e seu fluxo de alimentação em tarefa específica. Escrita idempotente por chave, conflitos/versionamento e reabertura com auditoria precisam fazer parte do contrato.
5. Não retroalimentar o controle histórico com status FECHADO baseado em MAX(competencia_data), presença de Orçado, soma não nula ou constante maio/2023. Certificação retroativa exige evidência do produtor/Controladoria por competência.
6. Conciliar manifesto × processamento × visão Gold no mesmo snapshot. Reabertura/falha posterior invalida a elegibilidade anterior até nova certificação.
7. Planejar disponibilização no Power BI separadamente. Importar tabela ou alterar consulta seria mudança estrutural fora do escopo atual; requer inspeção, aprovação, Desktop fechado, novo backup e validação de impacto. Não propor relacionamento automático com as fatos nem filtro bidirecional para resolver cobertura.

## Testes do controle antes de liberar as cinco medidas

- Unicidade da chave atual, chaves obrigatórias, cenário válido, competência normalizada e integridade de filial.
- Todos os pares esperados presentes; competência sem controle é desconhecida, não zero nem fechada.
- Carga parcial/falha/reaberta não elegível; sucesso técnico sem completude não elegível.
- Competência certificada sem movimento válida apesar de COUNT de fatos zero; competência sem carga também com COUNT zero continua não válida. Esses dois casos precisam ser demonstrados com evidência própria.
- Realizado com zero/estorno mantém cobertura; indicador BLANK não altera certificado global.
- Filiais com últimos meses distintos, filial sem cobertura e lacuna intermediária; corte comum e diagnóstico corretos.
- Limites de seleção, meses isolados, meses descontínuos, anos múltiplos e seleções parciais de dias; não inventar proporcionalidade diária.
- Versões de dados do certificado e do modelo coerentes; reprocessamento/reabertura invalida corte anterior.
- Casos sintéticos identificados separadamente; casos reais exportados em SQL e DAX mensal por filial/competência/cenário. O aceite agregado de Lote 2.2 não substitui esse teste.

## Decisões pendentes e sequência de desbloqueio

Definir: fonte autoritativa, responsável, critérios de completude, papel do fechamento, política de meses abertos, cobertura de Orçado/Previsto, lacunas, dias parciais, semântica de BLANK por indicador e mecanismo aprovado de consumo no Power BI. Política de corte comum já aprovada; não retornar à máscara individual por movimento proposta originalmente.

Sequência: executar investigação remota em leitura → homologar contrato temporal → aprovar/reutilizar controle (ou implementar separadamente se necessário) → disponibilizar controle com alteração aprovada → fechar Desktop e proteger o projeto → implementar apenas M37/M38/M39/M49/M50 → executar testes mensais/DAX/SQL e regressões. Até então, as cinco medidas permanecem **não implementadas e bloqueadas por dependência**, sem criar stubs ou corte fixo.

## Escopo didático vigente — 03/11/2026

A confirmação expressa do usuário de base fictícia permite a convenção DIDATICA-1.0-20261103 em docs/contrato-cobertura-temporal.md: Realizado disponibilizado Jan/2021–Mai/2023 para 01/02/03; Jun–Dez/2023 não fornecido; referências Jan/2021–Dez/2023. Hash do arquivo vinculado e validado. Isso não constitui carga completa certificada, mês vazio processado ou fechamento real. As exigências acima de certificação real permanecem como proposta para uso produtivo e não impedem o exercício por si sós. Recomenda-se mecanismo local de configuração desconectada descrito no contrato; não criar controle Databricks nesta tarefa. Desenho estrutural ainda pendente de aprovação; zero produção alterada.
