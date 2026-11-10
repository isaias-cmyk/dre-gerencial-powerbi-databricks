# Checklist de publicação (portfólio)

Data: 09/11/2026. Objetivo: publicar o projeto como peça de portfólio (repositório Git e, opcionalmente, Power BI Service). Nenhum item abaixo foi executado; publicação e deploy exigem autorização.

## 1. Segurança e privacidade

| # | Item | Situação | Ação |
| --- | --- | --- | --- |
| S1 | Credenciais no repositório | Nenhum token/senha encontrado; `mcp.json.txt`, `.env`, `*.key`, `*.pem` no `.gitignore` | Manter |
| S2 | Host do workspace Databricks e ID do SQL Warehouse gravados nas 8 partições TMDL | Não são credenciais, mas identificam o seu workspace | Recomendado antes de repositório público: criar parâmetros M `DatabricksHost` e `DatabricksHttpPath` e usá-los nas partições (mudança de modelo; exige autorização) |
| S3 | `backups/` | Fora do Git (`.gitignore`) | Manter |
| S4 | `docs/evidencias/` | Scripts e saídas de teste; contém `__pycache__` (ignorado) | Revisar se há caminhos locais ou nomes de usuário antes de tornar público |
| S5 | Cache do Desktop (`.pbi/cache.abf`, `localSettings.json`) | No `.gitignore` | Manter |

## 2. Conteúdo do repositório

- [x] `README.md` com objetivo, páginas, arquitetura, validação e limitações.
- [x] `PLANS.md` e `docs/` com planos, validações e homologação.
- [ ] Capturas de tela das 5 páginas em `docs/img/`, recortadas só na área do relatório (sem barra de título do Windows e nome de usuário).
- [ ] Licença (ex.: MIT para o código; dados fictícios declarados no README).
- [ ] Decidir se `AGENTS.md` e `CLAUDE.md` ficam públicos (mostram o processo de trabalho com IA; não têm dados sensíveis).

## 3. Power BI Service (opcional)

- [ ] Publicar em workspace pessoal (exige autorização).
- [ ] Configurar credenciais da fonte Databricks no Service e, se houver atualização agendada, o gateway/conexão de nuvem.
- [ ] Conferir após publicar: 5 páginas, navegador, segmentações sincronizadas, cartão de recorte comparável e os controles do README.
- [ ] "Publicar na Web" só se aceitar que o relatório fique público sem autenticação.

## 4. Antes do commit final

- [ ] `git status` sem arquivos inesperados (`*.abf`, `.env`, `mcp.json*`).
- [ ] Abrir o PBIP limpo (sem cache) e confirmar que carrega.
- [ ] Conferir os controles: Receita Líquida 146.417.811,17; Resultado Líquido 5.038.227,39.
