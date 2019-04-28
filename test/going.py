# -*- coding: utf-8 -*-
# @Time    : 2019/1/4 12:14
# @Author  : 胡子旋
# @FileName: going.py
# @Software: PyCharm
# @Email   ：1017190168@qq.com



from PyQt5.QtWebEngineWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import qtawesome
import dlib
import numpy as np
import cv2
import pandas as pd
import os
import csv
import datetime
import win32com.client
import time
from PyQt5.QtWidgets import *
from skimage import io as iio
import shutil
class Speak:
    def __init__(self):
        self.speak_out=win32com.client.Dispatch('SAPI.SPVOICE')
    def speak(self,data=''):
        self.speak_out.Speak(data)
        time.sleep(1)
path_make_dir = "face_image/"
path_feature_all = "recode/all_data.csv"

facerec = dlib.face_recognition_model_v1("E:/test/dlib_face_recognition_resnet_model_v1.dat")
# Dlib 预测器
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('E:/test/shape_predictor_68_face_landmarks.dat')
path_logcat_csv = "recode/data.csv"
def read_csv_to_recoders():
    recodes = []
    if os.path.exists(path_logcat_csv):
        with open(path_logcat_csv, "r", newline="") as csvfiler:
            reader = csv.reader(csvfiler)
            for row in reader:
                recodes.append(row)#包括header
    else:
        with open(path_logcat_csv, "w", newline="") as csvfilew:
            writer = csv.writer(csvfilew)
            header = ["姓名","日期","时间"]
            writer.writerow(header)
    return recodes
    pass
# 计算两个向量间的欧式距离
def return_euclidean_distance(feature_1, feature_2):
    feature_1 = np.array(feature_1)
    feature_2 = np.array(feature_2)
    dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
    print("欧式距离: ", dist)
    if dist > 0.4:
        return "diff"
    else:
        return "same"
path_feature_known_csv = "recode/all_data.csv"
csv_rd = pd.read_csv(path_feature_known_csv, header=None,encoding='gbk')
features_known_arr = []
for i in range(csv_rd.shape[0]):
    features_someone_arr = []
    for j in range(0, len(csv_rd.ix[i, :])):
        features_someone_arr.append(csv_rd.ix[i, :][j])
    #    print(features_someone_arr)
    features_known_arr.append(features_someone_arr)
print("数据库人脸数:", len(features_known_arr))
def get_128d_features(img_gray):
    dets = detector(img_gray, 1)
    shape = predictor(img_gray, dets[0])
    face_des = facerec.compute_face_descriptor(img_gray, shape)
    return face_des

class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui() #调用初始化的界面设置，展示界面的功能
    def init_ui(self):
        self.setFixedSize(960, 700)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格

        self.right_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)  # 设置右侧部件布局为网格

        self.right_widget_1 = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget_1.setObjectName('right_widget_1')
        self.right_layout_1 = QtWidgets.QGridLayout()

        self.right_widget_2 = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget_2.setObjectName('right_widget_2')
        self.right_layout_2 = QtWidgets.QVBoxLayout()
        self.right_widget_2.setLayout(self.right_layout_2)  # 设置右侧部件布局为网格

        ##
        self.right_widget_1.setLayout(self.right_layout_1)  # 设置右侧部件布局为网格
        self.main_layout.addWidget(self.left_widget, 0, 0, 12, 2)  # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget, 0, 2, 12, 10)  # 右侧部件在第0行第3列，占8行9列
        self.main_layout.addWidget(self.right_widget_1, 0, 2, 12, 10)  # 右侧部件_1在第0行第3列，占8行9列

