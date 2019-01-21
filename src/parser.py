import re


def load_file(filename):
    out = ''
    with open(filename, 'r', encoding='UTF-8') as file:
        for line in file:
            if not line.startswith('%'):
                out += line+' '
    return out


def split_parts(tex):
    risp_start = tex.index('\\begin{longtable}')
    risp_end = tex.index('\\end{longtable}', risp_start)
    risp = tex[risp_start:risp_end]

    dom_start = tex.index('\\begin{longtable}', risp_end)
    dom_end = tex.index('\\end{longtable}', dom_start)
    dom = tex[dom_start:dom_end]

    return dom, risp


def get_cards(tex):
    cards = []
    for m in re.finditer("\\\\carta{\s*(?:{(?:\\\\small\s+)?)?([^}\s](?:{.+?}|[^}])*[^}\s])\s*}", tex):
        c = m.group(1).replace("\n", " ").replace("\\-", "-").replace("--", "-").replace("\\%", "%")\
            .replace("``", '"').replace("''", '"')
        if c.find("{") >= 0:
            c = re.sub("\\\\[a-z]+{(.*?)}", "\\1", c)
        c = re.sub("\s{2,}", " ", c)
        cards.append(c)
    return cards


def build_black(texts):
    out = []
    for t in texts:
        pick = max(t.count('\\puntini'), 1)
        t = t.replace('\\puntini', '_')
        out.append({"text": t, "pick": pick})
    return out


def process_file(filename):
    tex = load_file(filename)
    btex, wtex = split_parts(tex)
    b = build_black(get_cards(btex))
    w = get_cards(wtex)
    return {"blackCards": b, "whiteCards": w}


def convert_file(filename):
    if type(filename) is list:
        for f in filename:
            convert_file(f)
    else:
        js = process_file(filename+'.tex')
        import json
        with open(filename+'.json', 'w', encoding='UTF-8') as file:
            file.write(json.dumps(js))


def find_anomalies(filename):
    tex = load_file(filename)
    cards = get_cards(tex)
    out = []
    for c in cards:
        if c.replace('\\puntini', '_').find("\\") >= 0:
            out.append(c)
        elif c.find("{") >= 0:
            out.append(c)
    return out


all_files = ['cah-ita-originale-federico-sfoltita', 'cah-ita-originale-federico', 'cah-ita-espansione-cah42proj']