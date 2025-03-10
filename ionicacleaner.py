import sys
import unicodedata

def normalize_text(text):
    return unicodedata.normalize("NFKC", text).casefold()

def process_input(user_input):
    lines = user_input.split("\n")
    numbers = []
    names = []
    
    for line in lines:
        clean_line = line.strip().replace("^Z", "")
        if clean_line.isdigit() and len(clean_line) <= 6:
            numbers.append(clean_line)
        elif any(char.isalpha() for char in clean_line):
            names.append(clean_line)
    
    return numbers, names

def main():
    while True:
        print("\n\nCole os dados bagunçados aqui:")
        user_input = sys.stdin.read()
        numbers, names = process_input(user_input)
        
        print("\nNúmeros:")
        for num in numbers:
            print(num)
        input("\n\nPRESS ENTER")
        
        print("\nPrimeiros nomes:")
        for name in names:
            first_name = name.split()[0]
            print(first_name)
        input("\n\nPRESS ENTER")
        
        print("\nSobrenomes:")
        for name in names:
            last_name = " ".join(name.split()[1:])
            print(last_name)
        input("\n\nPRESS ENTER")
        
        print("\nUsuário")
        for name in names:
            print(normalize_text(name.lower()))
        input("\n\nPRESS ENTER")
            
        print("\nSenhas")
        for name in names:
            print("sargento2025")
        
        turma = input("\n\nDigite a TURMA: ")
            
        print("\nTurmas")
        for name in names:
            print(turma)
            
        input("\n\nPRESS ENTER")
            
        print("\nEmails")
        for name in names:
            print("sargentoraymundo@edu.viamao.rs.gov.br")

if __name__ == "__main__":
    main()
