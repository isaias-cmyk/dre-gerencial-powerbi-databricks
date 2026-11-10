# Lote 2.3 — Desvios Financeiros e Comparações Orçamentárias

Data: 02/11/2026. **Planejamento preparado; nenhuma implementação iniciada.** Propostas abaixo dependem das decisões da seção final. Este documento não altera nem amplia os contratos das 36 medidas existentes.

## 1. Base confirmada e limites

Lidos AGENTS.md, PLANS.md, contratos, validações dos Lotes 2.1/2.2 e definição real de _Medidas. Encerramento técnico de 2.2 confirmado em docs/evidencias/lote2-2-sql-completo-20261102/aceite.json: 1.155 chaves SQL/DAX conciliadas, nenhuma reprovação, 110 NULL/BLANK coincidentes e maior diferença R$ 0,00000010. DAX: 35 combinações, 1.050 verificações das medidas novas, sem regressão nas seis antigas. Esse aceite é por recortes agregados; não constitui conciliação de cada competência mensal individual nem homologação contábil.

A inspeção de _Medidas.tmdl confirma 36 medidas: três bases `DRE | Realizado`, `DRE | Orçado`, `DRE | Previsto`; três `DRE | Resultado Líquido <cenário>` provisórias; trinta específicas de dez indicadores × três cenários. As específicas intersectam a posição por CALCULATE/KEEPFILTERS. As bases exigem posição única/descrição válida e suprimem rótulos EBIT. Reutilizar essas regras e valores ajustados da view; sem consultar fatos para refazer indicadores, reaplicar tipolancamento ou reconstruir subtotais.

Escopo proposto: desvios monetários/percentuais, referências comparáveis, impacto orçamentário, classificação e cumprimento quando aplicável. Fora: implementação nesta entrega; EBITDA/EBIT; margens percentuais novas; rankings; páginas; cores condicionais; alterações de fontes, culturas, relações, tabelas, consultas M ou credenciais. YTD automático é extensão separada, não implícita no recorte selecionado.

## 2. Quantidade e arquitetura recomendadas

**14 novas medidas genéricas**, compartilhadas pelos indicadores elegíveis. Total futuro máximo da proposta: 50 medidas (36 atuais + 14), após aprovação e implementação. Evitar criar onze cópias de cada comparação; as bases já selecionam a posição. Medidas específicas para cartões de posição fixa só serão consideradas depois de uma necessidade visual concreta, em outro escopo, sem criar automaticamente todas as combinações.

Usar `vw_dre_comparativo[ordem_dre]` e `[descricao_dre]` nos eixos gerenciais. Uma posição válida → cálculo; nenhuma/múltiplas posições → BLANK para números financeiros. Total entre filiais/competências da mesma posição → recalcular valores e razões sobre o contexto consolidado. Total entre posições → BLANK, nunca soma de analíticas/subtotais. Textos podem indicar "Selecione uma posição DRE". Indicadores 8 e 11 permanecem sem cálculo, inclusive comparação e classificação.

As três referências do período **selecionado** já existem: as bases Realizado/Orçado/Previsto. Não duplicá-las nem alterar seus valores. As referências **comparáveis** abaixo são novas e têm nomes distintos. Todos os componentes de um desvio devem usar a mesma máscara temporal/filial; não combinar Realizado selecionado com Orçado anual.

## 3. Notação, fórmulas e política de ausência

Para uma posição p e o contexto de filiais/calendário C, definir A como o conjunto de pares (filial, competência) selecionados nos quais a posição possui Realizado não BLANK, incluindo zero legítimo. R é a medida Realizado avaliada em A; O e P são as referências Orçado e Previsto avaliadas **nesse mesmo A**. Se A estiver vazio, R/O/P comparáveis e desvios são BLANK. Orçado/Previsto selecionados continuam acessíveis pelas bases, mesmo nos meses futuros.

Não substituir NULL por zero. Verificar ISBLANK antes de subtrair, dividir ou classificar: a aritmética DAX pode coagir BLANK para zero. Se faltar referência em qualquer par de A, a comparação contra esse cenário será BLANK, com aviso de cobertura incompleta; não reduzir silenciosamente R para esconder referência ausente. R e a comparação com o outro cenário podem continuar válidos. O zero de referência é valor presente e não falha de cobertura.

