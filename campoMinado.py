import pygame
import random


#Cria o campo
def campo():
    tamanho_escolha = int(input('Escolha um tamanho (9x9 ou 16x16):'))

    while tamanho_escolha != 9 and tamanho_escolha != 16:
        tamanho_escolha = int(input('Escolha um tamanho (9x9 ou 16x16):'))

    grade = [0]*tamanho_escolha
    for i in range(tamanho_escolha):
        grade[i] = [0]*tamanho_escolha

    return grade

#Aloca bombas aleatoriamente no campo
def bomba(grade):
    bomba = -1
    b_quant = 0
    if len(grade) == 9:
        b_quant = 10 #Número de bombas
        for x in range(b_quant):
            eixo_x = random.randint(0,8)
            eixo_y = random.randint(0,8)
            grade[eixo_x][eixo_y] = bomba
    elif len(grade) == 16:
        b_quant = 40
        for x in range(b_quant):
            eixo_x = random.randint(0,15)
            eixo_y = random.randint(0,15)
            grade[eixo_x][eixo_y] = bomba

    achaBomba(grade)

    for x in range(len(grade)):
        for y in range(len(grade)):
            print(grade[x][y], end="\t")
        print("\n")

def achaBomba(grade): #Itera sobre a matriz até achar uma bomba
    for x in range(len(grade)-1):
        for y in range(len(grade)-1):
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

def quadrado(grade, screen):
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

def game():
    pygame.init()

    grade = campo()
    bomba(grade)

    if len(grade) == 9:
        screen = pygame.display.set_mode((361, 361))
    else:
        screen = pygame.display.set_mode((641, 641))
    screen.fill((200, 202, 206))
    coord = quadrado(grade,screen)

    rodando = True

    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == True:
                    pos = pygame.mouse.get_pos()
                    print(pos)
                    if coord[8][8][0]<=pos[0]<=coord[8][8][2] and coord[8][8][1]<=pos[1]<=coord[8][8][3]:
                        print('ultimo quadrado')
                else:
                    pos = pygame.mouse.get_pos()
                    print(pos)
        pygame.display.update()
    pygame.quit()
    
game()
