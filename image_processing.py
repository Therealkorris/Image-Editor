import cv2
import numpy as np
from PyQt5.QtGui import QImage

def process_image(img, controls):
    #print("Processing image with controls:", controls.keys())  # Debug print
    gamma = controls['Gamma'].value() / 10.0
    gamma_table = np.array([((i / 255.0) ** (1.0 / gamma)) * 255 for i in np.arange(0, 256)]).astype("uint8")

    img = cv2.add(img, np.array([controls['Brightness'].value()] * 3, dtype=np.int16))
    img = cv2.convertScaleAbs(img, alpha=1 + controls['Contrast'].value() / 100.0, beta=0)

    for i, color in enumerate(['Blue', 'Green', 'Red']):
        img[:,:,i] = cv2.add(img[:,:,i], controls[f'Color Balance {color}'].value())

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:,:,1] *= (1 + controls['Saturation'].value() / 100.0)
    hsv[:,:,0] = (hsv[:,:,0] + controls['Hue'].value()) % 180
    img = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

    if controls['Blur'].value() > 0:
        img = cv2.GaussianBlur(img, (controls['Blur'].value() * 2 + 1, controls['Blur'].value() * 2 + 1), 0)

    if controls['Sharpen'].value() > 0:
        kernel = np.array([[-1, -1, -1], [-1, 9 + controls['Sharpen'].value(), -1], [-1, -1, -1]])
        img = cv2.filter2D(img, -1, kernel)

    img = cv2.LUT(img, gamma_table)

    if controls['Noise'].value() > 0:
        noise = np.random.normal(0, controls['Noise'].value(), img.shape).astype(np.uint8)
        img = cv2.add(img, noise)

    if controls['Edge Detection'].value() > 0:
        edges = cv2.Canny(img, controls['Edge Detection'].value(), controls['Edge Detection'].value() * 2)
        img = cv2.addWeighted(img, 1, cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR), 0.5, 0)

    if controls['Greyscale'].isChecked():
        img = cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)

    if controls['Invert'].isChecked():
        img = cv2.bitwise_not(img)

    if controls['Sepia'].isChecked():
        sepia_kernel = np.array([[0.272, 0.534, 0.131],
                                 [0.349, 0.686, 0.168],
                                 [0.393, 0.769, 0.189]])
        img = cv2.transform(img, sepia_kernel)

    # Rotation
    rotation_index = controls['Rotation'].currentIndex()
    if rotation_index > 0:
        img = np.rot90(img, k=rotation_index)

    # Flip
    flip_index = controls['Flip'].currentIndex()
    if flip_index == 1:
        img = cv2.flip(img, 1)  # Horizontal flip
    elif flip_index == 2:
        img = cv2.flip(img, 0)  # Vertical flip

    return img

def cv_to_qimage(img):
    height, width, channel = img.shape
    bytes_per_line = 3 * width
    qimg = QImage(img.data.tobytes(), width, height, bytes_per_line, QImage.Format_RGB888)
    return qimg.rgbSwapped()