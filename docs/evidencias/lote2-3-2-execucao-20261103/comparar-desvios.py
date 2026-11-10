"""Comparador L2.3.2 — desvios M40–M43, SQL independente (Databricks) x DAX (Power BI).

Uso:
    python comparar-desvios.py L232_SQL_desvios_agregados.csv L232_DAX_desvios_agregados.csv
    python comparar-desvios.py L232_SQL_desvios_mensais.csv L232_DAX_desvios_mensais.csv 9360 comparacao-desvios-mensal.json

Chave: grupo_filial, periodo, posicao, id. O CSV SQL é a segunda saída de
docs/testes/lote2-3-2/05-desvios-databricks-planejados.sql (2.340 linhas).
Critérios do plano (seção 3): BLANK/NULL devem coincidir antes da aritmética;
BRL com tolerância de R$ 0,01; razão com tolerância de 0,00000001; sinal igual.
Não altera nenhum arquivo; apenas imprime o resumo e grava um JSON ao lado.
Não substitui o comparador homologado do L2.3.1.
"""
import csv
import json
import sys
from pathlib import Path

TOL = {"M40": 0.01, "M42": 0.01, "M41": 0.00000001, "M43": 0.00000001}


def num(texto):
    texto = (texto or "").strip()
    if texto == "" or texto.upper() in ("NULL", "NONE", "NAN"):
        return None
    return float(texto.replace(",", ".")) if texto.count(",") == 1 and "." not in texto else float(texto)


def ler(caminho, col_grupo, col_valor):
    dados = {}
    duplicadas = 0
    with open(caminho, newline="", encoding="utf-8-sig") as f:
        for linha in csv.DictReader(f):
            chave = (linha[col_grupo].strip(), linha["periodo"].strip(), int(float(linha["posicao"])), linha["id"].strip())
            if chave in dados:
                duplicadas += 1
            dados[chave] = num(linha[col_valor])
    return dados, duplicadas


def main(sql_csv, dax_csv, esperadas=2340, nome_saida="comparacao-desvios.json"):
    sql, dup_sql = ler(sql_csv, "grupo_filial", "valor")
    dax, dup_dax = ler(dax_csv, "grupo_filial", "valor")
    ausentes = sorted(set(dax) - set(sql))
    extras = sorted(set(sql) - set(dax))
    aprovadas = reprovadas = nulos_coincidentes = 0
    max_dif = {"BRL": 0.0, "Razao": 0.0}
    falhas = []
    for chave in sorted(set(sql) & set(dax)):
        s, d = sql[chave], dax[chave]
        unidade = "BRL" if chave[3] in ("M40", "M42") else "Razao"
        if s is None or d is None:
            ok = s is None and d is None
            nulos_coincidentes += ok
        else:
            dif = abs(s - d)
            max_dif[unidade] = max(max_dif[unidade], dif)
            mesmo_sinal = (s > 0) == (d > 0) or abs(s) <= TOL[chave[3]] or abs(d) <= TOL[chave[3]]
            ok = dif <= TOL[chave[3]] and mesmo_sinal
        if ok:
            aprovadas += 1
        else:
            reprovadas += 1
            falhas.append({"chave": chave, "sql": s, "dax": d})
    resumo = {
        "esperadas": esperadas,
        "sql_linhas": len(sql), "dax_linhas": len(dax),
        "duplicadas_sql": dup_sql, "duplicadas_dax": dup_dax,
        "ausentes_no_sql": len(ausentes), "extras_no_sql": len(extras),
        "aprovadas": aprovadas, "reprovadas": reprovadas,
        "nulos_blank_coincidentes": nulos_coincidentes,
        "max_dif_brl": max_dif["BRL"], "max_dif_razao": max_dif["Razao"],
        "primeiras_falhas": falhas[:20],
        "aceite": (reprovadas == 0 and not ausentes and not extras and dup_sql == 0 and dup_dax == 0
                   and len(sql) == len(dax) == esperadas),
    }
    saida = Path(sql_csv).with_name(nome_saida)
    saida.write_text(json.dumps(resumo, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(json.dumps(resumo, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    if len(sys.argv) not in (3, 5):
        sys.exit("uso: python comparar-desvios.py <sql.csv> <dax.csv> [esperadas saida.json]")
    if len(sys.argv) == 5:
        main(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4])
    else:
        main(sys.argv[1], sys.argv[2])
