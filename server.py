#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import sys
import socketserver
import time
import json


class SIPRegistrerHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    data_client = {}

    def handle(self):
        print('IP client: ' + self.client_address[0])
        print('PORT client: ' + str(self.client_address[1]))
        self.cliente = self.rfile.read().decode('utf-8').split()
        print(self.cliente[-1])
        
        if self.cliente[0] == 'REGISTER':
            self.json2registered()
            self.now = time.time()
            self.client_list = []
            self.client_list.append(self.client_address[0])
            self.client_list.append(float(self.cliente[-1]) + float(self.now))
            self.data_client[self.cliente[1]] = self.client_list
            self.delete()
            self.client_list = []
        print(self.data_client)
        self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')
        self.register2json()

    def delete(self):
        """Metodo que eliminara un cliente del diccionario si ha expirado"""
        tmpList = []
        self.t_actual = time.strftime('%Y-%m-%d %H:%M:%S', 
                                      time.gmtime(time.time()))
        for client in self.data_client:
            self.expire = self.data_client[client][1]
            now = time.time()
            print("now", now, "expire", self.expire)
            if self.expire < now:
                tmpList.append(client)
        for cliente in tmpList:
            del self.data_client[cliente]
            print('ELIMINADO')
        self.register2json()


    def register2json(self):
        """Metodo con el que cada vez que un usuario se registre o se de 
        de baja, se imprimira en un fichero json con informacion sobre el
        usuario, su direccion y la hora de expiracion"""
        json.dump(self.data_client, open('registered.json', 'w'))

    def json2registered(self):
        """Metodo que comprobara si hay fichero json. Si hay, leera su
        contenido y lo usara como diccionario de usuarios. Si no hay, se
        ejecutara como si no hubiera fichero json"""
        try:
            with open('registered.json') as client_file:
                self.data_client = json.load(client_file)
                self.file_exists = True
        except:
            self.file_exists = False


if __name__ == "__main__":       # ip, puerto
    serv = socketserver.UDPServer(('', int(sys.argv[1])), SIPRegistrerHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
