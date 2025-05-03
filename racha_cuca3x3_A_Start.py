# Racha cuca 3x3 com solução automatica A*
import random
import heapq

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
# Solução automatica usando A*

def heuristica_manhattan(estado):
    distancia = 0
    for idx, valor in enumerate(estado):
        if valor == 0:
            continue  # espaço vazio não conta
        objetivo_idx = valor - 1
        linha_atual, coluna_atual = divmod(idx, 3)
        linha_objetivo, coluna_objetivo = divmod(objetivo_idx, 3)
        distancia += abs(linha_atual - linha_objetivo) + abs(coluna_atual - coluna_objetivo)
    return distancia

def resolver_astar(tabuleiro_inicial):
    estado_inicial = tabuleiro_para_estado(tabuleiro_inicial)
    estado_objetivo = tuple(range(1, 9)) + (0,)

    fila = []
    heapq.heappush(fila, (heuristica_manhattan(estado_inicial), 0, estado_inicial, []))
    visitados = set()
    visitados.add(estado_inicial)

    while fila:
        f, g, estado, caminho = heapq.heappop(fila)

        if estado == estado_objetivo:
            return caminho  # caminho de direções

        for direcao in MOVIMENTOS:
            novo_estado = mover_estado(estado, direcao)
            if novo_estado and novo_estado not in visitados:
                novo_g = g + 1
                novo_f = novo_g + heuristica_manhattan(novo_estado)
                heapq.heappush(fila, (novo_f, novo_g, novo_estado, caminho + [direcao]))
                visitados.add(novo_estado)

    return None  # sem solução

# Converte tabuleiro (matriz 4x4) para uma tupla linear (estado)
def tabuleiro_para_estado(tabuleiro):
    return tuple(num for linha in tabuleiro for num in linha)

# Converte estado (tupla linear) para tabuleiro (matriz 4x4)
def estado_para_tabuleiro(estado):
    return [list(estado[i:i+3]) for i in range(0, 9, 3)]

# Define os movimentos possíveis
MOVIMENTOS = ['cima', 'baixo', 'esquerda', 'direita']

# Move o espaço vazio no estado
def mover_estado(estado, direcao):
    idx = estado.index(0)
    linha, coluna = divmod(idx, 3)
    novo_estado = list(estado)

    if direcao == 'cima' and linha > 0:
        destino_idx = (linha - 1) * 3 + coluna
    elif direcao == 'baixo' and linha < 2:
        destino_idx = (linha + 1) * 3 + coluna
    elif direcao == 'esquerda' and coluna > 0:
        destino_idx = linha * 3 + (coluna - 1)
    elif direcao == 'direita' and coluna < 2:
        destino_idx = linha * 3 + (coluna + 1)
    else:
        return None  # Movimento inválido

    novo_estado[idx], novo_estado[destino_idx] = novo_estado[destino_idx], novo_estado[idx]
    return tuple(novo_estado)

#-----------------------------------------------

def jogar():
    tabuleiro = criar_tabuleiro()
    movimentos = 0
    while not venceu(tabuleiro):
        imprimir_tabuleiro(tabuleiro)
        print(f"Movimentos: {movimentos}")
        resposta = input("Digite o número que quer mover ou 's' para solução automática: ")

        if resposta.lower() == 's':
            caminho = resolver_astar(tabuleiro)
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
