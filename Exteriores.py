#Importaciones
import keyboard #detecta las teclas que se pican
import time #OBSOLETO
import click #para el menu de confirmacion
from pyparrot.Bebop import Bebop #controlador del dron
import math #para operaciones matematicas avanzadas

#declaracion de variables, c/u controla un aspecto del dron
dx=0
dy=0
dz=0

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
bebop.set_max_tilt(30)
bebop.set_max_rotation_speed(30)
bebop.set_max_vertical_speed(1)

#Takeoff
print("PIQUE x PARA DESPEGAR")
while True:
    if keyboard.is_pressed("x"): #picar X para proseguir y despegar
        break
print("DESPEGANDO")
bebop.safe_takeoff(10) #10 intentos de despegue
bebop.smart_sleep(0.5) #delay de medio segundo

#loop de control
while True:

    #Sensor de bateria
    print("Battery:", bebop.sensors.battery, "%,", end = ' ')

    #detección de teclado
    if keyboard.is_pressed("q"): #Movimiento relativo tipo espiral
        for i in range(500, 1000):
            if keyboard.is_pressed("s"): #X confirma que se quiere aterrizar
                print(" ")
                bebop.safe_land(5)
                break
            x= i*math.cos(i/20)/70;
            y= i*math.sin(i/20)/70;
            z= i/150-3;
            dx=x-dx
            dy=y-dy
            dz=z-dz
            bebop.moveBy(dx, dy, dz, 0);
            print("Spiral", end=' ')
    if keyboard.is_pressed("w"): #Movimiento relativo tipo circulo
        for i in range(0,100):
            if keyboard.is_pressed("s"): #X confirma que se quiere aterrizar
                print(" ")
                bebop.safe_land(5)
                break
            x= 10*math.cos(i/14);
            y= 10*math.sin(i/14);
            dx=x-dx
            dy=y-dy
            dz=z-dz
            bebop.moveBy(dx,dy,dz,0);
            print("Circle", end=' ')
    if keyboard.is_pressed("e"): #Movimiento relativo tipo Y=X^3
        for i in range(0,5):
            if keyboard.is_pressed("s"): #X confirma que se quiere aterrizar
                print(" ")
                bebop.safe_land(5)
                break
            x= (-2*i)/20;
            z= (i/70)**3;
            dx=x-dx
            dy=y-dy
            dz=z-dz
            bebop.moveBy(dx,dy, dz, 0);
            print("Rocket", end=' ')
    if keyboard.is_pressed("s"): #X confirma que se quiere aterrizar
        print(" ")
        bebop.safe_land(5)
        break
        print("CANCELANDO")
    dx=0
    dy=0
    dz=0
    #comando que mete el valor de todas las varibles de control a movimiento del dron
    print(" ")

#----------------------------------------------------------------------------------------------------#
print("DONE - disconnecting") #desconexión del dron
bebop.disconnect()
