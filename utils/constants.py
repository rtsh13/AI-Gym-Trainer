"""
Constants used throught the application
"""
# MediaPipe Constants
import mediapipe as mp
drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_drawing_styles = mp.solutions.drawing_styles
DETECTION = 0.5
TRACKING = 0.6

# Displaying Parameters
COUNTER = 0 
STAGE = None

# Arms Parameters
DUMBBELL = "Dumbbell"
BARBELL = "Barbell"
PUSHUPS = "Diamond Pushups"
BICEPS = "Bicep Curls"
CONCCURLS="Concentration curls"

# Legs Parameters
SQUATS = "Squats"
LUNGES = "Lunges"
JUMPING_JACKS = "Jumping Jacks"
SIDE_LEG_LIFTING = "Side Leg Lifting"

# Calculation Parameters
DOWN = "DOWN"
UP = "UP"