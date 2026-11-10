# Lote 4.1 — Contas contábeis (base das páginas Receitas e Despesas)

Data: 08/11/2026. Estado: **implementado e validado no modelo em 09/11/2026** ([validacao-lote4-1.md](validacao-lote4-1.md)); páginas pendentes.

## 1. Diagnóstico (somente leitura, modelo Power BI)

- `dim_conta`: 43 contas por filial (129 linhas), dois níveis (`descricaon1` → `descricaon2`), sinal em `tipolancamento` (+1 receita, −1 dedução/gasto) e linha da DRE em `mascaradre_id` → `dim_dre[id_dre]` (1 linha DRE por conta, todas as contas mapeadas na filial 01).
- Relacionamentos já existentes: `fato_*[planocontas_id]` → `dim_conta[id_conta]`; `fato_*[cod_filial]` → `dim_filial`; `fato_*[competencia_data]` → `dim_calendario[data]`. Não há relação conta → linha DRE.
- **Conciliação global (período inteiro, todas as filiais): Σ(valor × tipolancamento) por linha DRE = `vw_dre_comparativo` nas 8 linhas analíticas e nos 3 cenários.** Ex.: Receita Bruta R 199.326.296,52 / O 247.514.660,85 / P 247.322.501,03; Despesas Operacionais R −46.203.238,52; Outras Receitas e Despesas R −150.388,21 (contas + e −).
- Uma relação direta `dim_conta` → `dim_dre` criaria dois caminhos até `dim_filial` (ambiguidade); por isso a linha DRE entra como coluna calculada em `dim_conta`.

## 2. Decisões do usuário (08/11/2026)

| Tema | Decisão |
| --- | --- |
| Período | Comparável, igual às páginas DRE/Executiva/Filiais (meses com Realizado em todas as filiais selecionadas) |
| Sinal | Sinal da DRE: receitas +, deduções e gastos −; desvio positivo = favorável |
| Escopo | Receitas = linhas 1 e 2 (Receita Bruta, Deduções → Receita Líquida). Despesas = linhas 4, 6, 7, 9, 10 e 12 |

## 3. Implementação proposta

1. **Colunas calculadas em `dim_conta`** (não financeiras): `linha_dre` (descrição da linha DRE) e `ordem_dre` (posição), via `LOOKUPVALUE` em `dim_dre`; `linha_dre` ordenada por `ordem_dre`. Na implementação, grupo e conta ganharam colunas de exibição `grupo_conta` e `conta` (ordenadas pela menor `ordem_conta`), porque ordenar `descricaon1`/`descricaon2` por coluna derivada delas gera dependência circular. Tabela `dim_conta` volta a ficar visível; colunas técnicas (`id_conta`, `mascaradre_id`, `detalharn2`, `tipolancamento`, `cod_filial`) ocultas.
2. **Medidas novas** (pasta `Contas`), sem alterar as 52 existentes:
   - `Conta | Realizado Comparável`, `Conta | Orçado Comparável`, `Conta | Previsto Comparável`: Σ(valor × sinal) limitado ao período comparável, com as mesmas guardas de `_ConfigCobertura` das medidas Comparáveis (configuração inválida, mês parcial, filial sem cobertura, lacuna → BLANK; Orçado/Previsto exigem também cobertura do próprio cenário). Diferença deliberada: não exigem lançamento em todo par filial/mês, porque uma conta pode não ter movimento num mês.
   - `Conta | Desvio x Orçado (R$)` e `(%)`, `Conta | Desvio x Previsto (R$)` e `(%)`: mesma álgebra de M40–M43.
   - `Conta | Classificação x Orçado` e `Conta | Cor x Orçado`: mesma regra de M46 (±R$ 0,01), sem sufixo "provisório".
3. **Páginas** Receitas e Despesas: matriz linha DRE → grupo (`descricaon1`) → conta (`descricaon2`) com Realizado, Orçado, Previsto, desvios e classificação colorida; maiores desvios por conta (barras); filtros Filial/Ano/Mês e cartão de recorte.

## 4. Testes

| ID | Teste | Critério |
| --- | --- | --- |
| T1 | Σ contas comparáveis por linha DRE = M37/M38/M39, em 5 grupos de filiais × 45 recortes × 8 linhas | Diferença ≤ R$ 0,01 onde M37–M39 têm valor |
| T2 | SQL independente no Databricks: filial × mês × conta × cenário com sinal | ≤ R$ 0,01; NULL/BLANK coincidentes |
| T3 | Casos de borda: Jun–Dez/2023, mês parcial, filial sem cobertura | BLANK |
| R1 | Foto das 52 medidas existentes antes × depois | 100% idênticas |

Requisito: SQL Warehouse ligado para T2.

## 5. Backup e rollback

Backup completo do PBIP antes da escrita. Rollback: restaurar `_Medidas.tmdl` e `dim_conta.tmdl` (e as páginas, quando criadas).