Fórmulas conceituais, **não DAX implementado**:

```text
ΔO = R − O ; ΔP = R − P                     se ambos os componentes estiverem presentes
ΔO% = (R − O) / |O| ; ΔP% = (R − P) / |P|  se referência ≠ 0, senão BLANK
ImpactoX = direção(p, regime de sinais) × ΔX se regra de negócio aprovada e elegível
ClassificaçãoX = favorável / em linha / desfavorável segundo ImpactoX e tolerância
CumprimentoOrçamentário = R / O             apenas receitas elegíveis, O > 0 e R ≥ 0
```

O ABS aparece somente no **denominador do percentual**, para normalizar a escala de uma referência negativa. Não aplicar ABS ao valor financeiro da view nem alterar sinais. Exemplo de gasto: O = −100 e R = −120 → ΔO = −20, ΔO% = −20%; não usar R/O − 1 e interpretar +20% como desempenho bom. Percentual é variação relativa normalizada, não crescimento convencional universal nem favorabilidade automática.

Proposta de tolerância para classificação: |Impacto| ≤ R$ 0,01 → "Em linha"; acima → favorável; abaixo de −R$ 0,01 → desfavorável. Aplicar aos valores não arredondados; mostrar duas casas. Essa regra é proposta para aprovação, não homologação presumida. Tolerância de conciliação monetária também máxima R$ 0,01; para razões usar diferença absoluta ≤ 0,00000001 (razão decimal, não pontos percentuais), salvo ajuste formal aprovado.

Se R/O ou R/P mudar de sinal: desvio numérico e percentual normalizado continuam matematicamente definidos quando a referência não é zero; sinalizar "Mudança de sinal" no diagnóstico. Favorabilidade/cumprimento obedecem aos limites da natureza, sem forçar classificação por sinal do desvio.

## 4. Comparabilidade temporal

### Regra recomendada para o período selecionado

1. Obter as competências mensais efetivamente selecionadas pelo calendário validado e filiais selecionadas, preservando posição/descrição da própria view.
2. Para cada par filial/competência, testar a presença de Realizado da posição; zero conta como presente, NULL não. Não inferir presença por valor > 0, soma não zero ou última linha física.
3. Formar A e aplicar os mesmos pares aos três cenários, sem preencher lacunas. É preciso filtro de **tuplas**: filiais e meses filtrados isoladamente podem criar produto cartesiano e incluir meses sem realizado de outra filial.
4. Verificar cobertura de cada referência no A completo. Não usar a interseção R/O/P para ocultar falhas de uma referência; seu desvio fica indisponível se faltar cobertura.
5. Expor a quantidade de pares e o status. Todos os pares selecionados realizados → "Período integralmente comparável"; só parte → "Recorte comparável parcial"; nenhum → "Sem realizado no período"; referência incompleta → informar Orçado/Previsto afetado. A política detalhada para consolidado parcial por filial requer aprovação.

A soma dos meses selecionados deve respeitar seleção descontínua: janeiro e março não incluem fevereiro automaticamente. Em seleção com vários anos, usar a presença de cada competência, não um MAX global de data que transforme maio/2023 em corte de todos os anos. O conjunto A é recalculado no total; medidas de percentual não somam linhas e impactos/classificações exigem regime de sinais válido no contexto total.

Calendário diário com origem mensal: recomenda-se aceitar somente seleções formadas por meses completos. Datas parciais devem retornar BLANK nos números comparáveis e diagnóstico "Selecione meses completos", até definir política específica. Não presumir proporcionalidade diária nem considerar um mês apenas porque seu primeiro dia foi selecionado. Confirmar o grão/datas e implementação dessa guarda nos testes mensais.

Em 2023 integral, A inclui janeiro–maio por filial conforme a presença real; não inclui orçamento/previsão junho–dezembro como referência do realizado. Se a seleção for somente junho–dezembro/2023, A vazio → comparáveis/desvios BLANK. Integral 2021–2023 compara 2021/2022 completos mais o recorte realizado de 2023, respeitando os meses presentes por filial.

### YTD, se aprovado posteriormente

