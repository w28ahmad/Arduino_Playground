import cv2 as cv
import numpy as np
import serial

import torch
from torch.nn import Linear, ReLU, Sequential, Conv2d, MaxPool2d, Module, BatchNorm2d
import torchvision.transforms as transforms

class Net(Module):   
    def __init__(self):
        super(Net, self).__init__()

        self.cnn_layers = Sequential(
            # Defining a 2D convolution layer
            Conv2d(1, 4, kernel_size=3, stride=1, padding=1),
            BatchNorm2d(4),
            ReLU(inplace=True),
            MaxPool2d(kernel_size=2, stride=2),
            # Defining another 2D convolution layer
            Conv2d(4, 4, kernel_size=3, stride=1, padding=1),
            BatchNorm2d(4),
            ReLU(inplace=True),
            MaxPool2d(kernel_size=2, stride=2),
            # Defining another 2D convolution layer
            Conv2d(4, 4, kernel_size=3, stride=1, padding=1),
            BatchNorm2d(4),
            ReLU(inplace=True),
            MaxPool2d(kernel_size=2, stride=2),
            # Defining another 2D convolution layer
            Conv2d(4, 4, kernel_size=3, stride=1, padding=1),
            BatchNorm2d(4),
            ReLU(inplace=True),
            MaxPool2d(kernel_size=2, stride=2),
            # Defining another 2D convolution layer
            Conv2d(4, 4, kernel_size=3, stride=1, padding=1),
            BatchNorm2d(4),
            ReLU(inplace=True),
            MaxPool2d(kernel_size=2, stride=2),
        )

        self.linear_layers = Sequential(
            Linear(1200, 100),
            Linear(100, 50),
            Linear(50, 7)
        )

    # Defining the forward pass    
    def forward(self, x):
        x = self.cnn_layers(x)
        x = x.view(x.size(0), -1)
        x = self.linear_layers(x)
        return x


# load the model
model = Net()
model.load_state_dict(torch.load(r'models/model_95.ckpt', map_location=torch.device('cpu')))

valid_transform = transforms.Compose([transforms.ToPILImage(),
                                     transforms.ToTensor(),
                                     transforms.Normalize([7.524291],[43.089508])])

background = None

def createMask(background, foreground):
    # background = cv.blur(background, (6,6))
    diffImage = cv.absdiff(background, foreground)

    rows = diffImage.shape[0]
    cols = diffImage.shape[1]
    foregroundMask = np.zeros((rows, cols))

    threshold = 18
    dist = np.linalg.norm(diffImage, axis=2)
    foregroundMask[dist > threshold] = 255
    return foregroundMask.astype(np.uint8)


arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600)

hMin = 0 
sMin = 60
vMin = 82
hMax = 15 
sMax = 208
vMax = 210

# Start webcam
cap = cv.VideoCapture(0)
iter = 0

while(True):
    ret, frame = cap.read()
    if iter==0:
        background = frame

    # frame = cv.blur(frame, (6,6))
    filter_frame_1 = createMask(background, frame)
    # filter_frame_1 = cv.cvtColor(filter_frame_1, cv.COLOR_BGR2GRAY)
    # ret,filter_frame_1 = cv.threshold(filter_frame_1,20,255,cv.THRESH_BINARY)

    hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])

    skinRegion = cv.inRange(hsv_frame, lower, upper)
    ret,filter_frame_2 = cv.threshold(skinRegion,0,255,cv.THRESH_BINARY)

    filter_frame = cv.bitwise_and(filter_frame_1, filter_frame_2)

    se1 = cv.getStructuringElement(cv.MORPH_RECT, (2,2))
    filter_frame = cv.morphologyEx(filter_frame, cv.MORPH_OPEN, se1)

    if iter%20 == 0:
        filter_frame_transform = valid_transform(filter_frame)
        output = model(filter_frame_transform[None, ...])
        _, predicted = torch.max(output.data, 1)

        if predicted.item() != 6:
            arduino.write(bytes(str(predicted.item()), 'utf-8'))

    iter += 1
    cv.imshow("frame", filter_frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()




