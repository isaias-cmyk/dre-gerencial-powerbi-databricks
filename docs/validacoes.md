# Validações e evidências

## Fase 0 — 02/11/2026

Responsável: Codex. Execução autorizada exclusivamente para Segurança e Diagnóstico. Script preservado: [fase0-executar.ps1](evidencias/fase0-executar.ps1). Resultado: [resultado.json](evidencias/fase0-20261102-145703/resultado.json).

| Verificação executada | Resultado e evidência |
| --- | --- |
| Leitura integral de AGENTS.md e PLANS.md | Executada antes das operações |
| Processo PBIDesktop | Zero processos retornados no início do snapshot; ambiente.json |
| Inventário da entrada | 37 arquivos com tamanho, data e SHA-256; inventario-arquivos.json/csv |
| Git | Instalado; fora de repositório, códigos 128 em status/rev-parse; git.json |
| Tabelas / relações / medidas | 14 tabelas (8 de negócio), 18 relações serializadas, zero medidas explícitas; JSON específicos |
| Páginas / visuais | Uma página, zero arquivos de visual na entrada atual; paginas.json/visuais.json |
| Conexões estáticas | Oito partições M Import, mesmo endpoint e navegação workspace.gold; conexoes.json |
| Parsing JSON | 11 arquivos de projeto incluídos analisados sem erro; json-sintaxe.json |
| Cópia de segurança | 33 arquivos copiados e comparados individualmente por SHA-256 |
| ZIP e restauração isolada | 33 arquivos extraídos; quantidade exata e todos os hashes iguais; restauracao-hashes.json |
| Referências na restauração | Caminho PBIP → Report → SemanticModel/definition.pbism existente |
| Integridade da entrada | 37 arquivos inalterados até o fim do snapshot; integridade-original-antes-documentacao.json |

Os 11 testes JSON são somente análise sintática, sem validação de schemas remotos. A inspeção TMDL usa extração textual para inventário, sem alegar compilação. Não houve teste de cardinalidade, dados, filtros, DAX, conectividade, atualização, renderização ou abertura no Power BI Desktop. Esses testes pertencem às fases seguintes e permanecem pendentes.

### Backup verificável

Diretório: `backups/fase0-20261102-145703/`.

- `snapshot/`: cópia dos arquivos incluídos, com caminhos relativos preservados.
- `snapshot.zip`: arquivo para recuperação isolada.
- `manifesto-sha256.json`: 33 entradas, com hashes e metadados da origem.
- `restauracao-teste/`: restauração realizada a partir do ZIP, preservada para inspeção.

SHA-256 do ZIP: `7E550BB10CECEF3093F5EC3EE4EEEBA1F1CF2CC1088E21AD8BC82CA2637B58C2`.

Incluídos PBIP, fontes Report/SemanticModel, .platform, tema, diagramLayout, AGENTS.md, versão anterior à atualização de PLANS.md, .gitignore e BaseDados.xlsx. Documentos e evidências gerados nesta fase estão fora deste snapshot de entrada e permanecem em docs/. Novos backups futuros não devem incluir recursivamente backups antigos.

Exclusões explícitas (sem remoção ou alteração dos originais):

1. Report/.pbi/localSettings.json.
2. SemanticModel/.pbi/cache.abf.
3. SemanticModel/.pbi/editorSettings.json.
4. SemanticModel/.pbi/localSettings.json.

A regra aplicada exclui integralmente .pbi, evitando copiar cache e configurações locais/autenticação. [exclusoes-backup.json](evidencias/fase0-20261102-145703/exclusoes-backup.json) registra os caminhos reais. .git, docs e backups também ficam fora do snapshot; .git não existia nesta entrada.

O backup protege os arquivos de desenvolvimento presentes, não dados remotos, permissões, autenticação, cache importado ou visuais ausentes antes da captura. Por estar no mesmo disco, não protege contra perda física do disco; cópia externa não foi realizada.

### Recuperação e gatilhos de rollback

Interromper a edição se houver falha de integridade/abertura, divergência de hashes inesperada, alteração de IDs/conexões, regressão financeira/filtros ou escrita concorrente. Nenhum desses gatilhos foi provocado por esta fase.

1. Confirmar Desktop fechado e preservar cópia dos arquivos atuais antes de qualquer substituição.
2. Verificar SHA-256 do ZIP e manifesto; extrair para uma pasta nova, jamais sobre o original diretamente.
3. Conferir a quantidade e os hashes de todos os 33 arquivos, preservando os caminhos relativos PBIP/Report/SemanticModel.
4. Comparar diferenças com o estado atual. Não restaurar PLANS.md antigo sobre o acompanhamento mais recente nem apagar trabalho posterior do usuário sem análise.
5. Não substituir configurações locais nem credenciais. Cache e autenticação podem precisar ser restabelecidos pelo Desktop usando a configuração existente.
6. Validar abertura no Desktop e dados quando uma recuperação operacional for necessária; o teste desta fase comprovou extração, hashes e referências de entrada, sem abertura no Desktop.
7. Registrar motivo, arquivos recuperados, backup de origem e resultados. Não usar reset destrutivo nem limpeza de diretórios.