Não chamar o cálculo da seleção arbitrária de YTD. Uma extensão YTD deverá exigir ano único, iniciar em janeiro desse ano e terminar na menor data entre o fim do período solicitado e a última competência efetivamente realizada elegível. Detectar lacunas internas em vez de presumir todos os meses entre janeiro e MAX; meses sem realizado não viram zero. Para consolidado, decidir corte comum entre filiais versus cobertura individual antes de desenvolver a extensão. Ano múltiplo/seleção incompatível → BLANK e aviso. Nenhuma nova medida YTD está entre as 14 recomendadas.

## 5. Matriz de indicadores reutilizáveis

Em cada linha, `<cenário>` significa exatamente Realizado, Orçado e Previsto já existentes. Fonte gerencial de todas: `vw_dre_comparativo` via medidas de _Medidas; máscaras de disponibilidade podem inspecionar a presença na view, sem criar cálculos financeiros paralelos. Nomes de indicador abaixo são os nomes exatos usados nas 30 medidas existentes, com prefixo `DRE | ` e sufixo de cenário.

| Posição | Indicador / família de dependências existente | Regime esperado e favorabilidade proposta | Comparações / cumprimento / aceite específico |
| --- | --- | --- | --- |
| 1 | Receita Operacional Bruta | Em geral receita ≥ 0; R maior que referência pode ser favorável; aprovar direção +1 | Quatro desvios; impacto/classe após aprovação; cumprimento R/O apenas O > 0 e R ≥ 0; validar devoluções/sinais excepcionais |
| 2 | Deduções da Receita | Em geral ≤ 0; gasto líquido menor em magnitude pode elevar receita líquida, mas pode refletir volume/tributação/descontos | Desvios numéricos disponíveis; impacto/classe/cumprimento indisponíveis até regra de negócio; não equiparar automaticamente a despesa |
| 3 | Receita Operacional Líquida | Receita líquida maior pode ser favorável; direção +1 sob regra aprovada | Mesmo contrato de 1; não reconstruir a posição 3 por outras posições |
| 4 | Custos | No regime R ≤ 0 e X ≤ 0, aumento de magnitude é excesso de gasto; redução pode ser favorável em relação ao orçamento | Δ = R − X; impacto = −(|R| − |X|), equivalente a Δ só nesse regime. Testar sinais por filial/mês antes do total; cumprimento não aplicável |
| 5 | Margem de Contribuição | Valor monetário líquido: maior pode ser favorável; direção +1 a aprovar | Desvios e classificação após aprovação; sem cumprimento e sem margem percentual nova; usar posição 5 existente |
| 6 | Despesas Operacionais | Mesmo regime contábil de gastos da posição 4; redução de magnitude pode ser favorável ao envelope orçamentário | Mesmo contrato de 4; não afirmar eficiência ou qualidade operacional somente pelo gasto menor |
| 7 | Resultado Financeiro | Pode ser líquido, negativo ou positivo | Desvios numéricos disponíveis; favorabilidade suspensa até confirmar meta líquida/juros/receitas e objetivo financeiro; sem cumprimento |
| 9 | Depreciação e Amortização | Usualmente ≤ 0, não caixa; menor despesa pode decorrer de base de ativos/timing | Desvios numéricos disponíveis; classificação depende de política contábil/orçamentária adicional; sem cumprimento |
| 10 | Outras Receitas e Despesas | Natureza mista; não assumir sinal fixo | Desvios numéricos disponíveis; impacto/classe sem regra aprovada retornam BLANK/aviso; sem cumprimento |
| 12 | Provisão para IR e CSLL | Usualmente ≤ 0; menor imposto pode resultar de menor lucro, não melhor desempenho | Desvios numéricos disponíveis; classificação suspensa até regra fiscal/contábil aprovada; sem cumprimento |
| 13 | Resultado Líquido (provisório) | Resultado líquido maior pode ser favorável, mas indicador não homologado contabilmente | Usar as três medidas específicas existentes como referência de regressão; genéricas só na posição 13 válida. Desvios com aviso provisório; classe/impacto dependem de autorização explícita; sem cumprimento |
| 8 / 11 | EBITDA / EBIT | Pendentes de homologação | Fora do escopo; todos os novos números BLANK, sem classe favorável/desfavorável |