##

        self.main_layout.addWidget(self.right_widget_2, 0, 2, 12, 10)

        self.setCentralWidget(self.main_widget)  # 设置窗口主部件
        self.left_close = QtWidgets.QPushButton("")  # 关闭按钮
        self.left_max = QtWidgets.QPushButton("")  # 最大按钮
        self.left_mini = QtWidgets.QPushButton("")  # 最小化按钮

        self.left_label_1 = QtWidgets.QPushButton("基础功能")
        self.left_label_1.setObjectName('left_label')
        self.left_label_2 = QtWidgets.QPushButton("拓展功能")
        self.left_label_2.setObjectName('left_label')
        self.left_label_3 = QtWidgets.QPushButton("联系与帮助")
        self.left_label_3.setObjectName('left_label')

        self.left_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.list-ol', color='white'), "签到记录")
        self.left_button_1.setObjectName('left_button')
        self.left_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.user', color='white'), "人脸识别")
        self.left_button_2.setObjectName('left_button')
        self.left_button_3 = QtWidgets.QPushButton(qtawesome.icon('fa.edit', color='white'), "信息录入")
        self.left_button_3.setObjectName('left_button')
        self.left_button_4 = QtWidgets.QPushButton(qtawesome.icon('fa.bar-chart', color='white'), "数据可视")
        self.left_button_4.setObjectName('left_button')
        self.left_button_5 = QtWidgets.QPushButton(qtawesome.icon('fa.envelope', color='white'), "定时发送")
        self.left_button_5.setObjectName('left_button')
        self.left_button_6 = QtWidgets.QPushButton(qtawesome.icon('fa.mail-reply', color='white'), "返回上层")
        self.left_button_6.setObjectName('left_button')
        self.left_button_7 = QtWidgets.QPushButton(qtawesome.icon('fa.weibo', color='white'), "建议反馈")
        self.left_button_7.setObjectName('left_button')
        self.left_button_8 = QtWidgets.QPushButton(qtawesome.icon('fa.star', color='white'), "关注我们")
        self.left_button_8.setObjectName('left_button')
        self.left_button_9 = QtWidgets.QPushButton(qtawesome.icon('fa.book', color='white'), "使用手册")
        self.left_button_9.setObjectName('left_button')
        self.left_xxx = QtWidgets.QPushButton(" ")
        self.left_layout.addWidget(self.left_mini, 0, 0, 1, 1)
        self.left_layout.addWidget(self.left_close, 0, 2, 1, 1)
        self.left_layout.addWidget(self.left_max, 0, 1, 1, 1)
        self.left_layout.addWidget(self.left_label_1, 1, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_1, 2, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_2, 3, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_3, 4, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_2, 5, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_4, 6, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_5, 7, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_6, 8, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_3, 9, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_7, 10, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_8, 11, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_9, 12, 0, 1, 3)
        self.left_close.setFixedSize(20,20)  # 设置关闭按钮的大小
        self.left_max.setFixedSize(20,20)  # 设置最大化按钮大小
        self.left_mini.setFixedSize(20,20)  # 设置最小化按钮大小
        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_max.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')
        self.left_widget.setStyleSheet('''
            QPushButton{border:none;color:white;}
            QPushButton#left_label{
                border:none;
                border-bottom:1px solid white;
                font-size:20px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
            QWidget#left_widget{
    background:gray;
    border-top:0px solid white;
    border-bottom:0px solid white;
    border-left:0px solid white;
    border-top-left-radius:10px;
    border-bottom-left-radius:10px;
}
        ''')
        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel#right_lable{
                border:none;
                font-size:16px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
        ''')
        self.right_widget_1.setStyleSheet('''
                        QWidget#right_widget_1{
                            color:#232C51;
                            background:white;
                            border-top:0px solid darkGray;
                            border-bottom:0px solid darkGray;
                            border-right:0px solid darkGray;
                            border-top-right-radius:10px;
                            border-bottom-right-radius:10px;
                        }
                        QLabel#right_lable_1{
                            border:none;
                            font-size:16px;
                            font-weight:700;
                            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                        }
                    ''')



        self.init_right()
        self.init_right_show()
        self.setWindowOpacity(2)  # 设置窗口透明度
        self.right_widget.setStyleSheet("QWidget#right_widget{border-image:url(./picture/main2.jpg)}")
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.main_layout.setSpacing(0)
        self.left_close.clicked.connect(self.main_close)
        self.left_mini.clicked.connect(self.main_min)
        self.left_max.clicked.connect(self.main_max)
        self.left_button_2.clicked.connect(self.show_camera)
        self.left_button_3.clicked.connect(self.recode)
        self.left_button_4.clicked.connect(self.data_view)
        self.left_button_6.clicked.connect(self.init_right)
        self.right_widget.hide()
        self.right_widget_2.hide()
        self.register_flag = 0
        self.sc_number=0
# 数据可视化界面初始化界面构造函数
    def init_right_show(self):
        self.listw = QtWidgets.QListWidget()
        self._translate = QtCore.QCoreApplication.translate
        # self.right_combox = QtWidgets.QComboBox(self.right_widget_2)
        # self.right_combox.addItem("")
        # self.right_combox.addItem("")
        # self.right_combox.addItem("")
        # self.right_combox.addItem("")
        # self.right_combox.setMinimumSize(30, 30)
        # self.right_combox.currentIndexChanged.connect(self.right_combox_click)
        self.right_browser = QWebEngineView()
        # self.create_data_image()
        self.right_browser.load(QtCore.QUrl('D:/python/test/render.html'))
        self.right_browser.setMinimumSize(400, 400)
        # self.right_combox.setItemText(0, self._translate("right_widget_2", "lzf"))
        # self.right_combox.setItemText(1, self._translate("right_widget_2", "qz"))
        # self.right_combox.setItemText(2, self._translate("right_widget_2", "hzx"))
        # self.right_combox.setItemText(3, self._translate("right_widget_2", "  "))
        # self.right_layout_2.addWidget(self.right_combox, 0)
        self.right_layout_2.addWidget(self.right_browser, 1)
        self.right_widget_2.setStyleSheet('''
                                QWidget#right_widget_2{
                                    color:#232C51;
                                    background:white;
                                    border-top:1px solid darkGray;
                                    border-bottom:1px solid darkGray;
                                    border-right:1px solid darkGray;
                                    border-top-right-radius:10px;
                                    border-bottom-right-radius:10px;
                                }
                                QComboBox{
            border:none;
            color:gray;
            font-size:30px;
            height:40px;
            padding-left:5px;
            padding-right:10px;
            text-align:left;
        }
        QComboBox:hover{
            color:black;
            border:1px solid #F3F3F5;
            border-radius:10px;
            background:LightGray;
        }
                            ''')

    def data_view(self):
        # self.browser = QWebEngineView()
        # url = 'D:/python/test/render.html'
        # self.browser.load(QUrl(url))
        # self.setCentralWidget(self.browser)
        self.right_widget.hide()
        self.right_widget_2.show()
    def main_min(self):
        self.showMinimized()
    def main_max(self):  # 界面的最大化和正常化的切换
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
    def main_close(self):
        exit()
    def recode(self):
        path_make_dir="face_image/"
        self.name,self. ok=QInputDialog.getText(self,"标题","输入姓名：")
        if self.ok:
            for exsit_name in (os.listdir(path_make_dir)):
                if self.name==exsit_name:
                    self.name=''
                    QMessageBox.question(self,"提示","信息重复\n"
                                                   "请重新输入",QMessageBox.Yes|QMessageBox.No)
                    break
                os.makedirs(path_make_dir+self.name)
                print("新建文件夹："+self.name)
                self.Duplicate_checking()
                '''接下来就是调用摄像头和受用者进行对比，如果数据库中的数据进行比对
                如果匹配成功，就不再提取，否则就提取使用者的脸部特征信息     '''
    def Duplicate_checking(self):
        self.left_button1()
        self.cap = cv2.VideoCapture()
        self.cap.open(0)
        while self.cap.isOpened():
            flag, img= self.cap.read()
            QtWidgets.QApplication.processEvents()
            cv2.waitKey(1)
            # print("标记")
            dets = detector(img, 1)
            font = cv2.FONT_HERSHEY_SIMPLEX
            if len(dets) != 0:
                shape = predictor(img, dets[0])
                features_cap = facerec.compute_face_descriptor(img, shape)
                name = "Welcome"
                pos = tuple([(int)((dets[0].left() + dets[0].right()) / 2) - 50
                                , dets[0].bottom() + 20])
                for i in range(len(features_known_arr)):
                    compare = return_euclidean_distance(features_cap, features_known_arr[i][0:-1])
                    if compare == "same":  # 找到了相似脸
                        name = features_known_arr[i][-1]
                        QMessageBox.question(self,"提示",name+"\n已经录入信息\n"
                                                            "请检查是否签到",QMessageBox.Yes|QMessageBox.No)
                        self.cap.release()
                        self.right_label_0.close()
                        data = self.name
                        os.rmdir("face_image/" + self.name)
                        print("删除重复文件", data)
                        break
                    # if compare=="diff":
                    else:
                        for self.sc_number in range(10):
                            self.height = dets[0].bottom() - dets[0].top()
                            self.width = dets[0].right() - dets[0].left()
                            # print("标记1")
                            self.sc_number+=1
                            im_blank = np.zeros((self.height, self.width, 3), np.uint8)
                            # print("标记2")
                            #这里的下面是有错误的
                            for ii in range(self.height):
                                for jj in range(self.width):
                                    # print("falg2")
                                    ## 错误在self.imblank这里
                                    im_blank[ii][jj] = img[dets[0].top() + ii][dets[0].left() + jj]
                                    # print("标记3")
                            cv2.imencode('.jpg', im_blank)[1].tofile(
                                path_make_dir + self.name + "/img_face_" + str(self.sc_number) + ".jpg")  # 正确方法
                            # print("标记4")
                            print("写入本地：", str(path_make_dir + self.name) + "/img_face_" + str(self.sc_number) + ".jpg")
                        self.cap.release()
                        self.right_label_0.close()
                        self.Write_info()
                        break
                cv2.rectangle(img, tuple([dets[0].left(), dets[0].top()]), tuple([dets[0].right(), dets[0].bottom()]),
                              (100, 255, 0), 2)
                cv2.putText(img,name,pos, font, 0.8, (255, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(img, "faces: " + str(len(dets)), (10, 40), font, 1, (0, 255, 200), 1, cv2.LINE_AA)
            height, width = img.shape[:2]
            image1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            showImage = QtGui.QImage(image1, width, height, QtGui.QImage.Format_RGB888)
            self.right_label_0.setPixmap(QtGui.QPixmap.fromImage(showImage))

    def Write_info(self):
        # print("标记")
        ## 这下面可能有错误。。。。。。。。。
        if self.register_flag == 1:
            if os.path.exists(path_make_dir + self.name):
                shutil.rmtree(path_make_dir + self.name)
                print("重复录入，已删除姓名文件夹", path_make_dir + self.name)
        # print("flag")
        ##测试时，这里有错，不知道怎么搞的
        ## 测试时间1.12

        if self.sc_number == 0 and len(self.name) > 0:
            # print("flag2")
            ## flag处也具有错误、、、、、、、
            ##
            if os.path.exists(path_make_dir + self.name):
                print("flag3")
                shutil.rmtree(path_make_dir + self.name)
                print("您未保存截图，已删除姓名文件夹", path_make_dir + self.name)


        if self.register_flag == 0 and self.sc_number != 0:
            # print("标记1")
            pics = os.listdir(path_make_dir + self.name)
            feature_list = []
            feature_average = []
            # print("标记2")
            for i in range(len(pics)):
                pic_path = path_make_dir + self.name + "/" + pics[i]
                print("正在读的人脸图像：", pic_path)
                img = iio.imread(pic_path)
                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                dets = detector(img_gray, 1)
                if len(dets) != 0:
                    shape = predictor(img_gray, dets[0])
                    face_descriptor = facerec.compute_face_descriptor(img_gray, shape)
                    feature_list.append(face_descriptor)
                    # print("标记3")
                else:
                    print("未在照片中识别到人脸")
            if len(feature_list) > 0:
                for j in range(128):
                    feature_average.append(0)
                    for i in range(len(feature_list)):
                        feature_average[j] += feature_list[i][j]
                    feature_average[j] = (feature_average[j]) / len(feature_list)
                feature_average.append(self.name)
                with open(path_feature_all, "a+", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    # print('成功写入数据库', feature_average)
                    print('人脸信息入库成功')
                    writer.writerow(feature_average)

    def left_button1(self):
        self.right_label_0 = QtWidgets.QLabel(self)
        self.right_label_0.setObjectName("right_label_0")
        pixmap = QtGui.QPixmap("picture/main.jpg")  # 按指定路径找到图片
        self.right_label_0.setPixmap(pixmap)  # 在label上显示图片
        self.right_label_0.setScaledContents(True)  # 让图片自适应label大小
        self.right_layout_1.addWidget(self.right_label_0, 1, 1, 1, 1)
    def init_right(self):
        self.right_label_0 = QtWidgets.QLabel(self)
        self.right_label_0.setObjectName("right_label_0")
        pixmap = QtGui.QPixmap("picture/main.jpg")  # 按指定路径找到图片
        self.right_label_0.setPixmap(pixmap)  # 在label上显示图片
        self.right_label_0.setScaledContents(True)  # 让图片自适应label大小
        self.right_layout_1.addWidget(self.right_label_0, 1, 1, 1,1)
        movie=QtGui.QMovie('recognition.gif')
        movie.setCacheMode(QtGui.QMovie.CacheAll)
        self.right_label_0.setMovie(movie)
        movie.start()

    def show_camera(self):
        self.left_button1()
        self.cap = cv2.VideoCapture()
        self.cap.open(0)
        while self.cap.isOpened():
            flag, img = self.cap.read()
            QtWidgets.QApplication.processEvents()
            cv2.waitKey(1)
            dets = detector(img, 1)
            font = cv2.FONT_HERSHEY_SIMPLEX
            if len(dets) != 0:
                shape = predictor(img, dets[0])
                features_cap = facerec.compute_face_descriptor(img, shape)
                name = "Welcome"
                pos = tuple([(int)((dets[0].left() + dets[0].right()) / 2) - 50
                                , dets[0].bottom() + 20])
                for i in range(len(features_known_arr)):
                    self.pun_day_num = 0
                    compare = return_euclidean_distance(features_cap, features_known_arr[i][0:-1])
                    if compare == "same":  # 找到了相似脸
                        name = features_known_arr[i][-1]
                        recoder = []
                        recoder.append(name)
                        localtime = datetime.datetime.now()
                        date = str(localtime.year) + "/" + str(localtime.month) + "/" + str(localtime.day)
                        time = str(localtime.hour) + ":" + str(localtime.minute) + ":" + str(localtime.minute)
                        recoder.append(date)
                        recoder.append(time)
                        recoders = read_csv_to_recoders()
                        for item in recoders:
                            if item[0] == recoder[0]:
                                self.pun_day_num += 1
                        for item in recoders:
                            if recoder[0] == item[0] and recoder[1] == item[1]:
                                begin = Speak()
                                begin.speak(data=str(name)+'签到成功！！你已签到' + str(self.pun_day_num) + '天，请勿重复操作！！')
                                self.cap.release()
                                self.right_label_0.close()
                                exit()
                        self.pun_day_num+=1
                        begin=Speak()
                        begin.speak(data=str(name)+"签到成功，你已签到"+str(self.pun_day_num)+"天")
                        with open(path_logcat_csv,"a+",newline="") as csvfilew:
                            writer=csv.writer(csvfilew)
                            writer.writerow(recoder)
                        self.cap.release()
                        self.right_label_0.close()
                        break
                cv2.rectangle(img, tuple([dets[0].left(), dets[0].top()]), tuple([dets[0].right(), dets[0].bottom()]),
                              (100, 255, 0), 2)
                cv2.putText(img, name, pos, font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.putText(img, "faces: " + str(len(dets)), (10, 40), font, 1, (0, 255, 200), 1, cv2.LINE_AA)
            height, width = img.shape[:2]
            image1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            showImage = QtGui.QImage(image1,width,height,QtGui.QImage.Format_RGB888)
            self.right_label_0.setPixmap(QtGui.QPixmap.fromImage(showImage))
def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
