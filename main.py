#!/usr/bin/env python
# -*- coding: cp1252 -*-

# AUTHOR
#
# Daniel Jimenez Martinez (razorbreak@gmail.com)
#

# DESCRIPTION
#
# AiMasterMind es un juego en el que dos IAs (Inteligencias Artificiales) se
# enfrentan por ver quien de ellas descubre una contraseña generada
# aleatoriamente antes que su rival.
# La idea de este juego se basa en el MasterMind original.
#
# Cada IA puede usar cualquier tipo de algoritmo para su resolucion, tratando
# siempre de buscar la forma mas rapida y con menor coste posible.
#
# La implementacion de las IAs se realiza en los ficheros externos "ai_player_X.py"
# (mas info en los mismos).
#
# Modos de juego:
# ---------------
# EQUILIBRADO: ganara aquella que descubra la misma contraseña en menos
#              intentos. El turno y el orden se escogen aleatoriamente.
#
# ALEATORIO: cada rival tendra su propia contraseña aleatoria para adivinar.
#            El orden se establecera aleatoriamente antes de comenzar.
#

# INCLUDES
import aimastermind
import random
import collections
import pygame
###
import ai_player_1
import ai_player_2
import ai_player_3
import ai_player_4
# import ai_player_N
###


# VARS
# Añadir a la lista nuevos jugadores IA siguiendo el patron (no olvidar los import)
player_list = []
player_list.append((ai_player_1.AiPlayer(),1))
#player_list.append((ai_player_2.AiPlayer(),2))
#player_list.append((ai_player_3.AiPlayer(),3))
#player_list.append((ai_player_4.AiPlayer(),4))
#player_list.append((ai_player_N.AiPlayer(),N) #Seguir el mismo patron




#
# Editar segun la configuracion de juego deseada
#
pass_size = 10   #Longitud de la contraseña (en digitos)
digit_size = 25  #Valores que pueden tomar los digitos (de 0 hasta SIZE)
game_mode = 0   #Selector de modo de juego (0:equilibrado, 1:aleatorio).
nom = 3         #Number Of Matches: cantidad de veces que se jugara una partida
n_players = len(player_list)    #Number of players

time_round = 3  #Redondeo de la visualizacion de los tiempos de ejecucion (no. decimales)
ascii_mode = 0  #1:enabled, 0:disabled
displace = 97   #Solo modifica el dibujado en pantalla, para mostrar ASCII.
                # 48->0
                # 57->9
                # 97->a
                # 122->z
                #
                #Si se quiere mostrar letras de la 'a' a la 'z' basta con poner
                # 97 en displace y 25 en digit_size

extreme_visuals = False #Used to prevent extreme large window

# PRE-CONFIGURACION DE GRAFICOS Y PANTALLA
pygame.init()
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
Font_Led = "Resources/Fonts/Led.ttf"
Font_Visitor1 = "Resources/Fonts/visitor-tt1.ttf"
Font_Visitor2 = "Resources/Fonts/visitor-tt2.ttf"
tick_winner = pygame.image.load("Resources/Graphics/tick_winner.png")

columns = (2 if n_players>=2 else 1)
rows = int(round(float(n_players)/2))
win_width = 180 + 40*((pass_size-3) if pass_size>3 else 0)
win_height = 150
if win_width*columns > 1440:
    win_width = 380
    extreme_visuals = True
resolution = (win_width*columns,win_height*rows)
screen = pygame.display.set_mode(resolution)
caption = "AiMasterMind -"+("Equilibrado" if game_mode==0 else "Turnos")+"- by Razorbreak"
pygame.display.set_caption(caption)

clock = pygame.time.Clock()
FPS = 10 # Frames Per Second
exit = False





# Dibujar texto en pantalla, usando la fuente, tamaño y posicion establecida
def drawText(message,font_name,size,color,position,screen):
    screen.blit(pygame.font.Font(font_name,size).render(message,True,color),position)	

