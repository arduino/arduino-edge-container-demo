import cv2
import sys
import os


def detect_faces(f_cascade, colored_img, scaleFactor=1.1):
    img_copy = colored_img.copy()  # create a copy of the image
    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)  # convert image to grey scale for opencv
    faces = f_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=5)  # detect multiscale: some faces can be closer
    print('Faces found: ', len(faces))  # print faces found
    for (x, y, w, h) in faces:
        cv2.rectangle(img_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)  # draw rectangles on original coloured img
    return img_copy


def main():
    input_file = sys.argv[1]  # input file passed ad argument
    name, ext = os.path.splitext(input_file)
    output_file = name + '_ocv' + ext  # create the name of the output file
    test = cv2.imread(input_file)  # open the input file
    print('img loaded')
    haar_face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')  # load the cascade classifier trainig  file
    print('classifier loaded')
    faces_detected_img = detect_faces(haar_face_cascade, test)
    cv2.imwrite(output_file, faces_detected_img)  # save the image
    print('file saved')


if __name__ == '__main__':
    main()
