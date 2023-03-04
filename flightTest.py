# Import sys, OpenCV and the DJI Tello Python libraries
import sys
import cv2
from djitellopy import Tello

# Pathway functions

# Basic flight test, drone takes off, does a 360, and lands
def flightTest(drone):
    # Make the drone take off, turn 360 degree clockwise, then land
    drone.takeoff()
    drone.rotate_clockwise(360)
    drone.land()

# Open a video stream using pyGame
def videoStream(drone):
    # Start the drone's video stream
    drone.streamon()

    # Until Ctrl+C is pressed, display the drone's video in a PyGame window
    while True:
        # Get the frame from the drone's camera, get the actual image, resize it, feed it to the PyGame window
        frame = getFrame(drone)
        resizedFrame = cv2.resize(frame, (640, 480))
        cv2.imshow("Drone View", resizedFrame)
        cv2.waitKey(1)

# Take a picture with the drone's camera
def takePic(drone):
    # Get the frame from the drone
    frame = getFrame(drone)

    # Write to img file
    cv2.imwrite("dronePic.png", frame)


# Utility functions

# Create and return an instance of the Tello object
def createDrone():
    # Create an instance of Tello
    drone = Tello()

    # Open a connection to the drone
    drone.connect()

    # Log the battery level to the terminal
    print("Tello battery level: " + str(drone.get_battery()))

    return drone

# Get and return an image from the camera stream
def getFrame(drone):
    # Get frame read from the drone
    frameRead = drone.get_frame_read()

    # Extract the image data
    frame = frameRead.frame

    # Return the image
    return frame


# Main execution

# Get run type from command line argument
runType = sys.argv[1]

# Create drone
print("Creating Tello object...")
drone = createDrone()

# Route to correct path
match runType:
    case "flightTest":
        print("Running flight test")
        flightTest(drone)
    case "videoStream":
        print("Starting video stream")
        videoStream(drone)
    case "takePic":
        print("Taking a picture")
        takePic(drone)