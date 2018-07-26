import cv2
import sys
import os

camera_port = 0  # number of your camera port
ramp_frames = 15  # number of frames to skip (to take a better photo)
camera = cv2.VideoCapture(camera_port)  # initialize the camera
output_file = "/data/opencv.png"  # path to save the photo

def get_image():
	return_value, image = camera.read()  # take the photo
	return image  # return the photo


def detect_faces(f_cascade, colored_img, scaleFactor=1.1):
	img_copy = colored_img.copy()  # create a copy of the image
	gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)  # convert image to grey scale for opencv
	faces = f_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=5)  # detect multiscale: some faces can be closer
	print("Faces found: " + str(len(faces)))  # print faces found
	for (x, y, w, h) in faces:
		cv2.rectangle(img_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)  # draw rectangles on original coloured img
	return img_copy, len(faces)


def main():
	for i in range(ramp_frames):  # skips some frames to take a better photo
		temp = get_image()
	print("Taking image...")
	camera_capture = get_image()  # take the photo
	print("Done!")
	haar_face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')  # load the cascade classifier trainig file
	print('Classifier loaded')
	faces_detected_img, n_faces = detect_faces(haar_face_cascade, camera_capture)
	if(n_faces>0): # check if at least a face is detected
		cv2.imwrite(output_file, faces_detected_img)  # save the image
		print('File saved')
	else:
		print('File NOT saved, no faces detected')
	camera.release()

if __name__ == '__main__':
	main()
