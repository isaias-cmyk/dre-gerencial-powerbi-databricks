# Contratos de medidas DAX — Fase 2 / Lote 2.1

Estado atual de L2.3.1: políticas A–D recebidas; investigação somente leitura autorizada posteriormente pelo usuário. As cinco novas medidas permanecem não implementadas por falta de contrato de cobertura/fechamento confiável. Contratos condicionais e decisões aprovadas estão no adendo ao final; os contratos anteriores permanecem preservados.

Estado: contratos definidos antes da implementação; seis medidas implementadas em TMDL e estrutura lida pelo parser instalado. Lote restrito às seis medidas abaixo; aceite técnico concluído em 02/11/2026, com 11 consultas no modelo carregado e materialização Ready comprovada; evidências no relatório do lote. Fase 1 concluída tecnicamente; Resultado Líquido, EBITDA e EBIT continuam pendentes de homologação contábil. Ver [validação do lote](validacao-lote2-1.md).

## Armazenamento e limites comuns

Tabela lógica `_Medidas`, sem relacionamentos. Uma partição calculada local de uma linha, criada com DATATABLE, sustenta uma coluna `_Organizacao` oculta. Não consulta Databricks nem cria fonte externa. O formato TMDL existente foi lido pelo TmdlSerializer instalado antes desta decisão; a definição final será novamente analisada por esse parser. A coluna auxiliar não participa das medidas nem dos visuais financeiros.

Os nomes das seis medidas solicitadas serão preservados. As três de Resultado Líquido terão descrição explícita de provisoriedade e pasta `DRE\Resultado Líquido (provisório)`. Não criar margens, desvios, YTD, análise vertical/horizontal, EBITDA ou EBIT neste lote.

Valores vêm exclusivamente de `workspace.gold.vw_dre_comparativo`, importada na tabela homônima. Usar o valor ajustado, sem reaplicar tipolancamento, ABS ou inversão de sinal. Não transformar ausência em zero. A precisão double original é preservada; arredondamento a centavos é para apresentação/conciliação, não alteração dos valores na origem.

Formato monetário numérico: `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`, duas casas, negativos entre parênteses, zero real visível. BLANK permanece BLANK. Separadores seguem a cultura de exibição do Power BI; não alterar culture en-US/sourceQueryCulture pt-BR neste lote. A exibição pt-BR deverá ser conferida no Desktop. Não usar FORMAT para converter as medidas numéricas em texto.

### Contexto de uma posição e proteção contábil

Uma posição válida exige exatamente um valor visível de `vw_dre_comparativo[ordem_dre]` e uma descrição não vazia. As medidas base retornam a soma da coluna de cenário somente nessa posição, respeitando filial, calendário e demais filtros que realmente alcançam a view.

Zero ou múltiplas posições: BLANK. Total de matriz que reúna várias posições: BLANK. Subtotal entre filiais/competências da mesma posição: valor dessa posição somado nesses eixos. Se um filtro externo restringir o total geral a uma única posição, ele pode retornar esse valor; o contrato é pela cardinalidade do contexto, não pela aparência de uma linha de total.

Sem códigos de posição de EBITDA/EBIT comprovados nos arquivos de definição, não inventar seus números. Acrescentar proteção por descrição: qualquer posição cujo rótulo contenha `EBIT` (inclui EBITDA, sem distinção entre maiúsculas/minúsculas) retorna BLANK nas três medidas base, ainda que a view contenha valor. Isso é supressão de indicador pendente, não cálculo contábil. A consulta de validação deve listar as 13 descrições reais e confirmar que as posições de EBITDA/EBIT estão cobertas. Descrição ausente/inconsistente também resulta em BLANK e exige investigação; não habilitar outra convenção de rótulo sem atualizar o contrato.

`dim_filial` e `dim_calendario` propagam seus filtros pelos relacionamentos existentes. `dim_conta` e `dim_dre` não filtram automaticamente a view, conforme Fase 1. Usar ordem/descrição da própria view nos eixos gerenciais. Não implementar filtro virtual para essas dimensões nem misturar as fatos analíticas neste lote.

### Resultado Líquido provisório e filtros conflitantes

As medidas de Resultado Líquido aplicam `KEEPFILTERS(ordem_dre = 13)` sobre a medida base correspondente. Retornam exclusivamente a posição 13, sem reconstruir sua composição contábil.

