# L2.3.2 — Desvios Financeiros e Comparações Orçamentárias

Data: 03/11/2026. **Em planejamento; zero medidas implementadas neste sublote.** Contratos revisados e consultas futuras preparadas, sem execução DAX/SQL nesta entrega. L2.3.3 não iniciado.

## 1. Base real conferida e escopo definitivo

AGENTS.md, PLANS.md, plano do Lote 2.3, contratos das medidas, contrato de cobertura didática e validação L2.3.1 consultados. O aceite vigente de L2.3.1 consta de [aceite.json](evidencias/lote2-3-1-homologacao-20261103/aceite.json): persistência aprovada, nove intervalos, 41 medidas Valid e 1.755 chaves SQL/DAX aprovadas, 600 NULL/BLANK coincidentes, diferença máxima R$ 0,00000010. É evidência anterior, não reexecução nesta tarefa; não certifica fechamento contábil.

_Medidas.tmdl foi lido integralmente e as 41 expressões/dependências inventariadas em [inventario-41-medidas.json](evidencias/lote2-3-2-planejamento-20261103/inventario-41-medidas.json). Encontradas 36 medidas financeiras anteriores e as cinco de comparabilidade. **Nenhum dos quatro nomes M40–M43 existe como medida persistida.** Eles já constam da proposta original e serão reutilizados exatamente, sem nomes alternativos ou duplicações.

Recomendação: **quatro medidas genéricas novas**, na mesma tabela _Medidas, pasta `DRE\Desvios`. Após implementação aprovada: 45 medidas, 16 tabelas e 18 relacionamentos. Não criar tabela, configuração, relacionamento, fonte ou página adicional. Não recriar medidas por indicador/filial/cenário. Não alterar nenhuma das 41 existentes.

Fora do escopo: favorabilidade, classificação, impacto, cumprimento, cores, margens novas, YTD, rankings, wrappers de cartões, EBITDA/EBIT e L2.3.3. Resultado Líquido conserva caráter provisório.

## 2. Arquitetura e dependências

```text
_ConfigCobertura + dim_filial + dim_calendario
                  ↓ mecanismo já homologado no L2.3.1
Realizado Comparável (M37) + Orçado Comparável (M38) + Previsto Comparável (M39)
                  ↓ sem novo cálculo de cobertura ou financeiro nas fatos
M40 = R − O          M42 = R − P
M41 = M40 / |O|      M43 = M42 / |P|
M49 (pares) + M50 (status) → diagnóstico e testes, sem conversão em valor financeiro
```

Reutilizar exatamente:

- `DRE | Realizado Comparável` — R, fonte do realizado no recorte comum.
- `DRE | Orçado Comparável` — O, referência orçamentária equivalente.
- `DRE | Previsto Comparável` — P, referência prevista equivalente.
- `DRE | Pares Filial-Competência Comparáveis` — diagnóstico de cardinalidade, não denominador monetário.
- `DRE | Status Comparabilidade` — diagnóstico temporal/ausência; não será alterado nem interpretado como favorabilidade.

As quatro novas dependem financeiramente de M37–M39 e, indiretamente, do mecanismo aprovado. M49/M50 serão reutilizadas nos resultados de teste e na explicação do contexto, sem repetir 100 linhas de lógica temporal em cada nova fórmula. Não consultar _ConfigCobertura ou as fatos para reconstruir valores nas novas medidas; não usar bases antigas não comparáveis como fallback.

## 3. Contratos comuns — obrigatórios para cada medida

Estas regras integram individualmente os quatro contratos da seção seguinte.

