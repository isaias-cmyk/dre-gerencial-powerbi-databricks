# Histórico de alterações

## 02/11/2026 — Fase 0: Segurança e Diagnóstico

Solicitação: executar exclusivamente a Fase 0. Responsável: Codex.

- Lidos integralmente AGENTS.md e PLANS.md.
- Criados inventários de arquivos, schemas declarados, tabelas/colunas/tipos/lineageTags, conexões, relações com IDs, medidas, páginas, visuais e temas.
- Conferido Git: instalado, sem repositório nesta pasta. Nenhum init, commit ou publicação.
- Criado backup `backups/fase0-20261102-145703`, com 33 arquivos incluídos, quatro arquivos .pbi excluídos e manifesto SHA-256.
- Testada restauração do ZIP para pasta isolada: 33 arquivos com hashes idênticos e referências relativas de entrada preservadas.
- Criados docs/arquitetura.md, docs/validacoes.md e evidências reproduzíveis em docs/evidencias/.
- Atualizado PLANS.md para registrar conclusão apenas da Fase 0 e manter F1–F10 pendentes.
- Registrada diferença preexistente: visual anteriormente descrito no plano ausente na entrada atual; uma página sem arquivos de visual encontrados. Nenhum visual removido ou recriado nesta fase.

Impacto: somente documentação, evidências e cópias de segurança. Fontes PBIP/PBIR/TMDL/JSON, planilha e configurações locais preservadas. Nenhuma medida, relação, consulta ou página alterada.

Validações e limites: ver [validacoes.md](validacoes.md). Não se executaram auditoria da Fase 1, consultas de dados, DAX, homologação financeira ou inspeção visual no Desktop.

## 02/11/2026 — Fase 1: auditoria estática e registro de bloqueios

Responsável: Codex. Criado docs/auditoria-modelo-semantico.md, com inventário de 56 colunas de negócio, 18 relacionamentos, diagrama textual, riscos, recomendações, checklist de aceite e ações para desbloquear. Criados script/evidências em docs/evidencias/fase1-auditar.py e docs/evidencias/fase1/; roteiros SQL/DAX somente leitura preparados, não executados.

PLANS.md atualizado: F0 continua concluída; F1 Bloqueada para aceite por falta de testes de dados/mecanismo e contratos DRE/conta; F2–F10 não iniciadas. Arquitetura e validações receberam adendos, preservando o histórico da F0.

Fontes PBIP/PBIR/TMDL/JSON, consultas M, conexões, credenciais e configurações locais preservadas. Nenhuma melhoria de organização, alteração de relacionamento, nova medida ou mudança visual foi implementada. Valores da linha 13 não foram revalidados por consulta.

## 02/11/2026 — Continuação da Fase 1: completar execução dinâmica

Reutilizados os roteiros existentes; criados docs/execucao-testes-fase1.md, docs/evidencias/fase1-completar-testes.py e complemento em docs/evidencias/fase1-dinamica/. Produzidos vinte arquivos DAX, SQL complementar, fallback DMV, registro de testes e verificações locais. Atualizados auditoria-modelo-semantico.md, PLANS.md e validacoes.md.

Recomendada abordagem 1 para os visuais DRE, sem implementação. Descoberta de recursos confirmou ausência de modelo carregado/sessão autenticada disponível: zero testes SQL/DAX executados contra dados. Fase 1 continua Bloqueada; Fase 2 não liberada. Nenhuma alteração em AGENTS.md, consultas, conexões, credenciais, relações, medidas ou páginas de produção.

## 02/11/2026 — Testes dinâmicos reais no Power BI aberto

Após o usuário abrir o projeto, criada conexão ADOMD local somente leitura e executadas 23 consultas DAX/INFO. Identidade conferida pelo catálogo/tabelas esperadas. Saídas em quatro diretórios docs/evidencias/fase1-execucao-20261102-*; scripts de execução/consolidação preservados. Acrescentadas três consultas de auditoria (contrato DRE, partições e mês/filiais múltiplas), sem medidas ou objetos de produção.

Testes locais aprovados: integridade/chaves, propriedades efetivas das relações, 80 casos filial/período, quatro casos ano/mês/filiais múltiplas e 36 comparações de interseção nas fatos. Controles da linha 13 coincidiram a centavos; BLANK após maio/2023 preservado. Conta e dim_dre não filtram automaticamente a view; relação Filial–Conta permaneceu inativa.

