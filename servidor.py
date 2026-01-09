import socket
import threading
import time
import ranking

HOST = '0.0.0.0'
PORT = 12345
MAX_RODADAS = 5

REGRAS = {
    "PEDRA": ["TESOURA", "LAGARTO"],
    "PAPEL": ["PEDRA", "SPOCK"],
    "TESOURA": ["PAPEL", "LAGARTO"],
    "LAGARTO": ["PAPEL", "SPOCK"],
    "SPOCK": ["PEDRA", "TESOURA"]
}



clientes = []      
logins = {}         
jogadas = {}        
placar = {}        
rodada_atual = 1
game_over = False

lock = threading.Lock()
jogada_event = threading.Event() 

def log(msg):
    print(f"[SERVIDOR] {msg}")

def autenticar_ou_cadastrar(conn):
    try:
        conn.send("1 - Login\n2 - Cadastro\n3 - Ranking\nEscolha: ".encode())
        opcao = conn.recv(1024).decode().strip()
        if opcao in ["1", "2"]:
            conn.send("Login: ".encode())
            login = conn.recv(1024).decode().strip()
            
            conn.send("Senha: ".encode())
            senha = conn.recv(1024).decode().strip()
    except:
        return None 

    try: open("usuarios.txt", "a").close()
    except: pass

    if opcao == "2": 
        with open("usuarios.txt", "r") as f:
            if login in f.read():
                conn.send("Usuario ja existe.\n".encode())
                return "REPETIR" 
        
        with open("usuarios.txt", "a") as f:
            f.write(f"{login};{senha}\n")
        
        conn.send("Cadastro realizado! Logue agora.\n".encode())
        return "REPETIR"

    elif opcao == "1":
        auth = False
        with open("usuarios.txt", "r") as f:
            for linha in f:
                if ";" in linha:
                    u, p = linha.strip().split(";")
                    if u == login and p == senha:
                        auth = True
                        break
        if not auth:
            conn.send("Credenciais invalidas.\n".encode())
            return "REPETIR"
        
        if login in [l for l in logins.values()]:
             conn.send("Usuario ja esta logado.\n".encode())
             return "REPETIR"

        return login 
    elif opcao == "3":
        top_ranking = ranking.obter_top_5()
        conn.send(top_ranking.encode())
        conn.send("\n".encode())
        
        return "REPETIR"
    return "REPETIR"

def processar_rodada():
    global rodada_atual, game_over
    
    nomes = list(jogadas.keys())
    p1, p2 = nomes[0], nomes[1]
    j1, j2 = jogadas[p1], jogadas[p2]
    
    msg_resultado = ""
    vencedor_rodada = None

    log(f"Processando rodada {rodada_atual}: {p1}({j1}) vs {p2}({j2})")

    if j1 == j2:
        msg_resultado = f"Rodada empatada! Ambos jogaram {j1}"
    elif j2 in REGRAS[j1]:
        placar[p1] += 1
        msg_resultado = f"{p1} venceu a rodada! {j1} vence {j2}"
        vencedor_rodada = p1
    else:
        placar[p2] += 1
        msg_resultado = f"{p2} venceu a rodada! {j2} vence {j1}"
        vencedor_rodada = p2

    txt_placar = " | ".join([f"{k}: {v}" for k, v in placar.items()])
    
    msg_final = (
        f"\n--- RODADA {rodada_atual} ---\n"
        f"{msg_resultado}\n"
        f"Placar: {txt_placar}\n"
    )

    vencedor_partida = None
    if placar[p1] == 3: vencedor_partida = p1
    elif placar[p2] == 3: vencedor_partida = p2
    elif rodada_atual == MAX_RODADAS:
        if placar[p1] > placar[p2]: vencedor_partida = p1
        elif placar[p2] > placar[p1]: vencedor_partida = p2
        else: vencedor_partida = "EMPATE"

    broadcast(msg_final)

    if vencedor_partida:
        game_over = True
        if vencedor_partida != "EMPATE":
            perdedor_partida = p2 if vencedor_partida == p1 else p1
            ranking.registrar_partida(vencedor_partida, perdedor_partida)

        msg_vitoria = f"\n🏆 {vencedor_partida} venceu a partida!\n"
        broadcast(msg_vitoria)
        log(f"Fim de jogo. Vencedor: {vencedor_partida}")
        time.sleep(1.0) 
        broadcast("FIM_DA_PARTIDA")
        print(ranking.obter_top_5())
        threading.Timer(5.0, resetar_servidor).start()
    else:
        rodada_atual += 1
        jogadas.clear()
        broadcast("PROXIMA_RODADA")
        time.sleep(1.5)
        log("Iniciando próxima rodada...")

def broadcast(msg):
    for c in clientes:
        try:
            c.send(msg.encode())
        except:
            pass

def cliente_thread(conn, addr):
    global rodada_atual
    
    log(f"Nova conexão: {addr}")
    
    nome_usuario = None
    while True:
        resultado = autenticar_ou_cadastrar(conn)
        
        if resultado is None:
            conn.close()
            return
        elif resultado == "REPETIR":
            continue
        else:
            nome_usuario = resultado
            break

    conn.send(f"Bem-vindo, {nome_usuario}! Aguardando oponente...\n".encode())
    
    with lock:
        clientes.append(conn)
        logins[conn] = nome_usuario
        placar[nome_usuario] = 0
    
    log(f"Jogador logado: {nome_usuario}")

    while len(clientes) < 2:
        time.sleep(1)
        if len(clientes) < 2:
            conn.send("Aguardando...\n".encode()) 
            time.sleep(2)

    if len(jogadas) == 0 and rodada_atual == 1:
        conn.send("JOGO_INICIOU".encode())
        time.sleep(1.5)

    while not game_over:
        try:
            conn.send(f"\n--- RODADA {rodada_atual} ---\nDigite sua jogada (PEDRA, PAPEL, TESOURA, LAGARTO, SPOCK): ".encode())
            
            data = conn.recv(1024).decode().strip().upper()
            if not data: break

            if data not in REGRAS:
                conn.send("Jogada inválida! Tente novamente.\n".encode())
                continue

            log(f"{nome_usuario} jogou {data}")
            conn.send("Aguardando oponente...\n".encode())

            with lock:
                jogadas[nome_usuario] = data
                
                if len(jogadas) == 2:
                    processar_rodada()
                    jogada_event.set()
                else:
                    jogada_event.clear() 
            
            while len(jogadas) != 0 and not game_over:
                 time.sleep(0.5)
            
        except Exception as e:
            log(f"Erro com cliente {nome_usuario}: {e}")
            break

    conn.close()

def resetar_servidor():
    global clientes, logins, jogadas, placar, rodada_atual, game_over
    log("Resetando estado do servidor para nova partida...")
    clientes = []
    logins = {}
    jogadas = {}
    placar = {}
    rodada_atual = 1
    game_over = False
    jogada_event.clear()
    log("Servidor pronto para novos jogadores!")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(2)
    log(f"Servidor Jokenpo rodando na porta {PORT}")
    log("Aguardando jogadores...")

    while True:
        conn, addr = server.accept()
        t = threading.Thread(target=cliente_thread, args=(conn, addr))
        t.start()

if __name__ == "__main__":
    main()