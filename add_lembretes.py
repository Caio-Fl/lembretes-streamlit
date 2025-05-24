def adicionar_lembrete():
    import json
    data = input("Digite a data (AAAA-MM-DD): ")
    hora = input("Digite a hora (HH:MM): ")
    mensagem = input("Digite a mensagem: ")
    lembrete = {"data_hora": f"{data} {hora}", "mensagem": mensagem}

    try:
        with open('lembretes.json', 'r') as f:
            lembretes = json.load(f)
    except FileNotFoundError:
        lembretes = []

    lembretes.append(lembrete)
    with open('lembretes.json', 'w') as f:
        json.dump(lembretes, f, indent=2)

    print("✅ Lembrete adicionado com sucesso!")

if __name__ == "__main__":
    adicionar_lembrete()