#codigo para la lectura de marcados, por el moemtno para todos los biometricos

import sys
import os
import json
import requests

sys.path.insert(1,os.path.abspath("./pyzk"))
from zk import ZK, const

# create ZK instance
conn = None
zk = ZK('ip', port=0, timeout=5, password=0, force_udp=False, ommit_ping=False)
lugar='lugar'

# creamos API REST - TOMCAT sistea EGOVF modulo SCC  afa636b2fb7cc7ef69d9a6b7ab1550e02472114f
api_url = "http://ip/fhce-egovf-scc/marcado/"
headers={"Content-Type":"application/json"}
respuesta=0

try:
    # connect to device

    conn = zk.connect()
    # disable device, this method ensures no activity on the device while the process is run
    conn.disable_device()
    # another commands will be here!
    # Example: Get All Users

    registros= conn.get_attendance()
    for r in registros:
        #print(r)
        times=r.timestamp
        fecha = times.strftime("%Y-%m-%d")
        hora = times.strftime("%H:%M:%S")
        gestion=times.strftime("%Y")
        mes=times.strftime("%m")
        dia=times.strftime("%d")
        h=times.strftime("%H")
        m=times.strftime("%M")
        if(int (gestion) == 2023 and int(mes)==4):
            values = (r.uid,int(r.user_id),fecha ,hora,int(gestion),int(mes),int(dia),int(h),int(m),r.punch,r.status,lugar)
            print(values,',')
            marcado={
                "_01uid":r.uid,
                "_02user_id":r.user_id,
                "_03fecha":fecha,
                "_04hora":hora,
                "_05gestion":gestion,
                "_06mes":mes,
                "_07dia":dia,
                "_08h":h,
                "_09m":m,
                "_10punch":r.punch,
                "_11rstatus":r.status,
                "_12lugar":lugar
            }
            response = requests.post(api_url,data=json.dumps(marcado),headers=headers)
            respuesta=response.status_code
            print(respuesta)
    # Test Voice: Say Thank You
    conn.test_voice()
    # re-enable device after all commands already executed
    conn.enable_device()
except Exception as e:
    print ("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()