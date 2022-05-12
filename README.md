# AI Gym Trainer
> *On-device, Real-time Body Pose Tracking*

<br>
Human Pose Estimation plays an important role in quantifying physical exercises. AI Gym Trainer as a platform assists to exercise with the right posture and provide real time continuous feedback in the aim to avoid injuries and help the user consciously take decisions of their workout regime. 

<br>

## What happens underneath the hood?

Leveraging the most advanced algorithm - **BlazePose**, succesfully on-demand detects the human body and infers *33 different landmarks* from a single frame. 

Traditionally the current standard of human body pose is the COCO Topology which detects 17 different landmarks localizing ankle, wrist, torso, arms, legs and face however, lacking scale and orientation and restricts to only a few landmarks.
BlazePose Topology provides additional 16 different landmarks, acting as a subset of BlazeFace and BlazePalm topologies.

<br>

![Human Pose estimation pipeline](https://1.bp.blogspot.com/-J66lTDBjlgw/XzVwzgeQJ7I/AAAAAAAAGYM/WBIhbOqzi4ICUswEOHv8r7ItJIOJgL9iwCLcBGAsYHQ/s0/image11.jpg)

<br>

## Features Provided
+ Allows users to monitor their body posture
+ Multiple exercises targeting chest, biceps, triceps, and legs to work on
+ Visual aided output and automatic detection of the exercise to vivisect each rep of your set
+ Connect with blogs on how to maintain the right diet and fuel the motivation to keep yourself fit!
+ Dashboard to render a visualised result after your workout

<br>

## How to run
1. Clone the repo
2. run :  `pip install -r /path/to/requirements.txt`
3. run : `python run main.py`

<br>

### Future Releases on the way:
1. Make user specific accounts to store data and extensively make the user experience more enhanced.
2. Dockerise and Deploy to servers for wider audience
3. Add multiple combination of exercises and create a roadmap for different areas of your body to be targeted