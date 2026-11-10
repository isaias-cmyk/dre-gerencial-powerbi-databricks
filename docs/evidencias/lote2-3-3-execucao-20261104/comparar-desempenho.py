"""Comparador L2.3.3 — M44–M48, SQL independente (Databricks) x DAX (Power BI).

Uso: python comparar-desempenho.py L233_SQL_operandos.csv L233_DAX_desempenho.csv
O CSV SQL traz R/O/P comparáveis por (grupo_filial, periodo, posicao), saída do roteiro 07.
As regras do contrato (docs/plano-lote2-3-3.md, seção 2) são aplicadas aqui sobre os
operandos SQL; o resultado esperado é comparado com o exportado do Power BI.
Tolerâncias: R$ 0,01 (M44/M45); 1E-8 (M48); texto idêntico (M46/M47); BLANK = NULL.
"""
import csv, json, sys
from pathlib import Path

ELEGIVEIS = {1, 2, 3, 4, 5, 6, 7, 9, 10, 12, 13}


def num(t):
    t = (t or "").strip()
    return None if t == "" else float(t)


def classe(impacto, pos):
    if impacto is None:
        return None
    c = "Em linha" if abs(impacto) <= 0.01 + 1e-9 else ("Favorável" if impacto > 0 else "Desfavorável")
    return c + (" (provisório)" if pos == 13 else "")


def esperado(r, o, p, pos):
    i44 = None if r is None or o is None or pos not in ELEGIVEIS else r - o
    i45 = None if r is None or p is None or pos not in ELEGIVEIS else r - p
    m48 = None
    if pos in (1, 3) and r is not None and o is not None and o > 0 and r >= 0:
        m48 = r / o
    return {"M44": i44, "M45": i45, "M46": classe(i44, pos), "M47": classe(i45, pos), "M48": m48}


def main(sql_csv, dax_csv):
    exp = {}
    for l in csv.DictReader(open(sql_csv, encoding="utf-8-sig")):
        pos = int(l["posicao"])
        for k, v in esperado(num(l["r"]), num(l["o"]), num(l["p"]), pos).items():
            exp[(l["grupo_filial"], l["periodo"], pos, k)] = v
    dax, dup = {}, 0
    for l in csv.DictReader(open(dax_csv, encoding="utf-8-sig")):
        ch = (l["grupo_filial"], l["periodo"], int(l["posicao"]), l["id"])
        dup += ch in dax
        v = l["valor"]
        dax[ch] = (None if v == "" else v) if l["id"] in ("M46", "M47") else num(v)
    aprov = reprov = nulos = 0
    maxd = {"BRL": 0.0, "Razao": 0.0}
    falhas, contagem = [], {}
    for ch in sorted(set(exp) & set(dax)):
        e, d = exp[ch], dax[ch]
        if e is None or d is None:
            ok = e is None and d is None
            nulos += ok
        elif ch[3] in ("M46", "M47"):
            ok = e == d
        else:
            dif = abs(e - d)
            u = "BRL" if ch[3] in ("M44", "M45") else "Razao"
            maxd[u] = max(maxd[u], dif)
            ok = dif <= (0.01 if u == "BRL" else 1e-8)
        if ch[3] in ("M46", "M47") and d:
            contagem[d] = contagem.get(d, 0) + 1
        aprov += ok
        reprov += not ok
        if not ok:
            falhas.append({"chave": ch, "esperado": e, "dax": d})
    esperadas = len(exp)
    res = {
        "esperadas": esperadas, "dax_linhas": len(dax), "duplicadas_dax": dup,
        "ausentes_no_dax": len(set(exp) - set(dax)), "extras_no_dax": len(set(dax) - set(exp)),
        "aprovadas": aprov, "reprovadas": reprov, "nulos_blank_coincidentes": nulos,
        "max_dif_brl": maxd["BRL"], "max_dif_razao": maxd["Razao"],
        "classificacoes_dax": dict(sorted(contagem.items())),
        "primeiras_falhas": falhas[:20],
        "aceite": reprov == 0 and dup == 0 and len(dax) == esperadas and not (set(exp) ^ set(dax)),
    }
    Path(dax_csv).with_name("comparacao-desempenho.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("uso: python comparar-desempenho.py <sql_operandos.csv> <dax.csv>")
    main(sys.argv[1], sys.argv[2])
