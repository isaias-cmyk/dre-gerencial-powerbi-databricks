# Execução do roteiro único — L2.3.1

Roteiro: `docs/testes/lote2-3-1/08-roteiro-unico-competencias.sql`. Consolida os SQLs 05, 07 e 06, sem substituir os originais. Somente leitura, sem criação de objetos, inclusive temporários. Não executado remotamente pelo agente.

No SQL Editor do Databricks, usar o warehouse existente e selecionar **uma instrução por vez**. Exportar o resultado completo antes de seguir; não enviar apenas o último resultado do arquivo. Preservar cabeçalhos, NULL e códigos de filial com zero inicial. Não executar como DDL o texto retornado por SHOW CREATE nem executar automaticamente instruções geradas no B06.

## Resultados a exportar

| Arquivo CSV | Instrução / resultado |
| --- | --- |
| A01_schemas.csv | Schemas acessíveis |
| A02_controles_candidatos.csv | Objetos com nomes/comentários relacionados a controle, em todos os schemas acessíveis |
| A03_campos_candidatos.csv | Colunas/comentários de competência, processamento, completude, fechamento e rastreabilidade |
| A04_views.csv | Definições das três views, se autorizadas |
| A05_definicao_dre.csv | SHOW CREATE da view, somente texto |
| A06_rastreabilidade_gold.csv | Grupos de origem/ingestão, datas e contagens da fato Realizado |
| B01_objetos_camadas.csv | Inventário Bronze/Silver/Gold com catálogo e comentários |
| B02_colunas_camadas.csv | Todas as colunas reais das três camadas |
| B03_detail_gold.csv | DESCRIBE DETAIL da fato Gold |
| B04_propriedades_gold.csv | Propriedades da fato Gold |
| B05_history_gold.csv | Histórico completo retido; executar após confirmar formato Delta no DETAIL |
| B06_instrucoes_metadados.csv | Instruções geradas como texto; selecionar somente objetos pertinentes e executar manualmente conforme formato/permissão |
| B07_fora_grade.csv | Filiais/datas nulas ou sem correspondência nas dimensões |
| C01_grade108.csv | 108 pares fixos, contagens Gold/view, lacunas e último movimento |
| D01_dimensoes108.csv | Presença/unicidade das filiais e dias de calendário dos 108 pares |
| D02_resumo_gold.csv | Contagens, chaves nulas/fora do universo e limites de ingestão |
| E01_schema.csv / E01_amostra.csv | Silver flancamentos: colunas detalhadas e cinco registros |
| E02_schema.csv / E02_amostra.csv | Gold fato_lancamentos: colunas detalhadas e cinco registros |
| E03 a E11, cada um schema e amostra | Nove tabelas Bronze, na ordem filial 1 anos 1–3, filial 2 anos 1–3, filial 3 anos 1–3 |

São **38 resultados diretos** (seis A, sete B, um C, dois D e 18+4 E). Resultados vazios devem ser exportados com cabeçalho ou registrados explicitamente como zero linhas. Guardar também erros de autorização/objetos não suportados, SQL/ID das consultas, data/hora e fuso. Os resultados de amostra podem conter dados pessoais: compartilhar apenas em contexto autorizado, sem credenciais.

Para completar o histórico entre camadas, B06 permite selecionar `workspace.silver.flancamentos` e as nove tabelas Bronze identificadas. Executar DETAIL, propriedades e HISTORY (apenas Delta), exportando cada saída com o nome da tabela. Não é necessário inspecionar histórico de tabelas de orçamento para provar carga do Realizado. Permissões e retenção podem limitar o histórico.

## Como interpretar

- C01 deve ter exatamente 108 chaves distintas: três filiais × 36 meses de 2021–2023. Esse intervalo fixo é o universo do diagnóstico solicitado; **não é a regra definitiva do corte temporal**.
- A grade independe de linhas de movimento e do calendário. D01 testa a correspondência com as dimensões; B07 e D02 impedem ocultar registros fora desse universo. C01 agrega fatos e view separadamente, evitando multiplicação pelas 13 posições.
- Contagem zero significa ausência de registros observados no snapshot. Não significa carga concluída sem movimento. O SQL não preenche valores financeiros; zeros/NULL monetários permanecem distintos na origem.
- Lacuna intermediária é mês sem lançamentos entre o primeiro e último mês observado da mesma filial. Ausência de lacunas não demonstra completude. Contagens iguais nas camadas também não substituem manifesto de registros esperados/rejeitados.
- A06 e E examinam rastreabilidade. Amostras não provam ausência de campos/estados no conjunto completo: usar B02 para o schema completo. A distribuição completa mensal e a reconciliação Bronze→Silver dependem dos nomes/tipos efetivamente retornados; não presumir colunas de competência nem regra de filial nessas camadas.
- Se A02/A03/B02 revelar controle candidato, enviar seu schema e contrato antes de preparar o SELECT de registros. É necessário conhecer as chaves e os estados reais para verificar todos os pares esperados sem inventar campos. Pode haver mecanismo em pipelines/manifestações externas não exposto no catálogo; registrar essa limitação.

