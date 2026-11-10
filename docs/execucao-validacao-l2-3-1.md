# Execução e conciliação — implementação do L2.3.1

Estado em 03/11/2026: implementação e testes DAX locais executados; **conciliação Databricks independente pendente**. Relatório: docs/validacao-lote2-3-1.md, seção vigente de implementação.

## Testes Power BI

O projeto atualizado já foi aberto pelo agente no Desktop. _ConfigCobertura retornou nove linhas, 41 medidas estão Valid, 16 partições Ready. O Desktop permanece aberto para consulta; não editar TMDL externamente enquanto estiver aberto. Salvar o projeto pelo Desktop após revisar o resultado, sem aplicar alterações às conexões ou relacionamentos. Persistência após salvar/reabrir ainda não foi testada nesta execução.

Consultas em docs/testes/lote2-3-1/, para reutilização na Exibição de Consulta DAX:

| Arquivo | Resultado/critério |
| --- | --- |
| 09-matriz-comparabilidade.dax | 1.755 linhas, todas Aprovado=true; diferenças ≤ R$ 0,01 e BlankDivergente=false. Compara com a view importada, não com a origem independente |
| 10-configuracao-materializacao.dax | Primeira saída: nove intervalos iguais ao manifesto, com datas tipadas, hash e versão. Há também EVALUATEs de metadados; o executor local usado registrou somente a primeira saída, complementada por 16–19 |
| 11-guardas-contexto.dax | Três linhas: datas parciais, total entre posições e posição/descrição conflitantes; números e pares BLANK, status explicativo |
| 12-sintetico-zero.dax | Expressões privadas de teste: R=0, O=-100, P=0 e um par. Não corresponde a valores reais da origem |
| 13-sintetico-blank.dax | Expressões privadas: R/O/P BLANK e um par de cobertura, demonstrando que cobertura não depende do indicador |
| 14-regressao-36-medidas.dax | 1.620 linhas com Aprovado=true, comparadas à view importada sem limitar as medidas antigas ao novo corte |
| 16/17/18/19 | 16 tabelas, 41 medidas Valid, 16 partições Ready e 18 relacionamentos; nenhuma relação com a configuração |

12/13 redefinem as bases e as cinco expressões no escopo da consulta; não alteram medidas persistidas. As expressões copiadas são as mesmas registradas em docs/evidencias/lote2-3-1-implementacao-20261103-085405/expressoes-novas.json. Não remover as redefinições das cinco novas: substituir apenas as bases não afetou as dependências persistidas na tentativa inicial e não gerou teste sintético válido. Essa tentativa foi preservada no histórico e não foi contabilizada como aprovação.

## SQL independente — próxima execução necessária

Abrir **docs/testes/lote2-3-1/15-conciliacao-databricks.sql** no SQL Editor, com o warehouse existente. Executar cada uma das duas instruções separadamente, somente leitura:

1. Preflight de grão: exportar `L231_SQL_preflight.csv`. Resultado esperado: zero linhas. Se retornar duplicações, interromper conciliação e registrar as chaves; não corrigir a view automaticamente.
2. Consulta financeira: exportar `L231_SQL_comparabilidade.csv`, com **1.755 linhas** e sem truncar. Campos grupo_filial, periodo, posicao, cenario, pares, contagens e valor. Preservar NULL; não arredondar o arquivo nem preencher zeros. Não somar posições entre si.

Guardar texto SQL/ID, data/hora/fuso e referência à atualização/snapshot da origem; confirmar que corresponde ao conjunto importado no Power BI. As datas constantes no SQL são a declaração independente do contrato didático, não descoberta por MAX de dados nem consulta à tabela de configuração do Power BI. O SQL considera os intervalos idênticos entre filiais desta versão; não certifica configurações futuras diferentes.

Comparar o CSV completo com o JSON DAX já executado:

```powershell
python docs/testes/lote2-3-1/comparar-conciliacao.py "C:\caminho\L231_SQL_comparabilidade.csv" docs/evidencias/lote2-3-1-diagnostico-20261103-090110/09-matriz-comparabilidade.json docs/evidencias/L231-conciliacao-sql.json
```

O caminho do CSV é ilustrativo; usar o arquivo realmente exportado. O comparador valida 1.755 chaves únicas, chaves ausentes/extras, NULL versus BLANK, contagem de pares e diferença monetária máxima R$ 0,01. Ele não valida sozinho data de atualização, autoridade do contrato ou o preflight: esses itens devem acompanhar o aceite. Ainda **não executado** com resultado Databricks deste sublote.

Grupos: 01, 02, 03, Consolidado e 01+02. Períodos: Integral, 2021, 2022, 2023, 2023_JanMai, 2023_JunDez, 2023_Maio, 2023_Junho e 2023_JanMar (janeiro e março sem fevereiro). Treze posições × três cenários. Posições 8/11 são NULL/BLANK; nos períodos sem Realizado fornecido, financeiros são NULL/BLANK e pares=0 nas posições elegíveis.

O esperado temporal vem do contrato; o DAX executado mede o modelo importado; o SQL fornecerá a resposta financeira independente do Databricks. Essas três fontes têm papéis distintos e nenhuma significa fechamento contábil real.
