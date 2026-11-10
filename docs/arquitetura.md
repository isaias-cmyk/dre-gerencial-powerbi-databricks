# Arquitetura — inventário estático da Fase 0

Registro em 02/11/2026, horário America/Sao_Paulo. Responsável: Codex, por solicitação do usuário. Este documento inventaria a estrutura serializada; não é auditoria de cardinalidade, de dados ou de comportamento de filtros da Fase 1.

## Estrutura encontrada

Raiz: `C:\Projetos\PowerBI\DRE Moderno - Databricks`.

- PBIP 1.0: `DRE Moderno - Databricks.pbip` → pasta `DRE Moderno - Databricks.Report`.
- PBIR 4.0: `Report/definition.pbir` → `../DRE Moderno - Databricks.SemanticModel`; schema definitionProperties 2.0.0.
- Relatório expandido: `definition/version.json` 2.0.0, `report.json` schema 3.3.0, `pages/pages.json` schema 1.1.0 e `page.json` schema 2.1.0.
- PBISM 4.2, schema definitionProperties 1.0.0; TMDL em `definition/`, incluindo database, model, relationships, tables e culture en-US.
- Cultura do modelo en-US; sourceQueryCulture pt-BR. Sem mudanças de cultura nesta fase.
- `diagramLayout.json`, arquivos `.platform`, tema Fluent2-CY26SU08 e `BaseDados.xlsx` presentes. A planilha não foi aberta nem confirmada como fonte ativa.
- A raiz tinha 37 arquivos antes da documentação desta fase; o inventário completo contém caminho, tamanho, data UTC e SHA-256 de cada um.

## Objetos do modelo

| Objeto de negócio | Papel e campos de referência observados |
| --- | --- |
| dim_calendario | data, ano, mes, dia, trimestre, ano_mes, inicio_mes, numero_ano_mes |
| dim_filial | cod_filial, filial |
| dim_conta | id_conta, ordem_conta, descricaon1, descricaon2, detalharn2, mascaradre_id, tipolancamento, cod_filial |
| dim_dre | id_dre, ordem_dre, descricao_dre, subtotal, filial, cod_filial |
| fato_lancamentos | competencia_data, planocontas_id, valor, cod_filial, campos de rastreabilidade |
| fato_orcamento | competencia_data, planocontas_id, valor, cod_filial, campos de rastreabilidade |
| fato_previsao | competencia_data, planocontas_id, valor, cod_filial, campos de rastreabilidade |
| vw_dre_comparativo | cod_filial, filial, competencia, ano, ordem_dre, descricao_dre, subtotal, realizado, orcado, previsto |

Há também uma DateTableTemplate e cinco LocalDateTable: 14 tabelas TMDL ao todo. Os nomes completos, colunas, tipos serializados, partições, modos e lineageTags estão em [tabelas.json](evidencias/fase0-20261102-145703/tabelas.json). Não se avaliou unicidade de chaves, tipos nos dados nem necessidade de manter/remover tabelas técnicas.

Nenhuma medida explícita encontrada nas declarações TMDL das tabelas. Colunas e tabelas calculadas de data não são medidas financeiras. Evidência: [medidas.json](evidencias/fase0-20261102-145703/medidas.json).

## Conexões

As oito tabelas de negócio têm partições M Import com `DatabricksMultiCloud.Catalogs`. As oito declarações usam o mesmo host e HTTP Path de warehouse, com navegação `workspace` → `gold` → objeto correspondente. Os sete objetos de dimensões/fatos estão declarados como Table e vw_dre_comparativo como View.

Os endpoints completos já presentes no projeto e a navegação por objeto estão em [conexoes.json](evidencias/fase0-20261102-145703/conexoes.json). Não foram copiados tokens ou credenciais para a documentação. Nenhuma conexão, consulta ou configuração local foi alterada. A conectividade, permissões, definição SQL das views e identificação contratual Free Edition não foram verificadas remotamente.