Atualizados auditoria-modelo-semantico.md, PLANS.md, execucao-testes-fase1.md e validacoes.md com os resultados medidos. Comparação independente com Databricks SQL e aceite da estratégia/limites continuam pendentes; Fase 1 ainda sem aceite global, Fase 2 não iniciada. Nenhum arquivo de produção foi alterado pelo executor, comprovado pelos hashes das quatro rodadas.

## 02/11/2026 — Aceite técnico da Fase 1

Lidos integralmente AGENTS.md, PLANS.md, auditoria-modelo-semantico.md e execucao-testes-fase1.md. Conferida compatibilidade das evidências DAX existentes com os resultados da conciliação SQL informados pelo usuário: 16 linhas, controles da linha 13 coincidentes, diferenças consolidadas de R$ 0,00 e totais por filial coincidentes. Proveniência da confirmação SQL e da aprovação da abordagem DRE registrada em docs/evidencias/fase1-aceite-tecnico/aceite.json; nenhuma execução SQL atribuída ao agente nesta tarefa.

PLANS.md e auditoria atualizados: Fase 1 concluída com aceite técnico; Fase 2 liberada e ainda não iniciada. Guia de execução e validações sincronizados, mantendo os logs anteriores como histórico. Registrados estratégia inicial aprovada, pré-requisitos de F2 e pendências de homologação contábil de Resultado Líquido, EBITDA e EBIT.

Somente documentação e registro de aceite alterados. AGENTS.md, modelo semântico, consultas, conexões, credenciais, relacionamentos, medidas e páginas preservados; nenhuma implementação de F2 executada.

## 02/11/2026 — Fase 2 / Lote 2.1

Depois de o usuário fechar o Desktop, criado backup atualizado/verificável com 176 arquivos e restauração isolada conferida por hash. Estado do Git: sem repositório, nenhuma inicialização ou commit. Diferenças preexistentes de PLANS.md e dois localSettings.json preservadas.

Criados contratos em docs/contratos-medidas-dax.md antes das seis medidas. Adicionada tabela calculada local _Medidas.tmdl, com coluna auxiliar oculta e seis medidas fundamentais; model.tmdl recebeu somente sua referência. Não foram modificadas consultas M, conexões, credenciais, relações, tabelas anteriores ou páginas. AGENTS.md preservado.

Bases respeitam posição única e retornam BLANK em múltiplas posições/indicadores EBIT pendentes. As três específicas de Resultado Líquido usam interseção com ordem_dre = 13 e metadados de provisoriedade. Nenhuma medida de margem, desvio, YTD ou outro lote criada.

Parser TMDL instalado leu a definição completa sem erro: 15 tabelas, 18 relações e seis medidas; verificadas preservação de fontes/IDs e integridade. Criadas nove consultas em docs/testes/lote2-1/ e relatório docs/validacao-lote2-1.md. PLANS.md atualizado para F2 em andamento apenas neste lote, aguardando validação dinâmica. Lote 2.1 não concluído e Lote 2.2 não iniciado.


## Encerramento do Lote 2.1 — 02/11/2026

Lote concluído tecnicamente: 11 consultas DAX/INFO em leitura, zero erros, 20 casos filial/período e 60 verificações de cenário aprovadas. _Medidas materializada com uma linha e partição Ready, sem erro. Controles integrais coincidentes a centavos; BLANK, totais e EBITDA/EBIT conferidos. Cartão R$ 5,04M confirmado pelo usuário. Evidências em docs/evidencias/lote2-1-encerramento-20261102-162739 e relatório docs/validacao-lote2-1.md. Nenhuma alteração de produção nesta rodada. Lote 2.2 planejado em docs/plano-lote2-2.md e não iniciado. Homologações contábeis permanecem pendentes.


## Lote 2.2 — 02/11/2026

Implementadas 30 medidas de posições autorizadas na tabela _Medidas, preservando as seis existentes. Backup lote2-2-20261102-163559, 237 arquivos restaurados e hashes verificados. Parser TMDL aprovado: 36 medidas, 15 tabelas, 18 relações e oito partições M. Único arquivo de produção alterado: _Medidas.tmdl. Contratos e dez consultas DAX/uma SQL documentados. DAX/SQL não executados; lote não concluído até evidência dinâmica e conciliação independente. Ver docs/validacao-lote2-2.md. Lote 2.3 não iniciado; pendências contábeis mantidas.
