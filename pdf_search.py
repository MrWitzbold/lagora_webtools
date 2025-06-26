
import fitz
import os

def search_pdfs(folder, query):
    results = []
    query = query.strip().lower()
    for fname in os.listdir(folder):
        if not fname.endswith(".pdf"):
            continue
        year = fname.replace(".pdf", "")
        fpath = os.path.join(folder, fname)
        try:
            doc = fitz.open(fpath)
            for i, page in enumerate(doc):
                text = page.get_text().lower()
                if query in text:
                    results.append((year, i+1, fpath))
                    break
        except Exception as e:
            print(f"Erro ao ler {fname}: {e}")
    return results