Para custos/despesas, não basta observar o sinal do **total**: se existir crédito/estorno positivo em par filial/competência comparado, marcar classificação indisponível até aprovar tratamento líquido. O desvio numérico conserva esses sinais. A fórmula de magnitude é critério de interpretação proposto, não transformação dos valores de produção.

## 6. Matriz das 14 medidas propostas

Legenda de dependências: B_R/B_O/B_P = bases atuais; A = máscara de pares filial/competência com realizado; D = direção aprovada da matriz; C = guarda de contexto válido/meses completos; X = cenário de referência. Nenhum nome abaixo existe hoje: são propostas, não medidas criadas.

| ID / nome exato proposto | Fórmula / fonte / dependências | Posição, sinal, zero e aceite |
| --- | --- | --- |
| M37 — DRE \| Realizado Comparável | B_R avaliada em A; C + A + B_R | Posição única elegível; conservar sinal; A vazio → BLANK; zero real presente; conciliar soma da mesma posição nos pares A |
| M38 — DRE \| Orçado Comparável | B_O avaliada em A; C + A + cobertura O completa | Mesmo p e A de M37; não incluir futuro; referência ausente → BLANK e status; zero real mantido |
| M39 — DRE \| Previsto Comparável | B_P avaliada em A; C + A + cobertura P completa | Mesmo contrato de M38 para previsão |
| M40 — DRE \| Desvio Realizado x Orçado (R$) | M37 − M38 após presença explícita | Posição p; sinal puramente numérico; O = 0 válido para valor absoluto; ausência de R/O → BLANK |
| M41 — DRE \| Desvio Realizado x Orçado (%) | (M37 − M38) / ABS(M38) com divisão protegida | O = 0/BLANK → BLANK; O negativo permitido com normalização explicitada; não interpreta favorabilidade |
| M42 — DRE \| Desvio Realizado x Previsto (R$) | M37 − M39 após presença explícita | Mesmo contrato de M40, com P |
| M43 — DRE \| Desvio Realizado x Previsto (%) | (M37 − M39) / ABS(M39) | Mesmo contrato de M41, com P |
| M44 — DRE \| Impacto Favorável x Orçado (R$) | D(p, sinais nos pares) × M40; natureza aprovada | Positivo significa favorável pelo contrato aprovado, negativo desfavorável; ausência/regime inválido/sem regra → BLANK; para gastos usar a interpretação formal da seção 5 |
| M45 — DRE \| Impacto Favorável x Previsto (R$) | D(p, sinais nos pares) × M42 | Mesmo contrato de M44 contra previsão; retorno assinado inclui desfavorável, sem criar duas medidas para cada direção |
| M46 — DRE \| Classificação x Orçado | Texto de M44/guardas/status: Favorável, Em linha, Desfavorável, Sem dados comparáveis, Sem regra aprovada ou Regime de sinais não aprovado | Não inferir classe de M40 isoladamente; despesa −120 versus −100 desfavorável; classificar total a partir do cálculo agregado e natureza válida |
| M47 — DRE \| Classificação x Previsto | Mesmo contrato de M46 usando M45/P | Referência incompleta informada antes de classificação; nunca classificar BLANK como em linha |
| M48 — DRE \| Cumprimento Orçamentário (%) | M37/M38 somente posições 1/3 com contrato aprovado | O > 0 e R ≥ 0; outros indicadores, referência zero/negativa ou ausência → BLANK. 100% = meta atingida; >100% excedida. Não usar inversão O/R para gastos |
| M49 — DRE \| Pares Filial-Competência Comparáveis | Cardinalidade de A, inteiro; C + A | Conta pares, não meses distintos. A vazio e contexto válido → 0 diagnóstico; posição inválida → BLANK. Não confundir esse zero técnico com valor financeiro ausente |
| M50 — DRE \| Status Comparabilidade | Texto de C, A e cobertura O/P, incluindo exclusão de futuro e mudança de sinal | Diagnóstico deve indicar motivo/escopo (completo, parcial, sem realizado, referência incompleta, posição/meses inválidos); sem números financeiros inventados |

O cálculo do impacto pode coincidir numericamente com o desvio em regimes aprovados, mas tem semântica e guardas distintas; essa separação evita usar desvio bruto para cores. Não implementar cores nesta fase. As classificações/diagnósticos devem indicar separadamente a ausência de referência e a falta de política de favorabilidade.

