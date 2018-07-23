import cv2

camera_port = 0  # number of your camera port
ramp_frames = 15  # number of frames to skip (to take a better photo)
camera = cv2.VideoCapture(camera_port)  # initialize the camera


def get_image():
    return_value, image = camera.read()  # take the photo
    return image  # return the photo


for i in range(ramp_frames):  # skips some frames to take a better photo
    temp = get_image()
print("Taking image...")
camera_capture = get_image()  # take the photo
print("Done!")
file = "/data/opencv.png"  # path to save the photo
cv2.imwrite(file, camera_capture)  # save the photo
del(camera)
