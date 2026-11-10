# DRE Moderno — Instrucoes para Claude Code

Leia AGENTS.md e PLANS.md antes de iniciar qualquer trabalho.

## Objetivo
Desenvolver, corrigir, otimizar e validar o Power BI DRE Moderno.

## Autonomia
- Consultar e executar DAX sem confirmacoes repetitivas.
- Criar e corrigir medidas DAX de baixo risco no modelo local.
- Documentar alteracoes e resultados.
- Usar powerbi-modeling para desenvolvimento autorizado.
- Usar databricks-local exclusivamente para leitura.

## Seguranca
- Fazer e verificar backup restauravel antes de alteracoes estruturais.
- Pedir autorizacao para exclusoes, mudancas financeiras, refresh e publicacao.
- Preservar BLANK, NULL e contratos financeiros existentes.
- Nao modificar dados ou objetos no Databricks.
- Nao ignorar controles de permissao.

## Validacao
Comparar SQL e DAX no mesmo contexto de filial, periodo e posicao.
Aplicar tolerancia monetaria de R$ 0,01 quando prevista.
Registrar testes, divergencias e procedimento de reversao.
