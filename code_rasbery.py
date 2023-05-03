import utime
import network
import usocket
from machine import PWM,Pin

#Configuracion de servo  en el eje x
servo_x = PWM(Pin(14))
servo_x.freq(50)

#Configuracion de servo en el eje y
servo_y = PWM(Pin(15))
servo_y.freq(50)
angulo = 90
#configuracion de la conexion socket
socket_servidor = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
socket_servidor.bind(('0.0.0.0', 8080))
socket_servidor.listen(5)

# datos de red
ssid ='Wireless-UACh'
password = 'Chapingo'


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid,password)


#status de conexion wifi
max_wait = 10

while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >=3:
        break
    max_wait -= 1
    print('waiting for connection...')
    utime.sleep(1)
    
if wlan.status() !=3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print('ip = '+ status[0])
    
    
# comunicacion  a  traves de la libreria socket
while True:
    socket_cliente, direccion_cliente = socket_servidor.accept()
    print('Conexión recibida desde', direccion_cliente)
    
    while True:
        try:
            
            datos = socket_cliente.recv(4096) # aumentar el tamaño del buffer
            if not datos:
                break # Si no hay más datos, salir del bucle interno
            
            
            # Procesar los datos aquí
            datos_procesados = datos.decode().split(',') # ejemplo  
            print('Datos recibidos:', datos_procesados)
            
            dato = datos_procesados[0][0]
         

                     
            if dato == 'r':
                angulo  = angulo + 4
                if angulo > 180: # limite 180
                    angulo = 180
                duty = int((12.346*angulo**2 + 7777.8*angulo + 700000))
                servo_x.duty_ns(duty)
                print('right')
            elif dato == 'l':
                angulo = angulo - 4
                if angulo < 1: # limite 1
                    angulo = 1
                duty = int((12.346*angulo**2 + 7777.8*angulo + 700000))
                servo_x.duty_ns(duty)
                print('left')
            elif dato == 'u':
                angulo = angulo - 4
                if angulo < 50 : # limite 50
                    angulo = 50
                duty = int((12.346*angulo**2 + 7777.8*angulo + 700000))
                servo_y.duty_ns(duty)
                print('up')
            elif dato == 'd':
                angulo = angulo + 4
                if angulo > 120: # limite 180
                    angulo = 120
                duty = int((12.346*angulo**2 + 7777.8*angulo + 700000))
                servo_y.duty_ns(duty)
                print('down')
            #elif dato == 's':
             #   angulo = angulo
              #  duty = int((12.346*angulo**2 + 7777.8*angulo + 700000))
               # servo_y.duty_ns(duty)
                #servo_x.duty_ns(duty)
                #print('stop')
            
            
                
        except Exception as e:
            print('Error al recibir datos:', e)
            break # Si hay un error, salir del bucle interno
        
    socket_cliente.close()