# Racha cuca 3x3 com solução automatica BFS
import random
from collections import deque

def criar_tabuleiro():
    numeros = list(range(1, 9)) + [0]  # 0 representa o espaço vazio
    random.shuffle(numeros)
    return [numeros[i:i+3] for i in range(0, 9, 3)]

def imprimir_tabuleiro(tabuleiro):
    for linha in tabuleiro:
        print(' '.join(str(num) if num != 0 else ' ' for num in linha))

def encontrar_posicao(tabuleiro, numero):
    for i, linha in enumerate(tabuleiro):
        if numero in linha:
            return i, linha.index(numero)
    return None

def pode_mover(tabuleiro, linha, coluna):
    vazio_linha, vazio_coluna = encontrar_posicao(tabuleiro, 0)
    return abs(vazio_linha - linha) + abs(vazio_coluna - coluna) == 1

def mover(tabuleiro, linha, coluna):
    vazio_linha, vazio_coluna = encontrar_posicao(tabuleiro, 0)
    tabuleiro[vazio_linha][vazio_coluna], tabuleiro[linha][coluna] = tabuleiro[linha][coluna], tabuleiro[vazio_linha][vazio_coluna]

def venceu(tabuleiro):
    esperado = list(range(1, 9)) + [0]
    atual = [num for linha in tabuleiro for num in linha]
    return atual == esperado

#-----------------------------------------------
# Solução automatica usando BFS

# Movimento: (linha, coluna)
MOVIMENTOS = {
    "cima":    (-1, 0),
    "baixo":   (1, 0),
    "esquerda": (0, -1),
    "direita": (0, 1)
}

def tabuleiro_para_estado(tabuleiro):
    return tuple(num for linha in tabuleiro for num in linha)

def estado_para_tabuleiro(estado):
    return [list(estado[i:i+3]) for i in range(0, 9, 3)]

def mover_estado(estado, direcao):
    tabuleiro = estado_para_tabuleiro(estado)
    vazio_linha, vazio_coluna = encontrar_posicao(tabuleiro, 0)
    dl, dc = MOVIMENTOS[direcao]
    nova_linha, nova_coluna = vazio_linha + dl, vazio_coluna + dc
    if 0 <= nova_linha < 3 and 0 <= nova_coluna < 3:
        # Realiza o movimento
        tabuleiro[vazio_linha][vazio_coluna], tabuleiro[nova_linha][nova_coluna] = tabuleiro[nova_linha][nova_coluna], tabuleiro[vazio_linha][vazio_coluna]
        return tabuleiro_para_estado(tabuleiro)
    return None

def resolver(tabuleiro_inicial):
    estado_inicial = tabuleiro_para_estado(tabuleiro_inicial)
    estado_objetivo = tuple(range(1, 9)) + (0,)

    fila = deque()
    fila.append((estado_inicial, []))  # (estado, caminho até aqui)
    visitados = set()
    visitados.add(estado_inicial)

    while fila:
        estado, caminho = fila.popleft()

        if estado == estado_objetivo:
            return caminho  # sequência de movimentos

        for direcao in MOVIMENTOS:
            novo_estado = mover_estado(estado, direcao)
            if novo_estado and novo_estado not in visitados:
                fila.append((novo_estado, caminho + [direcao]))
                visitados.add(novo_estado)
    
    return None  # sem solução (impossível)
#-----------------------------------------------

def jogar():
    tabuleiro = criar_tabuleiro()
    movimentos = 0
    while not venceu(tabuleiro):
        imprimir_tabuleiro(tabuleiro)
        print(f"Movimentos: {movimentos}")
        resposta = input("Digite o número que quer mover ou 's' para solução automática: ")

        if resposta.lower() == 's':
            caminho = resolver(tabuleiro)
            if caminho:
                print(f"Solução encontrada em {len(caminho)} movimentos!")
                for direcao in caminho:
                    print(f"Movendo {direcao}...")
                    estado = tabuleiro_para_estado(tabuleiro)
                    novo_estado = mover_estado(estado, direcao)
                    tabuleiro = estado_para_tabuleiro(novo_estado)
                    movimentos += 1
                    imprimir_tabuleiro(tabuleiro)
                print(f"Tabuleiro resolvido automaticamente em {movimentos} movimentos!")
            else:
                print("Não foi possível resolver o tabuleiro.")
            break  # Depois da solução automática, termina o jogo
        else:
            try:
                numero = int(resposta)
                pos = encontrar_posicao(tabuleiro, numero)
                if pos and pode_mover(tabuleiro, *pos):
                    mover(tabuleiro, *pos)
                    movimentos += 1
                else:
                    print("Movimento inválido!")
            except ValueError:
                print("Por favor, digite um número válido ou 's' para resolver automaticamente!")

    if venceu(tabuleiro):
        imprimir_tabuleiro(tabuleiro)
        print(f"Parabéns, você venceu em {movimentos} movimentos!")

if __name__ == "__main__":
    jogar()
