# Fase 5 — Homologação (bateria completa)

Data: 09/11/2026. Modelo aberto no Desktop (estado do commit da Fase 4); Databricks somente leitura (`workspace.gold`). Nada foi alterado no modelo, no relatório ou no Databricks durante os testes. Estado: **homologação técnica concluída; pendências P1–P5 corrigidas em 09/11/2026 (seção 3).**

## 1. Resultado geral

| ID | Teste | Resultado |
| --- | --- | --- |
| H1 | Inventário | 10 tabelas (5 visíveis), 13 relacionamentos (12 ativos, nenhum bidirecional), 61 medidas sem erro, todas com descrição e pasta; expressões do modelo = TMDL salvo (61/61) |
| H2a | Indicadores base × SQL independente (fatos + `dim_conta` + `dim_dre`, sem usar a view), filial × mês × 11 linhas (1–7, 9, 10, 12, 13) | 9/9 conjuntos (3 cenários × 3 filiais) idênticos: 319 células Realizado e 396 Orçado/Previsto por filial; Σ, Σ\|v\|, Σv·linha·mês, Σv² e totais de Receita Líquida, Margem e Resultado Líquido iguais (statement `01f1dc7a-9c53-149c-81e7-7307fd5577b4`) |
| H2b | 33 medidas nomeadas por linha × medida genérica, filial × mês | 1.188/1.188 (231 BLANK coincidentes: Jun–Dez/2023 do Realizado) |
| H3 | Comparáveis, Desvio R$/%, Impacto, Classificação e Cumprimento × SQL independente; 5 grupos de filiais × 7 recortes × linhas 3, 5 e 13 | **1.260/1.260**; 240 BLANK/NULL coincidentes; dif. máx. R$ 4,5E-8, razão 9,6E-16 (statement `01f1dc7a-d698-1ce9-92dc-16703be0b6f9`) |
| H3b | Regressão das 50 medidas de DRE × foto do Lote 3.2 (feita em 09/11 no mesmo estado) | 53.300/53.300 |
| H4 | Medidas por conta × Databricks (T2 repetido no modelo reaberto) | 9/9 conjuntos, 1.247 células cada, iguais ao SQL de 09/11 |
| C01 | Controles | Receita Líquida 146.417.811,17; Margem 52.828.995,11; Resultado Líquido 5.038.227,39 (Realizado, consolidado, período inteiro); Comparável RL 2023 819.957,24 / Orçado 813.676,11 |

Conclusão técnica: **os indicadores do relatório conferem com o Databricks dentro de R$ 0,01 em todos os testes, com BLANK/NULL preservados.**

## 2. Revisão de layout, navegação e acessibilidade (H5)

| Página | Visuais | Situação |
| --- | --- | --- |
| Executiva | 23 (13 cartões, linha, cascata, 3 segmentações, 5 textos) | ok |
| DRE | 7 (matriz, cartão, 3 segmentações, 2 textos) | ok |
| Filiais | 8 (matriz, 2 barras, cartão, 2 segmentações, 2 textos) | ok |
| Receitas / Despesas | 8 cada (matriz, barras, cartão, 3 segmentações, 2 textos) | ok; rolagem horizontal da matriz e barras com todas as contas por decisão do usuário |

Verificado sem problema: nenhum visual fora da página ou sobreposto; ordem de tabulação única em todas as páginas; nenhuma medida inexistente; nenhum filtro em colunas da view (só `ordem_dre`/`descricao_dre`); segmentações nas dimensões.

### Pendências encontradas

| # | Pendência | Impacto | Esforço |
| --- | --- | --- | --- |
| P1 | Nenhum dos 54 visuais tem texto alternativo | Acessibilidade (leitor de tela, WCAG) | Baixo: só metadados |
| P2 | Segmentações não sincronizadas entre páginas: filtrar uma filial na Executiva não vale para a DRE | Navegação; risco de leitura com recortes diferentes | Baixo |
| P3 | Subtítulos automáticos em inglês ("and", "by") nos gráficos | Cosmético; vem da cultura en-US do modelo (limitação já registrada) | Baixo: desligar subtítulo ou escrever o texto |
| P4 | Medidas de cor (`DRE \| Cor…`, `Conta \| Cor x Orçado`) visíveis na lista de campos | Cosmético; boa prática é ocultar medidas técnicas | Baixo |
| P5 | Sem botões de navegação entre páginas (só as abas) | Opcional; as abas atendem no Desktop e no Serviço | Médio |

## 3. Correções aplicadas (09/11/2026, decisão do usuário: corrigir 1 a 5)

Backup: `backups/fase5-correcoes-pre-20261109-1740/` (`pages-pre.zip` com as 58 definições de página/visual + `_Medidas.tmdl` + manifesto SHA-256; hash do zip conferido no disco).

| # | Correção | Como |
| --- | --- | --- |
| P1 | Texto alternativo em todos os 54 visuais | `visualContainerObjects.general.altText` com descrição do conteúdo (título, campos, regra de cores) |
| P2 | Segmentações sincronizadas | `syncGroup` Filial, Ano e Mes nas 14 segmentações (Filiais não tem segmentação de filial, por desenho) |
| P3 | Subtítulos automáticos em inglês removidos | `subTitle.show = false` nos 6 gráficos |
| P4 | Medidas de cor ocultas | `isHidden` em `DRE \| Cor Classificação x Orçado/Previsto` e `Conta \| Cor x Orçado` (via MCP; expressões inalteradas; TMDL conferido) |
| P5 | Navegador de páginas (revertido, ver abaixo) | Visual `pageNavigator` no canto superior direito das 5 páginas |

Conferência: o usuário reabriu o projeto sem erro (09/11/2026 17:42); navegador funcionando nas 5 páginas e subtítulos removidos (prints).

**P5 revertido em 09/11/2026 (decisão do usuário):** o navegador duplicava as abas e no Desktop só responde com Ctrl+clique. Os 5 visuais `*0navegacao0000000h` foram ocultos e depois excluídos pelo usuário; títulos voltaram à largura original. Na mesma rodada, a matriz da DRE passou a 520 px de altura (última linha visível) e os cartões de EBITDA/EBIT desceram 30 px. Backup: `backups/fase5-navegador-pre-20261109-2120/pages-pre.zip`.

Rollback: com o Desktop fechado, extrair `pages-pre.zip` sobre `DRE Moderno - Databricks2.Report/definition/pages/` (apagando as pastas `*0navegacao0000000h`) e restaurar `_Medidas.tmdl`.

### Aceite de negócio (09/11/2026)

- **Resultado Líquido aceito**: sufixo "(provisório)" removido das classificações M46/M47, das pastas/descrições e dos textos das páginas (backup `backups/fase5-rl-pre-20261109-2020/`). Regressão: 1.620/1.680 valores idênticos; 60 classificações da linha 13 só perderam o sufixo.
- **EBITDA e EBIT homologados pelo padrão de mercado (CVM)** como medidas DAX novas; a view do Databricks não traz valores nessas linhas. Ver [plano-ebitda-ebit.md](plano-ebitda-ebit.md).
- **Base didática (DIDATICA-1.0)**: projeto encerrado como portfólio/estudo; README e [checklist-publicacao.md](checklist-publicacao.md) entregues.