vw_dre_provisoria e vw_financeiro_comparativo não existem como tabelas importadas nesta estrutura. Sua existência na origem não foi consultada.

## Relacionamentos

[relacionamentos.json](evidencias/fase0-20261102-145703/relacionamentos.json) registra os 18 IDs, endpoints, propriedades serializadas e classificação técnica/de negócio.

- 13 de negócio: cinco ligações ativas padrão para dim_filial (dim_dre, três fatos, view), quatro para dim_calendario (três fatos e view), três de fatos para dim_conta e uma explicitamente inativa de dim_conta para dim_filial.
- Cinco técnicas: dim_calendario.data, dim_calendario.inicio_mes e _data_ingestao das três fatos para LocalDateTable.Date, com datePartOnly.
- Apenas a relação dim_conta.cod_filial → dim_filial.cod_filial declara `isActive: false`; as outras 17 omitem a propriedade. A interpretação ativa padrão continua sujeita à conferência no mecanismo.
- Cardinalidade e direção de filtros não estão explicitamente serializadas. Os valores efetivos não foram comprovados nesta fase.
- Não há relação direta serializada de dim_dre para a view ou dim_conta. A view não apresenta chave de conta. São pontos de atenção para a Fase 1, sem proposta de alteração nesta execução.

## Relatório e diferença em relação à inspeção anterior

Uma página `Page 1`, ID `18fcfac0c5446040d274`, 1920 × 1080, consta dos arquivos atuais. O tema base continua Fluent2-CY26SU08, em SharedResources/BaseThemes.

**Nenhum visual.json está presente no snapshot da Fase 0.** A inspeção de elaboração do PLANS.md havia encontrado o visual tableEx `1b0098a77ab3a933ca5c`, filtrado em ordem_dre 13. Esse arquivo já não estava na entrada desta execução. A causa não foi determinada; não foi removido nem recriado nesta fase. O backup representa os arquivos efetivamente presentes, sem reconstruir versões anteriores.

Evidências: [paginas.json](evidencias/fase0-20261102-145703/paginas.json), [visuais.json](evidencias/fase0-20261102-145703/visuais.json), [temas.json](evidencias/fase0-20261102-145703/temas.json).

## Inventário e controle de versão

- [Inventário JSON](evidencias/fase0-20261102-145703/inventario-arquivos.json) e [CSV](evidencias/fase0-20261102-145703/inventario-arquivos.csv).
- Git 2.47.1.windows.2 instalado; status e rev-parse retornaram código 128, pasta fora de repositório. Não há branch, commit ou alterações não commitadas determináveis. Nenhum repositório foi inicializado.
- `.gitignore` existente exclui localSettings.json e cache.abf em .pbi. Não foi alterado. A exclusão de editorSettings e backups deverá ser avaliada antes de eventual adoção do Git.
- Antes desta execução não havia docs, testes nem backups. Agora existem docs/evidencias e backups; não foi criada suíte de testes do modelo.
- Backup e recuperação descritos em [validacoes.md](validacoes.md). Fase 1 não iniciada.

## Adendo — inspeção estática da Fase 1 em 02/11/2026

O registro acima preserva o diagnóstico da Fase 0. A auditoria posterior está em [auditoria-modelo-semantico.md](auditoria-modelo-semantico.md), com 56 colunas de negócio detalhadas e inventário completo das 18 relações. Endpoints e tipos TMDL são compatíveis, sem referência de tabela ausente detectada.

Os caminhos de filtro foram analisados sob hipótese unidirecional To → From, sem confirmação no mecanismo: Conta alcança as três fatos, mas não a view; a dimensão DRE não transmite posição à view. Ativar Filial–Conta criaria caminhos alternativos para as fatos. Nenhuma correção ou reorganização foi aplicada.

Fase 1: **Bloqueado** para aceite até testar chaves, integridade, calendário e filtros em dados/mecanismo e aprovar abordagem DRE/detalhamento por conta. Fase 2 não iniciada.
