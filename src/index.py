#Esse documento é responsável por computar TF, criar dicionário global, calcular DF/IDF
import json, math
from collections import Counter, defaultdict
from pathlib import Path

def build_indexes(processed_json="storage/docs_processed.json",
                  out_index="storage/index.json"):
    docs = json.load(open(processed_json, encoding="utf-8"))

    # Tabela de documentos e registro DocId/TotPal
    doc_table = [{
        "doc_id": d["doc_id"],
        "titulo": d["titulo"],
        "autores": d["autores"],
        "tot_significativos": d["tot_significativos"]
    } for d in docs]
    last_doc_id = max(d["doc_id"] for d in docs) if docs else 0
    reg_docid_totpal = { "ultimo_doc_id": last_doc_id }

    # TF por documento + dicionário global (contagem total)
    tf_by_doc = {}
    global_counts = Counter()
    df = Counter()

    for d in docs:
        tf = Counter(d["tokens"])
        tf_by_doc[str(d["doc_id"])] = dict(tf)
        global_counts.update(tf)
        for term in tf.keys():
            df[term] += 1

    N = len(docs)
    idf = {t: math.log((N + 1) / (df[t] + 1)) + 1 for t in df}  # idf suavizado

    data = {
        "doc_table": doc_table,
        "registro_docid_totpal": reg_docid_totpal,
        "dicionario_termos_total": dict(global_counts),  # requisito do trabalho
        "tf_by_doc": tf_by_doc,
        "df": dict(df),
        "idf": idf,
        "N": N
    }
    Path(out_index).parent.mkdir(parents=True, exist_ok=True)
    json.dump(data, open(out_index, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

if __name__ == "__main__":
    build_indexes()
