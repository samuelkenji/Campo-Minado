import pygame
import random

#Cria o campo dependendo da escolha do jogador
def campo():
    tamanho_escolha = int(input('Escolha um tamanho (9x9 ou 16x16):'))

    while tamanho_escolha != 9 and tamanho_escolha != 16:
        tamanho_escolha = int(input('Escolha um tamanho (9x9 ou 16x16):'))

    grade = [0]*tamanho_escolha
    for i in range(tamanho_escolha):
        grade[i] = [0]*tamanho_escolha

    return grade

#Aloca bombas aleatoriamente no campo escolhido pelo johador
def bomba(grade):
    bomba = -1
    b_quant = 0
    if len(grade) == 9:
        b_quant = 10 #Número de bombas
        cont = 0
        while cont < b_quant:
            eixo_x = random.randint(0,8)
            eixo_y = random.randint(0,8)
            if grade[eixo_x][eixo_y] != -1:
                grade[eixo_x][eixo_y] = bomba
                cont+=1
    elif len(grade) == 16:
        b_quant = 40
        cont = 0
        while cont < b_quant:
            eixo_x = random.randint(0,15)
            eixo_y = random.randint(0,15)
            if grade[eixo_x][eixo_y] != -1:
                grade[eixo_x][eixo_y] = bomba
                cont+=1

    achaBomba(grade)


def achaBomba(grade): #Itera sobre a matriz até achar uma bomba
    for x in range(len(grade)):
        for y in range(len(grade)):
            if grade[x][y] == -1:
                prox(grade, x, y) #Ao achar uma bomba, executa a função prox()

def limite(grade, lin, col): #Define os limites da matriz ('cantos')
    if lin < 0 or col < 0:
        return False
    if lin > len(grade)-1 or col > len(grade)-1:
        return False
    return True

def prox(grade, l, c): #Aumenta em 1 o valor dos elementos vizinhos
    for lin in range(-1,2):
        for col in range(-1,2):
            if limite(grade, l+lin, col+c) and grade[l+lin][c+col] != -1:
                grade[l+lin][col+c] += 1

def quadrado(grade, screen):#Colore os quadrados com a cor inicial do jogo.
    cor = (123, 124, 127)
    coord = [None]*len(grade)
    for c in range(len(grade)):
        coord[c] = [None]*len(grade)
        x = -1
        y = -1

    if len(grade) == 9:
        for i in range(0, 360, 40):
            x+=1
            for j in range(0, 360, 40):
                y += 1
                if y == 9:
                    y = 0

                pygame.draw.rect(screen, cor, (i,j,40,40),2)
                coordElementos = [i, j, i+40, j+40]
                coord[x][y] = coordElementos

                
    else:
        for i in range(0, 640, 40):
            x+=1
            for j in range(0, 640, 40):
                y+=1
                if y == 16:
                    y = 0
                pygame.draw.rect(screen, cor, (i,j,40,40),2)
                coordElementos = [i, j, i+40, j+40]
                coord[x][y] = coordElementos

    return coord

def buscaPosE(quadrado, grade, screen, statusMatriz): #Pega a posição do 'clique' do botão esquerdo
    pos = pygame.mouse.get_pos()
    coord = quadrado(grade, screen)

    

    for i in range(len(coord)):
        for j in range(len(coord[0])):
            if coord[i][j][0]<=pos[0]<=coord[i][j][2] and coord[i][j][1]<=pos[1]<=coord[i][j][3] and statusMatriz[i][j] == 0:
                if grade[i][j] == 0:
                    revelaVazio(grade, statusMatriz,i,j)
                    statusMatriz[i][j] = 1
                    status(grade, statusMatriz, screen, coord, i, j)
                elif grade[i][j] > 0:
                    statusMatriz[i][j] = 1
                    status(grade, statusMatriz, screen, coord, i, j)
                elif grade[i][j] == -1:
                    for i in range(len(coord)):
                        for j in range(len(coord[0])):
                            if grade[i][j]==-1:
                                pygame.draw.rect(screen, (239, 9, 17), (coord[i][j][0]+2, coord[i][j][1]+2, 38, 38))
                                pygame.display.update()
                            statusMatriz[i][j] = -1
                    status(grade, statusMatriz, screen, coord, i, j)

                break