- Sem filtro de posição: retorno da linha 13 no cenário, filial e calendário atuais.
- Seleção que inclui 13: interseção com 13, sem somar outras posições.
- Posição diferente de 13 ou descrição incompatível: BLANK; não substituir o contexto e não repetir o Resultado Líquido em todas as linhas de uma matriz.
- Total entre filiais/competências: soma somente da linha 13.
- Ausência de realizado após maio/2023: BLANK.

Os nomes solicitados permanecem `DRE | Resultado Líquido ...`; descrição e pasta identificam **provisório — homologação contábil pendente**. A conciliação técnica da linha 13 não homologa o conceito contábil de Resultado Líquido. Em visuais futuros, usar rótulo/título que explicite provisoriedade.

## M01 — DRE | Realizado

- **Finalidade:** valor realizado de uma posição gerencial válida no contexto atual.
- **Tabela de armazenamento:** `_Medidas`; pasta `DRE\Bases`.
- **Fonte:** `vw_dre_comparativo`, origem workspace.gold.
- **Coluna de valor:** `realizado`.
- **Posição DRE:** posição única do contexto; descrição não vazia e sem EBIT/EBITDA.
- **Regra de sinal:** conservar o valor ajustado; não reaplicar natureza.
- **Filtros respeitados:** Filial/Calendário e filtros efetivos da view; Conta/DRE dimensional sem propagação automática.
- **Totais:** BLANK com múltiplas posições; agregação permitida entre filiais/competências da mesma posição.
- **BLANK:** preservado, inclusive ausência após maio/2023 e contexto vazio/ambíguo.
- **Formatação:** monetária numérica BRL com duas casas, conforme contrato comum.
- **Dependências:** ordem_dre, descricao_dre e realizado da view; relacionamentos existentes com Filial/Calendário.
- **Validação:** na posição 13 consolidada, R$ 5.038.227,39; recortes conforme evidências F1; BLANK nos contextos múltiplos e nos indicadores pendentes.

## M02 — DRE | Orçado

- **Finalidade:** valor orçado de uma posição gerencial válida no contexto atual.
- **Tabela de armazenamento:** `_Medidas`; pasta `DRE\Bases`.
- **Fonte:** `vw_dre_comparativo`, origem workspace.gold.
- **Coluna de valor:** `orcado`.
- **Posição DRE:** posição única do contexto; descrição não vazia e sem EBIT/EBITDA.
- **Regra de sinal:** conservar o valor ajustado, sem multiplicação por tipolancamento.
- **Filtros respeitados:** Filial/Calendário e filtros efetivos da view; Conta/DRE dimensional sem propagação automática.
- **Totais:** BLANK entre posições; somar somente eixos aditivos da mesma posição.
- **BLANK:** preservar ausência; zero orçado real permanece zero.
- **Formatação:** monetária numérica BRL com duas casas, conforme contrato comum.
- **Dependências:** ordem_dre, descricao_dre e orcado da view; relações existentes.
- **Validação:** na posição 13 consolidada, R$ 6.622.493,82; recortes F1 e proteção dos totais/indicadores pendentes.

## M03 — DRE | Previsto

- **Finalidade:** valor previsto de uma posição gerencial válida no contexto atual.
- **Tabela de armazenamento:** `_Medidas`; pasta `DRE\Bases`.
- **Fonte:** `vw_dre_comparativo`, origem workspace.gold.
- **Coluna de valor:** `previsto`.
- **Posição DRE:** posição única do contexto; descrição não vazia e sem EBIT/EBITDA.
- **Regra de sinal:** conservar o valor ajustado, sem reaplicar natureza.
- **Filtros respeitados:** Filial/Calendário e filtros efetivos da view; Conta/DRE dimensional sem propagação automática.
- **Totais:** BLANK entre posições; somar somente eixos aditivos da mesma posição.
- **BLANK:** preservar ausência; zero previsto real permanece zero.
- **Formatação:** monetária numérica BRL com duas casas, conforme contrato comum.
- **Dependências:** ordem_dre, descricao_dre e previsto da view; relações existentes.
- **Validação:** na posição 13 consolidada, R$ 6.157.931,19; recortes F1 e proteção dos totais/indicadores pendentes.

