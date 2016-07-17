#!/usr/bin/env python
# -*- coding: cp1252 -*-

# INCLUDES
import random
import collections
import aimastermind
#import ai_player_1
#import ai_player_2
#import ai_player_3
#import ai_player_4

# CLASSES & FUNCTIONS
#
# Las clases definen atributos y metodos/funciones.
#
# Los atributos self.<atributo> son accesibles desde cualquier funcion interna
# asi como desde el exterior de la clase. Se deben inicializar en __init__.
#
# Los metodos y funciones con __ no son accesibles desde el exterior de la clase.
#
class AiMasterMind:
    """ Clase principal de gestion del juego """
    #Constructor de la clase
    # Parametros
    #   pass_size: longitud de las contraseñas
    #   digit_size: maximo valor que puede tomar un digito entre [0,value)
    #   game_mode: modo de juego (0:equilibrado, 1:turnos)
    #   nom:    cantidad de partidas consecutivas a ejecutar
    #   player: numero de jugadores a enfrentar
    #
    def __init__(self,pass_size,digit_size,game_mode,nom,n_players):
        # Creamos los atributos de la clase
        print "\nINICIALIZANDO REGLAS DE JUEGO"
        self.passwords = []     #Contraseña a adivinar para cada jugador i
                                # Formato: [ [d1..dn] , ... ]
                                #  di: digito de la contraseña
        self.statistics = []    #Coleccion de estadisticas de cada jugador i
                                # Formato: [ [[TRY,RES,id],...] , ... ]
                                #  TRY[]: contraseña intentada por jugador i
                                #  RES[]: array de aciertos para cada digito de TRY
                                #  id: identificador de No. intento
        self.passSize = pass_size
        self.digitSize = digit_size
        self.gameMode = game_mode
        self.numOfMatches = nom
        self.numPlayers = n_players
        # Generamos y asignamos las contraseñas
        com_password = self.__generarPassword()
        for i in range(self.numPlayers):
            print " Generando password No."+str(i+1)+"..."
            self.passwords.append(self.__generarPassword() if self.gameMode==1 else com_password)
            self.statistics.append([[["_" for x in range(self.passSize)],[2 for y in range(self.passSize)],0]]) #Inicio de la base de datos para el jugador i


    #Funcion generadora de contraseñas aleatorias.
    # Parametros:
    #   None
    # Retorno:
    #   password: array de enteros
    #
    def __generarPassword(self):
        return [random.randint(0,self.digitSize) for digit in range(self.passSize)]


    #Funcion que comprueba para un jugador i si la contraseña propuesta coincide
    # con la que debe adivinar.
    # Parametros:
    #   passwordTry: array con la contraseña estimada
    #   player: numero id del jugador que hace el intento
    # Retorno:
    #   passwordRes: array que contiene el nivel de acierto para cada digito (0:acierto,1:semifallo o 2:fallo)
    def checkTry(self,passwordTry,player):
        passwordRes = [2 for digit in range(self.passSize)]
        dicP = collections.defaultdict(lambda:0,collections.Counter(self.passwords[player]))
        dicT = collections.defaultdict(lambda:0)
        #Analisis en dos pasadas:
        # 1.Primero descartamos y marcamos los digitos acertados
        # 2.Luego para cada fallo, comprobamos si es o no semifallo
        for d in range(self.passSize):
            if self.passwords[player][d] == passwordTry[d]:
                passwordRes[d] = 0  #ACIERTO: El digito coincide
                dicT[passwordTry[d]] += 1
        for d in range(self.passSize):  #FALLO: comprobamos si es semifallo (el digito esta en otra posicio)
            if (passwordRes[d] == 2) & (dicT[passwordTry[d]] < dicP[passwordTry[d]]):
                passwordRes[d] = 1
                dicT[passwordTry[d]] += 1
            
        #print "\n PAS: "+str(self.passwords[player])
        #print " TRY: "+str(passwordTry)
        #print " RES: "+str(passwordRes)
        #print " dicP:",dict(dicP)
        #print " dicT:",dict(dicT)

        #Actualizamos las estadisticas del jugador <player>
        self.statistics[player].append([passwordTry,passwordRes,len(self.statistics[player])])

        return passwordRes


    #Funcion que retorna el no. de intentos de un jugador
    def getNumberOfTries(self,player):
        return self.statistics[player][-1][2]

    #Funcion que retorna un array indicando los digitos acertados con una X
    def getDiscoveredDigits(self,player):
        discovered = [[],[]]
        for d in range(self.passSize):
            if self.statistics[player][-1][1][d]==0:
                discovered[0].append(self.statistics[player][-1][0][d])
                discovered[1].append('X')
            else:
                discovered[0].append('_')
                discovered[1].append('_')
        return discovered

    #Funcion que calcula el porcentaje de la contraseña descubierta
    def getPercentDiscovered(self,player):
        percent = 100 * self.statistics[player][-1][1].count(0) / float(self.passSize)
        return round(percent,1)

    #Funciones para mostrar las estadisticas de cada partida o jugador
    # Parametros:
    #   None: muestra las estadisticas globales de la partida (primera funcion)
    #   n_player: numero del jugador a mostrar (usar la segunda funcion)
    # Retorno:
    #   s: cadena con las estadisticas formateadas (usar print para mostrarlas)
    #
    def printGlobalStatistics(self):
        s = "Not implemented yet"
        return s

    def printStatisticsByPlayer(self,n_player,player_name):
        print "\nESTADISTICAS"
        s = "--- Jugador "+player_name+" ---"
        for r in range(1,len(self.statistics[n_player])):
            s += "\n"+str(self.statistics[n_player][r][2])+". "+str(self.statistics[n_player][r][0])+" :: "+str(self.statistics[n_player][r][1])
        s += "\n---    -"+("-" if n_player>9 else "")+"--    ---"
        return s

    #Esta funcion permite usar el print directamente sobre el objeto instanciado
    # Paramatros:
    #   None
    # Retorno:
    #   s: cadena a mostrar por pantalla
    #
    def __str__(self):
        # Usar "print <instancia>" para mostrar este contenido
        print "\nMOSTRANDO DATOS"
        s = "--- AiMasterMind ---\n"
        s += "\n No. Jugadores: " + str(self.numPlayers)
        p = []
        for j in range(self.numPlayers):
            p.append("\n  Password("+str(j+1)+"): ")
            for d in range(self.passSize):
                p[j] += " ["+str(self.passwords[j][d])+"]"
            s += "\n" + p[j]
                
        s += "\n\n\n Tam. Diccionario: " + str(self.digitSize) + " digitos\n"
        s += "\n Modo de Juego: " + ("Equilibrado" if self.gameMode==0 else "Aleatorio\n")
        s += "\n---     ----     ---"
        return s

######## FIN DE LA CLASE AiMasterMind
########
########
