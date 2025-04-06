import cv2
import os
import subprocess

def face_authentication():
    # Load trained model
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    if not os.path.exists('trainer/trainer.yml'):
        print("Error: trainer.yml file not found! Train the model first.")
        return False

    recognizer.read('trainer/trainer.yml')
    
    # Load Haar cascade for face detection
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # Mapping IDs to names
    names = {0: 'Rahul'}#, 2: 'John'}  # Change/add IDs as needed
    
    # Initialize webcam
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640) # Set frame width
    cam.set(4, 480) # Set frame height
    
    # Define minimum window size for face recognition
    minW = int(0.1 * cam.get(3))
    minH = int(0.1 * cam.get(4))
    
    print("Scanning face for authentication...")
    
    while True:
        ret, img = cam.read()
        if not ret:
            print("Error: Failed to capture image from webcam.")
            break
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Convert image to grayscale
        faces = faceCascade.detectMultiScale(gray,
                                             scaleFactor=1.2,
                                             minNeighbors=5,
                                             minSize=(minW, minH))

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            
            # Convert confidence score into accuracy percentage
            accuracy = round(100 - confidence, 2)
            
            if accuracy > 40:  # Authentication threshold
                print("Authentication successful! Welcome,", names.get(id, "Unknown"))
                print("Confidence:", accuracy)
                
                cv2.putText(img, "Authentication successful!", (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                cv2.putText(img, f"Confidence: {accuracy}%", (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
                
                # Release resources
                cam.release()
                cv2.destroyAllWindows()
                return True
            
        cv2.imshow('Face Authentication', img)
        if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to exit
            break

    cam.release()
    cv2.destroyAllWindows()
    print("Authentication failed. Access denied.")
    return False

if __name__ == "__main__":
    if face_authentication():
        print("Launching Jarvis...")
        subprocess.run(["python", "main.py"])  # Ensure the filename of the second script is correct
