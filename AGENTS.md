# DRE Moderno — Regras compartilhadas para agentes

## Escopo
Projeto Power BI DRE Moderno com Databricks.

## Operacoes permitidas
- Inspecionar modelos, medidas, tabelas e relacionamentos.
- Executar consultas DAX e SQL somente leitura.
- Criar e corrigir medidas DAX de baixo risco no Power BI.
- Melhorar documentacao e organizacao.

## Operacoes que exigem autorizacao
- Excluir tabelas, colunas, medidas ou relacionamentos.
- Alterar relacionamentos, particoes ou regras contabeis.
- Modificar medidas financeiras homologadas.
- Publicar, executar deploy ou refresh completo.
- Sobrescrever arquivos ou objetos relevantes.

## Regras de protecao
- Verificar backup restauravel antes de mudancas estruturais.
- Databricks permanece exclusivamente para leitura.
- Nunca armazenar tokens ou credenciais no projeto.
- Nao contornar mecanismos de seguranca.

## Regras financeiras
- Preservar BLANK/NULL como diferentes de zero.
- Conciliar Realizado, Orcado e Previsto.
- Comparar contextos equivalentes de filial e periodo.
- Usar tolerancia de R$ 0,01 nas conciliacoes monetarias.
- Nao considerar EBITDA, EBIT ou Resultado Liquido provisorio homologados sem aceite.

## Processo
Diagnosticar, planejar, executar alteracoes autorizadas,
validar DAX e SQL, documentar resultados e atualizar PLANS.md.
