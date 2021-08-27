import cv2 as cv
import numpy as np

background = cv.imread('background.jpg')

# Start webcam
cap = cv.VideoCapture(0)


def nothing(x):
    pass

cv.namedWindow('filter_frame_1')
cv.namedWindow('filter_frame_2')

cv.createTrackbar('threshold', 'filter_frame_1', 0, 100, nothing)

threshold = 18

# Create trackbars for color change
# Hue is from 0-179 for Opencv
cv.createTrackbar('HMin', 'filter_frame_2', 0, 179, nothing)
cv.createTrackbar('SMin', 'filter_frame_2', 0, 255, nothing)
cv.createTrackbar('VMin', 'filter_frame_2', 0, 255, nothing)
cv.createTrackbar('HMax', 'filter_frame_2', 0, 179, nothing)
cv.createTrackbar('SMax', 'filter_frame_2', 0, 255, nothing)
cv.createTrackbar('VMax', 'filter_frame_2', 0, 255, nothing)


# Initialize HSV min/max values
# (hMin = 0 , sMin = 60, vMin = 82), (hMax = 15 , sMax = 168, vMax = 171)
# hMin = sMin = vMin = hMax = sMax = vMax = 0
hMin = 0 
sMin = 60
vMin = 82
hMax = 15 
sMax = 208
vMax = 210
phMin = psMin = pvMin = phMax = psMax = pvMax = 0

# Set default value for Max HSV trackbars
cv.setTrackbarPos('HMax', 'filter_frame_2', hMax)
cv.setTrackbarPos('SMax', 'filter_frame_2', sMax)
cv.setTrackbarPos('VMax', 'filter_frame_2', vMax)

cv.setTrackbarPos('HMin', 'filter_frame_2', hMin)
cv.setTrackbarPos('SMin', 'filter_frame_2', sMin)
cv.setTrackbarPos('VMin', 'filter_frame_2', vMin)
cv.setTrackbarPos('threshold', 'filter_frame_1', threshold)

def createMask(background, foreground):
    # background = cv.blur(background, (6,6))
    diffImage = cv.absdiff(background, foreground)

    rows = diffImage.shape[0]
    cols = diffImage.shape[1]
    foregroundMask = np.zeros((rows, cols))

    # threshold = 50
    dist = np.linalg.norm(diffImage, axis=2)
    foregroundMask[dist > threshold] = 255
    return foregroundMask.astype(np.uint8)

# while(True):
for i in range(1000, 2000):
    ret, frame = cap.read()
    hMin = cv.getTrackbarPos('HMin', 'filter_frame_2')
    sMin = cv.getTrackbarPos('SMin', 'filter_frame_2')
    vMin = cv.getTrackbarPos('VMin', 'filter_frame_2')
    hMax = cv.getTrackbarPos('HMax', 'filter_frame_2')
    sMax = cv.getTrackbarPos('SMax', 'filter_frame_2')
    vMax = cv.getTrackbarPos('VMax', 'filter_frame_2')
    threshold = cv.getTrackbarPos('threshold', 'filter_frame_1')

    # cv.imwrite("background.jpg", frame)
    # break

    # frame = cv.blur(frame, (6,6))
    filter_frame_1 = createMask(background, frame)

    hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])

    skinRegion = cv.inRange(hsv_frame, lower, upper)
    ret,filter_frame_2 = cv.threshold(skinRegion,0,255,cv.THRESH_BINARY)

    filter_frame = cv.bitwise_and(filter_frame_1, filter_frame_2)

    se1 = cv.getStructuringElement(cv.MORPH_RECT, (2,2))
    filter_frame = cv.morphologyEx(filter_frame, cv.MORPH_OPEN, se1)

    cv.imwrite("dataset/five/{}.jpg".format(i), filter_frame)
    print(i)
    # cv.imshow("filter_frame_1", filter_frame_1)
    # cv.imshow("filter_frame_2", filter_frame_2)
    cv.imshow("filter_frame", filter_frame)


    # Print if there is a change in HSV value
    if((phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax) ):
        print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (hMin , sMin , vMin, hMax, sMax , vMax))
        phMin = hMin
        psMin = sMin
        pvMin = vMin
        phMax = hMax
        psMax = sMax
        pvMax = vMax

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

