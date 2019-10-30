import cv2
import numpy as np
import math
import Char
import Plate

###### PREPROCESSING ######

# open image
img = cv2.imread('dataset keseluruhan/1.jpg')

# resize image
h, w = img.shape[:2]
h, w = int(h / 3), int(w / 3)
img = cv2.resize(img, (w, h))

# cv2.imwrite("hasil/1 - resize.jpg", img)
# cv2.imshow("Resize", img)

# crop image
h, w = img.shape[:2]
x1, y1 = int(h * .20), int(w * .02)
x2, y2 = int(h * .85), int(w * .80)
img = img[x1:x2, y1:y2]
cv2.imwrite('2 - cropped.jpg', img)
# cv2.imshow("Crop", img)

# grayscale image
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
hue, saturation, value = cv2.split(hsv)
gray = value
# cv2.imwrite('hasil/3 - grey.jpg', gray)
# cv2.imshow("Gray", gray)

# billateral filter untuk mengurangi noise
# kernel
bilfil = cv2.bilateralFilter(gray, 11, 17, 17)
# cv2.imwrite('hasil/4 - bilateral filter.jpg', bilfil)
# cv2.imshow("Bilateral Filter", bilfil)

# operasi morfologi
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
top = cv2.morphologyEx(bilfil, cv2.MORPH_TOPHAT, kernel)
# cv2.imwrite('hasil/111 - top.jpg', top)

black = cv2.morphologyEx(bilfil, cv2.MORPH_BLACKHAT, kernel)
# cv2.imwrite('hasil/111 - black.jpg', black)

add = cv2.add(bilfil, top)
# cv2.imwrite('hasil/5 - add.jpg', black)

# operasi subtraction
subtract = cv2.subtract(add, black)
# cv2.imwrite('hasil/6 - subtract.jpg', subtract)

# operasi gaussian blur untuk mengurangi noice
gauss = cv2.GaussianBlur(subtract, (7, 7), 0)
# cv2.imwrite('hasil/7 - gaussian blur.jpg', gauss)

# thresholding
thresh = cv2.adaptiveThreshold(gauss, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY_INV, 19, 9)
cv2.imwrite('8 - threshold.jpg', thresh)
cv2.imshow("Threshold", thresh)

# cannyedge
# thresh = cv2.Canny(thresh, 170, 200)

# find and draw contours
contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
# a = cv2.drawContours(img, contours, -1, (0, 255, 0))
# cv2.imshow('kontur', img)
# cv2.imwrite('hasil/9 - kontur awal.jpg', img)


### MENGECEK ADA CHAR NGGA DI DALAM CONTOUR ###
h, w = thresh.shape
blankImg = np.zeros((h, w, 3), dtype=np.uint8)
listMungkinChar = []
ctrs = []
count = 0

# ngecek apakah kontur yang dibuat itu char atau bukan
for i in range(0, len(contours)):
    mungkinChar = Char.cariChar(contours[i])
    # nyari yang kemungkinan char, dimasukin ke list
    # list td kemudian di cek, beneran char atau nggak sesuai dengan ukuran yang sudah ditentukan
    if Char.cekChar(mungkinChar) is True:  # kalo bener, diitung countnya + 1, trs dimasukin ke list
        count = count + 1
        listMungkinChar.append(mungkinChar)
# cv2.imwrite('hasil/10 - kontur dua.jpg', blankImg)
# cv2.imshow("Kontur 2", blankImg)

for char in listMungkinChar:  # dari list char td, digambar konturnya
    ctrs.append(char.contour)  # dimasukin ke blank image yg dbuat dengan menggunakan matriks yg bernilai 0

cv2.drawContours(blankImg, ctrs, -1, (255, 255, 255))
# cv2.imshow('Mungkin Char', blankImg)
# cv2.imwrite('hasil/11 - kontur tiga.jpg', blankImg)
# cv2.imshow("Kontur 2", blankImg)

### NGECEK CHAR YANG DIINGINKAN SESUAI DENGAN UKURAN DAN BANYAKNYA CHAR YANG DIBUTUHKAN ###
list_plate = []
list_match = []


def bedaJarak(Char1, Char2):
    x = abs(Char1.CenterX - Char2.CenterX)
    y = abs(Char1.CenterY - Char2.CenterY)

    jarak = math.sqrt((x ** 2) + (y ** 2))
    return jarak


def bedaSudut(Char1, Char2):
    x = float(abs(Char1.CenterX - Char2.CenterX))
    y = float(abs(Char1.CenterY - Char2.CenterY))

    if x != 0.0:
        sudut = math.atan(y / x)  # arc tangent
    else:
        sudut = 1.5708

    sudut = sudut * (180.0 / math.pi)  # konversi sudut ke bentuk derajat

    return sudut


def bedaLuas(Char1, Char2):
    luas = float(abs(Char2.Area - Char1.Area)) / float(Char1.Area)

    return luas


def bedaLebar(Char1, Char2):
    lebar = float(abs(Char2.Width - Char1.Width)) / float(Char1.Width)

    return lebar


