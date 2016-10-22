#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import sys
import socketserver


class SIPRegistrerHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    data_client = {}

    def handle(self):
        self.wfile.write(b"Hemos recibido tu peticion")
        print('IP client: ' + self.client_address[0])
        print('PORT client: ' + str(self.client_address[1]))
        cliente = self.rfile.read().decode('utf-8').split()
        print(cliente[1])
        if cliente[0] == 'REGISTRER':
            self.data_client[cliente[1]] = self.client_address[0]
            self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')
        #for line in self.rfile:
       #     print("El cliente nos manda ", line.decode('utf-8'))

if __name__ == "__main__":       # ip, puerto
    serv = socketserver.UDPServer(('', int(sys.argv[1])), SIPRegistrerHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
