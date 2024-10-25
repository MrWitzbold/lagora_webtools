import unicodedata
from colorama import Fore, Style
import colorama

colorama.init()

# Read student data from the file
students = open("alunos.txt", "r").readlines()

def normalize(name):
    normalized_name = unicodedata.normalize('NFD', name)
    cleaned_name = ''.join(c for c in normalized_name if unicodedata.category(c) != 'Mn')
    return cleaned_name

def view_dict(d, indent=0):
    """Recursively display any dictionary structure."""
    if isinstance(d, dict):
        for key, value in d.items():
            print(" " * indent + f"{key}:")
            view_dict(value, indent + 4)
    elif isinstance(d, list):
        for item in d:
            view_dict(item, indent + 4)
    else:
        print(" " * indent + str(d))

grades = {}
current_grade = ""
current_student = ""

for line in students:
    # Check for a new grade
    if "Turma: TURMA" in line:
        grade = line.split("TURMA ")[1].split(" ")[0].strip()  # .strip() removes any whitespace
        current_grade = grade
        # print("Current grade: " + current_grade)
        
    # Check for a student name
    elif "Nome: " in line:
        name = line.split('bold;">')[1].split("<")[0].strip()
        current_student = name
        # print("Current student: " + current_student)
        
    # Check for a phone number
    elif 'line-height: 1.215332;">' in line and "(" in line and "Telefone" not in line:
        phones = line.split('line-height: 1.215332;">')[1].split("<")[0].strip()
        
        # Initialize grade if not already in grades dictionary
        if current_grade not in grades:
            grades[current_grade] = {}
        
        # Add student and phone number
        grades[current_grade][current_student] = [phones]
        # print("Added phones: " + phones)
    elif 'Nasc' in line:
        date = line.split("Nasc.: ")[1].split("<")[0]
        

while True:
    command = input(Fore.RED + "Lagoraweb: " + Style.RESET_ALL)
    if command.isdigit() and command in grades:
        names = list(grades[command].keys())
        for name in names:
            print(Fore.GREEN + name + Style.RESET_ALL)
    else:
        for grade_, students_ in grades.items():
            for student_, phones_ in students_.items():
                if normalize(command.lower()) in normalize(student_.lower()):
                    print(Fore.RED + "Aluno: " + student_ + Style.RESET_ALL)
                    print(Fore.BLUE + "Turma: " + grade_ + Style.RESET_ALL)
                    print(Fore.GREEN + "Números: "+ str(phones_) + Style.RESET_ALL)
                    print("\n")