## M04 — DRE | Resultado Líquido Realizado

- **Finalidade:** referência provisória ao realizado da posição 13, sem homologação contábil.
- **Tabela de armazenamento:** `_Medidas`; pasta `DRE\Resultado Líquido (provisório)`.
- **Fonte:** `vw_dre_comparativo`, através de M01.
- **Coluna de valor:** `realizado`, herdada de M01.
- **Posição DRE:** exclusivamente ordem_dre = 13, por interseção KEEPFILTERS.
- **Regra de sinal:** herdada de M01, sem novo ajuste.
- **Filtros respeitados:** filial, calendário e demais filtros efetivos da view; posição/descrição incompatível retorna BLANK.
- **Totais:** somente linha 13; não totalizar a DRE inteira.
- **BLANK:** preservar ausência e conflito de posição; não converter realizado ausente em zero.
- **Formatação:** monetária numérica BRL com duas casas, conforme contrato comum.
- **Dependências:** M01 e filtro de posição 13.
- **Validação:** consolidado R$ 5.038.227,39 sem filtro de posição; recortes por filial/período iguais aos da linha 13; BLANK junho–dezembro/2023 e posição conflitante; provisoriedade nos metadados.

## M05 — DRE | Resultado Líquido Orçado

- **Finalidade:** referência provisória ao orçado da posição 13, sem homologação contábil.
- **Tabela de armazenamento:** `_Medidas`; pasta `DRE\Resultado Líquido (provisório)`.
- **Fonte:** `vw_dre_comparativo`, através de M02.
- **Coluna de valor:** `orcado`, herdada de M02.
- **Posição DRE:** exclusivamente ordem_dre = 13, por interseção KEEPFILTERS.
- **Regra de sinal:** herdada de M02, sem novo ajuste.
- **Filtros respeitados:** filial, calendário e filtros efetivos da view; posição/descrição incompatível retorna BLANK.
- **Totais:** somar somente a linha 13 nos eixos aditivos.
- **BLANK:** preservar ausência e conflito de posição; zero legítimo permanece zero.
- **Formatação:** monetária numérica BRL com duas casas, conforme contrato comum.
- **Dependências:** M02 e filtro de posição 13.
- **Validação:** consolidado R$ 6.622.493,82 sem filtro de posição; recortes F1 e conflito de posição; provisoriedade nos metadados.

## M06 — DRE | Resultado Líquido Previsto

- **Finalidade:** referência provisória ao previsto da posição 13, sem homologação contábil.
- **Tabela de armazenamento:** `_Medidas`; pasta `DRE\Resultado Líquido (provisório)`.
- **Fonte:** `vw_dre_comparativo`, através de M03.
- **Coluna de valor:** `previsto`, herdada de M03.
- **Posição DRE:** exclusivamente ordem_dre = 13, por interseção KEEPFILTERS.
- **Regra de sinal:** herdada de M03, sem novo ajuste.
- **Filtros respeitados:** filial, calendário e filtros efetivos da view; posição/descrição incompatível retorna BLANK.
- **Totais:** somar somente a linha 13 nos eixos aditivos.
- **BLANK:** preservar ausência e conflito de posição; zero legítimo permanece zero.
- **Formatação:** monetária numérica BRL com duas casas, conforme contrato comum.
- **Dependências:** M03 e filtro de posição 13.
- **Validação:** consolidado R$ 6.157.931,19 sem filtro de posição; recortes F1 e conflito de posição; provisoriedade nos metadados.

## Critério de aceite do lote

Exigir parser TMDL e integridade aprovados, exatamente seis medidas sem duplicação, referências/fontes/relações preservadas e execução das consultas das medidas no modelo reaberto. Comparar centavos com os controles; registrar também igualdade de BLANK/valor, pois BLANK não é zero. Conferir as 13 descrições e a supressão de EBITDA/EBIT. Testes de F1 ou expressões avaliadas sem as medidas persistidas não substituem esse aceite.

Sem execução dinâmica das medidas novas, registrar **implementado estaticamente, pendente de validação no Desktop**. Não concluir o lote nem avançar a 2.2.

## Referências oficiais utilizadas

