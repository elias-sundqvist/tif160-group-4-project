import cv2 

hand_cascade = cv2.CascadeClassifier('Hand_detector.xml')

cap = cv2.VideoCapture(0)

#Check whether user selected camera is opened successfully.
if not (cap.isOpened()):
    print("Could not open video device")

while(True):

    # Capture frame-by-frame
    _, frame = cap.read()

    hands = hand_cascade.detectMultiScale(image = frame, scaleFactor=1.2, minSize = [10,10], maxSize = [400,1100], minNeighbors = 20)

    for (x,y,w,h) in hands:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0),2)

    # Display the resulting frame
    cv2.imshow('preview',frame)

    #Waits for a user input to quit the application
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()