### Contratos comuns às 14

- **Filial/calendário:** preservar seleções únicas/múltiplas e tuplas A; não usar ALL/REMOVEFILTERS indiscriminadamente. Ao inspecionar cobertura, remover apenas o filtro estritamente necessário e reaplicá-lo explicitamente, mantendo os filtros efetivos da view.
- **Conta/dim_dre:** não propagam posição/conta à view automaticamente; mostrar esse limite, sem ativar a relação inativa ou criar TREATAS para mascarar detalhe inexistente. Posição/descrição conflitante gera contexto vazio/BLANK.
- **Totais:** monetários pelo cálculo agregado da mesma posição; percentuais e cumprimento como razão de somas comparáveis, não soma/média simples dos percentuais de filiais. Classes não são agregadas de rótulos; reavaliar o total e a natureza. Sem regra aprovada → impacto BLANK e texto explicativo.
- **Formatos propostos:** BRL numérico `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`; percentuais numéricos `0.00%;(0.00%);0.00%`; contagem `0`; classificações/status texto. Não FORMAT em números; não mudar en-US/pt-BR. Conferir renderização real posteriormente.
- **Organização futura:** mesma _Medidas; pastas candidatas `DRE\Comparabilidade`, `DRE\Desvios`, `DRE\Desempenho`. Nomes/IDs e pastas existentes preservados. Máscaras A são expressões de tabela locais às medidas, não novas tabelas de produção neste plano. Possível repetição da expressão temporal deve ser revisada e testada, sem impor calculation groups ou função DAX não suportada pela versão real.

## 7. Exemplos controlados para aprovar as regras

**Sintéticos**, não observações da origem nem testes executados:

| Natureza | R / referência | Desvio / percentual normalizado | Interpretação proposta |
| --- | --- | --- | --- |
| Receita elegível | 120 / 100 | +20 / +20% | Favorável se direção +1 aprovada; cumprimento 120% |
| Receita elegível | 80 / 100 | −20 / −20% | Desfavorável; cumprimento 80% |
| Receita elegível | 100 / 100 | 0 / 0% | Em linha; cumprimento 100% |
| Gasto negativo elegível | −120 / −100 | −20 / −20% | Maior gasto em magnitude, desfavorável |
| Gasto negativo elegível | −80 / −100 | +20 / +20% | Menor gasto em magnitude, favorável ao orçamento |
| Gasto negativo elegível | −100 / −100 | 0 / 0% | Em linha |
| Receita/gasto | 20 ou −20 / 0 | +20 ou −20 / BLANK | Desvio absoluto válido; percentual/cumprimento indisponíveis; classificar somente se natureza e regime aprovados |
| Qualquer elegível | 0 / 100 | −100 / −100% | Zero realizado presente; não é ausência |
| Qualquer | BLANK / 100 | BLANK / BLANK | Sem realizado; nenhuma classe favorável/desfavorável |
| Qualquer | 100 / BLANK | BLANK / BLANK | Referência ausente; não transformar em zero |
| Gasto com estorno | +10 / −100 | +110 / +110% | Desvio numérico válido; favorabilidade bloqueada até definir tratamento do estorno |
| Resultado líquido | −20 / −100 | +80 / +80% | Melhora numérica; interpretação depende de regra aprovada/provisoriedade |

Não exigir que a origem contenha exemplos de zero ou estorno. Se não houver, usar somente consultas temporárias com DATATABLE/ROW em ambiente de teste, sem criar tabelas/medidas persistidas. Nomear a saída como sintética e não juntá-la às evidências de origem real.

## 8. Plano de testes DAX e SQL (previstos, não executados)

