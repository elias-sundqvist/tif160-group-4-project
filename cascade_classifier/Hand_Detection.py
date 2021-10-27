import cv2 

def handDetection(handWidthRatio, camera, agent):
    hand_cascade = cv2.CascadeClassifier('cascade_classifier/Hand_detector.xml')
    cap = camera
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    #Check whether user selected camera is opened successfully.
    if not (cap.isOpened()):
        print("Could not open video device")

    minNeighbors = 20
    minNeighbors_min = 20
    minNeighbors_max = 40

    targetWaitFrames = 0
    targetCountdown = targetWaitFrames

    frameHeight = 1080
    frameWidth = 1920

    steeringCorrection = 0
    tiltCorrection = 0
    speedCorrection = 0
    while(True):

        if agent.release:
            return 0, 0, 0, 0, 0

        # Capture frame-by-frame
        _, frame = cap.read()

        hands = hand_cascade.detectMultiScale(image = frame, scaleFactor=1.2, minSize = (10,10), maxSize = (200,200), minNeighbors=minNeighbors)
        
        if len(hands) > 0:
            print("Found hand")
        # for (x,y,w,h) in hands:
        #     cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255),2)

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
                    #cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0),2)
                    print(f"{(x,y,w,h)}")
                    xCenter = x+w/2
                    yCenter = x+h/2
                    steeringCorrection = xCenter-frameWidth/2
                    tiltCorrection = yCenter-frameHeight/2
                    speedCorrection = handWidthRatio - w/frameWidth +1

                break

       
        

    # When everything done, release the capture
    return steeringCorrection, tiltCorrection, speedCorrection, xCenter, yCenter