| Campo contratual | Regra definitiva para o planejamento |
| --- | --- |
| Posição da DRE | Uma posição elegível de vw_dre_comparativo[ordem_dre] e descrição compatível; herdar guardas das comparáveis. Campos da view são os eixos gerenciais; dim_dre não filtra a view automaticamente |
| Filial | Respeitar dim_filial: 01, 02, 03, consolidado e 01+02, sem acrescentar outras filiais ou remover seus filtros. Herdar corte comum entre as filiais selecionadas |
| Calendário | Respeitar dim_calendario e meses completos efetivamente selecionados; seleções não consecutivas não incluem meses intermediários. Datas parciais/ausência de cobertura/inconsistência herdam BLANK e diagnóstico do L2.3.1 |
| Cobertura | Contrato DIDATICA-1.0-20261103 e _ConfigCobertura existentes. Neste conjunto Realizado disponibilizado Jan/2021–Mai/2023, referências Jan/2021–Dez/2023. Nenhuma data fixa nas novas expressões |
| Múltiplas posições | Nenhuma/múltiplas posições, descrição conflitante e posições 8/11 → BLANK; não somar as 13 linhas nem calcular EBITDA/EBIT |
| Total | Mesma posição entre filiais/meses: avaliar operandos comparáveis no contexto total. Monetário é diferença dos agregados; percentual é razão dos agregados. Total entre posições é BLANK. Não somar/médias simples de percentuais |
| Sinal | R − referência, valores já ajustados; nenhum tipolancamento, inversão de sinal, ABS no numerador ou no valor financeiro. Zero legítimo preservado |
| BLANK | Testar ISBLANK em R e referência antes da operação; se algum faltar, BLANK. Não usar COALESCE, `+0`, FORMAT numérico ou resultado alternativo zero na divisão |
| Referência negativa | Permitida. Monetário conserva R−X; percentual usa ABS(X) somente no denominador e conserva o sinal do numerador |
| Referência zero | Monetário válido se R presente: R−0. Somente percentual retorna BLANK por denominador zero. R=0 com referência não zero é um valor presente |
| Favorabilidade | Nenhuma classificação automática por sinal ou percentual. Desvio positivo pode resultar de aumento de receita, menor gasto negativo ou mudança de sinal; natureza e política pertencem ao L2.3.3 |
| Conta / estrutura DRE | Não criar propagação fictícia de dim_conta/dim_dre à view. Preservar limitações existentes e não ativar relacionamentos para atender estes desvios |
| Critério numérico | Sem arredondamento na expressão. Comparar BRL com tolerância máxima R$ 0,01 e percentuais com diferença absoluta ≤ 0,00000001 na razão decimal, conforme plano original. Correspondência de BLANK e sinal é obrigatória, independente da tolerância |
| Aceite funcional | Compilar/executar no Desktop, filtros/totais/ausência corretos, zero/negativo/sinal sintéticos, regressão das 41, persistência, SQL independente e integridade dos arquivos protegidos |

Uma referência incompleta em qualquer par já retorna BLANK da comparável desse cenário. O outro cenário pode permanecer válido. Não diminuir o conjunto de R para ocultar falta de O/P. M49=0 diagnóstico não autoriza resultado monetário zero; M50 não é uma certificação contábil.

## 4. Quatro contratos específicos e DAX proposto

