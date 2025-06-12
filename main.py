import os
import unicodedata
from colorama import Fore, Style
import colorama
from datetime import datetime

colorama.init()
# print(Fore.GREEN + name + Style.RESET_ALL)
# students2025 = open("2025", "r", encoding="utf-8").readlines()
# use phones modelo 2 html

def normalize_string(input_string):
    # Normalize the string to remove accents and other diacritics
    normalized_string = unicodedata.normalize('NFD', input_string)
    normalized_string = ''.join([char for char in normalized_string if unicodedata.category(char) != 'Mn'])
    
    # Convert to lowercase
    normalized_string = normalized_string.lower()
    
    return normalized_string

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
seen_ra = []
for line in file:
    if html_landmark in line or html_landmark2 in line:
        num += 1
        data.append(line.replace(html_landmark, "").replace(html_landmark2, "").replace("</span></td>", "").replace("<br/>", ", ").replace("\n", ""))
        if num == 9:
            if data[0] not in seen_ra:
                new_student = student(data[0], data[1], data[2], data[3], data[5], data[6], data[7], data[8]) # ignores 4th because it's redundant, its just like, 3º ano instead of 31 or 32
                if "AEE" not in str(data[5]):
                    students.append(new_student)
                    seen_ra.append(data[0])
            else:
                for studentx in students:
                    if data[0] == studentx.ra:
                        if studentx.phones != data[8]:
                            studentx.phones = studentx.phones + ", " + data[8] # merge phone numbers if cloned and phones are different
            num = 0
            data = []

# Check for cloned students
seen_ra = []
seen_student = []
pairs = []
count = 0
for i in range(0, len(students)):
    studentx = students[i]
    if studentx.ra in seen_ra:
        for j in range(0, len(seen_ra)):
            if seen_ra[j] == studentx.ra:
                count += 1
                print(studentx.name + str(studentx.ra) + " = " + seen_student[j] + str(seen_ra[j]))
                pairs.append([i])
    seen_ra.append(studentx.ra)
    seen_student.append(studentx.name)
    
print(str(count) + " cloned")
    
while True:
    command = input(Fore.RED + "Lagoraweb: " + Style.RESET_ALL)
    map1 = ["JARDIM I A", "JARDIM II B", "JARDIM II A"]
    map2 = ["J1A", "J2B", "J2A"]
    is_kindheit = False
    for i in range(0, len(map2)):
        if command == map2[i]:
            is_kindheit = True
            command = map1[i]
            
    if is_kindheit or command.isdigit():
        num = 0
        for studentx in students:
            if command.lower().strip() in studentx.cohort.lower().strip():
                print(Fore.GREEN + studentx.name + Style.RESET_ALL)
                num += 1
        print(str(num) + " alunos\n")
    else:
        if command != "c" and command != "":
            num = 0
            for studentx in students:
                if normalize_string(command) in normalize_string(studentx.name):
                    studentx.present()
                    num += 1
            print("Encontrei " + str(num) + " alunos")
        else:
            os.system('cls' if os.name == 'nt' else 'clear')