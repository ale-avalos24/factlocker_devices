import requests, rfid
from time import sleep

while True:
    rfid = rfid.rfid_read()

    res_user = requests.post("http://192.168.135.170:3000/api/auth/preauth", json={"rfid_code": rfid}).json()

    if (res_user["result"] == "auth"):
        if (not res_user["factor"]):
            res_user["factor"] = "passcode"

        if (res_user["factor"] == "push"):
            print("Usuario encontrado. Acepte la verificacion de la app")

            param = {"username": res_user["username"]}
            
            try:
                res_push = requests.post("http://192.168.135.170:3000/api/auth/push", json=param, timeout=7).json()

                if (res_push["result"] == "allow"):
                    print("Acceso concedido")
                    sleep(3)
                elif (res_push["result"] == "deny"):
                    print("Acceso denegado")
                    sleep(3)
            except requests.Timeout:
                print("Tiempo agotado. Intenta otra vez.")
                sleep(3)

        elif (res_user["factor"] == "passcode"):
            print("Usuario encontrado. Ingreso el codigo de verificacion")

            passcode = input("Ingrese el codigo generado")
            param = {
                "username": res_user["username"],
                "passcode": passcode
            }
            res_user = requests.post("http://192.168.135.170:3000/api/auth/passcode", json=param, timeout=7).json()
    else:
        print("Usuario no encontrado")
        sleep(3)