| ID | Teste e origem | Critério objetivo |
| --- | --- | --- |
| T01 | Inventário/expressões antes e depois da futura implementação | 36 antigas intactas, 14 novas somente se todo escopo aprovado; parser, nomes únicos, relações/partições/fontes preservadas |
| T02 | Casos sintéticos da seção 7: desvio positivo, negativo, zero, denominador zero/negativo, estorno, BLANK | Resultado esperado explícito, status correto, sem coagir BLANK a zero; tolerância monetária R$ 0,01 e de razão 1e-8 |
| T03 | Origem real por cada competência mensal de 2021–2023 × 11 posições × três filiais × três cenários | Exportação SQL independente e DAX correspondentes, mesma chave/atualização. Grade proposta 3.564 chaves; falta de linha e NULL registrados separadamente, sem presumir cobertura mensal do Lote 2.2 |
| T04 | Matriz ampliada herdada: cinco seleções × sete recortes × 11 posições | Comparações respeitam mesma máscara por cenário; nunca referência anual contra R Jan–Mai. Nem EBITDA nem EBIT incluídos como elegíveis |
| T05 | Meses sem realizado de junho–dezembro/2023, cada filial e consolidado | A vazio no período exclusivamente futuro; comparáveis/desvios BLANK; O/P selecionados continuam disponíveis nas bases |
| T06 | Orçamento/Previsão comparáveis versus selecionados em 2023 | Comparável somente pares realizados; selecionado mantém período original. Futuro excluído do comparável com diagnóstico visível |
| T07 | Lacunas, filiais com cortes diferentes e referência ausente, sintético se necessário | Preservar tuplas, não criar produto cartesiano; não esconder referência faltante por redução silenciosa de A; nenhuma soma de percentual |
| T08 | Seleções 01, 02, 03, consolidado e 01+02; mês, ano, anos múltiplos e meses descontínuos | Interseções corretas; no regime de cobertura individual aprovado, soma das filiais comparáveis = consolidado; se escolhida cobertura comum, comparar cada filial no mesmo conjunto comum antes de testar aditividade |
| T09 | Datas parciais e posição/descrição conflitante, nenhuma/múltiplas posições | BLANK/status conforme guardas; classificação não preenche ausência e total entre posições BLANK |
| T10 | Totais/subtotais e regimes mistos de sinal | Razões recalculadas; impacto sem política/regime retorna BLANK mesmo se sinal do total parecer válido |
| T11 | Regressão das 36 atuais e controles da linha 13 | Reutilizar roteiros já existentes 01–16, consultas consolidadas e comparador; valores antigos inalterados. Não refazer testes sem necessidade nem confundir retornos selecionados com comparáveis novos |
| T12 | Proteção de EBITDA/EBIT e provisoriedade RL | Posições 8/11 sem valores ou classes; nomes/descrições RL provisórios preservados e rótulos futuros coerentes |
| T13 | Formato e execução no mecanismo real | Compilação/avaliação DAX, metadados e renderização monetária/percentual; medir tempo dos contextos relevantes sem declarar meta de desempenho inventada |

### Estratégia SQL independente prevista

Primeiro exportar a grade mensal por cod_filial, competencia, ordem_dre e cenário, incluindo contagem de linhas/valores presentes e valor ajustado. Preservar original e SHA-256. Usar somente SELECT, sem DDL/DML, edição de views ou credenciais. Validar grão único antes de unir cenários; joins com duplicação bloquearão a comparação.

Depois definir CTEs de contexto e presença de Realizado por par/posição, aplicar a **mesma regra temporal aprovada** aos três cenários e calcular somas, desvios e percentuais independentemente das medidas. O SQL não deve reproduzir apenas os mesmos nomes DAX nem recalcular os indicadores a partir das fatos. Não somar posições gerenciais; avaliar cada posição e classe segundo o mapa aprovado. Usar NULLIF/CASE para denominador zero, sem COALESCE financeiro. Ausência de qualquer referência no conjunto comparável deve ser identificada antes do agregado.

Comparar a exportação SQL às saídas das futuras medidas por chave filial/grupo, competência ou recorte, posição, referência e métrica. Não usar o comparador de 1.155 linhas sem adaptar conscientemente seu esquema/contagem ao novo grão: preservar o comparador antigo e criar versão própria de teste, sem alterar as evidências anteriores. Registrar por chave esperado/obtido/diferença, sinal, ausência, cobertura e diagnóstico. Zero duplicações/ausências inesperadas; nenhuma divergência acima da tolerância sem investigação.

## 9. Etapas incrementais e primeiro lote sugerido

