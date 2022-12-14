import cv2
import numpy as np


videofile = 'demo.MP4'
cap = cv2.VideoCapture(videofile)

def resize(img, scale = 100):
    
    width = int(img.shape[1] * scale / 100)
    height = int(img.shape[0] * scale / 100)
    dim = (width, height)
    
    # resize image
    return cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

def combine2Center(img1, img2):

    img2 = resize(img2, 139)
    h1, w1, _ = img1.shape
    h2, w2, _ = img2.shape

    xoffset = int((w1 / 2) - (w2 / 2))
    yoffeset = int((h1 / 2) - (h2 / 2) + 12)
    
    ret = img1.copy()

    ret[yoffeset:yoffeset + img2.shape[0], xoffset:xoffset + img2.shape[1]] = img2


    return ret

def get_thermal(image, x, y, gain = True):
    """
    if gain = True then temperture range is between -40 °C to 150 °C
    otheerwise if gain is false then temperture range is between -40 °C to 550 °C
    """
    if gain:
        return round((190*(image[y][x]/255) - 40))

    return round((590*(image[y][x]/255) - 40))

def main():

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:

        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        x = int(gray.shape[1] / 2)
        y = int(gray.shape[0] / 2)

        temp = get_thermal(gray, x, y)

        cv2.putText(frame, f"{temp}C", (x + 3, y - 20), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1)
        cv2.circle(frame, (x, y), 4, (255, 255, 255), -1)
        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break

if __name__ == '__main__':
    main()