O DAX abaixo é **especificação documental, não implementação nem teste executado**. Não foi escrito em _Medidas.tmdl. A sintaxe de ausência/divisão foi conferida com a documentação oficial [ISBLANK](https://learn.microsoft.com/en-us/dax/isblank-function-dax) e [DIVIDE](https://learn.microsoft.com/en-us/dax/divide-function-dax); isso não substitui compilação/execução futura no mecanismo.

### M40 — DRE | Desvio Realizado x Orçado (R$)

- **Finalidade:** diferença monetária do Realizado para Orçado no mesmo contexto comparável.
- **Dependências diretas:** DRE | Realizado Comparável e DRE | Orçado Comparável. M49/M50 como diagnóstico, dependência temporal indireta da configuração.
- **Fórmula:** R−O. Não há denominador; O negativo preservado e O=0 válido se R presente.
- **Contextos, múltiplas posições, total, sinais e BLANK:** todas as regras comuns da seção 3; total na mesma posição calcula R_total−O_total.
- **Formato:** `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`, tipo numérico, pasta DRE\Desvios.
- **Aceite específico:** diferença igual à subtração das duas comparáveis/SQL equivalente, com ausências correspondentes, sinal preservado e erro ≤ R$ 0,01; R/O ausentes não viram zero, O=0 não torna monetário BLANK.

```dax
VAR _R = [DRE | Realizado Comparável]
VAR _O = [DRE | Orçado Comparável]
RETURN
    IF ( ISBLANK ( _R ) || ISBLANK ( _O ), BLANK (), _R - _O )
```

### M41 — DRE | Desvio Realizado x Orçado (%)

- **Finalidade:** diferença relativa normalizada em relação ao Orçado comparável, sem inferir favorabilidade ou cumprimento.
- **Dependências diretas:** M40, DRE | Realizado Comparável e DRE | Orçado Comparável; mesmas dependências indiretas/diagnósticas da seção 2.
- **Fórmula:** M40/ABS(O) = (R−O)/ABS(O). O negativo permitido; O=0 ou R/O ausentes → BLANK.
- **Contextos, múltiplas posições, sinais e BLANK:** seção 3; total calcula (R_total−O_total)/ABS(O_total), nunca soma ou média dos percentuais.
- **Formato:** `0.00%;(0.00%);0.00%`, numérico decimal, pasta DRE\Desvios. 0,20 deve renderizar 20,00% conforme cultura/visual, não multiplicar por 100 na medida.
- **Aceite específico:** divisão protegida, sinal igual ao desvio quando denominador positivo, negativos/zero/ausentes demonstrados; diferença ≤ 1E-8 na razão. Não substituir o denominador por ABS de parcelas somadas, nem pela soma dos ABS mensais.

```dax
VAR _R = [DRE | Realizado Comparável]
VAR _O = [DRE | Orçado Comparável]
VAR _D = [DRE | Desvio Realizado x Orçado (R$)]
RETURN
    IF (
        ISBLANK ( _R ) || ISBLANK ( _O ) || _O = 0,
        BLANK (),
        DIVIDE ( _D, ABS ( _O ) )
    )
```

### M42 — DRE | Desvio Realizado x Previsto (R$)

- **Finalidade:** diferença monetária do Realizado para Previsão no mesmo contexto comparável.
- **Dependências diretas:** DRE | Realizado Comparável e DRE | Previsto Comparável; M49/M50 diagnósticos e dependência indireta da configuração.
- **Fórmula:** R−P. Sem denominador; referência negativa mantém o sinal, P=0 válido se R presente.
- **Contextos, múltiplas posições, total, sinais e BLANK:** seção 3; total na mesma posição R_total−P_total.
- **Formato:** `R$ #,##0.00;(R$ #,##0.00);R$ 0.00`, numérico, pasta DRE\Desvios.
- **Aceite específico:** diferença das comparáveis e SQL equivalente com ausências/sinais idênticos, erro ≤ R$ 0,01; falta de Previsão não deve impedir comparação com Orçado válido.

```dax
VAR _R = [DRE | Realizado Comparável]
VAR _P = [DRE | Previsto Comparável]
RETURN
    IF ( ISBLANK ( _R ) || ISBLANK ( _P ), BLANK (), _R - _P )
```

### M43 — DRE | Desvio Realizado x Previsto (%)

- **Finalidade:** diferença relativa normalizada em relação à Previsão comparável.
- **Dependências diretas:** M42, DRE | Realizado Comparável e DRE | Previsto Comparável; mesmas indiretas/diagnósticas.
- **Fórmula:** M42/ABS(P) = (R−P)/ABS(P). P negativo permitido; P=0 ou R/P ausentes → BLANK.
- **Contextos, múltiplas posições, sinais e BLANK:** seção 3; total é razão dos agregados comparáveis, nunca soma/média das razões.
- **Formato:** `0.00%;(0.00%);0.00%`, decimal numérico, pasta DRE\Desvios.
- **Aceite específico:** ausência, zero e negativo preservados; erro ≤ 1E-8 na razão; percentual positivo não recebe interpretação favorável implícita.

```dax
VAR _R = [DRE | Realizado Comparável]
VAR _P = [DRE | Previsto Comparável]
VAR _D = [DRE | Desvio Realizado x Previsto (R$)]
RETURN
    IF (
        ISBLANK ( _R ) || ISBLANK ( _P ) || _P = 0,
        BLANK (),
        DIVIDE ( _D, ABS ( _P ) )
    )
```

## 5. Compatibilidade e diferenças do plano histórico

1. **Nomes, quantidade e fórmulas:** compatíveis com os M40–M43 originais; nenhuma medida equivalente persistida foi encontrada. Usar `x` no nome, exatamente como no plano, sem trocar por ×.
2. **Máscara temporal:** trechos antigos recomendavam presença de Realizado da posição. Foram superados pelo corte comum configurado no L2.3.1. Nenhum novo MAX/data fixa ou máscara por movimento nesta fase.
3. **Baseline:** testes antigos citam 36 medidas e 14 futuras. Para este sublote, preservar **41** e acrescentar **quatro**, total futuro **45**, sem implementar M44–M48.
4. **Fonte alternativa:** a definição já recebida de vw_financeiro_comparativo possui colunas de desvio por conta, mas esse grão e a ausência do mecanismo de cobertura comparável não equivalem às quatro medidas gerenciais; não importar nem somar seus percentuais como solução.
5. **Diagnóstico:** M50 atual explica cobertura/ausência, sem diagnóstico específico de mudança de sinal ou favorabilidade. O texto mais amplo do plano original não autoriza modificar M50 neste sublote.
6. **Zero:** a frase “denominador zero → BLANK” aplica-se às duas medidas percentuais. O plano original já permite monetário com referência zero; os quatro contratos tornam essa distinção explícita.

Não há incompatibilidade funcional impeditiva com o escopo vigente. As diferenças são atualização do contexto já aprovado; não justificam alterar medidas antigas. Análise documental não prova que o DAX proposto compile ou tenha desempenho satisfatório no mecanismo.

## 6. Matriz de testes planejados — todos não executados

| ID | Natureza e cobertura | Critério objetivo / artefato |
| --- | --- | --- |
| P01 | Estático: nomes/quantidade/expressões/arquivos antes e depois | 41 antigas idênticas; exatamente quatro novas, 45 totais; 16 tabelas/18 relações/configuração/conexões/páginas intactas; parser sem erros |
| D01 | Dados importados, 01/02/03, consolidado e 01+02 × nove recortes × 13 posições × quatro medidas | **2.340 células previstas**, igualdade com álgebra das comparáveis, mesmo BLANK e sinal; 01-matriz-desvios-planejada.dax |
| D02 | Dados importados, mesmos cinco grupos × 36 competências individuais × 13 posições × quatro medidas | **9.360 células previstas**, incluindo cada mês de 2021/2022 e Jan–Dez/2023; 02-mensal-desvios-planejada.dax |
| D03 | Períodos: Integral, 2021, 2022, 2023, JanMai/2023, JunDez/2023, maio, junho e janeiro+março/2023 | D01; janeiro+março não inclui fevereiro. JunDez/junho sem R → quatro BLANK; Orçado/Previsto selecionados antigos continuam disponíveis |
| S01 | Sintético: 15 pares R/X positivos, negativos, iguais, zero, ausentes e mudanças de sinal | 03-sinteticos-contrato-planejados.dax e 07-sinteticos-contrato-planejados.sql; álgebra pura, não origem real nem medidas persistidas |
| S02 | Sintético futuro de integração com as quatro expressões | Repetir 15 casos contra Orçado/Previsto, verificando M40–M43; após implementação, redefinir comparáveis e cópias idênticas das quatro expressões apenas na consulta. Não confiar em override somente das dependências persistidas (limitação identificada no L2.3.1). Ainda sem execução/resultado |
| G01 | Dias parciais, total entre posições, posição/descrição conflitantes | 04-guardas-desvios-planejadas.dax: quatro BLANK em cada um dos três contextos |
| G02 | Totais entre filiais/meses, referência total negativa, zero por compensação e valores mistos | Monetário soma das diferenças no mesmo conjunto; percentual razão dos agregados. Se referência total=0, percentual BLANK mesmo que parcelas tenham razão; não comparar com soma de percentuais |
| R01 | Regressão financeira e temporal das 41 medidas | Reutilizar 09/14 de L2.3.1; 36 antigas com seus contextos e cinco comparáveis/pares/status com todos os contextos já aceitos. Comparar a valores/BLANK/textos da baseline final, sem alterar os roteiros históricos |
| R02 | Metadados/materialização/persistência | Reutilizar 16–19 de L2.3.1, conferir nove linhas de configuração/versão/hash; 45 medidas válidas após salvar/fechar/reabrir. Sem novos relacionamentos |
| Q01 | SQL independente agregado e preflight | 05-desvios-databricks-planejados.sql: primeiro resultado zero duplicações; segundo **2.340 linhas** nas mesmas chaves de D01 |
| Q02 | SQL independente mensal e preflight | 06-mensal-databricks-planejado.sql: primeiro zero duplicações; segundo **9.360 linhas** nas mesmas chaves de D02 |
| Q03 | Comparação exportações | Preservar CSVs/hashes, mesmo snapshot quando identificável, comparar grupo/período/posição/ID/unidade, pares, R/X, valor e ausência; adaptar comparador em escopo futuro sem alterar o comparador homologado de L2.3.1 |
| V01 | Formatação/visual | Valores BRL e razão decimal, negativos e zero legíveis no Desktop, sem FORMAT numérico ou multiplicação percentual por 100; verificar total de matriz |

Os testes DAX D01/D02 usam comparáveis importadas como esperado **algébrico**; não são conciliação independente. Q01/Q02 fornecem valores financeiros SQL independentes do Power BI no mesmo contrato. S01/S02 são sintéticos e não comprovam origem financeira. Nenhuma linha de “Aprovado” emitida pelos scripts existe como resultado enquanto a consulta não for executada.

**Sintéticos de referência (R/X, desvio, percentual em razão):** 120/100→20/0,2; 80/100→−20/−0,2; −120/−100→−20/−0,2; −80/−100→20/0,2; −20/−100→80/0,8; 0/100→−100/−1; 20/0→20/BLANK; 0/0→0/BLANK; R ou X ausente→BLANK/BLANK; 100/−100→200/2. São expectativas contratuais, sem interpretação favorável/desfavorável e sem aprovação de execução.

## 7. Consultas SQL previstas e estratégia de conciliação

Roteiros em [docs/testes/lote2-3-2](testes/lote2-3-2/), **não executados**. 05 e 06 reutilizam o SQL de comparáveis homologado de L2.3.1, incluindo preflight, competência/cenário, contagens e preservação de NULL; acrescentam apenas uma camada SQL de desvio monetário/relativo. Não recalculam os indicadores nas fatos, não reaplicam tipolancamento e não leem a configuração Power BI como prova de origem.

Fluxo previsto:

```text
CTE cobertura (contrato didático explícito e versionado)
→ meses/grupos/períodos/posições
→ pares comuns (três filiais com os mesmos intervalos homologados)
→ contagens esperadas + LEFT JOIN da vw_dre_comparativo
→ valores comparáveis por cenário, com completude/NULL preservados
→ R/O/P por chave
→ quatro métricas, R−X e (R−X)/ABS(X), com guardas NULL/zero
```

Exportações futuras: `L232_SQL_preflight.csv` (ou captura identificável de zero linhas), `L232_SQL_desvios_agregados.csv` (2.340), `L232_SQL_desvios_mensais.csv` (9.360), `L232_SQL_sinteticos.csv` (15, pasta separada). DAX: CSV/JSON completos dos roteiros 01–04, sem truncamento, mais regressão/metadados reutilizados. Não juntar sintéticos ao comparador financeiro real.

Comparar sinal antes de tolerância, NULL/BLANK antes de aritmética, contagens de pares e operandos antes do desvio. Percentuais exportados como razão, não texto com `%`. Datas fixas em CTEs/testes representam a versão do contrato de referência; não serão inseridas nas quatro medidas. Alteração de configuração futura invalida esses esperados até atualização formal dos testes. Os SQLs atuais não generalizam cortes distintos entre filiais não existentes nesta versão.

Registrar SQL/ID, data/hora/fuso, atualização/versão da fonte e modelo quando disponíveis. A homologação anterior não identificou o commit exato do CSV SQL; não alegar essa rastreabilidade retroativamente nem confundir coincidência de valores com identidade de versões.

## 8. Riscos remanescentes

| Risco | Mitigação |
| --- | --- |
| Subtração DAX tratar BLANK como zero | ISBLANK explícito em ambos os operandos antes de calcular |
| Percentual com referência negativa inverter leitura | Denominador ABS(X), numerador assinado; rótulo de desvio, sem favorabilidade |
| Zero por compensação no total | Percentual BLANK com X_total=0; monetário permanece definido |
| Arredondamento/precisão DECIMAL versus modelo | Comparar sem arredondar a expressão; tolerâncias por unidade; investigar valores próximos de zero sem criar epsilon de negócio |
| Somar razões ou posições gerenciais | Razão dos agregados; total entre posições BLANK; teste de totais explícito |
| Comparar 2023 parcial com referência anual | Somente M37–M39 como fontes; nenhum SUM direto de coluna nas medidas propostas |
| Cobertura didática confundida com dado presente/fechado | M49/M50 diagnósticos e versão/hash preservados; 21 pares JunDez não fornecidos, não processados-vazios certificados |
| Mudar o contrato ou snapshot durante o teste | Registrar versão/hash e identificar atualização; revisar esperados e repetir conciliação pertinente |
| Evidências antigas com nomes “bloqueado/não implementado” | Aceite final L2.3.1 e este plano prevalecem cronologicamente; não reiniciar auditoria nem recriar configuração |
| Teste privado não substituir dependências de medidas persistidas | Integrar sintéticos com expressões privadas idênticas após implementação e registrar a limitação; teste algébrico sozinho não encerra o sublote |

## 9. Critérios de aceite e sequência futura

1. Autorizar explicitamente a implementação exclusiva destas quatro medidas. Antes de editar: ler instruções, conferir Git/alterações, confirmar Desktop fechado e criar backup novo/restaurável com SHA-256.
2. Preservar a baseline de **41 medidas**, configuração, relacionamentos e páginas. Acrescentar somente M40/M42 e depois M41/M43, com IDs próprios e pasta aprovada; sem modificar model.tmdl ou conexões para este escopo.
3. Parser sem erro e 45 medidas válidas no mecanismo; executar D01/D02/G01/G02/V01 e sintéticos, registrando casos reais e privados separadamente. Aprovar todos os casos esperados, zero divergências não justificadas, sinais e BLANK exatos, limites por unidade.
4. Regressão financeira/temporal/textual das 41 existentes e integridade dos arquivos; materialização e persistência após salvar/fechar/reabrir sem regressão.
5. SQL independente agregado e mensal completos, preflight sem duplicações, chave/operandos/cardinalidade/valor conciliados. Nenhum teste não executado pode receber estado aprovado.
6. Documentar resultados, falhas e limites em validação própria do L2.3.2 e atualizar PLANS.md. Somente então propor o aceite técnico. Não liberar automaticamente L2.3.3.

**Recomendação:** contratos coerentes e escopo tecnicamente pronto para autorização de implementação, sujeito às verificações de segurança e execução dos testes. Esta entrega **não é autorização implícita nem implementação**, e não conclui o L2.3.2.

## 10. Rollback previsto

Somente em futura implementação: usar backup obtido imediatamente antes de L2.3.2, com as **41 medidas aceitas e _ConfigCobertura já existente**. Não usar backup de 36 medidas para reverter este sublote.

Se houver erro de abertura, sintaxe, cobertura/regressão ou conciliação sem solução aprovada: registrar falha e chaves; fechar Desktop; conferir caminhos/alterações posteriores; restaurar apenas _Medidas.tmdl da baseline pertinente (ou retirar somente os quatro novos blocos/IDs após revisão). Preservar trabalhos posteriores e documentação das falhas; não sobrescrever projeto inteiro, remover a configuração, restaurar credenciais/cache ou alterar relações. Revalidar parser, 41 medidas, nove intervalos e testes de controle antes de declarar recuperação. ZIP sem teste de restauração não é backup aprovado.

## 11. Evidências desta entrega

- Inventário das 41 expressões e confirmação de ausência dos nomes propostos: docs/evidencias/lote2-3-2-planejamento-20261103/inventario-41-medidas.json.
- Baseline de hashes dos arquivos protegidos: baseline-producao.json, na mesma pasta.
- Quantidades e estado previsto dos testes: testes-previstos.json, na mesma pasta.
- Gerador documental dos roteiros: docs/evidencias/lote2-3-2-preparar-testes.py, sem execução de consultas ou edição de produção.

Status dos testes DAX/SQL do L2.3.2: **NÃO EXECUTADOS**. Revisão de contratos e arquivos é estática. Nenhuma das 41 medidas, configurações, conexões, relacionamentos ou páginas foi modificada nesta tarefa.
