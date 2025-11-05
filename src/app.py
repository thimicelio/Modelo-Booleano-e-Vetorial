#interface Streamlit
import streamlit as st
import json
from search_boolean import boolean_search
from search_vector import vector_search

idx = json.load(open("storage/index.json", encoding="utf-8"))
docmeta = {d["doc_id"]: d for d in idx["doc_table"]}

st.title("SRI Simplificado")
query = st.text_input("Consulta")
model = st.radio("Modelo", ["Booleano", "Espaço Vetorial"])

if st.button("Buscar") and query:
    if model == "Booleano":
        result_ids = boolean_search(query)
        results = [(doc_id, 1.0) for doc_id in result_ids]
    else:
        results = vector_search(query)

    st.subheader("Resultados")
    for doc_id, score in results:
        meta = docmeta.get(int(doc_id), {})
        st.markdown(f"**{meta.get('titulo','(sem título)')}**")
        st.caption(f"Autores: {', '.join(meta.get('autores', [])) or 'N/D'} — Score: {score:.4f}")
        with st.expander("Detalhes"):
            st.write(meta)