def bedaTinggi(Char1, Char2):
    tinggi = float(abs(Char2.Height - Char1.Height)) / float(Char1.Height)

    return tinggi


#####################

for char in listMungkinChar:
    def matchChar(char, listMungkinChar):
        listMatching = []
        for matchChar in listMungkinChar:
            if matchChar == char:
                continue

            # hitung perbedaan jarak, luas, lebar, dan tingginya
            bedaJarakChar = bedaJarak(char, matchChar)
            bedaSudutChar = bedaSudut(char, matchChar)
            bedaLuasChar = bedaLuas(char, matchChar)
            bedaLebarChar = bedaLebar(char, matchChar)
            bedaTinggiChar = bedaTinggi(char, matchChar)

            if (bedaJarakChar < (char.Diagonal) and bedaSudutChar < 15.0
                    and bedaLuasChar < 0.5 and bedaLebarChar < 0.8
                    and bedaTinggiChar < 0.2):
                listMatching.append(matchChar)

        return listMatching


    listMatching = matchChar(char, listMungkinChar)
    listMatching.append(char)

    # a = (len(max(listMatching,key=len))) #FindMaxLength(listMatching)

    if len(listMatching) < 5:
        continue

    list_match.append(listMatching)
    list_removed = list(set(listMungkinChar) - set(listMatching))

    recursive_match = []
    for recursive in recursive_match:
        list_match.append(recursive)
    break

blankImg = np.zeros((h, w, 3), dtype=np.uint8)

for listMatching in list_match:
    ctrs = []

    for match in listMatching:
        ctrs.append(match.contour)
    cv2.drawContours(blankImg, ctrs, -1, (255, 255, 0))

# cv2.imwrite('hasil/12 - kontur empat.jpg', blankImg)
cv2.imshow("Kontur Tiga", blankImg)

for listMatching in list_match:
    plate = Plate.Plate()
    panjangList = len(listMatching)
    listMatching.sort(key=lambda match: match.CenterX)

    # mencari titik tengah dari karakter di listMatching
    CenterX = (listMatching[0].CenterX + listMatching[len(listMatching) - 1].CenterX) / 2.0
    CenterY = (listMatching[0].CenterY + listMatching[len(listMatching) - 1].CenterY) / 2.0
    plateCenter = CenterX, CenterY

    # set lebar dan tinggi plat
    plateWidth = int(
        ((listMatching[panjangList - 1].sumbuX + listMatching[panjangList - 1].Width) - listMatching[0].sumbuX) * 1.2)

    # ngitung tinggi karakter keseluruhan
    total_h = 0
    for char in listMatching:
        total_h = total_h + char.Height

    avg = total_h / panjangList
    plateHeight = int(avg * 1.5)

    # hitung sudut plat berdasarkan char yang ada
    x = bedaJarak(listMatching[0], listMatching[panjangList - 1])
    y = listMatching[panjangList - 1].CenterY - listMatching[0].CenterY
    angle = math.asin(y / x)
    plateAngle = angle * (180 / math.pi)

    plate.Location = (tuple(plateCenter), (plateWidth, plateHeight), plateAngle)

    matrix_rot = cv2.getRotationMatrix2D(tuple(plateCenter), plateAngle, 1.0)
    h, w, nChannel = img.shape

    # merotasi image img dengan matriks rotation
    imgRot = cv2.warpAffine(img, matrix_rot, (w, h))

    # crop image plat yang terdeteksi
    crop = cv2.getRectSubPix(imgRot, (plateWidth, plateHeight), tuple(plateCenter))

    plate.Plate = crop
    if plate.Plate is not None:
        list_plate.append(plate)

    print(list_plate)

    # gambar ROI pada image asli
    for i in range(0, len(list_plate)):
        point = cv2.boxPoints(list_plate[i].Location)

        cv2.line(blankImg, tuple(point[0]), tuple(point[1]), (0, 255, 0), 2)
        cv2.line(blankImg, tuple(point[1]), tuple(point[2]), (0, 255, 0), 2)
        cv2.line(blankImg, tuple(point[2]), tuple(point[3]), (0, 255, 0), 2)
        cv2.line(blankImg, tuple(point[3]), tuple(point[0]), (0, 255, 0), 2)

        cv2.line(img, tuple(point[0]), tuple(point[1]), (0, 255, 0), 2)
        cv2.line(img, tuple(point[1]), tuple(point[2]), (0, 255, 0), 2)
        cv2.line(img, tuple(point[2]), tuple(point[3]), (0, 255, 0), 2)
        cv2.line(img, tuple(point[3]), tuple(point[0]), (0, 255, 0), 2)

cv2.imwrite('13 - License Plate Detection.jpg', img)
cv2.imshow("Deteksi", img)
cv2.imwrite('14 - Hasil Crop.jpg', crop)
cv2.imshow("Plate", crop)

cv2.waitKey(0)
cv2.destroyAllWindows()
