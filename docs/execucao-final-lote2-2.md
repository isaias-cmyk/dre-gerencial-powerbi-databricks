# Validação final do Lote 2.2 — execução e próximos passos

Data: 02/11/2026. Testes DAX executados por ADOMD no modelo carregado, exclusivamente em leitura. Não houve atualização, gravação do modelo, criação de medidas temporárias ou edição de arquivos de produção.

## Contextos autorizados

A matriz ampliada autorizada contém cinco seleções de filial × sete períodos = 35 combinações. Filiais: 01, 02, 03, consolidado e combinação 01+02. Períodos: integral (2021–2023), 2021, 2022, 2023, janeiro–maio/2023, junho–dezembro/2023 e junho/2023. Os seis cenários originais foram explicitamente confirmados pelo usuário e executados também pelo roteiro 13:

1. Filial 01, integral.
2. Filial 02, integral.
3. Filial 03, integral.
4. Consolidado, 2022.
5. Consolidado, janeiro–maio/2023.
6. Consolidado, junho–dezembro/2023; dez medidas Realizado obrigatoriamente BLANK.

Cada comparação medida × view usa exatamente a mesma posição, cenário e período. Integral/2023 têm realizado parcial; não há análise de desempenho comparando realizado parcial a orçamento anual. Nenhuma soma indiscriminada das 13 posições é feita.

## Resultado efetivamente executado

| Grupo | Evidência / resultado |
| --- | --- |
| Matriz das 30 medidas novas | 1.050/1.050 aprovações; zero reprovações; diferença medida × view máxima R$ 0,00; sinais preservados |
| Ausência | 100 casos BLANK nas medidas novas (dez Realizado × cinco seleções × dois recortes sem realizado); nenhum convertido em zero |
| Resultado Líquido adicional | 105/105 comparações aprovadas, dez BLANK |
| Seis cenários originais | 180/180 comparações aprovadas; os dez Realizado do sexto cenário são BLANK |
| Filtros de posição/descrição | 240/240 casos aprovados, incluindo conflitos, múltiplas posições e ausência |
| Matriz e total | 420 células verificadas: cada medida somente na sua posição e total correspondente; conflito retorna BLANK |
| Aditividade por período | 462/462 verificações: 231 para 01+02+03 = consolidado e 231 para 01+02 = seleção combinada, incluindo três RL; resíduo máximo R$ 0,000000089 |
| Regressão das seis antigas | 210/210 verificações financeiras; mais 175 contextos × seis valores = 1.050 valores verificados, sem regressão; cinco contextos integrais comparados com resultados do Lote 2.1 |
| EBITDA/EBIT | 35 combinações × duas posições = 70 contextos; todas as 36 medidas BLANK (2.520 células) |
| Receita Líquida/Margem | 105/105 casos de identidades coerentes |
| Modelo carregado | 36 medidas Valid, 15 partições Ready sem erro, _Medidas com uma linha e auxiliar zero |
| SQL independente | Não executado nesta rodada; zero casos conciliados com SQL |

Os grupos se sobrepõem deliberadamente para regressão. Não somar suas contagens e apresentá-las como casos financeiros distintos. A matriz principal tem exatamente 1.050 verificações das 30 medidas novas. Foram encontrados zero valores legitimamente iguais a zero nessa matriz; portanto, não se alega execução de caso de origem com zero real. A distinção de ausência foi testada por NULL/BLANK coincidente e conferência explícita de ISBLANK, sem comparação numérica frouxa com zero.

Resumo e resultados por combinação: [resumo.json](evidencias/lote2-2-validacao-final-20261102/resumo.json), [grupos-filtros.csv](evidencias/lote2-2-validacao-final-20261102/grupos-filtros.csv), [aditividade.csv](evidencias/lote2-2-validacao-final-20261102/aditividade.csv). [Divergências atuais](evidencias/lote2-2-validacao-final-20261102/divergencias.json): lista vazia. Se houver falha em uma nova execução, a consolidação registra filial, período, medida/posição/cenário ou contexto responsável.

