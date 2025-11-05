#busca vetorial (TF-IDF + cosseno)
import json, math
from collections import Counter
import re

TOKEN_RE = re.compile(r"[A-Za-zÀ-ÿ0-9]+(?:-[A-Za-zÀ-ÿ0-9]+)*", re.U)

def tokenize(q): return TOKEN_RE.findall(q.lower())

def load_stopwords(path="stopwords/stopwords.txt"):
    for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            with open(path, encoding=enc) as f:
                return set(w.strip().lower() for w in f if w.strip())
        except UnicodeDecodeError:
            continue
    with open(path, encoding="utf-8", errors="ignore") as f:
        return set(w.strip().lower() for w in f if w.strip())



def cosine(a, b):
    # a, b: dict termo->peso
    inter = set(a) & set(b)
    num = sum(a[t]*b[t] for t in inter)
    da = math.sqrt(sum(v*v for v in a.values()))
    db = math.sqrt(sum(v*v for v in b.values()))
    return 0.0 if da==0 or db==0 else num/(da*db)

def vector_search(q, index_path="storage/index.json", stopwords_path="stopwords/stopwords.txt", topk=10):
    idx = json.load(open(index_path, encoding="utf-8"))
    tf_by_doc = {int(k): v for k,v in idx["tf_by_doc"].items()}
    idf = idx["idf"]

    stop = load_stopwords(stopwords_path)

    q_tokens = [t for t in tokenize(q) if t not in stop]
    q_tf = Counter(q_tokens)
    q_vec = {t: q_tf[t]*idf.get(t, 0.0) for t in q_tf}

    scores = []
    for doc_id, tf in tf_by_doc.items():
        d_vec = {t: tf[t]*idf.get(t, 0.0) for t in tf}
        scores.append((doc_id, cosine(q_vec, d_vec)))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:topk]

if __name__ == "__main__":
    #utilizado para testes
    print(vector_search("biologia óssea"))
