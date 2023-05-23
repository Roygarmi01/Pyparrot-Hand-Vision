#Importaciones
import keyboard #detecta las teclas que se pican
import time #OBSOLETO
import click #para el menu de confirmacion
from pyparrot.Bebop import Bebop #controlador del dron
import math #para operaciones matematicas avanzadas

#config del dron
bebop = Bebop(drone_type="Bebop2")

#Conexion del dron
print("connecting")
success = bebop.connect(20)
if success == False: #si no se conecta al dron, mata el programa
    print("Conexion del dron:",success)
    exit()
print("Conexion del dron:",success)

#Checar sensores dron, print bateria
bebop.ask_for_state_update()
print("sleeping")
print("Battery:", bebop.sensors.battery, "%")
bebop.smart_sleep(1)

#Parametros de movimiento, tipo velocidades maximas
bebop.set_max_tilt(10)
bebop.set_max_rotation_speed(10)
bebop.set_max_vertical_speed(0.5)

#Takeoff
print("PIQUE q PARA DESPEGAR")
while True:
    if keyboard.is_pressed("q"): #picar X para proseguir y despegar
        break
    if keyboard.is_pressed("a"): #picar C para matar al programa
        if click.confirm('Matar al programa?', default=True):
            exit()

print("DESPEGANDO")
bebop.safe_takeoff(10) #10 intentos de despegue
bebop.smart_sleep(0.5) #delay de medio segundo

#loop de control
while True:
    #Sensor de bateria
    print("Battery:", bebop.sensors.battery, "%,", end = ' ')
    #detección de teclado
    if keyboard.is_pressed("w"): #w acciona un circulo de seguimiento
        while True:
            if not keyboard.is_pressed("w"): #Cancelar Seguimiento
                break
            bebop.fly_direct(roll=15, pitch=0, yaw=-80, vertical_movement=0, duration=1)
            print(" ") #print para que no se rompa la consola
        print(" Constant Circle", end=' ')
    if keyboard.is_pressed("e"): #e acciona circulo infinito
        while True:
            if keyboard.is_pressed("s"): #Cancelar While
                break
            bebop.fly_direct(roll=15, pitch=0, yaw=-80, vertical_movement=0, duration=10)
            print(" ") #print para que no se rompa la consola
        print(" Circle While", end=' ')
    if keyboard.is_pressed("r"): #a acciona alejamiento
        for i in range(20,40):
            bebop.fly_direct(roll=0, pitch=-i, yaw=0, vertical_movement=10, duration=1)
            print(" ") #print para que no se rompa la consola
            print(i, end=' ')
            if keyboard.is_pressed("s"): #Cancelar For
                break
        for i in range(20,40):
            bebop.fly_direct(roll=0, pitch=i, yaw=0, vertical_movement=-5, duration=1)
            print(" ") #print para que no se rompa la consola
            print(i, end=' ')
            if keyboard.is_pressed("s"): #Cancelar For
                break
        print(" ") #print para que no se rompa la consola
        print(" Rocket", end=' ')
    if keyboard.is_pressed("t"): #t para accionar espiral
        while True:
            if keyboard.is_pressed("s"): #Cancelar While
                break
            for i in range(0,50):
                bebop.fly_direct(roll=15, pitch=5, yaw=-80, vertical_movement=20, duration=1)
                print(" ") #print para que no se rompa la consola
                print(i, end=' ')
                if keyboard.is_pressed("s"): #Cancelar For
                    break
            for i in range(0,50):
                bebop.fly_direct(roll=-15, pitch=-5, yaw=80, vertical_movement=-5, duration=1)
                print(" ") #print para que no se rompa la consola
                print(i, end=' ')
                if keyboard.is_pressed("s"): #Cancelar For
                    break
        print(" Cyclone", end=' ')
    if keyboard.is_pressed("q"): #q confirma que se quiere aterrizar
        print(" ")
        if click.confirm('QUIERE ATERRIZAR EL DRON?', default=True):
            print("LANDING")
            bebop.safe_land(5)
            print("CANCELANDO")
            break
    print(" ")

#----------------------------------------------------------------------------------------------------#
print("DONE - disconnecting") #desconexión del dron
bebop.disconnect()