1. **L2.3-P — decisões e contratos:** aprovar as políticas da seção 11 e confirmar dados mensais/guardas; fechar Desktop antes de qualquer edição futura, verificar Git/diferenças de entrada, fazer novo backup restaurável. Planejamento atual não é autorização implícita para editar.
2. **L2.3.1 — comparabilidade:** primeiro lote recomendado com **cinco medidas**: M37, M38, M39, M49, M50. Validar máscaras, datas mensais, A vazio, zero e referência incompleta, inclusive diferenças entre filiais/anos. Sem favorabilidade ou desvios antes desse aceite.
3. **L2.3.2 — desvios numéricos:** quatro medidas M40–M43. Validar sintéticos e conciliar cada posição/mês/filial com SQL independente, preservando referências negativas e divisão por zero.
4. **L2.3.3 — desempenho aprovado:** cinco medidas M44–M48, somente nas naturezas/políticas autorizadas. Manter classificação bloqueada para naturezas sem decisão; cumprimento restrito a receitas elegíveis. Não ampliar silenciosamente elegibilidade.
5. **L2.3-A — regressão e aceite:** executar plano de testes completo proporcional às alterações, documentar dados reais versus sintéticos e decidir aceite de cada sublote. Não marcar implementação ou testes concluídos apenas pela existência de código ou deste plano.

Arquivos potencialmente afetados apenas na **futura** implementação: _Medidas.tmdl e documentação/consultas de teste; nenhuma relação, fonte ou página necessária no escopo proposto. Nesta entrega somente `docs/plano-lote2-3.md` e registro de planejamento no PLANS.md.

## 10. Riscos e critérios de aceite futuros

| Risco | Consequência / mitigação proposta |
| --- | --- |
| Corte global único ou produto cartesiano de filtros | Orçamento de filial/mês sem realizado; usar tuplas e testes de lacunas/filiais |
| Aritmética DAX sobre BLANK | Desvio falso e classificação indevida; presença explícita antes de operar |
| Percentual com referência negativa ou zero | Inversão de leitura/infinitos; normalizar denominador e separar favorabilidade |
| Soma de percentuais/subtotais | Consolidado errado; razão de agregados na mesma posição e máscara |
| Regime contábil misto ou meta não homologada | Crédito parecer economia; bloquear interpretação sem regra aprovada |
| Redução de despesa ligada a volume/ativos/impostos | Falso juízo de eficiência; rótulo orçamentário e suspensões da matriz |
| Excesso de medidas e fórmulas temporais repetidas | Manutenção divergente; 14 genéricas, contratos únicos e regressões de máscaras |
| Mensal não comprovado por aceite agregado anterior | Ocultar compensações entre meses; teste mensal independente obrigatório deste lote |
| Origem/Power BI em atualizações diferentes | Conciliação inconclusiva; identificar versões/horários e não presumir sincronia pelo nome do CSV |

Aceite futuro exige: decisões registradas; contratos finais consistentes; backup verificado; parser aprovado; produção protegida; medidas executadas no Desktop; grade mensal e agregada conciliadas com SQL independente; BLANK/zero/sinais/divisão demonstrados; totais e comparabilidade por filial/ano comprovados; 36 antigas sem regressão; sintéticos identificados; EBITDA/EBIT excluídos e RL provisório. Falha de cobertura ou divergência mantém o sublote pendente/bloqueado, com chave exata identificada. Registrar também testes não executados e seu motivo. Não aceitar referência futura disfarçada de período realizado.

## 11. Decisões necessárias antes de implementar

1. **Máscara temporal:** aprovar cobertura individual por par filial/competência (recomendação) ou corte comum entre filiais. A individual permite composições temporais distintas no consolidado e deve ser identificada como parcial; a comum exclui dados válidos para comparar filiais no mesmo intervalo. Não alternar a política silenciosamente.
2. **Ausência e datas:** confirmar presença por posição, aceitação somente de meses completos e bloqueio por referência incompleta. Meses sem realizado podem representar ausência ou lacuna de carga; sem contrato que os distinga não inferir fechamento contábil.
3. **Percentuais:** aprovar Δ/ABS(referência), tratamento de referência negativa, mudança de sinal e BLANK com referência zero. Não é a mesma métrica de R/X − 1 em referências negativas.
4. **Favorabilidade:** aprovar direção para receitas, margem e gastos 4/6 sob sinais não positivos em cada par. Definir se deduções, financeiro, depreciação, outras receitas/despesas e impostos terão política; enquanto não houver, manter somente desvios e diagnóstico sem impacto/classificação. RL continua provisório; sua classificação exige autorização específica.
5. **Classificação:** aprovar neutralidade de R$ 0,01 e rótulos propostos. Não definir cores antes dessas regras.
6. **Cumprimento:** aprovar somente receitas 1/3 com O > 0 e R ≥ 0, sem medida de cumprimento para gastos ou resultado nesta proposta.
7. **Escopo/nomenclatura:** aprovar as 14 medidas e os três sublotes; YTD automático e wrappers de cartões ficam fora até solicitação/contrato próprios.