### Limitações e pendências

- Arquivo do visual anteriormente inventariado ausente já na entrada; situação documentada sem reconstrução.
- Git não inicializado; adoção futura permanece uma decisão, não bloqueia backup da Fase 0.
- A enumeração de processos cobre processos visíveis na sessão no momento da consulta. Repetir antes de qualquer edição futura.
- Nenhuma homologação financeira foi realizada. Valores de controle, períodos, EBITDA e EBIT mantêm as regras do AGENTS.md.
- Fase 1 não iniciada. Não foram auditadas unicidade, cardinalidade efetiva nem propagação de filtros.

## Fase 1 — inspeção estática em 02/11/2026

O texto da Fase 0 acima é histórico. Nesta execução foi produzido [auditoria-modelo-semantico.md](auditoria-modelo-semantico.md) e o [resultado estático](evidencias/fase1/resultado.json).

Testes executados: comparação com F0 (36/36 arquivos, exceto plano atualizado), extração de 14 tabelas/56 colunas de negócio, verificação de 36 endpoints e 18 pares de tipos, referências model/tabela/variations, duplicidade de endpoints/lineageTags, parsing de 11 arquivos JSON e análise condicional de caminhos de filtro. Nenhum endpoint ausente ou par de tipos divergente foi encontrado.

O grafo condicional usa To → From e estados ativos inferidos das propriedades omitidas; não comprova cardinalidade/direção efetivas. Conta não possui caminho previsto até a view; dim_dre não transmite posição à view. Ativação simulada da inativa criaria dois caminhos de filial para cada fato.

A descoberta de recursos não encontrou sessão Codex Document Control, processo tabular/Desktop ativo nem CLI Databricks/DAX Studio/Tabular Editor no PATH consultado. [Limites registrados](evidencias/fase1/ambiente.json). Nenhuma credencial ou conexão foi alterada para estabelecer sessão.

**Não executados:** compilação TMDL, leitura de metadados efetivos, consultas SQL/DAX, testes de unicidade/NULL/órfãos, calendário, grão da view, filtros em dados e totais da linha 13. Roteiros de teste somente leitura estão preparados e explicitamente marcados como não executados. Não foram criadas medidas ou iniciada a Fase 2.

Integridade final das fontes: [integridade-final.json](evidencias/fase1/integridade-final.json). Fase 1 permanece **Bloqueada** até executar os testes e resolver contratos DRE/conta; ver checklist e ações no relatório. Nenhum controle financeiro ou resultado visual recebeu aceite nesta execução.

## Continuação da Fase 1 — pacote dinâmico

Em 02/11/2026 foram reutilizados os roteiros e criado o [guia executável de testes](execucao-testes-fase1.md), sem nova auditoria estática. A descoberta atual confirmou Desktop instalado, mas sem modelo tabular carregado/sessão conectada. [Evidência](evidencias/fase1-dinamica/ambiente.json).

Executadas localmente geração dos roteiros complementares e verificações de delimitadores, proteção dos originais e documentação. O pacote contém vinte consultas DAX independentes, complemento SQL, fallback DMV e registro com 13 grupos de teste. [Verificação local](evidencias/fase1-dinamica/verificacao-local.json) e [integridade](evidencias/fase1-dinamica/integridade-final.json).

**Consultas SQL/DAX executadas contra dados: zero.** Contagens de nulos/órfãos, estados efetivos, resultados de filtros e totais financeiros não foram medidos. O registro permanece NAO_EXECUTADO com campos observados vazios. A verificação local não valida sintaxe por mecanismo nem aprova dados. Fase 1 continua Bloqueada; Fase 2 não liberada.

## Execução real após abertura do Desktop — 02/11/2026

O registro anterior é histórico. O usuário abriu o projeto e foi possível consultar o modelo carregado via ADOMD local. Foram executadas **23 consultas DAX/INFO, sem erros nem falhas detectadas**, conforme [consolidação](evidencias/fase1-execucao-20261102-154642/consolidacao.json) e [registro com resultados](evidencias/fase1-execucao-20261102-154642/registro-testes-executados.csv).

Chaves únicas nas quatro dimensões; nenhum órfão/chave ausente detectado nos 13 testes de integridade; 18 relações Many:One/OneDirection/Ready, com 12 de negócio ativas, uma inativa e cinco técnicas ativas. Passaram 80 casos filial/período, quatro casos de ano/mês/múltiplas filiais e 36 comparações de interseção Conta + Filial + Período nas fatos. Calendário contínuo e grão da view sem duplicação; comportamento de isolamento Conta/DRE e relação inativa confirmado.

Linha 13 revalidada no modelo: R$ 5.038.227,39 / R$ 6.622.493,82 / R$ 6.157.931,19, com diferenças zero a centavos. Totais por filial/ano e período reconciliam o consolidado carregado. Realizado pós-maio/2023 preservado BLANK; EBITDA/EBIT não homologados.

