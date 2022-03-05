import numpy as np

def compute(first_angle,second_angle, third_angle):
    first_angle = np.array(first_angle) # First
    second_angle = np.array(second_angle) # Mid
    third_angle = np.array(third_angle) # End
    
    radians = np.arctan2(third_angle[1]-second_angle[1], third_angle[0]-second_angle[0]) - np.arctan2(first_angle[1]-second_angle[1], first_angle[0] - second_angle[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 
