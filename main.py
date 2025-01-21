import os
import unicodedata
from colorama import Fore, Style
import colorama

colorama.init()

# Read student data from the file
students = open("alunos.txt", "r", encoding="utf-8").readlines()

ages = []

def create_vcf(contact_name, phone_number):
    # Define the vCard format
    vcard_data = f"BEGIN:VCARD\nVERSION:3.0\nFN:{contact_name}\nTEL:{phone_number}\nEND:VCARD\n\n"
    return vcard_data

def get_age(name):
    for age in ages:
        if age[0] == name:
            return 2024-int(age[1])

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
    if "Turma: TURMA" in line or "Turma: JARDIM" in line:
        if "JARDIM" in line:
            grade = line.split("Turma: ")[1].split(" -")[0]
        else:
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
        ages.append([current_student, date.split("/")[2]])

while True:
    command = input(Fore.RED + "Lagoraweb: " + Style.RESET_ALL)

    if (command.isdigit() and command in grades or "J1" in command or "J2" in command) or command == "getphone":
        command_mappings = {
            "J1A": "JARDIM I A",
            "J2A": "JARDIM II A",
            "J1B": "JARDIM I B",
            "J2B": "JARDIM II B"
        }

        # Update command with the mapped full version if it exists
        if command == "getphone":
            print("Formatting phones...")
            phone_vcfs = ""
            
            for grade_, students_ in grades.items():
                for student_, phones_ in students_.items():
                    for phone_number in str(phones_).split(","):
                        vcf = create_vcf(student_, phone_number.replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace("'", ""))
                        phone_vcfs += vcf
                        print(vcf)
                            
            open("phones.vcf", "w", encoding="utf-8").write(phone_vcfs)
            
            
        else:
            if command in command_mappings:
                command = command_mappings[command]
        
            names = list(grades[command].keys())
            for name in names:
                print(Fore.GREEN + name + Style.RESET_ALL)
    else:
        for grade_, students_ in grades.items():
            for student_, phones_ in students_.items():
                if normalize(command.lower()) in normalize(student_.lower()):
                    print(Fore.RED + "Aluno: " + student_ + Style.RESET_ALL)
                    print(Fore.YELLOW + "Turma: " + grade_ + Style.RESET_ALL)
                    print(Fore.YELLOW + "Idade: " + str(get_age(student_)) + Style.RESET_ALL)
                    print(Fore.GREEN + "Números: " + str(phones_).replace("'", "").replace("[", "").replace("]", "") + Style.RESET_ALL)
                    print("\n")

    if command == "c":
        os.system("clear")