Nenhuma dessas propostas está marcada como homologada pelo fato de constar do plano. O próximo passo sugerido é aprovar os contratos de comparabilidade e autorizar explicitamente o L2.3.1; nenhuma implementação foi iniciada nesta tarefa.


## Atualização — investigação prévia do L2.3.1 em 02/11/2026

Recebidas políticas A–D e orientação posterior de investigar exclusivamente em leitura. Política A aprova corte comum das filiais selecionadas, substituindo a recomendação inicial de máscara por presença de Realizado da posição. A ausência de manifesto/certificado homologado impede tratar mês com movimento como mês fechado/processado completamente. Nenhuma data fixa autorizada para a lógica definitiva.

Quatro consultas DAX/INFO de diagnóstico executadas sem erro no modelo carregado; 108 combinações filial/mês, metadados de 114 colunas, 36 medidas e nove grupos de rastreabilidade. Não foi encontrado controle de carga/fechamento no modelo importado ou contrato correspondente nos SQL locais examinados. Isso não prova inexistência nos schemas remotos Bronze/Silver/Gold ainda não consultados. Movimento contínuo Jan/2021–Mai/2023 observado; não é certificado de cobertura.

**L2.3.1 bloqueado antes da implementação por dependência de contrato temporal.** As cinco medidas permanecem propostas, com contratos condicionais revisados em docs/contratos-medidas-dax.md. Proposta de controle sem criação: docs/proposta-controle-competencias.md. Relatório/evidências e roteiros remotos de leitura: docs/validacao-lote2-3-1.md. Não criar tabela, stub de medida, corte fixo ou iniciar outro sublote.

## Atualização de escopo didático — 03/11/2026

Premissa expressa de base fictícia registrada e validada documentalmente em docs/contrato-cobertura-temporal.md (DIDATICA-1.0-20261103), vinculada ao hash do Excel. Substitui a máscara por movimento e a exigência de fechamento real apenas no exercício: cobertura Realizado Jan/2021–Mai/2023 comum às filiais 01/02/03; Jun–Dez/2023 não fornecido; Orçado/Previsto Jan/2021–Dez/2023. Não há fechamento contábil certificado.

Proposta de arquitetura futura: uma tabela local desconectada e oculta de configuração, nove intervalos filial/cenário, sem novos relacionamentos e sem alteração das 36 medidas ou consultas Databricks. Datas são parâmetros versionados, não constantes nas cinco medidas. A pequena mudança estrutural é justificada no contrato e permanece pendente de aprovação; não implementada. Novo objeto potencial deverá ser incluído no escopo de backup/parser/materialização. Recomenda-se desbloquear L2.3.1 após aprovar esse desenho e cumprir segurança; nenhuma liberação para demais sublotes. Testes DAX/SQL e regressão continuam futuros. As seções iniciais sobre presença de valor por posição não regem mais o corte, que depende da configuração didática e respeita os meses selecionados.

## Estado de implementação — 03/11/2026

Implementada a arquitetura didática aprovada pelo usuário, com o nome efetivo _ConfigCobertura para a tabela local desconectada e as cinco medidas exatas M37/M38/M39/M49/M50. As 36 anteriores permanecem idênticas. O modelo possui 16 tabelas/18 relacionamentos/41 medidas; configuração materializada em nove linhas, testes DAX locais e regressão executados. Isso supera os estados históricos de apenas planejamento/investigação, sem liberar os demais sublotes. Roteiros e resultados em docs/validacao-lote2-3-1.md e docs/execucao-validacao-l2-3-1.md. **L2.3.1 em validação, aguardando conciliação SQL independente; L2.3.2 não iniciado.**