def status(grade, statusMatriz, screen, coord, i, j):#Define quais quadrados podem ser marcados, revelados e quais são escondidos, além de verificar quando uma bomba foi ativada ou quando há um ganhador.
    
    contador = 0
    bombas = 0

    myfont = pygame.font.SysFont('Comic Sans MS', 14)

    for x in range(len(statusMatriz)):
        for y in range(len(statusMatriz)):
            if grade[x][y] == -1:
                bombas+=1
            if statusMatriz[x][y] == 1 and grade[x][y] == 0:
                contador+=1
                pygame.draw.rect(screen, (22, 79, 170), (coord[x][y][0]+2, coord[x][y][1]+2, 38, 38))
            elif statusMatriz[x][y] == 1 and grade[x][y] > 0:
                contador+=1
                pygame.draw.rect(screen, (22, 79, 170), (coord[x][y][0]+2, coord[x][y][1]+2, 38, 38))
                texto = str(grade[x][y])
                textsurface = myfont.render(texto, False, (255, 255, 255))
                screen.blit(textsurface, (coord[x][y][0] + 17, coord[x][y][1] + 15))

    if contador == len(grade)**2 - bombas:
        titulo = 'Você ganhou!'
        print(titulo)
        pygame.display.set_caption(titulo)
        for i in range(len(grade)):
            for j in range(len(grade)):
                statusMatriz[i][j] = 3
    elif statusMatriz[0][0] == -1:
        titulo = 'Você perdeu!'
        print(titulo)
        pygame.display.set_caption(titulo)
        


    
def revelaVazio(grade, statusMatriz, i, j):#Revela as casas próximas ao 'clique' do jogador que estão sem bombas.
    for x in range(-1, 2, 1):
        for y in range(-1, 2, 1):
            if limite(grade, x+i, y+j) and statusMatriz[x+i][y+j] == 0:
                statusMatriz[x+i][y+j] = 1
                if grade[x+i][y+j] == 0:
                    revelaVazio(grade, statusMatriz, x+i, y+j)
                


def buscaPosD(quadrado, grade, screen, statusMatriz, bandeira):#Pega a posição do 'clique' do botão direito
    pos = pygame.mouse.get_pos()
    coord = quadrado(grade, screen)
    

    for i in range(len(coord)):
        for j in range(len(coord[0])):
            if coord[i][j][0]<=pos[0]<=coord[i][j][2] and coord[i][j][1]<=pos[1]<=coord[i][j][3] and (statusMatriz[i][j] == 0 or statusMatriz[i][j] == 2):
                if statusMatriz[i][j] == 0:
                    pygame.draw.rect(screen, (22, 79, 170), (coord[i][j][0]+2, coord[i][j][1]+2, 38, 38))
                    screen.blit(bandeira, (coord[i][j][0]+11, coord[i][j][1]+11))
                    statusMatriz[i][j] = 2
                    
                elif statusMatriz[i][j] == 2:
                    pygame.draw.rect(screen, (200, 202, 206), (coord[i][j][0]+2, coord[i][j][1]+2, 38, 38))
                    statusMatriz[i][j] = 0

                break


def game(): #Executa todas as outras funções do jogo.
    pygame.init()
    pygame.font.init()
    
    print("\n 'REGRAS DO JOGO' \n O 'Campo Minado' é composto por dois campos à escolha do jogador(9x9 ou 16x16). \n O botão direito serve para revelar o que há no quadrado e o botão direito serve para marcar ou desmarcar uma bomba.\n Ao abrir um quadradinho, aparecerá um número que indica quantas bombas há próximas a esse quadrado.\n Vence o jogo quem não abrir nenhuma bomba! \n BOA SORTE!")

    grade = campo()
    bomba(grade)

    statusMatriz = [0]*len(grade)
    for x in range(len(grade)):
        statusMatriz[x] = [0]*len(grade)

    if len(grade) == 9:
        screen = pygame.display.set_mode((361, 361))
    else:
        screen = pygame.display.set_mode((641, 641))
    screen.fill((200, 202, 206))
    coord = quadrado(grade,screen)

    bandeira = pygame.image.load("bandeira.png").convert_alpha()
    bandeira = pygame.transform.scale(bandeira, (20, 20))

    rodando = True

    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == True:
                    buscaPosE(quadrado, grade, screen, statusMatriz)
                elif pygame.mouse.get_pressed()[2] == True:
                    buscaPosD(quadrado, grade, screen, statusMatriz, bandeira)
        pygame.display.update()
    pygame.quit()
    
game()
