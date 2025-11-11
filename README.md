# SRI Simplificado (Booleano + Espaço Vetorial)

Projeto acadêmico de um Sistema de Recuperação de Informação (SRI) com:
- **Indexação** de 20 artigos científicos
- **Armazenamento** estruturado (dicionário de termos, tabela de documentos, TF/DF/IDF)
- **Busca** pelos modelos **Booleano** e **Espaço Vetorial (TF-IDF + cosseno)**
- **Interface gráfica** em Streamlit

## 📁 Estrutura de pastas

```
/sri/
 ├─ data/
 │   └─ raw/                 # PDFs originais
 ├─ storage/                 # índices e metadados gerados (.json)
 ├─ stopwords/
 │   └─ stopwords.txt        # lista de stopwords (UTF-8)
 └─ src/
     ├─ preprocess.py        # normaliza/tokeniza/remove stopwords
     ├─ index.py             # TF por doc, dicionário global, DF/IDF
     ├─ search_boolean.py    # busca booleana (AND/OR/NOT)
     ├─ search_vector.py     # busca vetorial (TF-IDF + cosseno)
     └─ app.py               # interface Streamlit
```

## ✅ Pré-requisitos

- Python 3.9+
- Pip atualizado (`python -m pip install --upgrade pip`)

## 📦 Instalação

Via `pip` (direto):
```bash
pip install -r requirements.txt
```
Ou se preferir manuealmente: 

```bash
pip install streamlit pdfminer.six nltk
```

Ou crie um ambiente virtual e instale:

```bash
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install streamlit pdfminer.six nltk

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
pip install streamlit pdfminer.six nltk
```

## 🗂️ Preparação dos dados

1. Coloque seus **PDFs** em `data/raw/`.
2. Garanta que `stopwords/stopwords.txt` está salvo

## 🔧 Geração dos índices

Arquivos gerados (exemplos):
- `storage/docs_raw.json` — metadados e resumos extraídos
- `storage/docs_processed.json` — tokens/contagens por doc
- `storage/index.json` — TF por doc, dicionário global, DF/IDF e tabela de docs

## ▶️ Executando a interface

```bash
streamlit run src/app.py
```

- Se a porta 8501 estiver ocupada:
  ```bash
  streamlit run src/app.py --server.port 8502
  ```

## 🔎 Como usar

1. Abra o app no navegador (link que o Streamlit mostra).
2. Digite sua consulta no campo **Consulta**.
3. Escolha o **Modelo**:
   - **Booleano**: use `AND`, `OR`, `NOT`  
     Ex.: `aprendizagem AND profunda NOT revisão`
   - **Espaço Vetorial**: termos livres; a ordenação é por similaridade cosseno (TF-IDF).  
     Ex.: `reconhecimento de fala robusto`

Os resultados aparecem com **Título**, **Autores** e **score** (no caso do vetorial). Clique para ver detalhes.

## 📝 Requisitos atendidos

- **Dicionário de termos** com quantidade total de ocorrências (em `storage/index.json` → `dicionario_termos_total`)
- **Tabela de documentos** `<DocId, Título, Autor, TotPal>` (em `doc_table`)
- **Registro `<DocId, TotPal>`** + último identificador (em `registro_docid_totpal`)
- **Documento original armazenado** (seus PDFs em `data/raw/`)
- **TF** por documento (em `tf_by_doc`) e **IDF** (em `idf`)
- **Interface gráfica** para os dois modelos

## 🧯 Troubleshooting

**Erro de encoding na stoplist (Windows):**  
`UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe0 ...`  
→ Abra `stopwords/pt.txt` no VS Code/Notepad++ e **salve como UTF-8** (sem BOM).  
Se preferir tolerar encodings automaticamente, adapte a função de leitura de stopwords (ex.: tentar `utf-8`, `utf-8-sig`, `cp1252`, `latin-1`).

**Resultados vazios no app:**  
- Confirme se rodou `ingest.py`, `preprocess.py` e `index.py`.
- Verifique se há PDFs em `data/raw/`.
- Confira se os resumos foram detectados (regex de `Resumo/Abstract` pode precisar ajuste conforme seus PDFs).

## 🧩 Personalizações sugeridas

- Ampliar lista de stopwords (`stopwords/pt.txt`)
- Ajustar heurísticas de extração em `ingest.py` (título, autores, filiação, resumo, palavras-chave)
- Adicionar suporte a parênteses na consulta booleana
- Exportar resultados (CSV/JSON) via Streamlit

## 📚 Licença

Uso acadêmico/educacional.
