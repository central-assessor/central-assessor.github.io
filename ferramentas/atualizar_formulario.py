"""Central do Assessor — põe um formulário novo dentro da Central e prepara a publicação.

Uso (na pasta com casca.html, central_parte.html, gerador_parte.html e formulario_parte.html,
extraídos com `ler_partes.py extrair`):

    python3 atualizar_formulario.py Laudo_Avaliacao_v78.0.0.html            # sobe a Central em 0.0.1
    python3 atualizar_formulario.py Laudo_Avaliacao_v78.0.0.html --central 3.4.0 --nota "texto curto"

Faz, nesta ordem:
  1. lê a APP_VERSION e o FORMATO_ARQUIVO do formulário (recusa o que não for o Laudo de Avaliação);
  2. copia o formulário para formulario_parte.html e grava nome e versão na casca;
  3. na Central: acrescenta a linha da versão na tabela FORMULARIO (se faltar) e a torna vigente;
  4. sobe a versão da Central (APP_VERSAO, CENTRAL_VERSAO da casca e o "Versão N" da tela);
  5. grava versao.json e monta Central_Assessor_v<versão>.html (com ler_partes.py).
Mudança nos dados do laudo (linha "Fv" no contrato) continua exigindo trabalho na Central: este script não faz isso.
"""
import argparse, datetime, json, os, re, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument("formulario")
ap.add_argument("--central", help="versão nova da Central (x.y.z); sem ela, sobe o último número")
ap.add_argument("--nota", default="", help="nota curta da versão na tabela FORMULARIO")
ap.add_argument("--data", default=datetime.date.today().isoformat())
a = ap.parse_args()

def ler(p): return open(p, encoding="utf-8").read()
def gravar(p, s): open(p, "w", encoding="utf-8").write(s)
def exibida(v): return re.sub(r"(\.0)+$", "", v)
def um(s, padrao, novo, nome):
    s2, n = re.subn(padrao, novo, s, count=1)
    if n != 1: sys.exit(f"não achei {nome}")
    return s2

f = ler(a.formulario)
if not re.search(r'app:\s*"laudo-avaliacao"', f): sys.exit("este arquivo não é o formulário do Laudo de Avaliação")
v = re.search(r'const APP_VERSION\s*=\s*"(\d+\.\d+\.\d+)"', f).group(1)
fmt = int(re.search(r"const FORMATO_ARQUIVO\s*=\s*(\d+)", f).group(1))
if fmt < 48: sys.exit("formulário anterior à Versão 67 (formato 48): não recebe os dados da OS")
nome = os.path.basename(a.formulario)

# 2. formulário e casca
gravar("formulario_parte.html", f)
casca = ler("casca.html")
casca = um(casca, r'id="parte-formulario" data-nome="[^"]*" data-versao="[^"]*"', f'id="parte-formulario" data-nome="{nome}" data-versao="{v}"', "a parte do formulário na casca")

# 3. tabela FORMULARIO da Central
central = ler("central_parte.html")
if f'versao: "{v}"' not in central:
    linha = f'    {{ versao: "{v}", exibida: "{exibida(v)}", data: "{a.data}", nota: {json.dumps(a.nota or "Formulário distribuído pela Central.", ensure_ascii=False)} }},\n'
    central = um(central, r'(const FORMULARIO = \{\n  vigente: "[^"]+",\n  minima: "[^"]+",\n  versoes: \[\n)', lambda m: m.group(1) + linha, "a tabela FORMULARIO")
central = um(central, r'(const FORMULARIO = \{\n  vigente: )"[^"]+"', lambda m: m.group(1) + f'"{v}"', "a versão vigente")

# 4. versão da Central
atual = re.search(r'const APP_VERSAO = "(\d+\.\d+\.\d+)";', central).group(1)
if a.central: nova = a.central
else:
    x = [int(n) for n in atual.split(".")]; x[2] += 1; nova = ".".join(map(str, x))
if nova != atual:
    central = central.replace(f'const APP_VERSAO = "{atual}";', f'const APP_VERSAO = "{nova}";')
for txt in (central, casca): pass
central = re.sub(r"Versão \d+(?:\.\d+){0,2} · use o", f"Versão {exibida(nova)} · use o", central)
central = re.sub(r'<span class="muted">Versão \d+(?:\.\d+){0,2}</span>', f'<span class="muted">Versão {exibida(nova)}</span>', central)
casca = re.sub(r"Versão \d+(?:\.\d+){0,2} · use o", f"Versão {exibida(nova)} · use o", casca)
casca = um(casca, r'const CENTRAL_VERSAO = "[^"]+";', f'const CENTRAL_VERSAO = "{nova}";', "CENTRAL_VERSAO na casca")
gravar("central_parte.html", central); gravar("casca.html", casca)

# 5. versao.json e montagem
gravar("versao.json", json.dumps({"central": nova, "formulario": v}, ensure_ascii=False) + "\n")
saida = f"Central_Assessor_v{nova}.html"
aqui = os.path.dirname(os.path.abspath(__file__))
subprocess.run([sys.executable, "-I", os.path.join(aqui, "ler_partes.py"), "montar", saida], check=True)
print(f"Central {nova} com o formulário {exibida(v)} (formato {fmt}): {saida} e versao.json")
print("Publicar: index.html = " + saida + ", e o versao.json, no mesmo envio.")
