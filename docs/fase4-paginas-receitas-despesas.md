# Fase 4 — Páginas Receitas e Despesas

Data: 09/11/2026. Base: Lote 4.1 ([validacao-lote4-1.md](validacao-lote4-1.md)). Estado: **concluída em 09/11/2026** (abertas no Desktop sem erro; totais conferidos: Receitas = Receita Líquida 146.417.811,17; Receitas − Despesas = Resultado Líquido 5.038.227,39). Por decisão do usuário, a matriz mantém as 7 colunas com rolagem horizontal e as barras mostram todas as contas.

## 1. Decisões do usuário

Período comparável (igual às demais páginas); sinal da DRE; escopo por linha da DRE: Receitas = linhas 1 e 2, Despesas = linhas 4, 6, 7, 9, 10 e 12.

## 2. Layout (1920 × 1080, igual nas duas páginas)

| Visual | Conteúdo |
| --- | --- |
| Título | Receitas: "Receita Bruta e Deduções por conta"; Despesas: "Custos, despesas e demais gastos por conta" |
| Segmentações | Filial, Ano, Mês (cópias das da página DRE, mesmos campos das dimensões) |
| Cartão de recorte | `DRE \| Status Comparabilidade` (filtro de visual na posição 13, como nas demais páginas) |
| Matriz | Linhas `linha_dre` → `grupo_conta` → `conta`; valores Realizado, Orçado, Desvio x Orç. (R$ e %), Previsto, Desvio x Prev. (R$ e %); desvios x Orçado coloridos por `Conta \| Cor x Orçado`; subtotais por linha e grupo |
| Barras | Desvio x Orçado (R$) por conta, ordem crescente (piores primeiro), cor pela classificação; dica com Realizado, Orçado, Desvio % e Classificação |
| Nota | Escopo, convenção de sinal, período comparável, regra "Em linha" |

Filtro de página (oculto no modo de leitura): `dim_conta[ordem_dre]` em {1, 2} (Receitas) e {4, 6, 7, 9, 10, 12} (Despesas). Na página Receitas, o total da matriz é a Receita Operacional Líquida.

## 3. Arquivos

Novos: `pages/rec0pagina00000000a1/` e `pages/des0pagina00000000a1/` (page.json + 8 visuais cada). Alterado: `pages/pages.json` (ordem: Executiva, DRE, Filiais, Receitas, Despesas). Backup: `backups/fase4-recdes-pre-20261109-1505/` (pages.json + manifesto SHA-256, hash conferido).

## 4. Rollback

Com o Desktop fechado: apagar as duas pastas de página e restaurar `pages.json` do backup.
