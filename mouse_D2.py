import cv2
import mediapipe as mp
from pynput.keyboard import Key, Controller

keyboard = Controller()

cap = cv2.VideoCapture(0)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

tipIds = [4, 8, 12, 16, 20]

def countFingers(image, hand_landmarks, handNo=0):

    global state 

    if hand_landmarks:

        landmarks = hand_landmarks[handNo].landmark

        fingers = []

        for lm_index in tipIds:
            #obtener la posicion de los d2
            finger_tip_y = landmarks[lm_index].y
            finger_bottom_y = landmarks[lm_index - 2].y

            #verificar si el d2 esta abierto o cerrado
            if lm_index != 4:
                if finger_tip_y < finger_bottom_y:
                    fingers.append(1)
                    #print("El dedo con id", lm_index, "esta abierto")

                if finger_tip_y > finger_bottom_y:
                    fingers.append(0)
                    #print("el dedo con id",lm_index, "esta cerrado. ")
                
        totalFingers = fingers.count(1)

        if totalFingers == 4:
            state = "play"

        if totalFingers == 0 and state == "play":
            state = "pause"
            keyboard.press(Key.space)
            
        finger_tip_x = (landmarks[8].x) * width
        if totalFingers == 1:
            if finger_tip_x < width-400:
                print("Anterior")
                keyboard.press(Key.left)

            if finger_tip_x > width-50:
                print("Siguiente")
                keyboard.press(Key.right)

def drawHandLandmarks(image, hand_landmarks):
    #dibuja las conexiones y puntos de la mano
    if hand_landmarks:

        for landmarks in hand_landmarks:
            
            mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)

while True:
    success, image = cap.read()

    if not success:
        print("No se pudo acceder a la cámara.")
        break

    image = cv2.flip(image, 1)

    results = hands.process(image)   
    hand_landmarks = results.multi_hand_landmarks

    #resultados
    drawHandLandmarks(image, results.multi_hand_landmarks)

    #obtener la posicion de los D2
    countFingers(image, results.multi_hand_landmarks)


    cv2.imshow("Controlador de medios", image)

    key = cv2.waitKey(1)
    if key == 32:
        break

    
cap.release()
cv2.destroyAllWindows()