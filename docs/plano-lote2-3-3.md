# L2.3.3 — Impacto, classificação e cumprimento (M44–M48)

Data: 04/11/2026. Base: [plano-lote2-3.md](plano-lote2-3.md) seções 3, 5, 6 e 11; L2.3.2 aceito em 04/11/2026 ([validacao-lote2-3-2.md](validacao-lote2-3-2.md)).

## 1. Decisões do usuário (04/11/2026)

| # | Tema | Decisão |
| --- | --- | --- |
| 1 | Favorabilidade | **Impacto no lucro em todas as linhas com valor** (1–7, 9, 10, 12, 13). Como a view grava gastos com sinal negativo, Realizado − Referência > 0 sempre aumenta o resultado → favorável. Direção D(p) = +1 para todas as posições elegíveis |
| 2 | Resultado Líquido | Recebe impacto e classificação, com sufixo **"(provisório)"** no texto |
| 3 | Neutralidade | **"Em linha" se \|impacto\| ≤ R$ 0,01**, sobre valores não arredondados. Faixas de materialidade ficam para a camada visual |
| 4 | Cumprimento | Só **posições 1 e 3**, com Orçado > 0 e Realizado ≥ 0 |

EBITDA (8) e EBIT (11) continuam fora: as medidas retornam BLANK.

### Evidência de sinais na base (consulta DAX 04/11/2026, 108 pares filial/mês por posição)

| Posições | Sinal observado em R, O e P |
| --- | --- |
| 1, 3, 5, 13 | sempre > 0 |
| 2, 4, 6, 7, 9, 10 | sempre < 0 |
| 12 (IR/CSLL) | misto (meses com crédito positivo) |

Com a convenção de impacto no lucro, o sinal misto do IR não exige tratamento especial: R − X continua sendo o efeito no resultado. Isso substitui a guarda "regime de sinais" da seção 5 do plano-mãe, que só era necessária na leitura por magnitude.

## 2. Contratos

| ID | Nome | Pasta | Formato | Regra |
| --- | --- | --- | --- | --- |
| M44 | DRE \| Impacto Favorável x Orçado (R$) | DRE\Desempenho | `R$ #,##0.00;(R$ #,##0.00);R$ 0.00` | = M40 se posição elegível; senão BLANK. M40 BLANK → BLANK |
| M45 | DRE \| Impacto Favorável x Previsto (R$) | DRE\Desempenho | idem | = M42 nas mesmas condições |
| M46 | DRE \| Classificação x Orçado | DRE\Desempenho | texto | M44 BLANK → BLANK; \|M44\| ≤ 0,01 → "Em linha"; > 0 → "Favorável"; < 0 → "Desfavorável"; posição 13 acrescenta " (provisório)" |
| M47 | DRE \| Classificação x Previsto | DRE\Desempenho | texto | idem sobre M45 |
| M48 | DRE \| Cumprimento Orçamentário (%) | DRE\Desempenho | `0.00%;(0.00%);0.00%` | M37 ÷ M38 só nas posições 1/3, com M38 > 0 e M37 ≥ 0; senão BLANK. Consistência: M48 = 1 + M41 |

Contratos comuns:
- Reutilizam M37, M38, M40 e M42; não recalculam valores nem cobertura. Herdam o corte comum, meses completos, BLANK entre posições e a regra de totais (razão dos agregados).
- **Texto BLANK sem dados** (prática de modelagem): classificações retornam BLANK quando não há impacto, em vez de "Sem dados comparáveis". Medidas de texto sempre preenchidas expandem matrizes com linhas vazias. O motivo da ausência continua em M50 `DRE | Status Comparabilidade`. Desvio dos rótulos sugeridos no plano-mãe, registrado aqui.
- Folga de ponto flutuante de 1E-9 na comparação com R$ 0,01.
- Sem cores, sem YTD, sem alteração das 45 medidas existentes, `_ConfigCobertura`, relacionamentos ou visuais.

## 3. Expressões

```dax
-- M44 (M45 idêntica com [DRE | Desvio Realizado x Previsto (R$)])
VAR _Desvio = [DRE | Desvio Realizado x Orçado (R$)]
VAR _Posicao = SELECTEDVALUE ( 'vw_dre_comparativo'[ordem_dre] )
VAR _Elegivel = _Posicao IN { 1, 2, 3, 4, 5, 6, 7, 9, 10, 12, 13 }
RETURN
    IF ( ISBLANK ( _Desvio ) || NOT _Elegivel, BLANK (), _Desvio )

-- M46 (M47 idêntica com [DRE | Impacto Favorável x Previsto (R$)])
VAR _Impacto = [DRE | Impacto Favorável x Orçado (R$)]
VAR _Posicao = SELECTEDVALUE ( 'vw_dre_comparativo'[ordem_dre] )
VAR _Tolerancia = 0.01
VAR _Folga = 0.000000001
VAR _Classe =
    SWITCH (
        TRUE (),
        ISBLANK ( _Impacto ), BLANK (),
        ABS ( _Impacto ) <= _Tolerancia + _Folga, "Em linha",
        _Impacto > 0, "Favorável",
        "Desfavorável"
    )
RETURN
    IF ( ISBLANK ( _Classe ), BLANK (), _Classe & IF ( _Posicao = 13, " (provisório)", "" ) )

-- M48
VAR _Posicao = SELECTEDVALUE ( 'vw_dre_comparativo'[ordem_dre] )
VAR _R = [DRE | Realizado Comparável]
VAR _O = [DRE | Orçado Comparável]
RETURN
    IF (
        NOT ( _Posicao IN { 1, 3 } ) || ISBLANK ( _R ) || ISBLANK ( _O ) || _O <= 0 || _R < 0,
        BLANK (),
        DIVIDE ( _R, _O )
    )
```

## 4. Testes

| ID | Teste | Critério |
| --- | --- | --- |
| S01 | Sintéticos da seção 7 do plano-mãe com cópias das expressões (DATATABLE) | 100% conforme tabela esperada |
| D01 | Grade agregada 5 grupos × 9 recortes × 13 posições × 5 medidas | Regras da seção 2 aplicadas sobre M37/M38/M40/M42 do próprio modelo; 0 divergências |
| D02 | Grade mensal 5 × 36 × 13 × 5 | idem |
| Q01/Q02 | SQL independente: classificação e impacto derivados das saídas SQL do L2.3.2 (Databricks); cumprimento por consulta SQL própria (posições 1/3) | Impacto R$ 0,01; razão 1E-8; texto idêntico; BLANK/NULL coincidentes |
| G01 | Total entre posições, posições 8/11, datas parciais | BLANK |
| R01 | Regressão: 45 medidas com expressão idêntica ao backup; controles RL e Comparável | Sem diferença |
| R02 | Persistência após salvar | `_Medidas.tmdl` com 50 medidas; 45 antigas idênticas |

## 5. Rollback

Com o Desktop fechado, restaurar `DRE Moderno - Databricks2.SemanticModel/definition/tables/_Medidas.tmdl` de `backups/lote2-3-3-pre-20261104-1325/` (45 medidas; SHA-256 no `manifesto.json`). Reabrir e conferir 45 medidas.

Aceite técnico/didático; não homologa fechamento, EBITDA, EBIT ou Resultado Líquido.
