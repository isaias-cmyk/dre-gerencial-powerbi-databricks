# PLANS.md — DRE Moderno

## Projeto
Diretorio: C:\Claude\Power BI
Arquivo: DRE Moderno - Databricks2.pbip

## Objetivo
Desenvolver uma DRE corporativa em Power BI, integrada ao
Databricks, com Realizado, Orcado e Previsto.

## Estado inicial — 03/11/2026

- 16 tabelas no modelo semantico.
- 41 medidas DAX (45 apos o L2.3.2; 50 apos o L2.3.3; 52 na Fase 4; 61 apos o Lote 4.1).
- 18 relacionamentos.
- 1 pagina no relatorio.
- 1 visual existente.
- Modelo armazenado em TMDL.
- MCP Databricks operacional e somente leitura.
- MCP Power BI disponivel para desenvolvimento.

## Fase 1 — Preparacao do ambiente (concluida em 03/11/2026)

- [x] Criar CLAUDE.md.
- [x] Criar AGENTS.md.
- [x] Criar backup inicial.
  - Backup fisico: C:\Claude\Backup_DRE_20261103_205156
- [x] Inicializar Git e registrar baseline.
  - Commit inicial: 512c4cc "Baseline DRE Moderno - 41 medidas e 18 relacionamentos" (branch master, 03/11/2026).
- [x] Validar abertura do PBIP no Desktop.
  - DRE Moderno - Databricks2.pbip aberto no Power BI Desktop sem erros (03/11/2026).
- [x] Confirmar conexao com MCP Power BI.
  - MCP powerbi-modeling conectado ao modelo DRE Moderno - Databricks2 (Power BI Desktop, localhost:63404) em 03/11/2026.
  - Inventario validado ao vivo: 16 tabelas, 41 medidas, 18 relacionamentos (17 ativos, 1 inativo); igual ao baseline.
  - Consulta DAX somente leitura executada com sucesso (vw_dre_comparativo 1.404 linhas; dim_calendario 1.095 linhas).

Status da Fase 1: concluida.

## Fase 2 — Auditoria e conciliacao

- [x] Inventariar medidas e contratos financeiros (docs/contratos-medidas-dax.md; 50 medidas).
- [x] Comparar Realizado, Orcado e Previsto entre SQL e DAX (Lotes 2.2, 2.3.1, 2.3.2, 2.3.3).
- [x] Validar filtros por filial e periodo (5 grupos de filiais x 45 recortes agregados/mensais).
- [x] Preservar NULL e BLANK (NULL/BLANK coincidentes em todas as conciliacoes).
- [x] Registrar divergencias com tolerancia de R$ 0,01 (nenhuma divergencia; maximo R$ 0,00000015).

### Lote 2.3 — Desvios financeiros (detalhes em docs/plano-lote2-3.md)

- [x] L2.3.1 — Comparaveis M37/M38/M39/M49/M50 e _ConfigCobertura. Aceite tecnico: 1.755 casos SQL x DAX, dif. max. R$ 0,00000010.
- [x] L2.3.2 — Desvios M40–M43 (pasta DRE\Desvios). Aceite tecnico do usuario em 04/11/2026.
  - Q01 2.340/2.340 e Q02 9.360/9.360 SQL x DAX; 41 medidas anteriores sem regressao.
  - Registro: docs/validacao-lote2-3-2.md; evidencias em docs/evidencias/lote2-3-2-execucao-20261103/.
- [x] L2.3.3 — Impacto, classificacao e cumprimento (M44–M48, pasta DRE\Desempenho). Aceite tecnico do usuario em 04/11/2026 (R02: 45/45 antigas identicas).
  - Decisoes: impacto no lucro em todas as linhas com valor; RL com "(provisorio)"; neutro ate R$ 0,01; cumprimento so posicoes 1/3.
  - 14.625/14.625 SQL x DAX; 31/31 sinteticos; 45 medidas anteriores sem regressao. Registro: docs/validacao-lote2-3-3.md.

