# Lote 2.2 — Receitas, Custos e Resultados Gerenciais

Estado em 02/11/2026: **implementação estática aprovada; validação dinâmica e SQL pendentes**. O planejamento original abaixo é preservado como histórico; acompanhamento atual em PLANS.md e docs/validacao-lote2-2.md. Lote 2.1 concluído tecnicamente; Fase 2 permanece em andamento. Este documento não implementa medidas nem autoriza alterações estruturais.

## Escopo proposto

Criar medidas monetárias específicas nos três cenários, reutilizando as bases validadas e a interseção de posição da própria view. Mapear cada nome e contrato antes de escrever DAX. Posições observadas na consulta 04 do encerramento do Lote 2.1:

| Posição | Indicador candidato |
| --- | --- |
| 1 | Receita operacional bruta |
| 2 | Deduções da receita bruta |
| 3 | Receita operacional líquida |
| 4 | Custos das mercadorias e serviços |
| 5 | Margem de contribuição em valor monetário |
| 6 | Despesas operacionais |
| 7 | Resultado financeiro |
| 9 | Depreciação e amortização |
| 10 | Outras receitas e despesas |
| 12 | Provisão para IR e CSLL |

Proposta máxima: dez indicadores × três cenários = 30 novas medidas; confirmar o escopo e os nomes no início do lote. A existência das posições comprova o mapeamento técnico, não homologa sua composição contábil. Reutilizar as três medidas existentes da posição 13, sem duplicá-las. Posições 8 (EBITDA) e 11 (EBIT) permanecem sem cálculo. Resultado Líquido permanece provisório.

Não incluir neste lote percentuais, desvios, favorabilidade, YTD, análise vertical/horizontal, rankings ou detalhamento por conta. Esses recursos exigem contratos e testes próprios. Não reconstruir subtotais somando outras posições.

## Sequência e pré-requisitos

- [ ] L2.2-P01: receber instrução para iniciar; ler AGENTS.md, PLANS.md, contratos e aceite do Lote 2.1; confirmar escopo final de indicadores.
- [ ] L2.2-P02: salvar trabalho e fechar Desktop antes de editar; conferir processos, diferenças de entrada e Git; preservar mudanças feitas pelo usuário, inclusive no cartão.
- [ ] L2.2-P03: preparar novo backup restaurável com manifesto e conferir hashes; não reutilizar o snapshot anterior como se contivesse o estado atual.
- [ ] L2.2-C01: confirmar rótulo/posição por filial e competência; definir nome, sinal ajustado, filtros, unidade, pasta, formato, BLANK, total e conflito de posição para cada medida. Documentar pendências contábeis específicas.
- [ ] L2.2-I01: somente após os preparativos, implementar em etapas em `_Medidas.tmdl`, reutilizando as bases; preservar tabelas, partições, relações, conexões e páginas. Não usar dim_dre ou dim_conta como se filtrassem a view.
- [ ] L2.2-V01: executar parser TMDL, conferir referências, IDs e integridade; reabrir e verificar materialização/estado das medidas no mecanismo.
- [ ] L2.2-V02: comparar cada indicador/cenário com a posição correspondente da view e, para aceite financeiro do lote, com consulta SQL independente no mesmo estado dos dados. Registrar esperado, obtido, diferença e ausência.
- [ ] L2.2-V03: testar filiais 01/02/03, consolidado, seleção múltipla, 2021/2022, Jan–Mai/2023, Jun–Dez/2023, mês individual, posição conflitante, contexto vazio e total de matriz. Preservar BLANK e zero legítimo; não fabricar dados para obter zero.
- [ ] L2.2-A01: registrar evidências e limitações; concluir somente com todos os critérios comprovados e sem regressão das seis medidas do Lote 2.1.

## Critérios de aceite e impactos

Cada medida deve selecionar exclusivamente sua posição por interseção, respeitar Filial/Calendário, conservar sinal e ausência, retornar BLANK para posição conflitante e somar somente eixos aditivos. Comparar valores arredondados a centavos; tolerância máxima R$ 0,01, investigando qualquer diferença. Testar identidades de receitas/custos apenas como conciliação das posições, sem homologar EBITDA/EBIT ou inventar fórmulas.

Comparações de desempenho, quando desenvolvidas em lote posterior, usarão competências equivalentes; os controles integrais atuais abrangem disponibilidades diferentes. Conta continua restrita às fatos para detalhamento, mediante contrato de sinal conciliado.

Arquivos previstos para a futura execução: `_Medidas.tmdl`, `docs/contratos-medidas-dax.md`, futuro relatório de validação do lote, testes/evidências, PLANS.md e histórico documental. Nenhuma mudança de PBIR, relações ou consultas é necessária ao escopo proposto. Se surgir necessidade estrutural, documentar impacto e obter aprovação específica antes de implementá-la.

Riscos principais: posição incorreta, duplicação de subtotal, inversão de sinal, conflito de contexto, ausência convertida em zero e comparação temporal desigual. A matriz de testes e os contratos são as condições para controlar esses riscos. Na elaboração original nenhuma implementação havia sido iniciada. A implementação posterior está registrada no adendo e no relatório de validação; não equivale ao aceite definitivo.


## Confronto com a solicitação de execução — 02/11/2026

Escopo confirmado: as dez posições propostas foram autorizadas, com três cenários e 30 medidas. Sem divergência funcional. Nomes adotam os indicadores da solicitação, com prefixo DRE e sufixo Realizado/Orçado/Previsto, registrados individualmente nos contratos antes da escrita TMDL. A instrução para iniciar foi recebida. Plano anterior preservado como histórico; estado atual e checklist de execução em PLANS.md e docs/validacao-lote2-2.md.
