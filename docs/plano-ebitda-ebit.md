# Fase 5 — EBITDA e EBIT (padrão de mercado)

Data: 09/11/2026. Estado: **plano aprovado; implementação pendente (Desktop aberto).**

## 1. Diagnóstico

`workspace.gold.vw_dre_comparativo` traz as linhas 8 (EBITDA) e 11 (EBIT) **sem valor** em todos os meses, filiais e cenários (statement `01f1dc94-967c-1e8e-883b-a1d7e9416f15`). Não há o que conciliar: era preciso definir a fórmula.

## 2. Decisões do usuário (09/11/2026)

| Tema | Decisão |
| --- | --- |
| Fórmula | Padrão de mercado (Resolução CVM 156, antiga ICVM 527): EBITDA = Margem de Contribuição + Despesas Operacionais + Outras Receitas e Despesas; EBIT = EBITDA + Depreciação e Amortização. Resultado Financeiro e IR/CSLL ficam abaixo do EBIT |
| Implementação | Medidas DAX novas; as 61 medidas existentes e o Databricks não mudam |
| Resultado Líquido | Aceito; sufixo "(provisório)" removido (medidas M46/M47 e textos das páginas) |

Identidade de controle: Resultado Líquido = EBIT + Resultado Financeiro + IR/CSLL (fecha em R$ 0,00 nos três cenários).

| Cenário (consolidado, período inteiro) | EBITDA | EBIT |
| --- | --- | --- |
| Realizado | 6.475.368,38 | 6.188.060,91 |
| Orçado | 8.460.586,44 | 8.100.193,13 |
| Previsto | 7.995.184,87 | 7.635.015,48 |

## 3. Medidas (pasta `DRE\EBITDA e EBIT`)

Para cada indicador (EBITDA e EBIT):

| Medida | Regra |
| --- | --- |
| Realizado / Orçado / Previsto | Soma das medidas nomeadas por linha; BLANK se a Margem de Contribuição do cenário for BLANK |
| Realizado / Orçado / Previsto Comparável | Soma de `DRE \| … Comparável` nas linhas componentes; BLANK se qualquer componente for BLANK |
| Desvio x Orçado / x Previsto (R$ e %) | Mesma álgebra de M40–M43 |
| Classificação x Orçado / x Previsto | Mesma regra de M46/M47 (±R$ 0,01) |

## 4. Testes

| ID | Teste | Critério |
| --- | --- | --- |
| E1 | Comparáveis × SQL independente, 5 grupos × 7 recortes | ≤ R$ 0,01; NULL/BLANK coincidentes |
| E2 | Identidade RL = EBIT + Res. Financeiro + IR/CSLL nos mesmos recortes | ≤ R$ 0,01 |
| E3 | Base (não comparável) × SQL por filial × mês | ≤ R$ 0,01 |
| R1 | 61 medidas existentes inalteradas (expressões e grade H3) | 100% |

## 5. Rollback

Restaurar `_Medidas.tmdl` de `backups/fase5-rl-pre-20261109-2020/` (antes da retirada do "provisório") ou excluir a pasta `DRE\EBITDA e EBIT`.
