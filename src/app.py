#interface Streamlit
import streamlit as st
import json
import base64
from urllib.parse import unquote
from search_boolean import boolean_search
from search_vector import vector_search

def pdf_embed_base64(pdf_path):
    with open(pdf_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def render_pdf_title_with_hover(title, pdf_path, uid):
    b64pdf = pdf_embed_base64(pdf_path)
    
    html = f"""
    <style>
        #toggle-{uid} {{
            display: none;
        }}
        #toast-{uid} {{
            display: none;
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 620px;
            height: 760px;
            background: #222;
            border-radius: 10px;
            padding: 10px;
            color: white;
            box-shadow: 0 3px 10px rgba(0,0,0,0.4);
            z-index: 99999;
        }}
        #toggle-{uid}:checked ~ #toast-{uid} {{
            display: block;
        }}
        label[for="toggle-{uid}"] {{
            font-weight: bold;
            color: #4EA8FF;
            text-decoration: none;
            cursor: pointer;
        }}
        label[for="toggle-{uid}"]:hover {{
            text-decoration: underline;
        }}
    </style>
    <input type="checkbox" id="toggle-{uid}">
    <label for="toggle-{uid}">{title}</label>
    <div id="toast-{uid}">
        <iframe
            src="data:application/pdf;base64,{b64pdf}"
            width="100%"
            height="700px"
            style="border: none; border-radius: 6px;">
        </iframe>
    </div>
    """
    return html

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
    if(not results):
        st.write("Nenhum documento encontrado.")
    for doc_id, score in results:
        meta = docmeta.get(int(doc_id), {})
        arquivo = meta.get("arquivo", "").replace("file:///", "")
        titulo = meta.get("titulo", "(sem título)")
        uid = f"{doc_id}-{score}".replace(".", "-")
        st.markdown(
            render_pdf_title_with_hover(titulo, unquote(arquivo), uid),
            unsafe_allow_html=True
        )
        st.caption(f"Autores: {', '.join(meta.get('autores', [])) or 'N/D'} — Score: {score:.4f}")
        with st.expander("Resumo"):
            st.write(meta.get("resumo", "Sem resumo disponível."))

