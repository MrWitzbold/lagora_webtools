import os
import unicodedata

# Read student data from the file
students2025 = open("2025", "r", encoding="utf-8").readlines()
# students2024 = open("2024", "r", encoding="utf-8").readlines()

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

class database:
    def __init__(self, students_file):
        self.students_file = students_file
        self.ages = []
        self.grades = {}
        self.current_grade = ""
        self.current_student = ""
        
        for line in students_file:
            # Check for a new grade
            if "Turma: TURMA" in line or "Turma: JARDIM" in line:
                if "JARDIM" in line:
                    self.grade = line.split("Turma: ")[1].split(" -")[0]
                else:
                    self.grade = line.split("TURMA ")[1].split(" ")[0].strip()  # .strip() removes any whitespace
                self.current_grade = self.grade
                # print("Current grade: " + current_grade)
                
            # Check for a student name
            elif "Nome: " in line:
                self.name = line.split('bold;">')[1].split("<")[0].strip()
                self.current_student = self.name
                # print("Current student: " + current_student)
                
            # Check for a phone number
            elif 'line-height: 1.215332;">' in line and "(" in line and "Telefone" not in line:
                self.phones = line.split('line-height: 1.215332;">')[1].split("<")[0].strip()
                
                # Initialize grade if not already in grades dictionary
                if self.current_grade not in self.grades:
                    self.grades[self.current_grade] = {}
                
                # Add student and phone number
                self.grades[self.current_grade][self.current_student] = [self.phones]
                # print("Added phones: " + phones)
            elif 'Nasc' in line:
                self.date = line.split("Nasc.: ")[1].split("<")[0]
                self.ages.append([self.current_student, self.date.split("/")[2]])
                
    def get_age(self, name):
        for age in self.ages:
            if age[0] == name:
                return 2024-int(age[1])
                
db2025 = database(students2025)
# db2024 = database(students2024)

while True:
    db = db2025
    command = input("Lagoraweb: ")

    if command.isdigit() and command in grades or "J1" in command or "J2" in command:
        command_mappings = {
            "J1A": "JARDIM I A",
            "J2A": "JARDIM II A",
            "J1B": "JARDIM I B",
            "J2B": "JARDIM II B"
        }

        # Update command with the mapped full version if it exists
        if command in command_mappings:
            command = command_mappings[command]
        
        names = list(db.grades[command].keys())
        for name in names:
            print(name)
    elif command == "compare":
        print("Comparing so farrily...")
        list1 = []
        list2 = []
        
        for grade_, students_ in db2024.grades.items():
            for student_, phones_ in students_.items():
                list1.append(student_)
                
        for grade_, students_ in db2025.grades.items():
            for student_, phones_ in students_.items():
                list2.append(student_)
                
        for student1 in list1:
            found = False
            for student2 in list2:
                if student1 == student2:
                    found = True
            if found == False:
                print(student1)
        
    else:
        for grade_, students_ in db.grades.items():
            for student_, phones_ in students_.items():
                if normalize(command.lower()) in normalize(student_.lower()):
                    print("Aluno: " + student_)
                    print("Turma: " + grade_)
                    print("Idade: " + str(db.get_age(student_)))
                    print("Números: " + str(phones_).replace("'", "").replace("[", "").replace("]", ""))
                    print("\n")

    if command == "c":
        os.system("clear")
