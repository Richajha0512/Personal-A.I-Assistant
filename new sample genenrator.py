import cv2
import time

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(3, 640)
cam.set(4, 480)

detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

face_id = input("Enter a Numeric user ID here: ")
print("Taking samples, follow the instructions...")

positions = ["Keep your face straight", "Turn your face to the left", "Turn your face to the right"]
count = 0  # Initializing sampling face count

for position in positions:
    print(position)
    time.sleep(2)  # Pause for the user to adjust
    sample_per_position = 20  # Capture 20 images per position

    while count < sample_per_position * (positions.index(position) + 1):
        ret, img = cam.read()
        converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(converted_image, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            count += 1
            
            cv2.imwrite(f"samples/face.{face_id}.{count}.jpg", converted_image[y:y + h, x:x + w])
            cv2.imshow('image', img)

        k = cv2.waitKey(100) & 0xff
        if k == 27:  # Press 'ESC' to stop
            break
    
print("Samples taken, now closing the program...")
cam.release()
cv2.destroyAllWindows()
