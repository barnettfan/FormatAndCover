# main.py
from PySide6.QtWidgets import QMainWindow, QApplication,QFileDialog
from PySide6.QtGui import QStandardItemModel, QStandardItem
from ui_main_window import Ui_MainWindow  # 导入生成的 UI 类
from PrintRedirector import PrintRedirector
import sys
import os 

class MainWindow(QMainWindow):
    # pyside6-uic main_window.ui -o E:\Python\FormatAndCover\ui\ui_main_window.py
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # 把 UI 应用到当前窗口
        
        # 创建重定向器，传入你的日志组件
        self.redirector = PrintRedirector(self.ui.logPrintText)  # 假设你的组件叫 logPrintText

        # 拦截全局 print
        sys.stdout = self.redirector

        # 连接信号
        self.ui.UploadFolederButtonByPDF.clicked.connect(self.on_upload_clicked)

    def on_upload_clicked(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹",  "", QFileDialog.ShowDirsOnly)
        if not folder_path:
            print("用户取消选择")
        
        print(f"选择的文件夹路径：{folder_path}")

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['文件夹名','图片数','进度','状态'])
        
        for index, path in enumerate(list):
            item = QStandardItem(path)
            model.setItem(index, 0, item)

        self.ui.progressTable.setModel(model)
        self.ui.progressTable.resizeColumnsToContents()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())