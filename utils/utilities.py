import numpy as np
import cv2

def preprocessing(cap,pose):
    _, frame = cap.read()
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    detections = pose.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    return image,detections

def assignAngles(image, angle1, pos1, angle2, pos2):
    cv2.putText(image, str(angle1), 
                    tuple(np.multiply(pos1, [640, 480]).astype(int)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)
                        
    cv2.putText(image, str(angle2), 
                    tuple(np.multiply(pos2, [640, 480]).astype(int)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)