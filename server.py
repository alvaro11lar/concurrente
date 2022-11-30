import socket
import threading
import sys
import pickle
import os


class Servidor():

    def __init__(self, host=socket.gethostname(), port=int(input("Que puerto quiere usar ? "))):
        self.clientes = []
        self.nicknames = []
        print('\nSu IP actual es : ', socket.gethostbyname(host))
        print('\n\tProceso con PID = ', os.getpid(), '\n\tHilo PRINCIPAL con ID =', threading.current_thread().getName(),
              '\n\tHilo en modo DAEMON = ', threading.current_thread().isDaemon(),
              '\n\tTotal Hilos activos en este punto del programa =', threading.active_count())
        self.s = socket.socket()
        self.s.bind((str(host), int(port)))
        self.s.listen(30)
        self.s.setblocking(False)

        threading.Thread(target=self.aceptarC, daemon=True).start()
        threading.Thread(target=self.procesarC, daemon=True).start()

        while True:  # funcion de cerrar
            msg = input('\n << SALIR = 1 >> \n')
            if msg == '1':
                print(" **** Me piro vampiro; cierro socket y mato SERVER con PID = ", os.getpid())
                self.s.close()
                sys.exit()
            else:
                pass

    def aceptarC(self):  # funcion para agregar nuevos clientes
        print('\nHilo ACEPTAR con ID =', threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ',
              threading.current_thread().isDaemon(), '\n\tPertenece al PROCESO con PID', os.getpid(),
              "\n\tHilos activos TOTALES ", threading.active_count())

        while True:
            try:
                conn, addr = self.s.accept()
                print(f"\nConexion aceptada via {addr}\n")
                conn.setblocking(False)
                self.clientes.append(conn)
            except:
                pass

    def procesarC(self):  # funcion que procesa los mensajes entrantes
        print('\nHilo PROCESAR con ID =', threading.current_thread().getName(), '\n\tHilo en modo DAEMON = ',
              threading.current_thread().isDaemon(), '\n\tPertenece al PROCESO con PID', os.getpid(),
              "\n\tHilos activos TOTALES ", threading.active_count())
        while True:
            if len(self.clientes) > 0:
                for c in self.clientes:
                    try:
                        data = c.recv(32)
                        mensaje = pickle.loads(data)
                        if mensaje.startswith('$'):  # si el mensaje empieza con un dollar, significa que es un username
                            self.nicknames.append(mensaje)
                        if data: self.broadcast(data, c)
                    except:
                        pass

    def broadcast(self, msg, cliente):  # envia el mensaje a los otros usuarios y lo guarda en el log
        for c in self.clientes:
            print("Clientes conectados Right now = ", len(self.clientes))
            print(*self.nicknames, sep="\n")  # imprimimos la lista de usuarios
            try:
                if len(self.nicknames) > 0:
                    for x in self.clientes:
                        if x == cliente:  # buscamos la posicion del username del usuario
                            numero = self.clientes.index(x)
                    mensajeconnick = self.nicknames[numero] + ": " + pickle.loads(msg)  # escribimos el username antes del mensaje
                    print(mensajeconnick)
                    c.send(pickle.dumps(mensajeconnick))
                    with open('21535220.txt', 'a') as f:  # guardamos el log de los mensajes
                        f.write('\n' + mensajeconnick)
            except:
                self.clientes.remove(c)


arrancar = Servidor()