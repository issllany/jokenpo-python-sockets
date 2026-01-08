import os

ARQUIVO = "ranking.txt"

def inicializar():
    if not os.path.exists(ARQUIVO):
        with open(ARQUIVO, "w") as f:
            pass 

def carregar_dados():
    dados = {}
    inicializar()
    
    with open(ARQUIVO, "r") as f:
        for linha in f:
            linha = linha.strip()
            if ";" in linha:
                user, vit, der = linha.split(";")
                dados[user] = {"vitorias": int(vit), "derrotas": int(der)}
    return dados

def salvar_dados(dados):
    with open(ARQUIVO, "w") as f:
        for user, stats in dados.items():
            f.write(f"{user};{stats['vitorias']};{stats['derrotas']}\n")

def registrar_partida(vencedor, perdedor):
    if vencedor == "EMPATE":
        return 

    dados = carregar_dados()

    if vencedor not in dados: dados[vencedor] = {"vitorias": 0, "derrotas": 0}
    if perdedor not in dados: dados[perdedor] = {"vitorias": 0, "derrotas": 0}

    dados[vencedor]["vitorias"] += 1
    dados[perdedor]["derrotas"] += 1

    salvar_dados(dados)
    print(f"[RANKING] Registrado: {vencedor} +1 win | {perdedor} +1 loss")

def obter_top_5():
    dados = carregar_dados()
    
    lista_ordenada = sorted(dados.items(), key=lambda item: (-item[1]['vitorias'], item[1]['derrotas']))
    
    texto = "\n🏆 === TOP 5 JOGADORES === 🏆\n"
    texto += f"{'POS':<4} {'NOME':<15} {'VIT':<5} {'DER':<5}\n"
    texto += "-"*35 + "\n"

    for i, (nome, stats) in enumerate(lista_ordenada[:5]):
        texto += f"{i+1:<4} {nome:<15} {stats['vitorias']:<5} {stats['derrotas']:<5}\n"
    
    return texto