import socket
import os
import time

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

HOST = input("Digite o IP do servidor (ou localhost): ")

PORT_INPUT = input("Digite a porta (padrão 12345): ")
PORT = int(PORT_INPUT) if PORT_INPUT else 12345

while True:
    limpar_tela()
    print("Tentando conectar ao servidor...")
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente.connect((HOST, PORT))
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        time.sleep(2)
        continue

    limpar_tela()
    print("Conectado! Aguarde...\n")    
    while True:
        try:

            msg = cliente.recv(4096).decode()
            if not msg:
                break


            if "JOGO_INICIOU" in msg:
                limpar_tela()
                print("=== PARTIDA INICIADA ===")
                msg = msg.replace("JOGO_INICIOU", "")      

            if "PROXIMA_RODADA" in msg:
                time.sleep(5) 
                limpar_tela()
                msg = msg.replace("PROXIMA_RODADA", "")

            if "FIM_DA_PARTIDA" in msg:
                print("\nO jogo acabou!")
                print("Aparte Enter para voltar a tela inicial")
                time.sleep(5)
                input()
                break


            print(msg, end="")

        
            if "Escolha:" in msg or "Login:" in msg or "Senha:" in msg or "Digite sua jogada" in msg:
                resposta = input()
                cliente.send(resposta.encode())
                
                if "Digite sua jogada" in msg:
                    print("\nEnviado! Aguardando resultado...")

        except KeyboardInterrupt:
            print("\nSaindo...")
            break
        except Exception as e:
            print(f"Erro: {e}")
            break

cliente.close()
