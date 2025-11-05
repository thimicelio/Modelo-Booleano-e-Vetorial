# busca booleana (AND/OR/NOT)
import json

def parse_query(q):
    # Simplíssimo: separa por espaço; aceita AND/OR/NOT em maiúsculas
    return q.strip()

def boolean_search(q, index_path="storage/index.json"):
    idx = json.load(open(index_path, encoding="utf-8"))
    tf_by_doc = idx["tf_by_doc"]
    all_docs = set(tf_by_doc.keys())

    # Conjuntos por termo
    def docs_for_term(t):
        t = t.lower()
        return {doc for doc, tf in tf_by_doc.items() if t in tf}

    tokens = q.replace("(", " ( ").replace(")", " ) ").split()
    # Shunting-yard / avaliação postfix seria o ideal;
    # aqui, para simplicidade, só AND/OR/NOT esquerda→direita:
    res = None
    op = None
    negate = False
    for tok in tokens:
        if tok in ("AND","OR","NOT"):
            if tok == "NOT":
                negate = True
            else:
                op = tok
            continue
        if tok in ("(",")"):
            # ignorado neste minimal; pode expandir
            continue
        s = docs_for_term(tok)
        if negate:
            s = all_docs - s
            negate = False
        if res is None:
            res = s
        else:
            res = (res & s) if op == "AND" else (res | s)
            op = None
    return sorted(int(d) for d in (res or set()))

if __name__ == "__main__":
    #utilizado para testes
    print(boolean_search("biologia óssea"))
