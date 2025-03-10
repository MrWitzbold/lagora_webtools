input("Tenha certeza de que tens o arquivo de ponto em ponto.txt na mesma pasta... Aperte enter.")
file = open("ponto.txt", "r", encoding='utf-8').readlines()

workers = []

for line in file:
    if "Nome:" in line:
        print(line)
        name = line.split("Nome: ")[1].split("  ")[0]
        matricula = line.split("Matrícula:")[1].replace(" ", "")
        workers.append([name.replace("\n", ""), matricula.replace("\n", "")])

data = ""
for worker in workers:
    data += "(" + worker[0] + ";" + worker[1] + "),"
    
print("\n\n" + data)

