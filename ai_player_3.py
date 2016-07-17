#!/usr/bin/env python
# -*- coding: cp1252 -*-

#INCLUDES
#
# Añade aqui las librerias que requieras usando:
#   import <lib>
#


# La siguiente clase implementa la inteligencia artificial del jugador.
# ¡No edites en las secciones preprogramadas a los comentarios!¡Son usadas
# por el motor del juego!
#

class AiPlayer:
    """ AI_Player Class"""
    def __init__(self):
        self.playerID="IA 3"    #Introduce aqui tu nombre

        #
        # Escribe aqui tu codigo
        #

        ## Fin del constructor
        





    # Esta funcion es invocada desde la clase del juego y es la que devuelve 
    # el intento propuesto por la IA. ¡No modificar la entrada de parametros
    # ni el formato del retornos!
    #   Parametros:
    #       pass_len:   longitud de la contraseña en entero
    #       digit_size: maximo valor que puede tomar un digito (entre 0 y digit_size).
    #   Retorno:
    #       solucion:   array de enteros con la contraseña estimada
    def generarSolucion(self,pass_len,digit_size):
        solucion = [0 for d in range(pass_len)]
        #
        # Escribe aqui tu codigo
        #
        #print "\n -> "+self.playerID+" sends "+str(solucion)
        return solucion








    # Esta funcion captura la salida del juego principal ante la propuesta de una
    # posible solucion. Tambien es llamada cuando el juego finaliza, pasando una
    # lista vacia [] y True.
    #   Parametros:
    #       respuesta:  vector de 0,1 o 2, que indica si ha acertado, no ha acertado
    #                   pero el digito se encuentra en otra posicion o ha fallado.
    #                   El vector tiene el mismo tamaño que el de la contraseña.
    #       finalizado: booleano que indica si la partida ha terminado o no (None==False)
    #   Retorno:
    #       None
    #
    def recibirRespuesta(self,respuesta,finalizado=None):
        #
        # Escribe aqui tu codigo
        #
        #print " <- "+self.playerID+" gets "+str(respuesta)+"\n"
        pass



    ##
    ## Añade a partir de aqui los metodos privados que necesites
    ##
    
    #def __myMethods(self,params):
    #   Aqui tu codigo
    #
