import pygame
import sys
import random
import heapq

TAMANHO = 300
TAMANHO_BOTAO = 100
ALTURA_TOTAL = TAMANHO + TAMANHO_BOTAO
TAMANHO_CELULA = TAMANHO // 3
FPS = 60
FONT_SIZE = 40
VEL_ANIMACAO = 10

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (200, 200, 200)
AZUL = (100, 149, 237)
VERDE = (34, 139, 34)

MOVIMENTOS = ['cima', 'baixo', 'esquerda', 'direita']

def criar_tabuleiro():
    numeros = list(range(1, 9)) + [0]
    while True:
        random.shuffle(numeros)
        tabuleiro = [numeros[i:i+3] for i in range(0, 9, 3)]
        if eh_solucionavel(tabuleiro):
            return tabuleiro

def tabuleiro_para_estado(tabuleiro):
    return tuple(num for linha in tabuleiro for num in linha)

def estado_para_tabuleiro(estado):
    return [list(estado[i:i+3]) for i in range(0, 9, 3)]

def contar_inversoes(estado):
    numeros = [n for n in estado if n != 0]
    inversoes = 0
    for i in range(len(numeros)):
        for j in range(i+1, len(numeros)):
            if numeros[i] > numeros[j]:
                inversoes += 1
    return inversoes

def eh_solucionavel(tabuleiro):
    estado = tabuleiro_para_estado(tabuleiro)
    return contar_inversoes(estado) % 2 == 0

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
    return tabuleiro_para_estado(tabuleiro) == tuple(range(1, 9)) + (0,)

def heuristica_manhattan(estado):
    distancia = 0
    for idx, valor in enumerate(estado):
        if valor == 0:
            continue
        objetivo_idx = valor - 1
        linha_atual, coluna_atual = divmod(idx, 3)
        linha_objetivo, coluna_objetivo = divmod(objetivo_idx, 3)
        distancia += abs(linha_atual - linha_objetivo) + abs(coluna_atual - coluna_objetivo)
    return distancia

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
        return None

    novo_estado[idx], novo_estado[destino_idx] = novo_estado[destino_idx], novo_estado[idx]
    return tuple(novo_estado)

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
            return caminho

        for direcao in MOVIMENTOS:
            novo_estado = mover_estado(estado, direcao)
            if novo_estado and novo_estado not in visitados:
                novo_g = g + 1
                novo_f = novo_g + heuristica_manhattan(novo_estado)
                heapq.heappush(fila, (novo_f, novo_g, novo_estado, caminho + [direcao]))
                visitados.add(novo_estado)

    return None

def desenhar_tabuleiro(tela, tabuleiro, fonte):
    tela.fill(BRANCO)
    for i in range(3):
        for j in range(3):
            valor = tabuleiro[i][j]
            x = j * TAMANHO_CELULA
            y = i * TAMANHO_CELULA
            rect = pygame.Rect(x, y, TAMANHO_CELULA, TAMANHO_CELULA)
            pygame.draw.rect(tela, CINZA, rect, 3)
            if valor != 0:
                texto = fonte.render(str(valor), True, PRETO)
                texto_rect = texto.get_rect(center=rect.center)
                tela.blit(texto, texto_rect)

    # Botão
    botao_rect = pygame.Rect(0, TAMANHO, TAMANHO, TAMANHO_BOTAO)
    pygame.draw.rect(tela, AZUL, botao_rect)
    texto_botao = fonte.render("Resolver", True, BRANCO)
    tela.blit(texto_botao, texto_botao.get_rect(center=botao_rect.center))

def animar_movimento(tela, tabuleiro, direcao, fonte, som_clique):
    estado = tabuleiro_para_estado(tabuleiro)
    novo_estado = mover_estado(estado, direcao)
    if not novo_estado:
        return tabuleiro

    idx_vazio = estado.index(0)
    idx_mover = novo_estado.index(0)
    li, ci = divmod(idx_mover, 3)
    lf, cf = divmod(idx_vazio, 3)
    valor = estado[idx_mover]

    for i in range(1, VEL_ANIMACAO + 1):
        tela.fill(BRANCO)
        progresso = i / VEL_ANIMACAO
        for l in range(3):
            for c in range(3):
                v = tabuleiro[l][c]
                if v == 0 or v == valor:
                    continue
                rect = pygame.Rect(c * TAMANHO_CELULA, l * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA)
                pygame.draw.rect(tela, CINZA, rect, 3)
                texto = fonte.render(str(v), True, PRETO)
                tela.blit(texto, texto.get_rect(center=rect.center))
        # Anima a peça movendo
        x = ci * TAMANHO_CELULA + (cf - ci) * TAMANHO_CELULA * progresso
        y = li * TAMANHO_CELULA + (lf - li) * TAMANHO_CELULA * progresso
        rect = pygame.Rect(x, y, TAMANHO_CELULA, TAMANHO_CELULA)
        pygame.draw.rect(tela, CINZA, rect, 3)
        texto = fonte.render(str(valor), True, PRETO)
        tela.blit(texto, texto.get_rect(center=rect.center))

        pygame.display.update()
        pygame.time.delay(10)

    som_clique.play()
    return estado_para_tabuleiro(novo_estado)

def exibir_vitoria(tela, fonte):
    tela.fill(BRANCO)
    texto = fonte.render("VOCÊ VENCEU!", True, VERDE)
    tela.blit(texto, texto.get_rect(center=(TAMANHO // 2, TAMANHO // 2)))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    pygame.init()
    tela = pygame.display.set_mode((TAMANHO, ALTURA_TOTAL))
    pygame.display.set_caption("8 Puzzle")
    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont(None, FONT_SIZE)

    som_clique = pygame.mixer.Sound("click.wav")
    som_vitoria = pygame.mixer.Sound("win.wav")

    tabuleiro = criar_tabuleiro()
    resolvendo = False
    caminho = []
    passos = 0

    rodando = True
    while rodando:
        clock.tick(FPS)
        desenhar_tabuleiro(tela, tabuleiro, fonte)
        pygame.display.update()

        if resolvendo and passos < len(caminho):
            direcao = caminho[passos]
            tabuleiro = animar_movimento(tela, tabuleiro, direcao, fonte, som_clique)
            passos += 1

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if y < TAMANHO:
                    coluna = x // TAMANHO_CELULA
                    linha = y // TAMANHO_CELULA
                    if pode_mover(tabuleiro, linha, coluna):
                        mover(tabuleiro, linha, coluna)
                        som_clique.play()
                        if venceu(tabuleiro):
                            som_vitoria.play()
                            exibir_vitoria(tela, fonte)
                else:
                    caminho = resolver_astar(tabuleiro)
                    if caminho:
                        resolvendo = True
                        passos = 0

        if venceu(tabuleiro) and not resolvendo:
            som_vitoria.play()
            exibir_vitoria(tela, fonte)
            resolvendo = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
