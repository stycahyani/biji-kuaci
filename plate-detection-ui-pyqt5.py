import sys
import numpy as np
import cv2
import math
import Char
import Plate

from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout, QGroupBox, QPushButton, QLineEdit, QFileDialog
from PyQt5.QtGui import QFont, QPixmap, QImage


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.image = None
        self.title = "License Plate Detection TPKS"
        self.top = 150
        self.left = 225
        self.width = 1000
        self.height = 530

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.initUI()

        self.show()

    def initUI(self):

        # ui left side ______________________________________ #
        # label nama image
        self.lblTagImage = QLabel("<b> Image : </b>", self)
        self.lblTagImage.setGeometry(30, 20, 50, 20)
        self.lblTagImage.setFont(QFont("Calibri", 11))

        # label for browse button
        self.lblImage = QLabel(self)
        self.lblImage.setGeometry(30, 50, 600, 450)
        self.lblImage.setStyleSheet("background-color: #ffffff")

        #######################____________ INPUT ____________ ######################

        # label input size
        self.lblInput = QLabel("<b> Input Ukuran Karakter Plat : </b>", self)
        self.lblInput.move(670, 50)
        self.lblInput.setFont(QFont("Calibri", 11))

        # label jarak
        self.lblJarak = QLabel("Jarak", self)
        self.lblJarak.move(670, 90)
        self.lblJarak.setFont(QFont("Calibri", 11))

        # :
        self.lblJr = QLabel(" : ", self)
        self.lblJr.move(710, 90)
        self.lblJr.setFont(QFont("Calibri", 11))

        # line edit jarak
        self.lineJarak = QLineEdit(self)
        self.lineJarak.setGeometry(730, 90, 65, 20)
        self.lineJarak.setFont(QFont("Calibri", 11))
        self.lineJarak.setText("5")

        # label sudut
        self.lblSudut = QLabel("Sudut", self)
        self.lblSudut.move(670, 125)
        self.lblSudut.setFont(QFont("Calibri", 11))

        # :
        self.lblSdt = QLabel(" : ", self)
        self.lblSdt.move(710, 125)
        self.lblSdt.setFont(QFont("Calibri", 11))

        # line edit sudut
        self.lineSudut = QLineEdit(self)
        self.lineSudut.setGeometry(730, 125, 65, 20)
        self.lineSudut.setFont(QFont("Calibri", 11))
        self.lineSudut.setText("15.0")

        # label luaa
        self.lblLuas = QLabel("Luas", self)
        self.lblLuas.move(670, 160)
        self.lblLuas.setFont(QFont("Calibri", 11))

        # :
        self.lblLs = QLabel(" : ", self)
        self.lblLs.move(710, 160)
        self.lblLs.setFont(QFont("Calibri", 11))

        # line edit luas
        self.lineLuas = QLineEdit(self)
        self.lineLuas.setGeometry(730, 160, 65, 20)
        self.lineLuas.setFont(QFont("Calibri", 11))
        self.lineLuas.setText("0.5")

        # label lebar
        self.lblLebar = QLabel("Lebar", self)
        self.lblLebar.move(840, 90)
        self.lblLebar.setFont(QFont("Calibri", 11))

        # :
        self.lblLbr = QLabel(" : ", self)
        self.lblLbr.move(880, 90)
        self.lblLbr.setFont(QFont("Calibri", 11))

        # line edit lebar
        self.lineLebar = QLineEdit(self)
        self.lineLebar.setGeometry(900, 90, 65, 20)
        self.lineLebar.setFont(QFont("Calibri", 11))
        self.lineLebar.setText("0.8")

        # label tinggi
        self.lblTinggi = QLabel("Tinggi", self)
        self.lblTinggi.move(840, 125)
        self.lblTinggi.setFont(QFont("Calibri", 11))

        # :
        self.lblTg = QLabel(" : ", self)
        self.lblTg.move(880, 125)
        self.lblTg.setFont(QFont("Calibri", 11))

        # line edit tinggi
        self.lineTinggi = QLineEdit(self)
        self.lineTinggi.setGeometry(900, 125, 65, 20)
        self.lineTinggi.setFont(QFont("Calibri", 11))
        self.lineTinggi.setText("0.2")

        ##################___________________ BUTTON ___________________ ######################

        # hbox
        hbox = QHBoxLayout(self)

        # groupbox button
        groupbox = QGroupBox("Button Browse and Process Image", self)
        groupbox.setFont(QFont("Calibri", 11))
        groupbox.setGeometry(670, 220, 300, 120)

        # button browse
        self.btnBrowse = QPushButton("Browse", self)
        self.btnBrowse.setGeometry(40, 30, 85, 30)
        self.btnBrowse.setFont(QFont("Calibri", 11))
        self.btnBrowse.clicked.connect(self.browseImage)
        hbox.addWidget(self.btnBrowse)

        # button process image
        self.btnProcess = QPushButton("Process", self)
        self.btnProcess.setGeometry(140, 30, 85, 30)
        self.btnProcess.setFont(QFont("Calibri", 11))
        self.btnProcess.clicked.connect(self.processImage)
        hbox.addWidget(self.btnProcess)
        groupbox.setLayout(hbox)

        ##################___________________ CROP IMAGE _________________ ############
        # label plate
        self.lblPlate = QLabel("<b> Crop Plate : </b>", self)
        self.lblPlate.move(670, 370)
        self.lblPlate.setFont(QFont("Calibri", 11))

        # label for crop license plate image
        self.imgCrop = QLabel(self)
        self.imgCrop.setGeometry(670, 405, 140, 45)
        self.imgCrop.setStyleSheet("background-color: #ffffff")


    def browseImage(self):
        fname, _ = QFileDialog.getOpenFileName(None, "Browse Image", ".", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if fname:
            with open(fname, "rb") as file:
                data = np.array(bytearray(file.read()))

                self.image = cv2.imdecode(data, cv2.IMREAD_UNCHANGED)
                self.displayImage()

    def processImage(self):
        if self.image is not None:

            # grayscale image
            hsv = cv2.cvtColor(self.image, cv2.COLOR_RGB2HSV)
            hue, saturation, value = cv2.split(hsv)
            gray = value

            # histogram equalization
            #eqhis = cv2.equalizeHist(value)
            #res = np.hstack((value, eqhis))

            # bilateral filter
            image = cv2.bilateralFilter(gray, 11, 17, 17)

            # proses morfologi
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
            top = cv2.morphologyEx(image, cv2.MORPH_TOPHAT, kernel)
            black = cv2.morphologyEx(image, cv2.MORPH_BLACKHAT, kernel)
            add = cv2.add(image, top)
            subtract = cv2.subtract(add, black)

            gauss = cv2.GaussianBlur(subtract, (29, 29), 0, 0)

            thresh = cv2.adaptiveThreshold(gauss, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 89, 7)

            contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            # cv2.drawContours(self.image, contours, -1, (0, 255, 0))

            # cek char dari kontur awal
            h, w = thresh.shape
            blankImg = np.zeros((h, w, 3), dtype=np.uint8)
            listMungkinChar = []
            ctrs = []
            count = 0

            # cek apakah kontur tsb char atau bukan
            for i in range(0, len(contours)):
                mungkinChar = Char.cariChar(contours[i])
                if Char.cekChar(mungkinChar) is True:
                    count = count + 1
                    listMungkinChar.append(mungkinChar)

            for char in listMungkinChar:
                ctrs.append(char.contour)

            cv2.drawContours(blankImg, ctrs, -1, (255, 255, 255))

            # mengcek apakah yang termasuk char tadi adalah char plat yang diinginkan
            # berdasarkan ukuran, jarak, sudut, dan banyaknya char
            list_plate = []
            list_match = []

            for char in listMungkinChar:
                def matchChar(char, listMungkinChar):
                    listMatching = []
                    for match in listMungkinChar:
                        if match == char:
                            continue

                        bedaJarakChar = self.bedaJarak(char, match)
                        bedaSudutChar = self.bedaSudut(char, match)
                        bedaLuasChar = self.bedaLuas(char, match)
                        bedaLebarChar = self.bedaLebar(char, match)
                        bedaTinggiChar = self.bedaTinggi(char, match)

                        if (bedaJarakChar < (char.Diagonal * float(self.lineJarak.text())) and bedaSudutChar < float(self.lineSudut.text())
                                and bedaLuasChar < float(self.lineLuas.text()) and bedaLebarChar < float(self.lineLebar.text())
                                and bedaTinggiChar < float(self.lineTinggi.text())):
                            listMatching.append(match)

                    return listMatching

                listMatching = matchChar(char, listMungkinChar)
                listMatching.append(char)

                if len(listMatching) < 5:
                    continue

                list_match.append(listMatching)

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


            # ROI AND CROP IMAGE ------------------------------------------ #######
            for listMatching in list_match:
                plate = Plate.Plate()
                panjangList = len(listMatching)
                listMatching.sort(key=lambda match: match.CenterX)

                # mencari titik tengah dari char plat
                CenterX = (listMatching[0].CenterX + listMatching[panjangList - 1].CenterX) / 2.0
                CenterY = (listMatching[0].CenterY + listMatching[panjangList - 1].CenterY) / 2.0
                plateCenter = CenterX, CenterY

                #set lebar dan tinggi plat
                plateWidth = int(((listMatching[panjangList - 1].sumbuX + listMatching[panjangList - 1].Width) - listMatching[0].sumbuX) * 1.2)

                # hitung tinggi char secara keseluruhan
                total_h = 0
                for char in listMatching:
                    total_h = total_h + char.Height

                average = total_h / panjangList
                plateHeight = int(average * 1.5)

                # hitung sudut plat dari beberapa char yang ada
                x = self.bedaJarak(listMatching[0], listMatching[panjangList - 1])
                y = listMatching[panjangList - 1].CenterY - listMatching[0].CenterY
                angle = math.asin(y / x)
                plateAngle = angle * (180 / math.pi)

                plate.Location = (tuple(plateCenter), (plateWidth, plateHeight), plateAngle)

                matrix_rotation = cv2.getRotationMatrix2D(tuple(plateCenter), plateAngle, 1.0)
                h, w, jmlChannel = self.image.shape
                img_rotation = cv2.warpAffine(self.image, matrix_rotation, (w, h))

                crop = cv2.getRectSubPix(img_rotation, (plateWidth, plateHeight), tuple(plateCenter))

                plate.Plate = crop
                if plate.Plate is not None:
                    list_plate.append(plate)

                # gambar ROI pada image asli
                for i in range(0, len(list_plate)):
                    point = cv2.boxPoints(list_plate[i].Location)

                    cv2.line(self.image, tuple(point[0]), tuple(point[1]), (0, 255, 0), 10)
                    cv2.line(self.image, tuple(point[1]), tuple(point[2]), (0, 255, 0), 10)
                    cv2.line(self.image, tuple(point[2]), tuple(point[3]), (0, 255, 0), 10)
                    cv2.line(self.image, tuple(point[3]), tuple(point[0]), (0, 255, 0), 10)

            self.displayImage()
            # code for display blank image after draw contours
            size = crop.shape
            step = crop.size / size[0]
            formatImg = QImage.Format_Indexed8

            if len(size) == 3:
                if size[2] == 4:
                    formatImg = QImage.Format_RGBA8888
                else:
                    formatImg = QImage.Format_RGB888
            img = QImage(crop, size[1], size[0], step, formatImg)
            img = img.rgbSwapped()

            self.imgCrop.setPixmap(QPixmap.fromImage(img))
            self.imgCrop.setScaledContents(True)


    def bedaJarak(self, Char1, Char2):
        x = abs(Char1.CenterX - Char2.CenterX)
        y = abs(Char1.CenterY - Char2.CenterY)

        jarak = math.sqrt((x**2) + (y**2))
        return jarak

    def bedaSudut(self, Char1, Char2):
        x = float(abs(Char1.CenterX - Char2.CenterX))
        y = float(abs(Char1.CenterY - Char2.CenterY))

        if x != 0.0:
            sudut = math.atan(y / x) #arc tangent
        else:
            sudut = 1.5708

        self.sudut = sudut * (180.0 / math.pi) #konversi sudut ke dalam bentuk derajat
        return self.sudut

    def bedaLuas(self, Char1, Char2):
        self.luas = float(abs(Char2.Area - Char1.Area)) / float(Char1.Area)

        return self.luas

    def bedaLebar(self, Char1, Char2):
        self.lebar = float(abs(Char2.Width - Char1.Width)) / float(Char1.Width)

        return self.lebar

    def bedaTinggi(self, Char1, Char2):
        self.tinggi = float(abs(Char2.Height - Char1.Height)) / float(Char1.Height)

        return self.tinggi

    def displayImage(self):
        size = self.image.shape
        step = self.image.size / size[0]
        formatImg = QImage.Format_Indexed8

        if len(size) == 3:
            if size[2] == 4:
                formatImg = QImage.Format_RGBA8888
            else:
                formatImg = QImage.Format_RGB888
        img = QImage(self.image, size[1], size[0], step, formatImg)
        img = img.rgbSwapped()

        self.lblImage.setPixmap(QPixmap.fromImage(img))
        self.lblImage.setScaledContents(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())