## Scripts reutilizados e complementos

A consulta [consolidada original](teste-consolidado-lote2-2.dax) foi preservada. O [roteiro 13](testes/lote2-2/13-seis-cenarios-consolidado.dax) reutiliza sua expressão CALCULATETABLE, variando somente os parâmetros de contexto e devolvendo 180 linhas em uma execução.

A matriz ampliada utiliza [02-filiais-periodos-conciliacao.dax](testes/lote2-2/02-filiais-periodos-conciliacao.dax), existente e corrigida. Na primeira execução, UNION falhou porque a coluna AusenciaAposMaio existia somente em parte dos blocos. A correção uniformizou a quantidade/ordem das colunas das linhas Orçado/Previsto, mantendo TRUE para a regra que só se aplica ao Realizado. Nenhuma medida de produção foi alterada. O erro original foi preservado no log; reexecução aprovou as 1.155 linhas (30 medidas novas + três RL × 35).

Reutilizados os roteiros 01, 03–09 e 11. Complementos estritamente de teste:

- [12 — regressão ampliada](testes/lote2-2/12-regressao-ampliada.dax): seis medidas × 35 combinações; bases avaliadas na posição 13 e RL sem filtro artificial de posição.
- [13 — seis cenários](testes/lote2-2/13-seis-cenarios-consolidado.dax): reutilização da consulta consolidada, conforme acima.
- [14 — EBITDA/EBIT ampliado](testes/lote2-2/14-ebitda-ebit-ampliado.dax): 36 medidas em 70 contextos, preservando as linhas com contagem da origem.
- [15 — estado](testes/lote2-2/15-estado-particoes.dax): estados e horários de partição, sem retornar consultas/conexões.
- [16 — contextos de regressão](testes/lote2-2/16-regressao-contextos-ampliada.dax): reutiliza o roteiro 08 nas 35 combinações; sem filtro, múltiplas posições, posição 13, posição 1 e contexto sem dados.

## Reprodução no Power BI Desktop

1. Abrir o PBIP atualizado já existente; não alterar medidas, relações ou fontes.
2. Na Exibição de Consulta DAX, criar uma consulta de teste, colar o arquivo inteiro e Executar. Não usar a barra de criação de medidas nem aplicar alterações ao modelo.
3. Executar 02 para a matriz ampliada (1.155 linhas) e 13 para os seis cenários originais (180 linhas). Todos os Aprovado devem ser TRUE; em 02, AusenciaAposMaio também deve ser TRUE.
4. Executar os demais roteiros para reproduzir os testes específicos, conforme tabela no relatório do lote. Exportar as saídas completas, incluindo os casos BLANK, e registrar catálogo, versão, data e atualização dos dados. Não usar segmentadores das páginas como substitutos dos filtros explícitos das consultas DAX.
5. Para automatizar em Windows com PowerShell e as bibliotecas instaladas: `& '.\docs\evidencias\lote2-2-executar-local.ps1'`. O executor desta rodada descobre o workspace padrão da instalação Desktop e exige um único catálogo com as oito tabelas esperadas. Se usar Desktop Store ou mais de uma instância, ajustar explicitamente a seleção do workspace antes de executar; não escolher catálogo por suposição. Ele somente consulta e grava CSV/JSON em docs/evidencias.

Os scripts de preparação/geração de medidas de tarefas anteriores NÃO devem ser executados nesta etapa. O script [lote2-2-consolidar-dinamica.py](evidencias/lote2-2-consolidar-dinamica.py) analisa as quatro rodadas datadas desta entrega e não executa DAX/SQL. Para rodadas futuras, ajustar seus caminhos de entrada às novas evidências, preservando as anteriores.

## Conciliação independente Databricks SQL — ação restante

