#Esse documento é responsavel por limpar, retirar as stopwords e tokenzizar.# src/preprocess.py
import json, re, unicodedata
from pathlib import Path

def load_stopwords(path="stopwords/pt.txt"):
    # tenta encodings comuns no Windows e cai para 'replace'
    for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            with open(path, encoding=enc) as f:
                return set(w.strip().lower() for w in f if w.strip())
        except UnicodeDecodeError:
            continue
    with open(path, encoding="utf-8", errors="replace") as f:
        return set(w.strip().lower() for w in f if w.strip())

# Mantém acentuação e aceita hífen dentro da palavra
TOKEN_RE = re.compile(r"[A-Za-zÀ-ÿ0-9]+(?:-[A-Za-zÀ-ÿ0-9]+)*", re.U)

def tokenize(text):
    return TOKEN_RE.findall(text.lower())

def preprocess_docs(in_json="storage/docs_raw.json",
                    out_json="storage/docs_processed.json",
                    stop_path="stopwords/stopwords.txt"):
    stop = load_stopwords(stop_path)
    docs = json.load(open(in_json, encoding="utf-8"))
    for d in docs:
        tokens = [t for t in tokenize(d.get("resumo","")) if t not in stop]
        d["tokens"] = tokens
        d["tot_significativos"] = len(tokens)
    Path(out_json).parent.mkdir(parents=True, exist_ok=True)
    json.dump(docs, open(out_json, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

if __name__ == "__main__":
    preprocess_docs()
