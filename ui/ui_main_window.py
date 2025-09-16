# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QHeaderView,
    QMainWindow, QPlainTextEdit, QPushButton, QSizePolicy,
    QStatusBar, QTabWidget, QTableView, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(978, 799)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.mainWidget = QWidget(self.centralwidget)
        self.mainWidget.setObjectName(u"mainWidget")
        self.mainWidget.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(self.mainWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.topWidget = QWidget(self.mainWidget)
        self.topWidget.setObjectName(u"topWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.topWidget.sizePolicy().hasHeightForWidth())
        self.topWidget.setSizePolicy(sizePolicy)
        self.topWidget.setMinimumSize(QSize(0, 100))
        self.topWidget.setStyleSheet(u"margin: 5px;")
        self.horizontalLayout = QHBoxLayout(self.topWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridTabWidget = QTabWidget(self.topWidget)
        self.gridTabWidget.setObjectName(u"gridTabWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.gridTabWidget.sizePolicy().hasHeightForWidth())
        self.gridTabWidget.setSizePolicy(sizePolicy1)
        self.gridTabWidget.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        self.gridTabWidgetPage1 = QWidget()
        self.gridTabWidgetPage1.setObjectName(u"gridTabWidgetPage1")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.gridTabWidgetPage1.sizePolicy().hasHeightForWidth())
        self.gridTabWidgetPage1.setSizePolicy(sizePolicy2)
        self.UploadFolederButtonByPDF = QPushButton(self.gridTabWidgetPage1)
        self.UploadFolederButtonByPDF.setObjectName(u"UploadFolederButtonByPDF")
        self.UploadFolederButtonByPDF.setGeometry(QRect(0, 0, 101, 41))
        self.gridTabWidget.addTab(self.gridTabWidgetPage1, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridTabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridTabWidget.addTab(self.tab_2, "")

        self.horizontalLayout.addWidget(self.gridTabWidget)


        self.verticalLayout.addWidget(self.topWidget)

        self.middleWidget = QWidget(self.mainWidget)
        self.middleWidget.setObjectName(u"middleWidget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.middleWidget.sizePolicy().hasHeightForWidth())
        self.middleWidget.setSizePolicy(sizePolicy3)
        self.middleWidget.setMinimumSize(QSize(0, 300))
        self.verticalLayout_3 = QVBoxLayout(self.middleWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.progressTable = QTableView(self.middleWidget)
        self.progressTable.setObjectName(u"progressTable")

        self.verticalLayout_3.addWidget(self.progressTable)


        self.verticalLayout.addWidget(self.middleWidget)

        self.buttomWidget = QWidget(self.mainWidget)
        self.buttomWidget.setObjectName(u"buttomWidget")
        self.verticalLayout_2 = QVBoxLayout(self.buttomWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.logPrintText = QPlainTextEdit(self.buttomWidget)
        self.logPrintText.setObjectName(u"logPrintText")

        self.verticalLayout_2.addWidget(self.logPrintText)


        self.verticalLayout.addWidget(self.buttomWidget)


        self.gridLayout.addWidget(self.mainWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.gridTabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Log Viewer", None))
        self.UploadFolederButtonByPDF.setText(QCoreApplication.translate("MainWindow", u"+ \u4e0a\u4f20\u6587\u4ef6\u5939", None))
        self.gridTabWidget.setTabText(self.gridTabWidget.indexOf(self.gridTabWidgetPage1), QCoreApplication.translate("MainWindow", u"PDF\u8f6c\u6362", None))
        self.gridTabWidget.setTabText(self.gridTabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\u83b7\u53d6\u5c01\u9762", None))
        self.gridTabWidget.setTabText(self.gridTabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\u8f6cH265", None))
    # retranslateUi