Os quatro diretórios de execução contêm resultados CSV/JSON, logs e integridade por SHA-256, sem alteração dos arquivos de entrada pelo executor. Resultado técnico detalhado e limites atuais na seção 13 de [auditoria-modelo-semantico.md](auditoria-modelo-semantico.md).

**Ainda não executado:** comparação independente com Databricks SQL da mesma atualização. Aceite do responsável da abordagem DRE 1/limites de Conta ainda pendente. Portanto, testes dinâmicos locais aprovados, Fase 1 global Bloqueada e Fase 2 não iniciada. Nenhuma consulta M, relação, medida ou conexão de produção foi alterada.

## Aceite técnico final da Fase 1 — 02/11/2026

O usuário confirmou a conciliação independente Databricks SQL × DAX: consulta SQL com 16 linhas, diferenças consolidadas de R$ 0,00 nos três cenários e totais por filial coincidentes. A confirmação é compatível com a consolidação DAX existente (23 consultas sem falhas e 80 casos filial/período aprovados), conferida nesta tarefa. [Registro de aceite e proveniência](evidencias/fase1-aceite-tecnico/aceite.json).

A origem da evidência SQL é a declaração expressa do usuário nesta conversa; o agente não reexecutou SQL nem reconstruiu a grade bruta de 16 linhas. Os logs anteriores foram preservados como histórico. A mesma instrução do usuário aprovou a abordagem 1 e os limites de Conta, encerrando as dependências do aceite técnico.

**Fase 1 concluída tecnicamente; Fase 2 liberada e não iniciada.** A liberação segue a estratégia da view para os eixos DRE e dim_conta/fatos para detalhe por conta, preservando relações, posições, BLANK e períodos equivalentes. Ver seção 14 da [auditoria](auditoria-modelo-semantico.md).

Resultado Líquido, EBITDA e EBIT continuam pendentes de homologação contábil; EBITDA/EBIT permanecem sem cálculo. Não foram homologados indicadores contábeis pela coincidência numérica da linha 13. Nesta tarefa foram apenas conferidas evidências e atualizados documentos; nenhuma consulta de produção, medida ou página foi alterada.

## Fase 2 / Lote 2.1 — 02/11/2026

Seis medidas implementadas em TMDL após confirmação do fechamento do Desktop, backup atualizado/verificado e contratos documentados. Tabela auxiliar _Medidas local com uma coluna oculta e DATATABLE constante; sem fonte externa ou nova relação. Somente model.tmdl recebeu referência adicional entre os arquivos de produção preexistentes.

Executados: restauração isolada/hash de 176 arquivos; parser TMDL Microsoft.PowerBI.Tabular antes/depois; contagem de 15 tabelas, 18 relações e seis medidas finais; oito partições M preservadas; nomes únicos, lineageTags, referências, contratos de metadados e integridade de arquivos. Nove consultas DAX de validação preparadas; delimitadores conferidos.

**Não executados:** compilação/execução das seis medidas persistidas, materialização da tabela local, resultados por cenário/filial/período, contextos/totais e confirmação dos rótulos de EBITDA/EBIT no modelo reaberto. O parser não substitui esses testes, e os resultados de F1 não foram reutilizados como aprovação do código novo.

[Relatório e critérios](validacao-lote2-1.md), [contratos](contratos-medidas-dax.md) e [evidência estrutural](evidencias/lote2-1-20261102-160536/validacao-tmdl.json). **Lote não concluído, aguardando validação no Desktop; Lote 2.2 não iniciado.**


## Encerramento do Lote 2.1 — 02/11/2026

Lote concluído tecnicamente: 11 consultas DAX/INFO em leitura, zero erros, 20 casos filial/período e 60 verificações de cenário aprovadas. _Medidas materializada com uma linha e partição Ready, sem erro. Controles integrais coincidentes a centavos; BLANK, totais e EBITDA/EBIT conferidos. Cartão R$ 5,04M confirmado pelo usuário. Evidências em docs/evidencias/lote2-1-encerramento-20261102-162739 e relatório docs/validacao-lote2-1.md. Nenhuma alteração de produção nesta rodada. Lote 2.2 planejado em docs/plano-lote2-2.md e não iniciado. Homologações contábeis permanecem pendentes.


## Lote 2.2 — 02/11/2026

Implementadas 30 medidas de posições autorizadas na tabela _Medidas, preservando as seis existentes. Backup lote2-2-20261102-163559, 237 arquivos restaurados e hashes verificados. Parser TMDL aprovado: 36 medidas, 15 tabelas, 18 relações e oito partições M. Único arquivo de produção alterado: _Medidas.tmdl. Contratos e dez consultas DAX/uma SQL documentados. DAX/SQL não executados; lote não concluído até evidência dinâmica e conciliação independente. Ver docs/validacao-lote2-2.md. Lote 2.3 não iniciado; pendências contábeis mantidas.
