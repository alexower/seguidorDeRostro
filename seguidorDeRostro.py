import cv2
import socket
import mediapipe as mp 

#Conexxion serial a la placa rasbery mediante wifi
ip_servidor = '10.11.202.55'
puerto_servidor = 8080
socket_serial = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_serial.connect((ip_servidor, puerto_servidor))

#iniciamos la libreria mediapipe 
detector = mp.solutions.face_detection
dibujo = mp.solutions.drawing_utils 

#conectamos la camaa web
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

#declaramos varibles de la cumincacion serial
right = 'r'
left = 'l'
stop = 's'
up = 'u'
down = 'd'

#Empezamos el while True si se detecta el rostro

with detector.FaceDetection(min_detection_confidence=0.75) as rostros:
    rostro_rastreado = False
    while True:
        ret, frame = cap.read()

        #Aplicamos espejo a los frames
        frame = cv2.flip(frame,1)

        #Correccion de color
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        #Detectamos los rostros
        resultado = rostros.process(rgb)


        #Si hay rostros entramos al if
        if resultado.detections is not None:
            for rostro in resultado.detections:
                # dibuja el recuadro
                if not rostro_rastreado:
                    dibujo.draw_detection(frame,rostro,dibujo.DrawingSpec(color=(255,0,255)))

                    for id, puntos in enumerate(resultado.detections):
                        #Mostramos toda la informacion
                        #print("Puntos: ", resultado.detections)

                        #Extraemos el ancho y el alto del frame
                        #al altura an ancho c canal
                        al, an, c = frame.shape

                        #Extraemos el medio de la pantalla de la altura y el ancho
                        centro_de_ancho  =  int(an / 2)
                        centro_de_altura =  int(al/2)
                        #print('Centro del frame', centro_de_ancho, centro_de_altura)
                        #Extraemos las coordenadas X e Y min
                        x = puntos.location_data.relative_bounding_box.xmin
                        y = puntos.location_data.relative_bounding_box.ymin

                        #Extraemos el ancho y el alto
                        ancho = puntos.location_data.relative_bounding_box.width
                        alto = puntos.location_data.relative_bounding_box.height

                        #Pasamos x e y a coordenadas en pixeles
                        x, y = int(x * an), int(y * al)
                        #print("X, Y: ", x, y)

                        #Pasamos el ancho y el alto del cuadro delimitador de rostros  a pixeles
                        x1, y1 = int(ancho * an), int(alto * al)

                        #Extraemos el punto central
                        cx = (x + (x + x1)) // 2
                        cy = (y + (y + y1)) // 2
                        #print("Centro: ", cx, cy)

                        #Mostrar un punto en el centro
                        cv2.circle(frame, (cx, cy), 6, (0, 255, 0),thickness=1, lineType=cv2.LINE_AA)
                        cv2.line(frame, (cx, 0), (cx, 480), (0, 255,0 ), 2)
                        cv2.line(frame, (0,cy ), (1000, cy), (0, 0, 255), 2)
                        
                        # Condiciones para mover el servo 
                        if cx < centro_de_ancho - 50:
                            #Movemos hacia la izquierda
                            print("Izquierda")
                            socket_serial.send(left.encode())
                            
                        elif cx > centro_de_ancho + 50:
                            #Movemos hacia la derecha
                            print("Derecha")
                            socket_serial.send(right.encode())
                            
                        elif cx == centro_de_ancho:
                            #Paramos el servo
                            print("Parar(X)")
                            socket_serial.send(stop.encode())
                            
                        elif cy < centro_de_altura-50:
                            print("arriba")
                            socket_serial.send(up.encode())
                            
                        elif cy > centro_de_altura + 50:
                            print("abajo")
                            socket_serial.send(down.encode())
                            
                        elif cy == centro_de_altura :
                            print("Parar(Y)")
                            socket_serial.send(stop.encode())
                            
                        

        cv2.imshow("imagenDeCamara", frame)
        t = cv2.waitKey(1)
        if t == 27:
            break
cap.release()
cv2.destroyAllWindows()