def drawArray(array,position,screen):
    s = " " # Un espacio o _ son 10*16px
    if not extreme_visuals:
        for d in range(len(array)):
            if ascii_mode:
                if type(array[d]) is int:
                    s += "["+str(chr(array[d]+displace))+"] "
                else:
                    s += "["+str(array[d])+"] "
            else:
                s += "["+str(array[d])+"] "
    else:
        s += "NOT AVAILABLE"
    drawText(s,Font_Visitor1,20,BLACK,position,screen)











# LOOP DE GRAFICOS PRINCIPAL
timers = [0.0 for i in range(n_players)]
positions = collections.defaultdict(lambda:0)
startgame = False
continuous = False
wins = collections.defaultdict(lambda:0)
winner = -1

print "\n\n\n=== PARTIDA No."+str(sum(wins.values())+1)+" ==="
newgame = aimastermind.AiMasterMind(pass_size,digit_size,game_mode,nom,n_players)    #Instanciamos un objetos de la clase

while not exit:
    # FETCH EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True #Finish game
        if event.type == pygame.KEYDOWN:
            #print "Keyboard:",event.key #Debug - Keyboard codes
            if event.key == pygame.K_r: #Press R to restart board
                print "\n\n\n\nRESETEANDO JUEGO...\n\n"
                newgame = aimastermind.AiMasterMind(pass_size,digit_size,game_mode,nom,n_players)    #Instanciamos un objetos de la clase
                random.shuffle(player_list)
                timers = [0.0 for i in range(n_players)]
                positions = collections.defaultdict(lambda:0)
                for n in range(n_players):
                    player_list[n][0].recibirRespuesta([],finalizado=True)
                wins = collections.defaultdict(lambda:0)
                startgame = False
                continuous = False
                start_time = pygame.time.get_ticks()
                winner = -1
            if event.key == pygame.K_q: #Press Q to quit
                exit = True
            if event.key == pygame.K_c: #Press C to change game mode
                game_mode = (0 if game_mode==1 else 1)
                caption = "AiMasterMind -"+("Equilibrado" if game_mode==0 else "Turnos")+"- by Razorbreak"
                pygame.display.set_caption(caption)
                print "\n\n\n\nRESETEANDO JUEGO...\n\n"
                newgame = aimastermind.AiMasterMind(pass_size,digit_size,game_mode,nom,n_players)    #Instanciamos un objetos de la clase
                random.shuffle(player_list)
                timers = [0.0 for i in range(n_players)]
                positions = collections.defaultdict(lambda:0)
                for n in range(n_players):
                    player_list[n][0].recibirRespuesta([],finalizado=True)
                wins = collections.defaultdict(lambda:0)
                startgame = False
                continuous = False
                winner = -1
                start_time = pygame.time.get_ticks()
            if event.key == pygame.K_s: #Press S to start match
                print "\n\n\n=== PARTIDA No."+str(sum(wins.values())+1)+" ==="
                random.shuffle(player_list)
                newgame = aimastermind.AiMasterMind(pass_size,digit_size,game_mode,nom,n_players)    #Instanciamos un objetos de la clase
                timers = [0.0 for i in range(n_players)]
                positions = collections.defaultdict(lambda:0)
                for n in range(n_players):
                    player_list[n][0].recibirRespuesta([],finalizado=True)
                start_time = pygame.time.get_ticks()
                startgame = True
                winner = -1
            if event.key == pygame.K_a: #Press A to launch every match
                if (not startgame)&(sum(wins.values())<nom):
                    print "\n\n\n=== PARTIDA No."+str(sum(wins.values())+1)+" ==="
                    random.shuffle(player_list)
                    newgame = aimastermind.AiMasterMind(pass_size,digit_size,game_mode,nom,n_players)    #Instanciamos un objetos de la clase
                    timers = [0.0 for i in range(n_players)]
                    positions = collections.defaultdict(lambda:0)
                    for n in range(n_players):
                        player_list[n][0].recibirRespuesta([],finalizado=True)
                    start_time = pygame.time.get_ticks()
                    continuous = True
                    startgame = True
                    winner = -1
            if event.key == pygame.K_d: #Press D to change between ASCII and Integer
                ascii_mode = not(ascii_mode)
                    

    # RENDERIZADO
    x0=5;x1=30;x2=x1+30;x3=0
    y0=5;y1=30;y2=y1+30;y3=y2+30
    screen.fill(WHITE)
    clock.tick(FPS)
    #Dibujado de los limites de la pantalla
    if columns==2:
        pygame.draw.line(screen,BLUE,(resolution[0]/2,0),(resolution[0]/2,resolution[1]),1)
    for i in range(rows-1):
        pygame.draw.line(screen,BLUE,(0,win_height*(i+1)),(resolution[0],win_height*(i+1)),1)

    #Codigo control y dibujado de los jugadores
    for pj in range(n_players):
        mx = (win_width if (pj+1)%2==0 else 0)
        my = (win_height*(pj/2) if (pj+1)>2 else 0)
        if startgame:
            #Codigo de control
            tim = pygame.time.get_ticks()
            pj_solution = player_list[pj][0].generarSolucion(pass_size,digit_size)
            timers[pj] += float(pygame.time.get_ticks() - tim)/1000
            pj_response = newgame.checkTry(pj_solution,pj)
            player_list[pj][0].recibirRespuesta(pj_response)

            if pj_response.count(0)==pass_size:
                wins[player_list[pj][1]] += 1
                print "\n\n >>> JUGADOR "+player_list[pj][0].playerID+" GANA! <<<"
                winner = pj
                print newgame,"\n"
                print dict(wins),"\n"
                for n in range(n_players):
                    player_list[n][0].recibirRespuesta([],finalizado=True)
                    print newgame.printStatisticsByPlayer(n,player_list[n][0].playerID)
                
                if not(continuous & (sum(wins.values()) < nom)):
                    startgame = False
                    continuous = False
                else:
                    print "\n\n\n=== PARTIDA No."+str(sum(wins.values())+1)+" ==="
                    random.shuffle(player_list)
                    newgame = aimastermind.AiMasterMind(pass_size,digit_size,game_mode,nom,n_players)    #Instanciamos un objetos de la clase
                    timers = [0.0 for i in range(n_players)]
                    positions = collections.defaultdict(lambda:0)
                    start_time = pygame.time.get_ticks()
                break
        elif (not startgame) & (winner == pj):
            screen.blit(tick_winner,(win_width+mx-40,y1+my-15))
                    
        discoveredPass = newgame.getDiscoveredDigits(pj)
        #Codigo de dibujado
        drawArray(discoveredPass[0],(x1+mx,y1+my),screen)
        drawArray(discoveredPass[1],(x1+mx,y2+my),screen)
        drawText("PASS:",Font_Visitor2,12,BLACK,(x0+5+mx,y1+5+my),screen)
        drawText("TRY:",Font_Visitor2,12,BLACK,(x0+5+mx,y2+5+my),screen)
        positions[pj] = newgame.getPercentDiscovered(pj)
        drawText("Completado: "+str(positions[pj])+"%",Font_Visitor1,15,BLACK,(x0+mx,y3+my),screen)
        drawText("Intentos: "+str(newgame.getNumberOfTries(pj)),Font_Visitor1,15,BLACK,(x0+mx,y3+15+my),screen)
        drawText("Tiempo: "+str(round(timers[pj],time_round)),Font_Visitor1,15,BLACK,(x0+mx,y3+30+my),screen)
        drawText("Wins: "+str(wins[player_list[pj][1]]),Font_Visitor1,15,BLACK,(win_width-60+mx,y3+30+my),screen)
        
    #Indicamos la posicion de cada jugador segun su % completado y tiempo tardado    
    pos = 1
    for i in sorted(positions,key=positions.get,reverse=True):
        mx = (win_width if (i+1)%2==0 else 0)
        my = (win_height*(i/2) if (i+1)>2 else 0)
        drawText(player_list[i][0].playerID+" ("+str(pos)+")",Font_Visitor1,15,BLACK,(x0+mx,y0+my),screen)
        pos += 1
        
    #Fin codigo dibujado
    pygame.display.flip()   #Volcado del render sobre la pantalla

print "\n\n\n=== FIN DEL JUEGO ==="
                    
pygame.quit()
