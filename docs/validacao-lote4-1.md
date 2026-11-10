# Lote 4.1 — Contas contábeis: implementação e validação

Data: 09/11/2026. Plano e decisões: [plano-lote4-1-contas.md](plano-lote4-1-contas.md). Estado: **concluído em 09/11/2026** (persistência conferida no TMDL salvo: 61 medidas, 52 antigas idênticas ao backup; colunas e ordenações gravadas; model.tmdl e relationships.tmdl inalterados).

Backup prévio: `backups/lote4-1-pre-20261109-1450/` (14 arquivos do SemanticModel + manifesto SHA-256).

## 1. Alterações (via MCP, modelo aberto no Desktop)

### `dim_conta`

| Coluna | Tipo | Visível | Regra |
| --- | --- | --- | --- |
| `linha_dre` | calculada, texto | sim | `LOOKUPVALUE ( dim_dre[descricao_dre], dim_dre[id_dre], dim_conta[mascaradre_id] )`; ordenada por `ordem_dre` |
| `ordem_dre` | calculada, inteiro | não | `LOOKUPVALUE ( dim_dre[ordem_dre], … )` |
| `grupo_conta` | calculada, texto | sim | cópia de `descricaon1`; ordenada por `ordem_grupo` |
| `conta` | calculada, texto | sim | cópia de `descricaon2`; ordenada por `ordem_subconta` |
| `ordem_grupo` / `ordem_subconta` | calculadas, inteiro | não | menor `ordem_conta` do grupo / da conta (`MINX` sobre `ALLNOBLANKROW`) |

- Tabela `dim_conta` voltou a ficar visível. Ocultas: `id_conta`, `ordem_conta`, `descricaon1`, `descricaon2`, `detalharn2`, `mascaradre_id`, `tipolancamento`, `cod_filial`.
- Por que `grupo_conta`/`conta` em vez de ordenar `descricaon1`/`descricaon2`: o Power BI não permite ordenar uma coluna por outra calculada a partir dela (dependência circular). A cópia de exibição é a solução padrão; as colunas originais seguem intactas e ocultas.
- Recálculo das colunas: atualização do tipo **Calculate** (só recalcula objetos calculados no próprio modelo; não consulta o Databricks nem altera dados importados).

### Medidas novas (`_Medidas`, pasta `Contas`)

| Medida | Formato | Regra |
| --- | --- | --- |
| `Conta \| Realizado Comparável` | R$ | Σ(valor × `tipolancamento`) em `fato_lancamentos`, sob a mesma máscara e as mesmas guardas de cobertura de `DRE \| Realizado Comparável` |
| `Conta \| Orçado Comparável` | R$ | idem em `fato_orcamento`; exige cobertura de Orçado |
| `Conta \| Previsto Comparável` | R$ | idem em `fato_previsao`; exige cobertura de Previsto |
| `Conta \| Desvio x Orçado (R$)` / `x Previsto (R$)` | R$ | R − X; BLANK se faltar operando |
| `Conta \| Desvio x Orçado (%)` / `x Previsto (%)` | % | (R − X) ÷ \|X\|; BLANK se faltar operando ou X = 0 |
| `Conta \| Classificação x Orçado` | texto | \|desvio\| ≤ R$ 0,01 (+1E-9) → "Em linha"; > 0 → "Favorável"; < 0 → "Desfavorável"; BLANK sem desvio |
| `Conta \| Cor x Orçado` | texto | #107C10 / #C50F1F / #605E5C (mesma paleta da DRE) |

Nenhuma das 52 medidas existentes, relacionamento, `_ConfigCobertura` ou visual foi alterado. Total: 61 medidas.

## 2. Testes

| ID | Teste | Resultado |
| --- | --- | --- |
| T1 | Σ contas por linha DRE (`dim_conta[ordem_dre]`) × M37/M38/M39, em 5 grupos de filiais × 12 recortes × 8 linhas | **480/480** nos três cenários; 120 BLANK coincidentes; dif. máx. R$ 8,9E-8 |
| T2 | SQL independente no Databricks (`workspace.gold`, statement `01f1dc66-65d6-138f-8c58-ca3e3a829f0f`): filial × mês × conta × cenário com sinal, meses com Realizado | 9/9 conjuntos (3 cenários × 3 filiais) idênticos: 29 meses e 1.247 células cada (3.741 por cenário); Σv, Σ\|v\|, Σv·ordem, Σv·ordem·mês e Σv² iguais até o arredondamento (≤ 1E-4) |
| T3 | Bordas: mês parcial (01–15/03/2022), Jun–Dez/2023, conta de outra filial | Todos BLANK |
| T3b | Classificação, cor e Desvio % em 3.741 células filial × mês × conta | 3.741/3.741 conforme regra (1.826 Favorável, 1.898 Desfavorável, 17 Em linha) |
| C01 | Controle: Σ de todas as contas em 2023 = Resultado Líquido Comparável 2023 | 819.957,24 = 819.957,24 |
| R1 | Foto das 50 medidas do Lote 3.2 (filial × ano × mês com subtotais × posição × descrição, 2022–2023) | **53.300/53.300 idênticas**, diferença 0 |
| D01 | Desempenho: matriz linha → grupo → conta, 2022, 8 medidas | 723 ms (cache frio do plano) |

## 3. Pendente

- Concluído: TMDL conferido após salvar.
- Páginas Receitas e Despesas: concluídas ([fase4-paginas-receitas-despesas.md](fase4-paginas-receitas-despesas.md)).

## 4. Rollback

Com o Desktop fechado, restaurar `tables/_Medidas.tmdl` e `tables/dim_conta.tmdl` de `backups/lote4-1-pre-20261109-1450/` e reabrir.

Aceite técnico/didático; não homologa fechamento, EBITDA, EBIT ou Resultado Líquido.
