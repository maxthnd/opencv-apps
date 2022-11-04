# Imports
import mediapipe as mp;
import cv2 as cv2;


# Methods


# Main Class
def main():
    

    cap = cv2.VideoCapture(0)  # Aktiviere Video Input
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)  # Ausgabe-Fenster Breite
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)  # Ausgabe-Fenster Höhe

    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils

    finger_coordinates = [(8, 6), (12, 10), (16, 14), (20, 18)]
    thumb_coordinates = (4, 2)

    with mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        while True:
            success, image = cap.read()

            if not success:
                continue


            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            results = hands.process(image_rgb)

            multi_hand_landmarks = results.multi_hand_landmarks

            if multi_hand_landmarks:
                up_count = 0
                for multi_hand_landmark in multi_hand_landmarks:
                    hand_points = []

                    mp_draw.draw_landmarks(image, multi_hand_landmark, mp_hands.HAND_CONNECTIONS)

                    for i, hand_landmark in enumerate(multi_hand_landmark.landmark):
                        h, w, _ = image.shape
                        cx, cy = int(hand_landmark.x * w), int(hand_landmark.y * h) # Errechnung der Koordinate
                        hand_points.append((cx, cy)) # immutable

                    for hand_point in hand_points: 
                        cv2.circle(image, hand_point, 10, (200, 0, 200), cv2.FILLED)

                    for finger_coordinate in finger_coordinates:
                        if hand_points[finger_coordinate[0]][1] < hand_points[finger_coordinate[1]][1]:
                            up_count += 1

                    if hand_points[17][0] < hand_points[5][0]:
                        if hand_points[thumb_coordinates[0]][0] > hand_points[thumb_coordinates[1]][0]:
                            up_count += 1
                    elif hand_points[thumb_coordinates[0]][0] < hand_points[thumb_coordinates[1]][0]:
                        up_count += 1

                up_count_txt = str(up_count)

                (w, h), b = cv2.getTextSize(up_count_txt, cv2.FONT_HERSHEY_PLAIN, 10, 25) #(w, h) = Tupel

                label_w = 225
                label_h = 200
                label_x1 = 50
                label_y1 = 25
                label_x2 = label_x1 + label_w
                label_y2 = label_y1 + label_h
                label_coordinate1 = (label_x1, label_y1)
                label_coordinate2 = (label_x2, label_y2)

                txt_coordinate = (label_x1 + (label_w - w) // 2, label_y2 - 50)

                cv2.rectangle(image, label_coordinate1, label_coordinate2, (255, 255, 0), cv2.FILLED)
                cv2.putText(image, up_count_txt, txt_coordinate, cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 255), 25)

            cv2.imshow('image', image)

            if cv2.waitKey(1) == 27:
                break


if __name__ == '__main__':
    main()
