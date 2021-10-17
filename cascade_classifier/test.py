import cv2 

hand_cascade = cv2.CascadeClassifier('Hand_detector.xml')

cap = cv2.VideoCapture(1)

#Check whether user selected camera is opened successfully.
if not (cap.isOpened()):
    print("Could not open video device")

minNeighbors = 20
minNeighbors_min = 20
minNeighbors_max = 40

targetWaitFrames = 3
targetCountdown = targetWaitFrames

frameHeight = 1080
frameWidth = 1920

handWidthFactor = 0.3

steerCorrection = 0
tiltCorrection = 0
speedCorrection = 0
while(True):

    # Capture frame-by-frame
    _, frame = cap.read()

    hands = hand_cascade.detectMultiScale(image = frame, scaleFactor=1.2, minSize = (10,10), maxSize = (200,200), minNeighbors=minNeighbors)

    for (x,y,w,h) in hands:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255),2)

    if (len(hands)>1):
        targetCountdown = targetWaitFrames
        minNeighbors +=1
        if (minNeighbors > minNeighbors_max):
            minNeighbors = minNeighbors_max

    elif (len(hands)<1):
        targetCountdown = targetWaitFrames
        minNeighbors -=1
        if (minNeighbors < minNeighbors_min):
            minNeighbors = minNeighbors_min
    else:
        targetCountdown -=1
        if (targetCountdown < 0):
            targetCountdown = 0
            for (x,y,w,h) in hands:
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0),2)
                xCenter = x+w/2
                yCenter = x+h/2
                steeringCorrection = xCenter-frameWidth/2
                tiltCorrection = yCenter-frameHeight/2
                speedCorrection = handWidthFactor - h/frameWidth
    

    # Display the resulting frame
    cv2.imshow('preview',frame)

    #Waits for a user input to quit the application
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
