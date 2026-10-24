# Central do Assessor — extrai e remonta as partes compactadas do arquivo único (desde a 3.0.0; formulário desde a 3.3.0).
# python3 ler_partes.py extrair Central_Assessor_vX.html  -> casca.html, central_parte.html, gerador_parte.html, formulario_parte.html
# python3 ler_partes.py montar   Central_Assessor_vX.html  -> junta de novo (o formulário só entra se a casca tiver @@FORMULARIO@@)
import sys, re, gzip, base64, os
modo, arq = sys.argv[1], sys.argv[2]
PARTES = ("central", "gerador", "formulario")
if modo == "extrair":
    s = open(arq, encoding="utf-8").read()
    for p in PARTES:
        m = re.search(r'<script type="application/octet-stream" id="parte-%s"[^>]*>(.*?)</script>' % p, s, re.S)
        if not m:
            continue
        open(p + "_parte.html", "wb").write(gzip.decompress(base64.b64decode(m.group(1).strip())))
        s = s.replace(m.group(1), "@@" + p.upper() + "@@")
    open("casca.html", "w", encoding="utf-8").write(s)
else:
    s = open("casca.html", encoding="utf-8").read()
    for p in PARTES:
        marca = "@@" + p.upper() + "@@"
        if marca in s:
            s = s.replace(marca, base64.b64encode(gzip.compress(open(p + "_parte.html", "rb").read(), 9)).decode())
    open(arq, "w", encoding="utf-8").write(s)