- Commit Git 0a9fd51 (04/11/2026): L2.3.2 + L2.3.3; backups/ fora do Git (.gitignore).

Aceites do Lote 2.3 sao tecnicos/didaticos (base ficticia, cobertura DIDATICA-1.0-20261103); nao homologam fechamento, EBITDA, EBIT ou Resultado Liquido.

Status da Fase 2: concluida em 04/11/2026 (aceites tecnicos/didaticos).

## Fase 3 — Evolucao da modelagem (concluida em 05/11/2026)

- [x] Revisar relacionamentos e propagacao de filtros (docs/diagnostico-fase3.md; filtros pela view ocultados).
- [x] Avaliar dimensoes e tabelas auxiliares (data automatica removida; dim_calendario tabela de datas; tabelas sem uso ocultas).
- [x] Revisar desempenho das medidas (Lote 3.2 em 05/11/2026: M37-M39, M41, M43 otimizadas; -25% matriz pesada, -55% matriz DRE x mes; 53.300/53.300 e 6.279/6.279 SQL; docs/validacao-lote3-2.md).
- [x] Corrigir problemas comprovados, com testes de regressao (Lote 3.1 em 05/11/2026: 53.300/53.300 celulas identicas).

## Fase 4 — Desenvolvimento visual (concluida em 09/11/2026)

- [x] Pagina Executiva (05/11/2026; cartoes Receita/Margem/RL, linha mensal, cascata do desvio do RL; docs/fase4-pagina-executiva.md).
- [x] Pagina DRE (05/11/2026; matriz comparavel com desvios e classificacao colorida; docs/fase4-pagina-dre.md).
- [x] Pagina Filiais (08/11/2026; matriz filial x Receita/Margem/RL com Total consolidado; desvio da Receita e impacto no RL por filial; docs/fase4-pagina-filiais.md).
- [x] Lote 4.1 — base por conta contabil (09/11/2026; colunas linha_dre/grupo_conta/conta em dim_conta e 9 medidas na pasta Contas; T1 480/480, T2 Databricks 9/9 conjuntos, R1 53.300/53.300; docs/validacao-lote4-1.md).
- [x] Pagina Receitas (09/11/2026; linhas 1 e 2; matriz linha -> grupo -> conta e desvio x Orcado por conta; total = Receita Liquida; docs/fase4-paginas-receitas-despesas.md).
- [x] Pagina Despesas (09/11/2026; linhas 4, 6, 7, 9, 10 e 12; Receitas - Despesas = Resultado Liquido 5.038.227,39).

## Fase 5 — Homologacao (tecnica concluida em 09/11/2026)

- [x] Executar testes DAX e SQL (H1-H4: inventario 61 medidas; indicadores base 9/9 conjuntos e 1.188/1.188; Comparaveis/desvios/desempenho 1.260/1.260 contra SQL independente; regressao 53.300/53.300; contas 9/9).
- [x] Validar indicadores financeiros (Receita Liquida 146.417.811,17; Margem 52.828.995,11; Resultado Liquido 5.038.227,39, todos conferidos com o Databricks).
- [x] Revisar layout e navegacao (H5) e corrigir P1-P5: texto alternativo em 54 visuais, segmentacoes Filial/Ano/Mes sincronizadas, subtitulos automaticos desligados, medidas de cor ocultas, navegador de paginas (backup backups/fase5-correcoes-pre-20261109-1740).
- [x] Documentar resultados e pendencias (docs/homologacao-fase5.md).
- [ ] Aceite de negocio: EBITDA/EBIT em homologacao; Resultado Liquido provisorio; base didatica DIDATICA-1.0.

## Regras obrigatorias

- Databricks exclusivamente para leitura.
- Alteracoes Power BI permitidas conforme CLAUDE.md e AGENTS.md.
- Backup restauravel antes de mudancas estruturais.
- Nao alterar regras financeiras homologadas sem autorizacao.
- Nao excluir objetos sem autorizacao.
- Nao publicar nem executar refresh completo sem autorizacao.
- Preservar BLANK e NULL.
- Registrar alteracoes e resultados dos testes.
