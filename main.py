
import os
import socket
import unicodedata
from datetime import datetime
from flask import Flask, request, render_template_string, url_for, Response, send_file
from pdf_search import search_pdfs

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>LagoraWeb</title>
    <style>
        body {
            font-family: sans-serif;
            padding: 20px;
            background-color: #121212;
            color: #e0e0e0;
        }
        input {
            padding: 5px;
            font-size: 16px;
            background-color: #222;
            border: 1px solid #444;
            color: #eee;
            border-radius: 4px;
        }
        input::placeholder {
            color: #888;
        }
        input:focus {
            outline: none;
            border-color: #66aaff;
            box-shadow: 0 0 5px #66aaff;
            background-color: #1e1e1e;
        }
        input[type="submit"] {
            cursor: pointer;
            background-color: #3366cc;
            border: none;
            color: white;
            font-weight: bold;
            transition: background-color 0.3s ease;
        }
        input[type="submit"]:hover {
            background-color: #5599ff;
        }
        .student {
            margin: 10px 0;
            padding: 10px;
            background-color: #1e1e1e;
            border-radius: 5px;
            box-shadow: 0 0 5px #000;
            color: #ddd;
        }
        h2, h3, strong, p {
            color: #ddd;
        }
        img {
            filter: drop-shadow(0 0 3px #000);
        }
    </style>
</head>
<body>
    <img src="{{ url_for('static', filename='logo.png') }}" width="200" height="200">
    <h2>Buscar Aluno ou Turma</h2>
    <form method="GET">
        <input name="query" placeholder="Nome ou Turma (ex: J2A, 31)" autofocus>
        <input type="submit" name="action" value="Buscar">
        <input type="submit" name="action" value="Exportar dados da turma" id="exportar" style="background-color: #8c6200;">
        <input type="submit" name="action" value="Exportar arquivo de contatos" id="exportar_contatos" style="background-color: #8c6200;">
        <input type="submit" name="action" value="Procurar nas atas 2022 - 2000" id="pesquisar_astas" style="background-color: #cc3333;">
    </form>
    {% if results %}
    <h3>Resultados:</h3>
    {% if mode == 'search' %}
        <p><strong>{{ results|length }} alunos encontrados.</strong></p>
        {% for s in results %}
            <div class="student">
                <strong>Nome:</strong> {{ s.name }}<br>
                <strong>Turma:</strong> {{ s.cohort }}<br>
                <strong>Idade:</strong> {{ s.age }}<br>
                <strong>Números:</strong> {{ s.phones }}<br>
            </div>
        {% endfor %}
    {% elif mode == 'export' %}
        {% for line in results %}
            <div class="student">{{ line | safe }}</div>
        {% endfor %}
    {% elif mode == 'atas' %}
        {% for line in results %}
            <div class="student">{{ line | safe }}</div>
        {% endfor %}
    {% endif %}
    {% endif %}
<script>
document.querySelector("form").addEventListener("keydown", function(e) {
    if (e.key === "Enter") {
        e.preventDefault();
        const form = e.target.form;
        const buscarBtn = form.querySelector("input[type='submit'][value='Buscar']");
        if (buscarBtn) buscarBtn.click();
    }
});
</script>
</body>
</html>
"""

def generate_vcf(student):
    vcards = []
    phones = [p.strip() for p in student.phones.split(",") if p.strip()]
    for phone in phones:
        vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{student.name}
TEL:{phone}
END:VCARD"""
        vcards.append(vcard)
    return "\n".join(vcards)

def normalize_string(input_string):
    normalized = unicodedata.normalize('NFD', input_string)
    return ''.join([c for c in normalized if unicodedata.category(c) != 'Mn']).lower()

def normalize_text(text):
    return unicodedata.normalize("NFKC", text).casefold()

def calculate_age(birth_str):
    birth_date = datetime.strptime(birth_str, "%d/%m/%Y")
    today = datetime.today()
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age

class Student:
    def __init__(self, ra, name, sex, birth, cohort, state, mat, phones):
        self.ra = ra
        self.name = name
        self.sex = sex
        self.birth = birth
        self.cohort = cohort
        self.state = state
        self.mat = mat
        self.phones = phones
        self.age = calculate_age(self.birth)

current_dir = os.path.dirname(os.path.abspath(__file__))
html_landmark = '<span style="font-family: \'DejaVu Sans\', Arial, Helvetica, sans-serif; color: #000000; font-size: 8px; line-height: 1.1640625;">'
html_landmark2 = '<span style="font-family: \'DejaVu Sans\', Arial, Helvetica, sans-serif; color: #000000; font-size: 8px; line-height: 1; *line-height: normal;">'
html_files = [f for f in os.listdir(current_dir) if f.lower().endswith('.html')]
file = open(os.path.join(current_dir, html_files[0]), "r", encoding="utf-8").readlines()

students, data, seen_ra = [], [], []

for line in file:
    if html_landmark in line or html_landmark2 in line:
        data.append(line.replace(html_landmark, "").replace(html_landmark2, "").replace("</span></td>", "").replace("<br/>", ", ").strip())
        if len(data) == 9:
            if data[0] not in seen_ra and "AEE" not in str(data[5]):
                students.append(Student(data[0], data[1].replace("&nbsp;", ""), data[2], data[3], data[5], data[6], data[7], data[8]))
                seen_ra.append(data[0])
            else:
                for s in students:
                    if data[0] == s.ra and s.phones != data[8]:
                        s.phones += ", " + data[8]
            data = []

@app.route("/", methods=["GET"])
def index():
    query = request.args.get("query", "").strip()
    action = request.args.get("action")
    results = []
    mode = None

    if query and action == "Buscar":
        mode = "search"
        map1 = ["JARDIM I A", "JARDIM II B", "JARDIM II A"]
        map2 = ["J1A", "J2B", "J2A"]
        if query in map2:
            query = map1[map2.index(query)]
        for s in students:
            if query.lower() in s.cohort.lower() or normalize_string(query) in normalize_string(s.name):
                results.append(s)

    elif query and action == "Exportar dados da turma":
        mode = "export"
        RAs, fullnames, firstnames, lastnames, users, passwords, cohorts, emails = (
            ["RA: "], ["Nomes completos: "], ["Primeiros nomes: "], ["Sobrenomes: "],
            ["Usuários"], ["Senhas: "], ["Turmas: "], ["Emails: "]
        )
        for s in students:
            if query.lower() in s.cohort.lower():
                RAs.append(s.ra)
                fullnames.append(str(s.name))
                firstnames.append(s.name.split()[0])
                lastnames.append(" ".join(s.name.split()[1:]))
                users.append(normalize_text(s.name.lower()))
                passwords.append("sargento2025")
                cohorts.append(str(s.cohort).replace("TURMA ", ""))
                emails.append("sargentoraymundo@edu.viamao.rs.gov.br")
        results = [
            "Número de alunos: " + str(len(RAs)-1),
            "<br>".join(RAs),
            "<br>".join(fullnames),
            "<br>".join(firstnames),
            "<br>".join(lastnames),
            "<br>".join(users),
            "<br>".join(passwords),
            "<br>".join(cohorts),
            "<br>".join(emails)
        ]

    elif action == "Exportar arquivo de contatos":
        vcards = [generate_vcf(s) for s in students]
        return Response(
            "\n\n".join(vcards),
            mimetype="text/vcard",
            headers={"Content-Disposition": 'attachment; filename="contatos.vcf"'}
        )

    elif query and action == "Procurar nas atas 2022 - 2000":
        mode = "atas"
        pdf_folder = os.path.join("static", "atas_organizadas")
        search_hits = search_pdfs(pdf_folder, query)
        results = []
        for year, page, path in search_hits:
            link = url_for("download_pdf", filepath=path)
            results.append(f"Ano: {year} | Página: {page} — <a href='{link}'>Baixar PDF</a>")

    return render_template_string(HTML_TEMPLATE, results=results, url_for=url_for, mode=mode)

@app.route("/download_pdf")
def download_pdf():
    filepath = request.args.get("filepath")
    return send_file(filepath, as_attachment=True)

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

if __name__ == "__main__":
    port = 5000
    ip = get_local_ip()
    print(f"Servidor rodando em: http://{ip}:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
