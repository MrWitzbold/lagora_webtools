import os
import unicodedata
from colorama import Fore, Style
import colorama
from datetime import datetime

colorama.init()
# print(Fore.GREEN + name + Style.RESET_ALL)
# students2025 = open("2025", "r", encoding="utf-8").readlines()
# use phones modelo 2 html

def calculate_age(birth_str):
    birth_date = datetime.strptime(birth_str, "%d/%m/%Y")
    today = datetime.today()
    age = today.year - birth_date.year

    # Adjust if birthday hasn't occurred yet this year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1

    return age

current_dir = os.path.dirname(os.path.abspath(__file__))
html_landmark = '<span style="font-family: \'DejaVu Sans\', Arial, Helvetica, sans-serif; color: #000000; font-size: 8px; line-height: 1.1640625;">'
html_landmark2 = '<span style="font-family: \'DejaVu Sans\', Arial, Helvetica, sans-serif; color: #000000; font-size: 8px; line-height: 1; *line-height: normal;">'
html_files = [f for f in os.listdir(current_dir) if f.lower().endswith('.html')]
html_path = ""

if html_files:
    html_path = os.path.join(current_dir, html_files[0])
else:
    print("No HTML files found in the folder.")
    input("")
    exit()
    
file = open(html_path, "r", encoding="utf-8").readlines()

class student:
    def __init__(self, ra, name, sex, birth, cohort, state, mat, phones):
        self.ra = ra
        self.name = name
        self.sex = sex
        self.birth = birth
        self.cohort = cohort
        self.state = state
        self.mat = mat
        self.phones = phones
    def present(self):
        print(Fore.RED + "Aluno: " + self.name + Style.RESET_ALL)
        print(Fore.YELLOW + "Turma: " + self.cohort + Style.RESET_ALL)
        print(Fore.YELLOW + "Idade: " + str(calculate_age(self.birth)) + Style.RESET_ALL)
        print(Fore.GREEN + "Números: " + self.phones + Style.RESET_ALL)
        print("\n")

students = []
num = 0
data = []

for line in file:
    if html_landmark in line or html_landmark2 in line:
        num += 1
        data.append(line.replace(html_landmark, "").replace(html_landmark2, "").replace("</span></td>", "").replace("<br/>", "").replace("\n", ""))
        if num == 9:
            new_student = student(data[0], data[1], data[2], data[3], data[5], data[6], data[7], data[8]) # ignores 4th because it's redundant, its just like, 3º ano instead of 31 or 32
            students.append(new_student)
            num = 0
            data = []
            
while True:
    command = input(Fore.RED + "Lagoraweb: " + Style.RESET_ALL)
    map1 = ["JARDIM I A", "JARDIM I B", "JARDIM II A", "JARDIM II B"]
    map2 = ["J1A", "J2B", "J2A", "J2B"]
    is_kindheit = False
    for i in range(0, len(map2)):
        if command == map2[i]:
            is_kindheit = True
            command = map1[i]
            
    if is_kindheit or command.isdigit():
        num = 0
        for studentx in students:
            if command in studentx.cohort:
                print(Fore.GREEN + studentx.name + Style.RESET_ALL)
                num += 1
        print(str(num) + " alunos\n")
    else:
        num = 0
        for studentx in students:
            if command.lower() in studentx.name.lower():
                studentx.present()
                num += 1
        print("Encontrei " + str(num) + " alunos")