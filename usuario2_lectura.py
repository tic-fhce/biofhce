#CODIGO PARA LA LECGTURA  DE USUARIOS DE LOS BIOMETRICOS  SOLO PARA LA BIOMETRICOS ZK800

import sys
import os
from zk import ZK, const
sys.path.insert(1,os.path.abspath("./pyzk"))

conn=None

zk= ZK('Ip',port=0,timeout=5,password=0,force_udp=False,ommit_ping=False)
lugar = 'Lugar'

try:
    conn = zk.connect() #conectamos el dispositivo
    conn.disable_device() #lo desabilitamos para hacer mas rrapido la transferencia
    users = conn.get_users() #recuperamos los usuarios
    for user in users:
        values = (user.user_id, user.name, 0, 0, 0,lugar,0)
        print(values)
    conn.test_voice() #verificamos la pruebade coneccion
    conn.enable_device() # abilitamos nuebamente el dispositivo
except Exception as e:
    print("Process terminate :{}",format(e))
finally:
    if conn:
        conn.disconnect()
