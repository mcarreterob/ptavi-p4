#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""

import sys
import socket

# Constantes. Dirección IP del servidor y contenido a enviar
#SERVER = 'localhost'
#PORT = 6001
#LINE = '¡Hola mundo!'

ip = sys.argv[1]
port = int(sys.argv[2])
metodo = sys.argv[3]
line = ' '.join(sys.argv[4:])

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
                   # tipo de red, tipo de paquete
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((ip, port))
    if metodo == 'REGISTER':
        line = 'REGISTER sip:' + line + ' SIP/2.0\r\n\r\n'
    print("Enviando:", line)             # bytes
    my_socket.send(bytes(line, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)
    print('Recibido -- ', data.decode('utf-8'))

print("Socket terminado.")
