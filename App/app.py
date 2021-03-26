import torch
from transformers import BertTokenizer, BertModel, BertConfig
from tqdm import tqdm
from summarizer import Summarizer

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys

import pickle
import os


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.textBox = QtWidgets.QTextEdit(self.centralwidget)
        self.textBox.setGeometry(QtCore.QRect(10, 50, 571, 411))
        self.textBox.setObjectName("textBox")

        self.readyButton = QtWidgets.QPushButton(self.centralwidget)
        self.readyButton.setGeometry(QtCore.QRect(590, 440, 90, 25))
        self.readyButton.setObjectName("readyButton")
        self.readyButton.clicked.connect(self.clickMethod)
        
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(590, 50, 171, 25))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(["Среднее","MAE","MSE","RMSE"])
        
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(560, 30, 231, 17))
        self.label_2.setObjectName("label_2")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 30, 141, 17))
        self.label.setObjectName("label")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.progressBar = QtWidgets.QProgressBar(MainWindow)
        self.progressBar.setGeometry(10, 480, 750, 30)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.readyButton.setText(_translate("MainWindow", "Готово"))
        self.label.setText(_translate("MainWindow", "Введите текст:"))
        self.label_2.setText(_translate("MainWindow", "Выберите функцию расстояния"))

    def ComputeError(self, embText, embProf):
        print("start compute")
        error = {}
        c = 0
        for name, arr in tqdm(embProf.items()):
            c += 1
            self.progressBar.setValue(int(c/60*100))
            sum = 0
            avg = 0
            mae = 0
            rmae = 0
            mse = 0
            rmse = 0
            for i in range(len(embText)):
                for arrRow in range(len(arr)):
                    for j in range(768):
                        sum  += embText[i][j] - arr[arrRow][j]
                        mae  += abs(embText[i][j] - arr[arrRow][j])
                        rmae += abs(embText[i][j] - arr[arrRow][j]) ** 0.5
                        mse  += (embText[i][j] - arr[arrRow][j]) ** 2
                        rmse += ((embText[i][j] - arr[arrRow][j]) ** 2) ** 0.5
            error[sum] = name
        return error

    def loadModel(self):
        device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        print(torch.cuda.get_device_name(0))

        custom_config = BertConfig.from_pretrained('DeepPavlov/rubert-base-cased')
        custom_config.output_hidden_states = True
        custom_tokenizer = BertTokenizer.from_pretrained('DeepPavlov/rubert-base-cased')
        custom_model = BertModel.from_pretrained('DeepPavlov/rubert-base-cased', config=custom_config)
        custom_model.to(device)
        custom_model.eval()
        print("load model")
        return Summarizer(custom_model=custom_model, custom_tokenizer=custom_tokenizer)

    def clickMethod(self):
        text = self.textBox.toPlainText()
        text = "".join([i.replace('\n', ' ').replace('\t', ' ') for i in text])
        modelSum =  self.loadModel()
        embText = modelSum.run_embeddings(text, num_sentences=10)
        print("compute")
        error =  self.ComputeError(embText, emb)
        QMessageBox.about(MainWindow, "Title", error[min(error.keys())])


def loadEmb():
    path = '../data/embeddingsPickle'
    directories = os.listdir(path)
    emb = {}
    for file in directories:
        with open(path + '/' + file, "rb") as f:
            arr = pickle.load(f)
            emb[file.split('.')[0]] = arr
    return emb


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    emb = loadEmb()
    MainWindow.show()
    sys.exit(app.exec_())
