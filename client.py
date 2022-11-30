import threading
import sys
import socket
import pickle
import os
#import de varias librerias que vamos a usar atraves del programa
class Cliente(): #clase cliente, la cua crea una entidad cliente

	def __init__(self, host=input("Intoduzca la IP del servidor ?  "), port=int(input("Intoduzca el PUERTO del servidor ?  ")), nickname=input("Intoduzca su NICKNAME  ")): #constructor de cliente
		#le paso los valores a los parmetros
		self.s = socket.socket()
		self.s.connect((host, int(port)))
		self.enviar('$'+nickname)
		print('\n\tProceso con PID = ',os.getpid(), '\n\tHilo PRINCIPAL con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tTotal Hilos activos en este punto del programa =', threading.active_count())
		threading.Thread(target=self.recibir, daemon=True).start()

		while True: #buscle donde pido el mensaje
			msg = input('\nEscriba texto ?   ** Enviar = ENTER   ** Salir Chat = 1 \n')
			if msg != '1' : self.enviar(msg)
			else:
				print(" **** Me piro vampiro; cierro socket y mato al CLIENTE con PID = ", os.getpid())
				self.s.close()
				sys.exit()

	def recibir(self): #funcion que especifica el hilo que recibo
		print('\nHilo RECIBIR con ID =',threading.currentThread().getName(), '\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())
		while True: #bucle para pedir el mensaje
			try:
				data = self.s.recv(32)
				if data: print(pickle.loads(data)) #deserializa el mensaje para que el cliente lo pueda ver
			except: pass

	def enviar(self, msg):
		self.s.send(pickle.dumps(msg)) #serializa el mensaje para poder ser enviado

arrancar = Cliente()