Não existe conector de execução Databricks entre as ferramentas disponíveis nesta rodada. O SELECT já preparado foi preservado e não foi substituído por uma consulta aos dados importados.

1. No Databricks SQL, selecionar o warehouse existente com acesso a workspace.gold. Não alterar autenticação ou conexão do projeto.
2. Abrir [10-referencia-databricks.sql](testes/lote2-2/10-referencia-databricks.sql), colar o conteúdo completo no editor e executar o SELECT. Ele retorna 1.155 chaves, valores e contagens, incluindo posição 13 para regressão; não soma diferentes posições nem converte NULL em zero.
3. Confirmar que os dados da origem correspondem à atualização importada no Desktop. Os horários reportados pelas partições estão na saída 15; não presumir que uma consulta SQL atual e um modelo importado anterior representam o mesmo estado. Registrar a data/hora da execução SQL e a referência da atualização. Caso haja diferença de estado, investigar antes de aprovar.
4. Exportar todas as 1.155 linhas SQL para CSV UTF-8 com cabeçalhos originais, valores numéricos sem símbolo monetário/agrupamento de milhar e NULL preservado. Não fornecer somente totais ou captura parcial.
5. Comparar com o CSV DAX já executado, usando no terminal, a partir da raiz do projeto:

```powershell
python '.\docs\testes\lote2-2\comparar-exportacoes.py' '.\docs\evidencias\lote2-2-execucao-20261102-185954\02-filiais-periodos-conciliacao.csv' 'C:\caminho\resultado-databricks.csv' '.\docs\evidencias\lote2-2-validacao-final-20261102\conciliacao-sql.json'
```

Substituir somente o caminho do CSV SQL por seu arquivo real. O comparador exige conjuntos de 1.155 chaves únicos e iguais, BLANK/NULL coincidentes e diferença absoluta ≤ R$ 0,01. Não houve execução deste comparador sobre resultados SQL reais nesta rodada. Os casos SQL permanecerão pendentes até receber e conferir a exportação real.

## Evidências e status

Foram 16 tentativas DAX/INFO: 15 execuções com sucesso e uma falha histórica de sintaxe/estrutura do roteiro 02, corrigida e reexecutada. Não há falha financeira atual encontrada. Logs e saídas:

- [Rodada inicial](evidencias/lote2-2-execucao-20261102-185937/execucao.json).
- [Matriz corrigida](evidencias/lote2-2-execucao-20261102-185954/execucao.json).
- [Complementos](evidencias/lote2-2-execucao-20261102-190116/execucao.json).
- [Regressão de contextos](evidencias/lote2-2-execucao-20261102-190257/execucao.json).

Em todas as rodadas, comparação dos hashes de entrada/saída indicou nenhum arquivo de produção alterado. Formatos foram lidos em metadados; não houve inspeção visual adicional de cartões/páginas, teste de desempenho ou homologação contábil.

**Lote 2.2 permanece não concluído, aguardando conciliação SQL independente.** Resultado Líquido provisório; EBITDA/EBIT sem cálculo. Lote 2.3 não iniciado.


## Atualização após recebimento do SQL completo — 02/11/2026

A ação restante descrita acima foi atendida por exportação Databricks fornecida pelo usuário, sem nova execução SQL pelo agente. O comparador original aprovou 1.155/1.155 chaves, zero divergências e 110 NULL/BLANK coincidentes, com diferença máxima R$ 0,00000010. Evidências em docs/evidencias/lote2-2-sql-completo-20261102/aceite.json e docs/evidencias/lote2-2-validacao-final-20261102/conciliacao-sql-completa.json.

Lote 2.2 concluído tecnicamente no grão agregado por recorte previsto nos scripts; não constitui conciliação de cada competência mensal individual. Lote 2.3 liberado somente para planejamento, sem implementação. Seções anteriores preservadas como histórico e instruções de reprodução. Produção e pendências contábeis preservadas.