- [TMDL e estrutura TOM](https://learn.microsoft.com/en-us/analysis-services/tmdl/tmdl-overview).
- [TmdlSerializer e leitura de pasta](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.tmdlserializer).
- [HASONEVALUE](https://learn.microsoft.com/en-us/dax/hasonevalue-function-dax): exige uma posição visível no contexto.
- [KEEPFILTERS](https://learn.microsoft.com/en-us/dax/keepfilters-function-dax): preserva a interseção com a posição 13.
- [DATATABLE](https://learn.microsoft.com/en-us/dax/datatable-function-dax): tabela auxiliar local, sem nova origem.


# Lote 2.2 — contratos autorizados antes da implementação

Estado: escopo de 30 novas medidas confirmado pela solicitação do usuário. Compatível com docs/plano-lote2-2.md, sem divergência funcional. Nomes normalizados conforme a lista autorizada; Margem de Contribuição é monetária, sem percentual. Lote 2.1 e seus contratos permanecem preservados.

## DRE | Receita Operacional Bruta Realizado

- **Posição:** ordem_dre = 1; indicador Receita Operacional Bruta.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[realizado], via [DRE | Realizado]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `DRE\Receita Operacional Bruta`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição 1 da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.

## DRE | Receita Operacional Bruta Orçado

- **Posição:** ordem_dre = 1; indicador Receita Operacional Bruta.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[orcado], via [DRE | Orçado]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `DRE\Receita Operacional Bruta`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição 1 da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.

## DRE | Receita Operacional Bruta Previsto

- **Posição:** ordem_dre = 1; indicador Receita Operacional Bruta.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[previsto], via [DRE | Previsto]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `DRE\Receita Operacional Bruta`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição 1 da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.

## DRE | Deduções da Receita Realizado

- **Posição:** ordem_dre = 2; indicador Deduções da Receita.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[realizado], via [DRE | Realizado]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `DRE\Deduções da Receita`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição 2 da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.

## DRE | Deduções da Receita Orçado

- **Posição:** ordem_dre = 2; indicador Deduções da Receita.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[orcado], via [DRE | Orçado]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `DRE\Deduções da Receita`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição 2 da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.

## DRE | Deduções da Receita Previsto

- **Posição:** ordem_dre = 2; indicador Deduções da Receita.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[previsto], via [DRE | Previsto]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `DRE\Deduções da Receita`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição 2 da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.

## DRE | Receita Operacional Líquida Realizado

- **Posição:** ordem_dre = 3; indicador Receita Operacional Líquida.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[realizado], via [DRE | Realizado]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `DRE\Receita Operacional Líquida`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição 3 da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.

## DRE | Receita Operacional Líquida Orçado

- **Posição:** ordem_dre = 3; indicador Receita Operacional Líquida.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[orcado], via [DRE | Orçado]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `DRE\Receita Operacional Líquida`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição 3 da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.

## DRE | Receita Operacional Líquida Previsto

- **Posição:** ordem_dre = 3; indicador Receita Operacional Líquida.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[previsto], via [DRE | Previsto]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `DRE\Receita Operacional Líquida`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição 3 da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.

## DRE | Custos Realizado

- **Posição:** ordem_dre = 4; indicador Custos.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[realizado], via [DRE | Realizado]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `DRE\Custos`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição 4 da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.

## DRE | Custos Orçado

- **Posição:** ordem_dre = 4; indicador Custos.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[orcado], via [DRE | Orçado]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `DRE\Custos`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição 4 da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.

## DRE | Custos Previsto

- **Posição:** ordem_dre = 4; indicador Custos.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[previsto], via [DRE | Previsto]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `DRE\Custos`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição 4 da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.

## DRE | Margem de Contribuição Realizado

- **Posição:** ordem_dre = 5; indicador Margem de Contribuição.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[realizado], via [DRE | Realizado]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `DRE\Margem de Contribuição`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição 5 da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.

## DRE | Margem de Contribuição Orçado

- **Posição:** ordem_dre = 5; indicador Margem de Contribuição.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[orcado], via [DRE | Orçado]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `DRE\Margem de Contribuição`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição 5 da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.

## DRE | Margem de Contribuição Previsto

- **Posição:** ordem_dre = 5; indicador Margem de Contribuição.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[previsto], via [DRE | Previsto]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `DRE\Margem de Contribuição`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição 5 da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.

## DRE | Despesas Operacionais Realizado

- **Posição:** ordem_dre = 6; indicador Despesas Operacionais.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[realizado], via [DRE | Realizado]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `DRE\Despesas Operacionais`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição 6 da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.

## DRE | Despesas Operacionais Orçado

- **Posição:** ordem_dre = 6; indicador Despesas Operacionais.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[orcado], via [DRE | Orçado]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `DRE\Despesas Operacionais`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição 6 da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.

## DRE | Despesas Operacionais Previsto

- **Posição:** ordem_dre = 6; indicador Despesas Operacionais.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[previsto], via [DRE | Previsto]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `DRE\Despesas Operacionais`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição 6 da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.

## DRE | Resultado Financeiro Realizado

- **Posição:** ordem_dre = 7; indicador Resultado Financeiro.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[realizado], via [DRE | Realizado]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `DRE\Resultado Financeiro`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição 7 da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.

## DRE | Resultado Financeiro Orçado

- **Posição:** ordem_dre = 7; indicador Resultado Financeiro.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[orcado], via [DRE | Orçado]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `DRE\Resultado Financeiro`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição 7 da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.

## DRE | Resultado Financeiro Previsto

- **Posição:** ordem_dre = 7; indicador Resultado Financeiro.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[previsto], via [DRE | Previsto]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `DRE\Resultado Financeiro`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição 7 da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.

## DRE | Depreciação e Amortização Realizado

- **Posição:** ordem_dre = 9; indicador Depreciação e Amortização.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[realizado], via [DRE | Realizado]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `DRE\Depreciação e Amortização`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição 9 da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.

## DRE | Depreciação e Amortização Orçado

- **Posição:** ordem_dre = 9; indicador Depreciação e Amortização.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[orcado], via [DRE | Orçado]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `DRE\Depreciação e Amortização`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição 9 da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.

## DRE | Depreciação e Amortização Previsto

- **Posição:** ordem_dre = 9; indicador Depreciação e Amortização.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[previsto], via [DRE | Previsto]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `DRE\Depreciação e Amortização`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição 9 da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.

## DRE | Outras Receitas e Despesas Realizado

- **Posição:** ordem_dre = 10; indicador Outras Receitas e Despesas.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[realizado], via [DRE | Realizado]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `DRE\Outras Receitas e Despesas`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição 10 da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.

## DRE | Outras Receitas e Despesas Orçado

- **Posição:** ordem_dre = 10; indicador Outras Receitas e Despesas.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[orcado], via [DRE | Orçado]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `DRE\Outras Receitas e Despesas`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição 10 da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.

## DRE | Outras Receitas e Despesas Previsto

- **Posição:** ordem_dre = 10; indicador Outras Receitas e Despesas.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[previsto], via [DRE | Previsto]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `DRE\Outras Receitas e Despesas`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição 10 da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.

## DRE | Provisão para IR e CSLL Realizado

- **Posição:** ordem_dre = 12; indicador Provisão para IR e CSLL.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[realizado], via [DRE | Realizado]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `DRE\Provisão para IR e CSLL`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição 12 da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.

## DRE | Provisão para IR e CSLL Orçado

- **Posição:** ordem_dre = 12; indicador Provisão para IR e CSLL.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[orcado], via [DRE | Orçado]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `DRE\Provisão para IR e CSLL`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição 12 da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.

## DRE | Provisão para IR e CSLL Previsto

- **Posição:** ordem_dre = 12; indicador Provisão para IR e CSLL.
- **Fonte/valor:** workspace.gold.vw_dre_comparativo[previsto], via [DRE | Previsto]. Grão da origem: filial × competência × posição.
- **Armazenamento:** _Medidas; pasta `DRE\Provisão para IR e CSLL`; nome exato no título.
- **Sinal:** conservar valores ajustados, sem tipolancamento, ABS ou inversão. Posições 3 e 5 usam o subtotal da view, sem recomposição.
- **Filial:** respeitar dim_filial e seleções únicas/múltiplas propagadas pelas relações existentes.
- **Calendário:** respeitar dim_calendario e competências selecionadas; Realizado até maio/2023; Orçado/Previsto até dezembro/2023.
- **Posição/descrição:** CALCULATE com KEEPFILTERS na posição fixa. Posição ou descrição incompatível retorna BLANK. Seleção múltipla que inclua a posição retorna somente ela; se a excluir, BLANK.
- **Totais:** somar somente a posição fixa entre filiais/competências. Total de matriz pode retornar essa posição; não soma posições distintas e não repete valores em linhas incompatíveis.
- **BLANK:** preservar ausência e contexto vazio, sem COALESCE; zero legítimo permanece zero. Descrição ausente ou EBIT continua protegida pela base.
- **Formato:** numérico BRL `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; sem FORMAT e sem migração de cultura.
- **Dependências:** medida base acima, ordem_dre/descricao_dre e coluna de cenário da view; relações Filial/Calendário. Conta e dim_dre não filtram a view automaticamente.
- **Aceite:** medida válida no mecanismo; conciliar com posição 12 da view e SQL independente por filial/período, distinguindo BLANK de zero e usando tolerância máxima R$ 0,01. Testar filtros conflitantes, matriz, aditividade e regressão do Lote 2.1. Inspeção estática não conclui o lote.



# Lote 2.3 / L2.3.1 — políticas aprovadas e contratos condicionais

Registro em 02/11/2026. A orientação mais recente do usuário restringe o trabalho à investigação em leitura e determina não implementar comparabilidade enquanto o contrato temporal não estiver definido. Nenhuma das cinco medidas abaixo foi criada, nem como stub.

## Políticas A–D recebidas

- **A — corte:** única filial pela última competência coberta validamente; múltiplas filiais por corte comum, respeitando seleção e a disponibilidade válida de todas. Não confundir BLANK de indicador com ausência de cobertura global; zero/estorno não eliminam cobertura. A distinção entre sem movimento e não carregado precisa ser confiável; sem ela, bloquear. Maio/2023 é limite observado do conjunto, não constante autorizada na fórmula.
- **B — percentuais futuros:** Δ/ABS(referência) quando referência negativa, preservando sinal do numerador; referência zero/BLANK gera BLANK. Não é aprovação universal de fórmula de cumprimento.
- **C — interpretação:** manter sinais ajustados, sem inverter custos/despesas/estornos. Favorabilidade por natureza e contrato do indicador; ambiguidades permanecem sem classificação. Não se presume aprovação dos direcionadores específicos propostos na matriz original.
- **D — neutralidade/cumprimento:** R$ 0,01 como tolerância monetária inicial, não faixa percentual de desempenho. Cumprimento somente com denominador válido e interpretação documentada. Nenhuma faixa percentual de neutralidade foi definida.

Resultado Líquido continua provisório; EBITDA/EBIT sem cálculo. Não desenvolver M40–M48 ou qualquer outro sublote nesta tarefa.

## Mudança explícita em relação ao plano original

A máscara por presença de Realizado da própria posição, recomendada originalmente, NÃO é o contrato autorizado. O usuário escolheu corte comum entre filiais e exigiu cobertura independente do movimento do indicador. Preservar o plano como histórico e aplicar este adendo: a cobertura global vem de controle/contrato certificado, ainda ausente nas evidências disponíveis. Não substituí-lo por COUNT de fatos, MAX de data, soma, linha 13 ou presença de Orçado/Previsto.

Uma futura máscara A deverá ser obtida da cobertura homologada, respeitar os meses selecionados e o corte comum de todas as filiais. Se uma filial selecionada não tiver cobertura, não ignorá-la. Lacunas internas, referência ausente, dias parciais e status de processamento/fechamento elegíveis precisam ser definidos antes da implementação. Sem essa definição, não inventar nem data nem valores comparáveis.

## M37 — DRE | Realizado Comparável (não implementada)

- **Nome exato:** DRE | Realizado Comparável; nome preservado do planejamento.
- **Fonte/dependências:** vw_dre_comparativo[realizado] via [DRE | Realizado], dimensão Filial/Calendário existentes e futuro controle de cobertura homologado; nenhum recálculo nas fatos.
- **Filial/corte:** todas as filiais selecionadas; uma filial usa último mês certificado na seleção; várias usam corte comum, sem ignorar filial sem certificado e sem tratar ausência de movimento como ausência de carga.
- **Calendário:** intersectar meses selecionados com a cobertura elegível/corte; não apagar filtros de toda a dimensão; datas parciais e lacunas ainda exigem decisão.
- **Posição/totais:** posição única válida da view; preservar guardas da base, descrições e proteção EBIT. Somar a mesma posição somente nos meses/filiais certificados, nunca várias posições gerenciais.
- **BLANK/zero/sinal:** preservar valores ajustados e ausência do indicador. Certificado sem movimento pode manter mês elegível sem converter valor financeiro BLANK em zero. Não usar o BLANK da posição como evidência de cobertura global. Tratamento de referência ausente deve ser homologado separadamente.
- **Formatação futura:** BRL numérico `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`, sem FORMAT ou alteração de cultura.
- **Aceite:** controle/contrato temporal aprovado, parser, materialização, execução DAX mensal e por seleção, conciliação SQL no mesmo snapshot e ausência de regressão das 36 atuais. Comparação monetária máxima R$ 0,01.
- **Estado:** bloqueada por dependência de cobertura; nenhuma expressão definitiva escrita.

## M38 — DRE | Orçado Comparável (não implementada)

- **Nome exato:** DRE | Orçado Comparável; nome preservado do planejamento.
- **Fonte/dependências:** vw_dre_comparativo[orcado] via [DRE | Orçado], dimensão Filial/Calendário existentes e futuro controle de cobertura homologado; nenhum recálculo nas fatos.
- **Filial/corte:** todas as filiais selecionadas; uma filial usa último mês certificado na seleção; várias usam corte comum, sem ignorar filial sem certificado e sem tratar ausência de movimento como ausência de carga.
- **Calendário:** intersectar meses selecionados com a cobertura elegível/corte; não apagar filtros de toda a dimensão; datas parciais e lacunas ainda exigem decisão.
- **Posição/totais:** posição única válida da view; preservar guardas da base, descrições e proteção EBIT. Somar a mesma posição somente nos meses/filiais certificados, nunca várias posições gerenciais.
- **BLANK/zero/sinal:** preservar valores ajustados e ausência do indicador. Certificado sem movimento pode manter mês elegível sem converter valor financeiro BLANK em zero. Não usar o BLANK da posição como evidência de cobertura global. Tratamento de referência ausente deve ser homologado separadamente.
- **Formatação futura:** BRL numérico `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`, sem FORMAT ou alteração de cultura.
- **Aceite:** controle/contrato temporal aprovado, parser, materialização, execução DAX mensal e por seleção, conciliação SQL no mesmo snapshot e ausência de regressão das 36 atuais. Comparação monetária máxima R$ 0,01.
- **Estado:** bloqueada por dependência de cobertura; nenhuma expressão definitiva escrita.

## M39 — DRE | Previsto Comparável (não implementada)

- **Nome exato:** DRE | Previsto Comparável; nome preservado do planejamento.
- **Fonte/dependências:** vw_dre_comparativo[previsto] via [DRE | Previsto], dimensão Filial/Calendário existentes e futuro controle de cobertura homologado; nenhum recálculo nas fatos.
- **Filial/corte:** todas as filiais selecionadas; uma filial usa último mês certificado na seleção; várias usam corte comum, sem ignorar filial sem certificado e sem tratar ausência de movimento como ausência de carga.
- **Calendário:** intersectar meses selecionados com a cobertura elegível/corte; não apagar filtros de toda a dimensão; datas parciais e lacunas ainda exigem decisão.
- **Posição/totais:** posição única válida da view; preservar guardas da base, descrições e proteção EBIT. Somar a mesma posição somente nos meses/filiais certificados, nunca várias posições gerenciais.
- **BLANK/zero/sinal:** preservar valores ajustados e ausência do indicador. Certificado sem movimento pode manter mês elegível sem converter valor financeiro BLANK em zero. Não usar o BLANK da posição como evidência de cobertura global. Tratamento de referência ausente deve ser homologado separadamente.
- **Formatação futura:** BRL numérico `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`, sem FORMAT ou alteração de cultura.
- **Aceite:** controle/contrato temporal aprovado, parser, materialização, execução DAX mensal e por seleção, conciliação SQL no mesmo snapshot e ausência de regressão das 36 atuais. Comparação monetária máxima R$ 0,01.
- **Estado:** bloqueada por dependência de cobertura; nenhuma expressão definitiva escrita.

## M49 — DRE | Pares Filial-Competência Comparáveis (não implementada)

- **Nome exato:** DRE | Pares Filial-Competência Comparáveis; não trocar por contagem de lançamentos ou competências com valor do indicador.
- **Fonte/dependências:** mesma máscara A baseada no controle temporal aprovado, filiais e meses do contexto; coluna monetária não é critério de cobertura.
- **Filial/calendário/corte:** herda o corte comum e os mesmos pares das três financeiras; recalcular no consolidado em vez de somar máscaras de cortes individuais diferentes.
- **Posição/totais:** respeitar elegibilidade/guardas do contexto gerencial sem usar o valor da posição para certificar mês. Detalhar decisão de diagnóstico com várias posições antes de implementar.
- **Ausência/zero:** cobertura desconhecida → BLANK, não zero. Conjunto certificado comprovadamente vazio pode retornar zero diagnóstico, se assim homologado. Zero técnico não preenche valores financeiros. Um mês certificado sem movimento conta como par.
- **Formatação:** inteiro `0`.
- **Aceite/estado:** igualar a cardinalidade da máscara certificada no SQL/DAX, testar filiais sem cobertura e lacunas; bloqueada, não implementada.

## M50 — DRE | Status Comparabilidade (não implementada)

- **Nome exato:** DRE | Status Comparabilidade; não criar stub constante enquanto a implementação está suspensa.
- **Fonte/dependências:** guardas de contexto, controle de carga/completude/fechamento homologado, cobertura das referências e máscara das três financeiras.
- **Filial/calendário/corte:** explicar corte comum, filial sem cobertura, lacuna e recorte parcial. Não informar "Sem movimento" se só há ausência de linhas.
- **BLANK/totais/posição:** diagnóstico do contexto total, sem agregar rótulos; distinguir cobertura desconhecida, sem realizado no período, posição inválida e referência indisponível. Rótulos finais e datas parciais dependem do contrato; não afirmar fechamento por uma posição não BLANK.
- **Formatação:** texto.
- **Aceite/estado:** mensagens coerentes com estados certificados e testes reais/sintéticos identificados; bloqueada, não implementada.

## Dependência e sequência

Ver docs/proposta-controle-competencias.md e docs/validacao-lote2-3-1.md. Primeiro investigar controles/SQL remoto e homologar estados elegíveis/completude/fechamento. Somente então decidir a disponibilização aprovada do controle, confirmar Desktop fechado, novo backup e implementação exclusiva das cinco medidas. Não criar controle, alterar origem ou instalar novas relações nesta investigação.

## Contratos definitivos implementados — L2.3.1, 03/11/2026

Prevalecem sobre os estados históricos “não implementada/bloqueada” das cinco medidas acima, somente no escopo DIDATICA-1.0-20261103 autorizado pelo usuário. Configuração real _ConfigCobertura oculta/desconectada, nove intervalos tipados e versão/hash iguais a docs/cobertura-temporal-didatica.json; sem fonte remota nova e sem modificar as 36 medidas anteriores.

- M37 DRE | Realizado Comparável: base Realizado no corte comum das filiais e seleção mensal completa; se qualquer par necessário tiver Realizado da posição BLANK, resultado BLANK, sem reduzir a máscara.
- M38 DRE | Orçado Comparável e M39 DRE | Previsto Comparável: mesma máscara, cobertura configurada do cenário e dados presentes em todos os pares; Realizado ausente bloqueia o comparável daquela posição; referência ausente bloqueia o próprio cenário e é informada no status. Zero é presente.
- M49 DRE | Pares Filial-Competência Comparáveis: conta os pares de cobertura independentemente do valor do indicador; posição/contexto inválidos BLANK, período válido sem Realizado fornecido zero diagnóstico.
- M50 DRE | Status Comparabilidade: texto com natureza didática/versão, corte comum e motivos de indisponibilidade/parcialidade, sem declarar fechamento real.

Todos consultam a configuração e preservam seleção de filiais e meses descontínuos. Datas parciais, configuração inválida/desconhecida e lacunas bloqueiam o contexto. Valores ajustados e guardas de posição/EBIT das bases preservados. Código e evidências em docs/validacao-lote2-3-1.md; testes locais aprovados, conciliação SQL independente e aceite final pendentes. Sublote em validação, não concluído.
