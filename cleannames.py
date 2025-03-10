import sys

while True:
    print("\n\nCole os nomes dos alunos aqui:")
    user_input = sys.stdin.read()  # Reads until EOF (Ctrl + Z)
    
    lines = user_input.split("\n")
    students = []
    for line in lines:
        line2 = line.replace("^Z", "")
        if any(char.isdigit() for char in line2) == False and any(char.isalpha() for char in line2):
            students.append(line2.replace("\n", ""))
            
    print("Alunos:\n")
    for student in students:
        print(student)