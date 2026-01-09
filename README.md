# ✊✋✌️ Jokenpo: Pedra, Papel, Tesoura, Lagarto e Spock

Um jogo multiplayer baseado em rede (Client-Server) desenvolvido em **Python**, utilizando **Sockets** e **Multi-threading**. O projeto inclui sistema de autenticação de usuários, persistência de dados e um ranking competitivo.

---

## 📖 Sobre o Jogo

Esta é a versão expandida do clássico Jokenpo, popularizada pela série *The Big Bang Theory*. A adição de **Lagarto** e **Spock** reduz drasticamente a probabilidade de empates.

### Regras de Vitória:
* **Tesoura** corta Papel e decapita Lagarto.
* **Papel** cobre Pedra e refuta Spock.
* **Pedra** esmaga Lagarto e quebra Tesoura.
* **Lagarto** envenena Spock e come Papel.
* **Spock** derrete Tesoura e esmaga Pedra.

---

## 🛠️ Tecnologias e Conceitos
* **Sockets (TCP):** Comunicação confiável entre cliente e servidor.
* **Multi-threading:** O servidor gerencia múltiplos clientes simultaneamente.
* **Persistência:** Cadastro de usuários e senhas via manipulação de arquivos `.txt`.
* **Sincronização:** Uso de `threading.Lock` e `threading.Event` para controle de rodadas.

---

## FUNCIONALIDADES IMPLEMENTADAS
* **Autenticação:** Sistema de Login e Cadastro persistente.
* **Mecânica de Jogo:** Validação de jogadas e suporte a 5 opções (Pedra, Papel, Tesoura, Lagarto e Spock).
* **Lógica de Partida:** Sistema de melhor de 5 rodadas ou 3 pontos.
* **Ranking Global:** Integração com módulo de ranking para exibir o Top 5.
* **Resiliência:** O cliente tenta reconectar automaticamente caso o servidor caia.
* **Experiência do Usuário:** Limpeza dinâmica de tela para manter o terminal organizado.

---

## 🚀 Como Executar

### Pré-requisitos
* Python 3.x instalado.

### 1. Inicie o Servidor
No terminal, execute o servidor primeiro:
```bash
python servidor.
``` 

### 2. Inicie dois clientes na mesma máquima, ou em máquinas diferentes.
No terminal, execute o servidor primeiro:
```bash
python cliente.py