**Carga técnica:** commit/ingestão/contagem e execução. **Cobertura temporal:** certificado de completude por filial/mês/cenário, inclusive meses sem movimento e versões/rejeições. **Fechamento contábil:** estado autorizado pela Controladoria, com reabertura e data/rastreabilidade. Uma categoria não comprova automaticamente as demais.

O aceite exige fonte autoritativa e política aprovada, não apenas um número de linhas ou último mês com valor. Após receber os CSVs, conciliar os pares, registrar divergências e decidir se a evidência atende ao contrato. Até lá, L2.3.1 bloqueado; 36 medidas preservadas e nenhum outro sublote iniciado.


## Primeira rodada prioritária — descoberta de controle

Executar primeiro, nesta ordem, **A01 → A02 → A03 → B02 → B04**: cinco consultas e cinco CSVs. Os identificadores A01–A06 correspondem às instruções numeradas 1–6 do bloco A; B02 é a segunda instrução do bloco B e B04 é o SHOW TBLPROPERTIES da fato Gold. Selecionar somente a instrução correspondente; não executar os 38 resultados nesta rodada. SQL original preservado.

| Identificador original | Objetivo | CSV esperado | Evidência possível | Critério de interpretação |
| --- | --- | --- | --- | --- |
| A01 | Delimitar os schemas acessíveis | A01_schemas.csv | Alcance visível da busca no catálogo workspace | Schema listado demonstra visibilidade; ausência não comprova inexistência nem acesso a todos os objetos. Registrar permissões/erros. |
| A02 | Localizar objetos candidatos a manifesto, carga, auditoria ou fechamento em todos os schemas visíveis | A02_controles_candidatos.csv | Nome, tipo, catálogo e comentário de possível controle | Candidato precisa declarar o grão filial/competência/cenário e a semântica de seus estados. Nome ou comentário isolado não homologa. Resultado vazio significa nenhum candidato encontrado por esse padrão e privilégio, não inexistência global. |
| A03 | Buscar campos de competência, filial, cenário, estados e rastreabilidade, mesmo em tabelas com nomes genéricos | A03_campos_candidatos.csv | Tipos e comentários de campos que podem formar um certificado mensal | Procurar em um mesmo mecanismo chaves temporais/filial, carga/completude, confirmação de mês sem movimento e autoridade de fechamento. Apenas data de ingestão/status técnico não prova completude ou fechamento. Filtro por palavras pode omitir campos com outros nomes. |
| B02 | Examinar todas as colunas das camadas, sem filtro por nome de campo | B02_colunas_camadas.csv | Schema completo visível Bronze/Silver/Gold, inclusive campos omitidos pela busca A03 | Permite avaliar se os objetos visíveis têm estrutura para controle mensal e rejeitar hipóteses sobre campos inexistentes nesses objetos. Falta de campos não exclui controle em outro objeto/schema, pipeline ou manifesto externo. |
| B04 | Procurar propriedades explícitas ou referências a contrato/manifesto na fato Gold | B04_propriedades_gold.csv | Propriedades de workspace.gold.fato_lancamentos e eventual referência a mecanismo externo | Propriedades Delta técnicas/compressão não certificam carga mensal. Referência de governança exige consultar a fonte e validar contrato/estados. Nenhuma propriedade, por si só, comprova fechamento contábil dos 108 pares. |

Exportar integralmente, inclusive resultados vazios com cabeçalho; registrar erro se não houver permissão. Anexar SQL/ID, horário/fuso e limitações conhecidas de acesso. Não é necessário repetir B05/history neste primeiro passo: o commit já recebido comprova carga técnica e foi identificado pelo usuário como pertencente à fato Gold, mas não certifica competências.

**Limite desta rodada:** são consultas de descoberta de metadados. Elas podem identificar um controle candidato ou refutar uma hipótese específica sobre objetos/campos visíveis; não demonstram ausência global de controle e não substituem a consulta aos registros do certificado. Se surgir candidato, o próximo passo é conferir seu schema completo/contrato e então consultar seus estados reais por filial/competência/cenário, sem inventar campos ou implementar o controle.

Contexto registrado: **87 pares com lançamentos e 21 pares sem lançamentos observados na matriz de 108 pares**. No terceiro CSV, os 21 pares não aparecem como registros: foram identificados por diferença para a grade esperada, em coerência com o diagnóstico local anterior. A cobertura desses 21 pares **ainda não foi certificada**. Ausência de lançamento não significa ausência de processamento, nem certifica processamento completo. Os 87 pares com movimento também não estão automaticamente certificados como completos/fechados.

C01, A06, amostras E e históricos complementares ficam para a rodada dirigida pelos resultados; não são prioridades para descobrir um certificado existente. O critério de liberação continua sendo evidência autoritativa de cobertura, inclusive mês sem movimento, e política aprovada de fechamento. L2.3.1 permanece bloqueado; nenhuma nova consulta remota executada pelo agente nesta organização.
